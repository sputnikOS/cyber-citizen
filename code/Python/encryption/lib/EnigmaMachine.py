class EnigmaMachine:
    def __init__(self, rotor_config, reflector):
        self.rotors = rotor_config
        self.reflector = reflector
        self.positions = [0] * len(self.rotors)

    def rotate_rotors(self):
        """Rotates the rotors one step, cascading to the next rotor if needed."""
        for i in range(len(self.positions)):
            self.positions[i] = (self.positions[i] + 1) % 26
            if self.positions[i] != 0:  # Stop cascading if rotor didn't complete a full turn
                break

    def pass_through_rotor(self, char, rotor, position):
        """Passes a character through a rotor considering its position."""
        offset = ord(char) - ord('A')
        encoded = (offset + position) % 26
        return rotor[encoded]

    def pass_back_through_rotor(self, char, rotor, position):
        """Passes a character back through a rotor."""
        offset = rotor.index(char)
        decoded = (offset - position) % 26
        return chr(decoded + ord('A'))

    def encrypt_character(self, char):
        """Encrypts a single character."""
        if not char.isalpha():  # Ignore non-alphabetic characters
            return char

        char = char.upper()
        self.rotate_rotors()

        # Forward pass through rotors
        for i, rotor in enumerate(self.rotors):
            char = self.pass_through_rotor(char, rotor, self.positions[i])

        # Reflector
        char = self.reflector[ord(char) - ord('A')]

        # Backward pass through rotors
        for i, rotor in reversed(list(enumerate(self.rotors))):
            char = self.pass_back_through_rotor(char, rotor, self.positions[i])

        return char

    def encrypt(self, text):
        """Encrypts a string."""
        return ''.join(self.encrypt_character(c) for c in text)

# Example configuration for Enigma machine
rotor1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"  # Rotor I
rotor2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"  # Rotor II
rotor3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"  # Rotor III
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"  # Reflector B

# Create the Enigma machine
enigma = EnigmaMachine([rotor1, rotor2, rotor3], reflector)

# Encrypt a string
plain_text = "HELLO WORLD"
encrypted_text = enigma.encrypt(plain_text)

print("Original Text:", plain_text)
print("Encrypted Text:", encrypted_text)
