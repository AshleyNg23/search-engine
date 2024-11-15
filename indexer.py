from postings import Postings
from tokenizer import tokenizer, computeWordFrequencies
import os
from bs4 import BeautifulSoup
import re
import sys
import pickle
import json
import heapq

class Index(object):
    def __init__(self):
          self.inverted_index = {}
          self.base_directory = ""
          self.currentDocId = 1
          self.amountOfPartial = 0
          self.chunkSize = 100000
    
    def index(self, dir_name):
        chunk = 0
        self.base_directory = dir_name
        for folders in os.listdir(self.base_directory):
            folderPath = os.path.join(self.base_directory, folders)
            for files in os.listdir(folderPath):
                filePath = os.path.join(folderPath, files)
                # Open the HTML file
                with open(filePath, "r") as file:
                    html_content = json.load(file)

                # Create a BeautifulSoup object
                soup = BeautifulSoup(html_content["content"], "lxml")
                text = soup.get_text()
                space_delemited_text = re.sub(r'\s+',' ',text)
                # Now you can use BeautifulSoup methods to extract data from the file
                # For example, to get all the links:
                tokens = tokenizer(space_delemited_text)
                freq = computeWordFrequencies(tokens)
                # Iterate through the tokens to log them into our inverted Index O(N) run-time O(N) space comp
                for key,values in freq.items():
                    self.logTokens(filePath, key, self.currentDocId, values)
                    chunk += 1
                    if chunk >= self.chunkSize:
                        self.createPartial()
                        chunk = 0
                self.currentDocId += 1
        self.mergePartial()
            
    

    def createPartial(self):
        with open(f"PartialIndex{self.amountOfPartial}.pkl", "wb") as file:
            for tokens, postings in sorted(self.inverted_index.items()):
                pickle.dump((tokens,postings), file)
        self.amountOfPartial += 1
        self.inverted_index.clear()

    def mergePartial(self):
        currentChunk = 0
        listOfFiles = []
        heap = []
        for i in range(self.amountOfPartial):
            file = open(f"PartialIndex{i}.pkl", "rb")
            listOfFiles.append(file)
            try:
                token, postings = pickle.load(file)
                heapq.heappush(heap, (token, i, postings))
            except EOFError:
                file.close()
        
        mergedIndex = {}
        currentTerm = None
        currentPostings = []
                
        while heap:
            term, fileIndex, postings = heapq.heappop(heap)

            if term == currentTerm:
                currentPostings.extend(postings)
            else:
                if currentTerm != None:
                    mergedIndex[currentTerm] = currentPostings
                
                #Keep track of the amount of unique tokens so we don't have to open the file to check.            
                currentPostings = postings
                currentTerm = term
                currentChunk += 1
            
            if currentChunk >= self.chunkSize:
                self.dumpFinal(mergedIndex)
                mergedIndex.clear()
            
            try:
                nextToken, nextPostings = pickle.load(listOfFiles[fileIndex])
                heapq.heappush(heap, (nextToken, fileIndex, nextPostings))
            except EOFError:
                listOfFiles[fileIndex].close()
        self.dumpFinal(mergedIndex)


    def dumpFinal(self, mergedIndex, fileName = "FinalIndex.pkl"):
        with open(fileName, "ab") as file:
            for token, post in mergedIndex.items():
                pickle.dump((token, post), file)
            
         

    def logTokens(self, filePath, token, docId, frequency):
        # key = token
        # value = (docId, frequency)
        # self.invertex_index[key] array, append value tuple
        if token not in self.inverted_index:
            self.inverted_index[token] = []
        self.inverted_index[token].append(Postings(filePath, docId, frequency))
        pass

    def printReport(self):
        unique_tokens = set()
        total_size = 0
        with open("FinalIndex.pkl", "rb") as file:
            while True:
                try:
                    token, postings = pickle.load(file)
                    unique_tokens.add(token)
                    total_size += sys.getsizeof((token, postings))
                except EOFError:
                    break  # End of file reached
            print("Indexed Documents: " + str(self.currentDocId))
            print("Unique Tokens: " + str(len(unique_tokens)))
            print("Total Size: " + str(round((total_size)/1024,2)) + "kb")
