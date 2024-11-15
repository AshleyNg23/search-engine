import hashlib
from nltk import PorterStemmer

def tokenizer(listOfWords):
    tokens = []

    stopWords = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no",
    "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our",
    "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd",
    "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
    "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't",
    "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's",
    "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom",
    "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll",
    "you're", "you've", "your", "yours", "yourself", "yourselves"
    }
    i = 0
    fullStr = ""
    ps = PorterStemmer()
    while i < len(listOfWords):
        character = listOfWords[i] # Read character by character
        if not character:
            if fullStr != "": # If fullStr has a string, append it to tokens
                tokens.append(fullStr)
            fullStr = ""
            break
        if not character.isalnum():
            if fullStr != "" and fullStr not in stopWords and len(fullStr) > 1: # If fullStr is not empty, append it to tokens
                tokens.append(ps.stem(fullStr))
            fullStr = "" 
        else:
            fullStr += character.lower() # Convert to lowercase for consistency
        i += 1
    return tokens

def computeWordFrequencies(tokens: list): 
    '''
    Time Complexity: O(n log n) - Iterates through the tokens list (O(n)) to populate 
    the dictionary, then sorts it using Python's sorted function, which has 
    an average time complexity of O(n log n) (Timsort algorithm).
    '''
    
    tokenMap = {}
    
    for values in tokens:
        if values not in tokenMap:
            tokenMap[values] = 0
        tokenMap[values] += 1
    
    tokenMap = dict(sorted(tokenMap.items(), key=lambda x: x[1], reverse=True)) 
    return tokenMap