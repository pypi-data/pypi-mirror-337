use std::{env, fs::File, hint::black_box, io::Read, sync::Arc, vec};

use llguidance::{
    api::{ParserLimits, TopLevelGrammar},
    toktrie::{InferenceCapabilities, TokEnv, TokRxInfo, TokTrie, TokenId, TokenizerEnv},
    Constraint, TokenParser,
};

struct SingleByteTokenizer {
    tok_trie: TokTrie,
}

impl SingleByteTokenizer {
    fn new() -> Self {
        let mut words = (0..=255).map(|x| vec![x]).collect::<Vec<_>>();
        words.push("<eos>".as_bytes().to_vec());
        let info = TokRxInfo {
            vocab_size: words.len() as u32,
            tok_eos: words.len() as u32 - 1,
            tok_bos: None,
            tok_pad: None,
            tok_unk: None,
            tok_end_of_turn: None,
        };
        let tok_trie = TokTrie::from(&info, &words);
        SingleByteTokenizer { tok_trie }
    }

    fn into_env(self) -> TokEnv {
        Arc::new(self)
    }
}

impl TokenizerEnv for SingleByteTokenizer {
    fn tok_trie(&self) -> &TokTrie {
        &self.tok_trie
    }

    fn tokenize_bytes(&self, s: &[u8]) -> Vec<TokenId> {
        self.tok_trie.greedy_tokenize(s)
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <schema.ll.json> <sample.json>", args[0]);
        std::process::exit(1);
    }

    let schema_file = read_file_to_string(&args[1]);
    let schema: TopLevelGrammar = if args[1].ends_with(".ll.json") {
        serde_json::from_str(&schema_file).expect("Invalid JSON in schema")
    } else if args[1].ends_with(".schema.json") {
        let val = serde_json::from_str(&schema_file).expect("Invalid JSON in schema");
        TopLevelGrammar::from_json_schema(val)
    } else {
        panic!("Unknown schema file extension")
    };
    let obj_str = read_file_to_string(&args[2]);

    let tok_env: TokEnv = SingleByteTokenizer::new().into_env();

    let tokens = tok_env.tokenize(&obj_str);

    let verbose = false;

    // set to 2 for more output; 1 is warnings only
    let stderr_log_level = 1;

    // typically set to 2, to send info-level output to the user
    let buffer_log_level = 2;

    let parser = TokenParser::from_grammar(
        tok_env.clone(),
        schema,
        llguidance::Logger::new(buffer_log_level, stderr_log_level),
        InferenceCapabilities {
            ff_tokens: true,  // can the engine append multiple tokens?
            backtrack: false, // can the engine remove generated tokens?

            conditional_ff_tokens: false, // not used
            fork: false,                  // not used
        },
        ParserLimits::default(),
        vec![],
    )
    .unwrap();
    let mut constraint = Constraint::new(parser);

    // enable sending parser results back via the logs (constraint.flush_logs())
    constraint.log_json_progress = true;

    let trie = tok_env.tok_trie();

    eprintln!("Parsing tokens: {}", trie.tokens_dbg(&tokens));

    let mut idx = 0;
    while idx < tokens.len() {
        let res = constraint.compute_mask().unwrap();

        if res.is_stop() {
            // stop sequence
            break;
        }

        let sampled_token = if let Some(mask) = &res.sample_mask {
            // Simulate sampling - it should use the mask and temperature
            black_box(mask);
            black_box(constraint.temperature);
            let sampled_token = tokens[idx];

            if verbose {
                println!(
                    "SAMPLE {}: {} {}",
                    idx,
                    sampled_token,
                    tok_env.tok_trie().token_dbg(sampled_token)
                );
            }
            Some(sampled_token)
        } else {
            // sampling not required
            if verbose {
                println!("NO SAMPLE");
            }
            None
        };

        let splice = constraint.commit_token(sampled_token).unwrap();
        if splice.stop {
            // stop sequence
            break;
        }

        assert!(splice.backtrack == 0); // we didn't allow backtracking in InferenceCaps

        // The splice contains the tokens (possibly more than one since we enabled ff_tokens
        // in InferenceCaps) that the parser wants to append to the output.

        // if this fails, our test data is broken
        if tokens[idx..idx + splice.ff_tokens.len()] != splice.ff_tokens {
            panic!(
                "BAD TEST: ff_tokens mismatch:\n{}\n{}",
                trie.tokens_dbg(&tokens[idx..idx + splice.ff_tokens.len()]),
                trie.tokens_dbg(&splice.ff_tokens)
            );
        }

        if splice.ff_tokens.len() > 1 {
            println!("FF: {}", trie.tokens_dbg(&splice.ff_tokens));
        }

        idx += splice.ff_tokens.len();

        // send output to the user
        send_output(&constraint.flush_logs());
    }

    // flush any output
    send_output(&constraint.flush_logs());
    // the stop reason should be likely also sent to the user
    println!("Stop reason: {:?}", constraint.parser.stop_reason());
}

fn read_file_to_string(filename: &str) -> String {
    let mut file = File::open(filename).expect("Unable to open file");
    let mut content = String::new();
    file.read_to_string(&mut content)
        .expect("Unable to read file");
    content
}

fn send_output(user_output: &str) {
    // enable if you want to see the output
    if false {
        println!("{}", user_output);
    }
}
