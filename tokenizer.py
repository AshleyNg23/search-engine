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


def computeSimHashFrequencies(tokens: list):
    '''
    Time Complexity: O(n log n) - Iterates through the tokens list (O(n)) to populate
    the dictionary, then sorts it using Python's sorted function, which has
    an average time complexity of O(n log n) (Timsort algorithm).
    '''
   
    tokenMap = {}
   
    for values in tokens:
        values = bin(int(hashlib.sha256(values.encode()).hexdigest(), 16))[2::]
        if values not in tokenMap:
            tokenMap[values] = 0
        tokenMap[values] += 1
   
    tokenMap = dict(sorted(tokenMap.items(), key=lambda x: x[1], reverse=True))
    return tokenMap




'''
SimHashing: (Used for finding if two texts are similar)
To sim hash add or subtract the hashString to the index at hashNum
Go through this with every token and store the result in hashNum
When this is done continue go through the hashNum and append the values to a hashString
Turn the hashString back to hex and return the hex


For better detailed description look up Sim Hashing Algorithm.
'''


def simHash(freq):
    hashNum = [0] * 256 #Initialize a 256 bit array since I use sha256
    for bits,frequency in freq.items():
        for i in range(len(bits)):
            if bits[i] == "1":
                hashNum[i] += (1 * frequency)
            else:
                hashNum[i] -= (1 * frequency)
    hashString = ""
    for i in range(len(hashNum)):
        if hashNum[i] > 0:
            hashString += "1"
        else:
            hashString += "0"
    return hashString


def checkSimilar(hashes, currentSimHash):
    if currentSimHash in hashes:
        return True
    for items in list(hashes):
        x = int(items,2) ^ int(currentSimHash, 2) # XOR to find differing bits
        distance = 0
        while x:
            distance += x & 1  # Count the number of 1's in the result
            x >>= 1
        if distance <= 4:
            return True
    return False