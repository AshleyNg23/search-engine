import pickle
from postings import Postings

def pickleTest(listOfTuples, fileName = "pickleTest.pkl"):
    with open(fileName, "wb") as file:
        for tokens, postings in sorted(listOfTuples):
            pickle.dump((tokens,postings), file)
    pickleLoad()
    

def pickleLoad(fileName = "pickleTest.pkl"):
    with open(fileName, "rb") as file:
        token, postings = pickle.load(file)
        print(token, postings)
    



myDict = {"F": [Postings("a1", 1, 32), Postings("a2", 2, 33), Postings("b3", 3, 34)], "B": [Postings("a1", 1, 20), Postings("b3", 3, 34)]}

pickleTest(myDict.items(),"pickleTest.pkl")