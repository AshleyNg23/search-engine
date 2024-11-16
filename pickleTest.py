import pickle
from postings import Postings

def pickleTest(index, fileName = "pickleTest.pkl"):
    with open(fileName, "ab") as file:
        pickle.dump(index, file)
    

def pickleLoad(fileName = "pickleTest.pkl"):
    load_count = 1
    with open(fileName, "rb") as file:
       data = pickle.load(file)
       print(data)
    



myDict = {"F": [Postings("a1", 1, 32), Postings("a2", 2, 33), Postings("b3", 3, 34)], "B": [Postings("a1", 1, 20), Postings("b3", 3, 34)]}
myDict2 = {"FS": [Postings("A2", 21, 21)]}

pickleTest(myDict)
pickleTest(myDict2)
pickleLoad()
pickleLoad()