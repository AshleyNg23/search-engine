import hashlib
from nltk import PorterStemmer

def tokenizer(listOfWords):
    tokens = []
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
            if fullStr != "" and len(fullStr) > 1: # If fullStr is not empty, append it to tokens
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