#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Function to encrypt the text using Caesar cipher
void encrypt(char *text, int key) {
    for (int i = 0; text[i] != '\0'; ++i) {
        char ch = text[i];
        if (isalpha(ch)) {
            char base = islower(ch) ? 'a' : 'A';
            text[i] = (ch - base + key) % 26 + base;
        }
    }
}

// Function to decrypt the text using Caesar cipher
void decrypt(char *text, int key) {
    for (int i = 0; text[i] != '\0'; ++i) {
        char ch = text[i];
        if (isalpha(ch)) {
            char base = islower(ch) ? 'a' : 'A';
            text[i] = (ch - base - key + 26) % 26 + base;
        }
    }
}

int main() {
    char text[256];
    int key, choice;

    printf("Enter the text to encrypt or decrypt: ");
    fgets(text, sizeof(text), stdin);
    text[strcspn(text, "\n")] = '\0'; // Remove newline character

    printf("Enter the encryption key (positive integer): ");
    scanf("%d", &key);

    printf("Choose an option:\n");
    printf("1. Encrypt\n");
    printf("2. Decrypt\n");
    printf("Enter your choice: ");
    scanf("%d", &choice);

    if (choice == 1) {
        encrypt(text, key);
        printf("Encrypted text: %s\n", text);
    } else if (choice == 2) {
        decrypt(text, key);
        printf("Decrypted text: %s\n", text);
    } else {
        printf("Invalid choice!\n");
    }

    return 0;
}
