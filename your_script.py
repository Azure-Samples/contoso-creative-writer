import re
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Element:
    def __init__(self, name, symbol, representation, properties, interactions, defense_ability):
        self.name = name
        self.symbol = symbol
        self.representation = representation
        self.properties = properties
        self.interactions = interactions
        self.defense_ability = defense_ability

    def display_properties(self):
        print(f"Properties of {self.name} ({self.symbol}):")
        for prop in self.properties:
            print(f"  - {prop}")

    def display_interactions(self):
        print(f"Interactions of {self.name} ({self.symbol}):")
        for interaction in self.interactions:
            print(f"  - {interaction}")

    def display_defense_ability(self):
        print(f"Defense Ability of {self.name} ({self.symbol}): {self.defense_ability}")

    def execute_defense_function(self):
        defense_functions = {
            "evasion": self.evasion,
            "adaptability": self.adaptability,
            "fortification": self.fortification,
            "barrier": self.barrier,
            "regeneration": self.regeneration,
            "resilience": self.resilience,
            "illumination": self.illumination,
            "shield": self.shield,
            "reflection": self.reflection,
            "protection": self.protection
        }
        defense_function = defense_functions.get(self.defense_ability.lower(), self.no_defense)
        defense_function()

    def evasion(self):
        print(f"{self.name} uses Evasion to avoid threats and remain undetected.")

    def adaptability(self):
        print(f"{self.name} adapts to changing environments and evolves to overcome challenges.")

    def fortification(self):
        print(f"{self.name} strengthens defenses and fortifies positions to withstand attacks.")

    def barrier(self):
        print(f"{self.name} creates barriers to protect against external threats.")

    def regeneration(self):
        print(f"{self.name} regenerates lost or damaged parts to maintain functionality.")

    def resilience(self):
        print(f"{self.name} exhibits resilience to recover quickly from setbacks.")

    def illumination(self):
        print(f"{self.name} uses illumination to reveal hidden threats and illuminate dark areas.")

    def shield(self):
        print(f"{self.name} uses a shield to block incoming attacks and protect allies.")

    def reflection(self):
        print(f"{self.name} reflects attacks back to the source, turning the enemy's power against them.")

    def protection(self):
        print(f"{self.name} offers protection to prevent harm and ensure safety.")

    def no_defense(self):
        print("No defense function available.")

class CustomRecognizer:
    class RecognizerResult:
        def __init__(self, text):
            self.text = text
            self.intents = []

    class Intent:
        def __init__(self, name, score):
            self.name = name
            self.score = score

    def recognize(self, text):
        recognizer_result = self.RecognizerResult(text)
        regex_element = re.compile(r"^(Hydrogen|Carbon|Iron|Silicon|Oxygen|Nitrogen|Phosphorus|Gold|Silver|Lead|Diamond)$", re.IGNORECASE)
        is_element = regex_element.match(text)

        if is_element:
            recognizer_result.intents.append(self.Intent("ElementDefense", 100))
        return recognizer_result

    def get_top_intent(self, recognizer_result):
        recognizer_result.intents.sort(key=lambda x: x.score, reverse=True)
        return recognizer_result.intents[0].name if recognizer_result.intents else None

class DataProtector:
    sensitive_keywords = {"AI", "sensitive", "confidential", "data"}

    @staticmethod
    def contains_sensitive_info(text):
        return any(keyword.lower() in text.lower() for keyword in DataProtector.sensitive_keywords)

    @staticmethod
    def mask_sensitive_info(text):
        for keyword in DataProtector.sensitive_keywords:
            text = re.sub(keyword, '*' * len(keyword), text, flags=re.IGNORECASE)
        return text

    @staticmethod
    def encrypt_string(plain_text, key):
        backend = default_backend()
        key_bytes = key.encode('utf-8')
        iv = key_bytes[:16]

        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return encrypted_data.hex()

    @staticmethod
    def decrypt_string(cipher_text, key):
        backend = default_backend()
        key_bytes = key.encode('utf-8')
        iv = key_bytes[:16]

        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()

        encrypted_data = bytes.fromhex(cipher_text)
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        return decrypted_data.decode('utf-8')

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment

def initialize_elements():
    elements = [
        Element(
            name="Hydrogen",
            symbol="H",
            representation="Lua",
            properties=["Simple", "Lightweight", "Versatile"],
            interactions=["Easily integrates with other languages and systems"],
            defense_ability="Evasion"
        ),
        Element(
            name="Carbon",
            symbol="C",
            representation="Python",
            properties=["Flexible", "Widely used", "Powerful"],
            interactions=["Can be used for a variety of tasks, from web development to data analysis"],
            defense_ability="Adaptability"
        ),
        Element(
            name="Iron",
            symbol="Fe",
            representation="C++",
            properties=["Strong", "Durable", "Efficient"],
            interactions=["Used in system programming and game development"],
            defense_ability="Fortification"
        ),
        Element(
            name="Silicon",
            symbol="Si",
            representation="Java",
            properties=["Robust", "Platform-independent", "Secure"],
            interactions=["Widely used in enterprise applications"],
            defense_ability="Barrier"
        ),
        Element(
            name="Oxygen",
            symbol="O",
            representation="JavaScript",
            properties=["Dynamic", "Versatile", "Ubiquitous"],
            interactions=["Essential for web development"],
            defense_ability="Regeneration"
        ),
        Element(
            name="Nitrogen",
            symbol="N",
            representation="Ruby",
            properties=["Elegant", "Productive", "Flexible"],
            interactions=["Popular in web development with Rails"],
            defense_ability="Resilience"
        ),
        Element(
            name="Phosphorus",
            symbol="P",
            representation="PHP",
            properties=["Server-side", "Web-focused", "Embedded"],
            interactions=["Commonly used in web development"],
            defense_ability="Illumination"
        ),
        Element(
            name="Gold",
            symbol="Au",
            representation="Swift",
            properties=["Modern", "Safe", "Fast"],
            interactions=["Used for iOS and macOS development"],
            defense_ability="Shield"
        ),
        Element(
            name="Silver",
            symbol="Ag",
            representation="Go",
            properties=["Concurrent", "Efficient", "Scalable"],
            interactions=["Ideal for cloud services and backend systems"],
            defense_ability="Reflection"
        ),
        Element(
            name="Lead",
            symbol="Pb",
            representation="Rust",
            properties=["Safe", "Concurrent", "Fast"],
            interactions=["Used for system-level programming"],
            defense_ability="Protection"
        ),
        Element(
            name="Diamond",
            symbol="D",
            representation="Kotlin",
            properties=["Modern", "Concise", "Safe"],
            interactions=["Used for Android development"],
            defense_ability="Adaptability"
        )
    ]
    return elements
