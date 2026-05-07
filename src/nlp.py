import nltk
from nltk.corpus import wordnet

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():

            synonyms.add(lemma.name())
    return list(synonyms)