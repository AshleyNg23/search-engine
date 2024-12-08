import os
import pickle
import math
import heapq
from collections import defaultdict
from postings import Postings
from tokenizer import tokenizer
from bs4 import BeautifulSoup
import re
import json




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
        for folders in os.listdir(self.base_directory):
            folderPath = os.path.join(self.base_directory, folders)
            self.simHashes = set()
            for files in os.listdir(folderPath):
                filePath = os.path.join(folderPath, files)
                with open(filePath, "r", encoding = "utf-8") as file:
                    html_content = json.load(file)
               
                soup = BeautifulSoup(html_content["content"], "lxml")
                soup1 = BeautifulSoup(html_content["url"], "lxml")
                text = soup.get_text()
                url = soup1.get_text()
                space_delemited_url = re.sub(r'\s+',' ',url)
                word_tag_freq = defaultdict(list)
                for htmltag in soup.descendants:
                    if htmltag.name and htmltag.string:
                        text = htmltag.get_text()
                        space_delimited_text = re.sub(r'\s+', ' ', text)
                        tokens = tokenizer(space_delimited_text)
                        for token in tokens:
                            if htmltag.name in ["h1", "h2", "h3", "bold", "strong", "title"]:
                                word_tag_freq[token].append(1.25)
                            else:
                                word_tag_freq[token].append(1)


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
                pickle.dump((tokens, postings), file)
        self.amountOfPartial += 1
        self.inverted_index.clear()




    def mergePartial(self):
        listOfFiles = []
        heap = []
        for i in range(self.amountOfPartial):
            with open(f"PartialIndex{i}.pkl", "rb") as file:
                while True:
                    try:
                        token,postings = pickle.load(file)
                        heapq.heappush(heap, (token, i, postings))
                    except EOFError:
                        break
       
        currentTerm = None
        currentPostings = []
        currentLetter = None
        with open("MergedIndex.txt", "w", encoding = "utf-8") as output_file:
            seek_locations = {}
            seek_position = output_file.tell()
           
            while heap:
                term, fileIndex, postings = heapq.heappop(heap)
                if term == currentTerm:
                    currentPostings.extend(postings)
                else:
                    if currentTerm is not None:
                        posting_str = chr(0x1D).join(f"{post.docId} {post.docName} {post.getTfidf(math.log(self.currentDocId/len(currentPostings), 10))} {post.tag_weight}" for post in currentPostings)
                        output_file.write(f"{currentTerm} {posting_str}\n")
                        seek_locations[currentTerm] = seek_position
                        seek_position = output_file.tell()
                   
                    currentPostings = postings
                    currentTerm = term
               
           
            # Dump the final term and its postings
            posting_str = chr(0x1D).join(f"{post.docId} {post.docName} {post.tf} {post.tag_weight}" for post in currentPostings)
            output_file.write(f"{currentTerm},{posting_str}\n")
            seek_locations[currentTerm] = seek_position
       
        # Store seek locations in a pickle file
        with open("term_seek_locations.pkl", "wb") as seek_file:
            pickle.dump(seek_locations, seek_file)




    def printReport(self):
        unique_tokens = set()
        with open("FinalIndex.pkl", "rb") as file:
            while True:
                try:
                    pickleFile = pickle.load(file)
                    for token in pickleFile.keys():
                        unique_tokens.add(token)
                except EOFError:
                    break
           
            with open("FileCount" , "wb") as fileCount:
                pickle.dump(self.currentDocId, fileCount)
            print("Indexed Documents: " + str(self.currentDocId))
            print("Unique Tokens: " + str(len(unique_tokens)))


