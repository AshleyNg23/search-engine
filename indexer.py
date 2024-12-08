from postings import Postings
<<<<<<< HEAD
from tokenizer import tokenizer, computeWordFrequencies
=======
from tokenizer import tokenizer
>>>>>>> da426cd933e6ac61c2531b0db542d674b7d00fa9
import os
from bs4 import BeautifulSoup
import re
import pickle
import json
import math
import heapq
from collections import defaultdict


class Index(object):
    def __init__(self):
          self.chunk = 0
          self.inverted_index = {}
          self.simHashes = set()
          self.base_directory = ""
          self.currentDocId = 1
          self.amountOfPartial = 0
          self.chunkSize = 100000


    def index(self, dir_name):
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
            #Reset the simHash for the new set of pages
            self.simHashes = set()
            for files in os.listdir(folderPath):
                filePath = os.path.join(folderPath, files)
                # Open the HTML file
                with open(filePath, "r") as file:
                    html_content = json.load(file)
               
                # Create a BeautifulSoup object
                soup = BeautifulSoup(html_content["content"], "lxml")
                soup1 = BeautifulSoup(html_content["url"],"lxml")
                text = soup.get_text()
<<<<<<< HEAD
                #space_delemited_text = re.sub(r'\s+',' ',text)
=======
>>>>>>> da426cd933e6ac61c2531b0db542d674b7d00fa9
                #Get url for faster finding in the search
                url = soup1.get_text()
                space_delemited_url = re.sub(r'\s+',' ',url)
                # Now you can use BeautifulSoup methods to extract data from the file
                # For example, to get all the links:
<<<<<<< HEAD


                # tokens = tokenizer(space_delemited_text)
                # freq = computeWordFrequencies(tokens)
=======
                word_tag_freq = defaultdict(list)
                for htmltag in soup.descendants:
                    if htmltag.name and htmltag.string: 
                        text = htmltag.get_text()
                        space_delimited_text = re.sub(r'\s+', ' ', text)
                        tokens = tokenizer(space_delimited_text)  # Tokenize the text
                        for token in tokens:
                            if htmltag.name == "h1" or htmltag.name == "h2" or htmltag.name == "h3" or htmltag.name == "bold" or htmltag.name == "strong" or htmltag.name == "title":
                                word_tag_freq[token].append(1.25)
                            else:
                                word_tag_freq[token].append(1)
>>>>>>> da426cd933e6ac61c2531b0db542d674b7d00fa9

                word_tag_freq = defaultdict(list)
                for htmltag in soup.descendants:
                    if htmltag.name and htmltag.string: 
                        text = htmltag.get_text()
                        space_delimited_text = re.sub(r'\s+', ' ', text)
                        tokens = tokenizer(space_delimited_text)  # Tokenize the text
                        for token in tokens:
                            if htmltag.name == "h1" or htmltag.name == "h2" or htmltag.name == "h3" or htmltag.name == "bold" or htmltag.name == "strong" or htmltag.name == "title":
                                word_tag_freq[token].append(1.25)
                            else:
                                word_tag_freq[token].append(1)
                # Duplication/Similiarity Check
                # Iterate through the tokens to log them into our inverted Index O(N) run-time O(N) space comp
<<<<<<< HEAD
                # for key,values in freq.items():
                #         self.logTokens(filePath, space_delemited_url, key, self.currentDocId, 1 + math.log(values, 10) ,values)
=======
>>>>>>> da426cd933e6ac61c2531b0db542d674b7d00fa9
                for key,tag_weight in word_tag_freq.items():
                        term_freq = len(tag_weight) 
                        self.logTokens(filePath, space_delemited_url, key, self.currentDocId, 1 + math.log(term_freq, 10) , max(tag_weight))
                        self.chunk += 1
                        if self.chunk >= self.chunkSize:
                            self.createPartial()
                            self.chunk = 0
                self.currentDocId += 1
        self.createPartial()
        self.mergePartial()
           
    def logTokens(self, filePath, url, token, docId, tf, tag_weight):
        if token not in self.inverted_index:
            self.inverted_index[token] = []
        self.inverted_index[token].append(Postings(filePath, url, docId, tf, tag_weight))


    def createPartial(self):
        with open(f"PartialIndex{self.amountOfPartial}.pkl", "wb") as file:
            for tokens, postings in sorted(self.inverted_index.items()):
                pickle.dump((tokens,postings), file)
        self.amountOfPartial += 1
        self.inverted_index.clear()


    def mergePartial(self):
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
        currentLetter = None
               
        while heap:
            term, fileIndex, postings = heapq.heappop(heap)
            #Find the first letter of each term
            if currentLetter == None:
                currentLetter = term[0]
            #If the term is equal to the currentTerm extend the currentPostings
            if term == currentTerm:
                currentPostings.extend(postings)
            else:
                #Check to see if the currentTerm is not None
                if currentTerm != None:
                    # for posts in currentPostings:
                    #     posts.setTfidf(math.log(self.currentDocId/len(currentPostings),10)) #Set the tfIDF value for this posts
                    mergedIndex[currentTerm] = currentPostings
               
                #Keep track of the amount of unique tokens so we don't have to open the file to check.            
                currentPostings = postings
                currentTerm = term
           
            if currentTerm[0] != currentLetter:
                self.dumpFinal(currentLetter,mergedIndex)
                currentLetter = currentTerm[0]
                mergedIndex.clear()
           
            try:
                nextToken, nextPostings = pickle.load(listOfFiles[fileIndex])
                heapq.heappush(heap, (nextToken, fileIndex, nextPostings))
            except EOFError:
                listOfFiles[fileIndex].close()
        self.dumpFinal(currentLetter, mergedIndex)




    def dumpFinal(self, curLetter, mergedIndex, fileName = "FinalIndex.pkl"):
        try:
            os.mkdir("IndexOfIndex")
        except FileExistsError:
            pass
        with open(f"IndexOfIndex/IndexesWith{curLetter}", "wb") as file:
            pickle.dump(mergedIndex, file)
        with open(fileName, "ab") as file:
            pickle.dump(mergedIndex,file)
   
    def printReport(self):
        unique_tokens = set()
        with open("FinalIndex.pkl", "rb") as file:
            while True:
                try:
                    pickleFile = pickle.load(file)
                    for token in pickleFile.keys():
                        unique_tokens.add(token)
                except EOFError:
                    break  # End of file reached
            with open("FileCount" , "wb") as fileCount:
                pickle.dump(self.currentDocId, fileCount)
            print("Indexed Documents: " + str(self.currentDocId))
            print("Unique Tokens: " + str(len(unique_tokens)))
