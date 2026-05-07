"""
nlp.py — NLP helper utilities for NLP Chatbot.

PEP 8 compliant. Keep concise and readable.
"""

import nltk
from nltk.corpus import wordnet

# Ensure wordnet data is available
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)


def get_synonyms(word: str) -> list:
    """
    Return a list of synonyms for the given word using WordNet.

    Parameters
    ----------
    word : str
        The word to look up.

    Returns
    -------
    list
        A list of synonym strings (may be empty if none found).
    """
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace("_", " "))
    return sorted(synonyms)
