#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>

#define MAX_TRANSACTIONS 5
#define BLOCK_DATA_SIZE 256
#define HASH_SIZE 64
#define DIFFICULTY 4

typedef struct Transaction {
    char sender[32];
    char receiver[32];
    int amount;
} Transaction;

typedef struct Block {
    int index;
    char prev_hash[HASH_SIZE];
    char hash[HASH_SIZE];
    Transaction transactions[MAX_TRANSACTIONS];
    int transaction_count;
    int nonce;
} Block;

typedef struct Blockchain {
    Block *blocks;
    int size;
} Blockchain;

void compute_hash(Block *block, char *output) {
    char data[BLOCK_DATA_SIZE];
    snprintf(data, BLOCK_DATA_SIZE, "%d%s%d", block->index, block->prev_hash, block->nonce);
    for (int i = 0; i < block->transaction_count; i++) {
        snprintf(data + strlen(data), BLOCK_DATA_SIZE - strlen(data), "%s%s%d",
                 block->transactions[i].sender,
                 block->transactions[i].receiver,
                 block->transactions[i].amount);
    }

    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char *)data, strlen(data), hash);

    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        snprintf(output + i * 2, HASH_SIZE, "%02x", hash[i]);
    }
}

int valid_hash(char *hash) {
    for (int i = 0; i < DIFFICULTY; i++) {
        if (hash[i] != '0') {
            return 0;
        }
    }
    return 1;
}

void mine_block(Block *block) {
    block->nonce = 0;
    do {
        block->nonce++;
        compute_hash(block, block->hash);
    } while (!valid_hash(block->hash));
}

Blockchain *create_blockchain() {
    Blockchain *blockchain = malloc(sizeof(Blockchain));
    blockchain->blocks = malloc(sizeof(Block));
    blockchain->size = 1;

    Block *genesis_block = &blockchain->blocks[0];
    genesis_block->index = 0;
    strcpy(genesis_block->prev_hash, "0");
    genesis_block->transaction_count = 0;
    mine_block(genesis_block);

    return blockchain;
}

void add_transaction(Block *block, const char *sender, const char *receiver, int amount) {
    if (block->transaction_count < MAX_TRANSACTIONS) {
        Transaction *transaction = &block->transactions[block->transaction_count++];
        strncpy(transaction->sender, sender, sizeof(transaction->sender) - 1);
        strncpy(transaction->receiver, receiver, sizeof(transaction->receiver) - 1);
        transaction->sender[sizeof(transaction->sender) - 1] = '\0';
        transaction->receiver[sizeof(transaction->receiver) - 1] = '\0';
        transaction->amount = amount;
        printf("Transaction added: %s -> %s: %d coins\n", sender, receiver, amount);
    } else {
        printf("Transaction limit reached for current block. Mine a new block first.\n");
    }
}

void add_block(Blockchain *blockchain) {
    blockchain->blocks = realloc(blockchain->blocks, (blockchain->size + 1) * sizeof(Block));
    Block *prev_block = &blockchain->blocks[blockchain->size - 1];
    Block *new_block = &blockchain->blocks[blockchain->size++];

    new_block->index = blockchain->size - 1;
    strcpy(new_block->prev_hash, prev_block->hash);
    new_block->transaction_count = 0;

    mine_block(new_block);
    printf("Block %d mined successfully!\n", new_block->index);
}

void print_blockchain(Blockchain *blockchain) {
    for (int i = 0; i < blockchain->size; i++) {
        Block *block = &blockchain->blocks[i];
        printf("Block %d\n", block->index);
        printf("Previous Hash: %s\n", block->prev_hash);
        printf("Hash: %s\n", block->hash);
        printf("Transactions:\n");
        for (int j = 0; j < block->transaction_count; j++) {
            Transaction *t = &block->transactions[j];
            printf("  %s -> %s: %d coins\n", t->sender, t->receiver, t->amount);
        }
        printf("\n");
    }
}

int main(int argc, char *argv[]) {
    Blockchain *blockchain = create_blockchain();

    if (argc < 2) {
        printf("Usage:\n");
        printf("  %s add_transaction <sender> <receiver> <amount>\n", argv[0]);
        printf("  %s mine_block\n", argv[0]);
        printf("  %s print\n", argv[0]);
        free(blockchain->blocks);
        free(blockchain);
        return 0;
    }

    if (strcmp(argv[1], "add_transaction") == 0) {
        if (argc != 5) {
            printf("Usage: %s add_transaction <sender> <receiver> <amount>\n", argv[0]);
        } else {
            const char *sender = argv[2];
            const char *receiver = argv[3];
            int amount = atoi(argv[4]);
            add_transaction(&blockchain->blocks[blockchain->size - 1], sender, receiver, amount);
        }
    } else if (strcmp(argv[1], "mine_block") == 0) {
        add_block(blockchain);
    } else if (strcmp(argv[1], "print") == 0) {
        print_blockchain(blockchain);
    } else {
        printf("Unknown command.\n");
    }

    free(blockchain->blocks);
    free(blockchain);
    return 0;
}
