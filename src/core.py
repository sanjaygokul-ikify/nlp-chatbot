import re
import random
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from src.utils import log_message

# Download required NLTK data silently
for resource in ["punkt", "wordnet", "punkt_tab", "omw-1.4"]:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass


# Intent patterns: (compiled_regex, list_of_responses)
INTENTS = [
    (
        re.compile(r"\b(hi|hello|hey|howdy|greetings)\b", re.I),
        [
            "Hello! How can I help you today?",
            "Hey there! What's on your mind?",
            "Hi! Nice to meet you. How can I assist?",
        ],
    ),
    (
        re.compile(r"\b(bye|goodbye|see you|quit|exit|farewell)\b", re.I),
        [
            "Goodbye! Have a wonderful day!",
            "See you later! Take care.",
            "Bye! Feel free to come back anytime.",
        ],
    ),
    (
        re.compile(r"\b(how are you|how do you do|you doing|are you okay)\b", re.I),
        [
            "I'm doing great, thanks for asking! How about you?",
            "I'm just a bot, but I feel fantastic! What about you?",
            "All systems running smoothly! How can I help?",
        ],
    ),
    (
        re.compile(r"\b(what is your name|who are you|what are you|your name)\b", re.I),
        [
            "I'm NLP Chatbot, your friendly AI assistant!",
            "You can call me ChatBot. I'm here to chat and help!",
        ],
    ),
    (
        re.compile(r"\b(help|assist|support|what can you do)\b", re.I),
        [
            "I can chat with you, answer questions, and keep you company! "
            "Try saying hello, asking how I am, or just telling me something.",
            "I'm here to help! You can ask me questions or just have a conversation.",
        ],
    ),
    (
        re.compile(r"\b(thank|thanks|thank you|thx|ty)\b", re.I),
        [
            "You're welcome! Happy to help.",
            "Glad I could assist! Anything else?",
            "No problem at all!",
        ],
    ),
    (
        re.compile(r"\b(weather|temperature|forecast|rain|sunny|cloudy)\b", re.I),
        [
            "I don't have live weather data, but you can check weather.com or Google Weather!",
            "Unfortunately I can't fetch real-time weather. Try a weather app for that!",
        ],
    ),
    (
        re.compile(r"\b(joke|funny|laugh|humor)\b", re.I),
        [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
        ],
    ),
    (
        re.compile(r"\b(time|clock|what time)\b", re.I),
        [
            "I don't have access to real-time clocks, but your device can tell you the time!",
        ],
    ),
    (
        re.compile(r"\b(age|old|how old)\b", re.I),
        [
            "I was just born the moment you started chatting with me!",
            "Age is just a number, and mine is undefined. 😄",
        ],
    ),
]

FALLBACK_RESPONSES = [
    "Hmm, I'm not sure about that. Could you rephrase?",
    "Interesting! Tell me more.",
    "I'm still learning. Could you ask me something else?",
    "That's a bit beyond me right now, but I'm always improving!",
    "I didn't quite catch that. Try asking something different!",
]


class ChatBot:
    """NLP Chatbot with intent matching and lemmatization."""

    def __init__(self, config: dict):
        self.config = config
        self.lemmatizer = WordNetLemmatizer()

    def _preprocess(self, text: str) -> str:
        """Tokenize and lemmatize input text."""
        try:
            tokens = word_tokenize(text.lower())
            lemmatized = [self.lemmatizer.lemmatize(t) for t in tokens]
            return " ".join(lemmatized)
        except Exception:
            return text.lower()

    def respond(self, user_input: str) -> str:
        """Return a response string for the given user input."""
        if not user_input or not user_input.strip():
            return "Please say something — I'm listening!"

        log_message(f"User: {user_input}")
        processed = self._preprocess(user_input)

        for pattern, responses in INTENTS:
            if pattern.search(processed) or pattern.search(user_input):
                reply = random.choice(responses)
                log_message(f"Bot: {reply}")
                return reply

        reply = random.choice(FALLBACK_RESPONSES)
        log_message(f"Bot (fallback): {reply}")
        return reply
