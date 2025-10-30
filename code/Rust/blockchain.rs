use serde::{Serialize, Deserialize};
use sha2::{Sha256, Digest};
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Block {
    index: u64,
    timestamp: u64,
    data: String,
    previous_hash: String,
    hash: String,
}

impl Block {
    // Create a new block
    fn new(index: u64, data: String, previous_hash: String) -> Block {
        let timestamp = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs();
        let block_data = Block {
            index,
            timestamp,
            data,
            previous_hash,
            hash: String::new(), // We'll compute the hash later
        };
        let mut block = block_data.clone();
        block.hash = block.calculate_hash();
        block
    }

    // Calculate the block's hash
    fn calculate_hash(&self) -> String {
        let block_string = format!(
            "{}{}{}{}",
            self.index, self.timestamp, self.data, self.previous_hash
        );
        let mut hasher = Sha256::new();
        hasher.update(block_string);
        let result = hasher.finalize();
        hex::encode(result)
    }
}
