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
          # {token_name = [(docId, docFrequency), (1, 7), (2, 3)]}
          self.base_directory = ""
          self.currentDocId = 0
          self.amountOfPartial = 0
          self.chunkSize = 10000
    
    def index(self, dir_name):
        chunk = 0
        self.base_directory = dir_name
         # Loop through all directories in DEV folder 
         # while theres still directories in the folder
            # open the directory -> get list of pages in the directory
            # for each page in the directory
                # retrieve tokens from doc - call getTokens
                # add tokens to inverted index, increase freq +1 and note doc id
                # currentDocId += 1
        for folders in os.listdir(self.base_directory):
            folderPath = os.path.join(self.base_directory, folders)
            for files in os.listdir(folderPath):
                self.currentDocId += 1
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
        self.createPartial()
        self.mergePartial()
    

    def logTokens(self, filePath, token, docId, frequency):
        # key = token
        # value = (docId, frequency)
        # self.invertex_index[key] array, append value tuple
        if token not in self.inverted_index:
            self.inverted_index[token] = []
        self.inverted_index[token].append(Postings(filePath, docId, frequency))
        pass
            
    

    def createPartial(self):
        with open(f"PartialIndex{self.amountOfPartial}.pkl", "wb") as file:
            batch = []
            for key, value in sorted(self.inverted_index.items()):
                batch.append((key,value))
            # Dump the entire batch at once
            pickle.dump(batch, file)

        self.amountOfPartial += 1
        self.inverted_index.clear()

    def mergePartial(self):
        listOfFiles = []
        heap = []
        batch_indices = [0] * self.amountOfPartial
        listOfComp = [False] * self.amountOfPartial

        # Open all partial index files
        for i in range(self.amountOfPartial):
            try:
                listOfFiles.append(f"PartialIndex{i}.pkl")
                file = open(f"PartialIndex{i}.pkl", "rb")
                batch = pickle.load(file)
                start_index = 0  # Start from the current position in the batch
                end_index = min(start_index + 500, len(batch))
                if end_index == len(batch):
                        listOfComp[i] = True
                for token, postings in batch[start_index: end_index]:  # Load only a small part of the batch
                    heapq.heappush(heap, (token, i, postings))
            except EOFError:
                listOfComp[i] = True
            file.close()
        
        mergedIndex = {}
        currentTerm = None
        currentPostings = []
        # Merge partial indexes
        while heap:
            term, fileIndex, postings = heapq.heappop(heap)

            if term == currentTerm:
                currentPostings.extend(postings)
            else:
                if currentTerm is not None:
                    mergedIndex[currentTerm] = currentPostings
                
                currentPostings = postings
                currentTerm = term

            # Flush merged index to disk if it exceeds memory limit
            if len(mergedIndex) >= self.chunkSize:
                self.dumpFinal(mergedIndex)

                mergedIndex.clear()

            # Load the next batch of tokens from the same file
            try:
                if listOfComp[fileIndex] != True and len(heap) < 10:
                    file = open(listOfFiles[fileIndex], "rb")
                    batch = pickle.load(file)
                    start_index = batch_indices[fileIndex]  # Start from the current position in the batch
                    end_index = min(start_index + 500, len(batch))  # Ensure we don't exceed batch size
                    if end_index == len(batch):
                        listOfComp[fileIndex] = True
                    # Update batch index to reflect the next set of tokens to load
                    batch_indices[fileIndex] = end_index
                    for nextToken, nextPostings in batch[start_index: end_index]:  # Load only a small part of the batch
                        heapq.heappush(heap, (nextToken, fileIndex, nextPostings))
                    file.close()
            except EOFError:
                listOfComp[fileIndex] = True

        # Dump the remaining merged index
        if mergedIndex:
            self.dumpFinal(mergedIndex)


    def dumpFinal(self, mergedIndex, fileName="FinalIndex.pkl"):
        with open(fileName, "ab") as file:
            pickle.dump(mergedIndex, file)
            

    def printReport(self):
        unique_tokens = set()
        total_size = 0
        with open("FinalIndex.pkl", "rb") as file:
            while True:
                try:
                    data = pickle.load(file)
                    for token in data.keys():
                        unique_tokens.add(token)
                    total_size += sys.getsizeof(data)
                except EOFError:
                    break  # End of file reached
            print("Indexed Documents: " + str(self.currentDocId))
            print("Unique Tokens: " + str(len(unique_tokens)))
            print("Total Size: " + str(round((total_size)/1024,2)) + "kb")
         # maybe print top 10 most frequent tokens
         # print the most common document?
