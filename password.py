import random
import string
import secrets
import argparse
from typing import List

class PasswordGenerator:
    def __init__(self):
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate_random_password(self, length: int = 16, use_symbols: bool = True) -> str:
        """Generate a truly random password using secrets module (cryptographically secure)"""
        characters = self.uppercase + self.lowercase + self.digits
        if use_symbols:
            characters += self.symbols
        
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    
    def generate_passphrase(self, word_count: int = 4, separator: str = "-", capitalize: bool = True, add_number: bool = True, add_symbol: bool = True) -> str:
        """Generate a memorable passphrase using random words"""
        # Common word list - you can expand this
        words = [
            "apple", "brave", "cloud", "dragon", "eagle", "flame", "globe", "heart",
            "ice", "jump", "knight", "light", "mountain", "night", "ocean", "planet",
            "quantum", "river", "star", "tiger", "unity", "vortex", "water", "xray",
            "yellow", "zenith", "alpha", "beta", "gamma", "delta"
        ]
        
        selected_words = [secrets.choice(words) for _ in range(word_count)]
        
        # Apply transformations
        if capitalize:
            selected_words = [word.capitalize() for word in selected_words]
        
        passphrase = separator.join(selected_words)
        
        # Add extra security elements
        if add_number:
            passphrase += str(secrets.randbelow(90) + 10)  # Add 2-digit number
        
        if add_symbol:  # FIXED: Removed the undefined 'use_symbols' parameter
            passphrase += secrets.choice(self.symbols)
        
        return passphrase
    
    def generate_pronounceable_password(self, syllable_count: int = 5) -> str:
        """Generate a somewhat pronounceable password"""
        consonants = "bcdfghjklmnpqrstvwxyz"
        vowels = "aeiou"
        
        password = ""
        for i in range(syllable_count):
            # Alternate consonant-vowel pattern
            if i == 0 or secrets.randbelow(2) == 0:
                password += secrets.choice(consonants)
            password += secrets.choice(vowels)
        
        # Add capital letter and symbols/numbers
        password = password.capitalize()
        password += str(secrets.randbelow(10))
        password += secrets.choice(self.symbols)
        
        return password
    
    def check_password_strength(self, password: str) -> dict:
        """Check the strength of a generated password"""
        strength = {
            "length": len(password) >= 12,
            "uppercase": any(c in self.uppercase for c in password),
            "lowercase": any(c in self.lowercase for c in password),
            "digit": any(c in self.digits for c in password),
            "symbol": any(c in self.symbols for c in password),
            "common_patterns": not any(pattern in password.lower() for pattern in ["123", "abc", "qwerty", "password"]),
            "unique_chars": len(set(password)) >= len(password) * 0.6
        }
        
        score = sum(strength.values())
        if score >= 6:
            rating = "Very Strong"
        elif score >= 5:
            rating = "Strong"
        elif score >= 4:
            rating = "Good"
        elif score >= 3:
            rating = "Weak"
        else:
            rating = "Very Weak"
        
        return {
            "score": score,
            "rating": rating,
            "details": strength
        }

def display_password_info(password: str, generator: PasswordGenerator):
    """Display password and its strength information"""
    strength = generator.check_password_strength(password)
    
    print(f"Password: {password}")
    print(f"Length: {len(password)}")
    print(f"Strength: {strength['rating']} ({strength['score']}/7)")
    print("Details:")
    for check, passed in strength["details"].items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check.replace('_', ' ').title()}")
    print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description="Generate strong passwords")
    parser.add_argument("--type", choices=["random", "passphrase", "pronounceable"], 
                       default="random", help="Type of password to generate")
    parser.add_argument("--length", type=int, default=16, help="Password length")
    parser.add_argument("--count", type=int, default=5, help="Number of passwords to generate")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    
    args = parser.parse_args()
    
    generator = PasswordGenerator()
    
    print("=" * 50)
    print("STRONG PASSWORD GENERATOR")
    print("=" * 50)
    
    for i in range(args.count):
        print(f"\nPassword #{i + 1}:")
        
        if args.type == "random":
            password = generator.generate_random_password(
                length=args.length, 
                use_symbols=not args.no_symbols
            )
        elif args.type == "passphrase":
            password = generator.generate_passphrase()
        elif args.type == "pronounceable":
            password = generator.generate_pronounceable_password()
        
        display_password_info(password, generator)

# Advanced function for bulk generation
def generate_admin_passwords():
    """Generate passwords specifically for admin accounts"""
    generator = PasswordGenerator()
    
    print("ADMIN-LEVEL PASSWORDS (Very Strong)")
    print("=" * 60)
    
    # Generate different types of strong admin passwords
    passwords = []
    
    # Type 1: Ultra-strong random
    passwords.append(generator.generate_random_password(length=20))
    
    # Type 2: Strong passphrase
    passwords.append(generator.generate_passphrase(word_count=5, separator="!"))
    
    # Type 3: Mixed pattern
    passwords.append(generator.generate_random_password(length=24))
    
    # Type 4: Pronounceable but long
    passwords.append(generator.generate_pronounceable_password(syllable_count=8))
    
    # Type 5: Maximum complexity
    complex_chars = generator.uppercase + generator.lowercase + generator.digits + generator.symbols
    max_complex = ''.join(secrets.choice(complex_chars) for _ in range(25))
    passwords.append(max_complex)
    
    for i, password in enumerate(passwords, 1):
        print(f"\nAdmin Password #{i}:")
        display_password_info(password, generator)

if __name__ == "__main__":
    # Generate standard passwords
    main()
    
    # Also generate admin-specific passwords
    print("\n" + "=" * 60)
    generate_admin_passwords()