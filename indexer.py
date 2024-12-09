import os
import pickle
import math
import heapq
from collections import defaultdict
from postings import Postings
from tokenizer import tokenizer, computeSimHashFrequencies, checkSimilar, simHash
from bs4 import BeautifulSoup
import re
import json
import numpy as np




class Index(object):
    def __init__(self):
        self.chunk = 0
        self.inverted_index = {}
        self.simHashes = set()
        self.base_directory = ""
        self.currentDocId = 1
        self.amountOfPartial = 0
        self.chunkSize = 100000
        self.url_list = {}
        self.PR=[]
        self.url=[]




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
                #Similarity check with SimHash
                sh = simHash(computeSimHashFrequencies(tokenizer(text)))
                if not checkSimilar(self.simHashes, sh):
                    self.simHashes.add(sh)
                    url = soup1.get_text()
                    space_delemited_url = re.sub(r'\s+',' ',url)
                    for link in soup.find_all('a'):
                        if link.get('href'):
                            l=re.sub(r'\s+',' ',link.get('href'))
                            if space_delemited_url in self.url_list:
                                self.url_list[space_delemited_url].append(l)
                            else:
                                self.url_list[space_delemited_url]=[l]
                    if space_delemited_url not in self.url_list:
                        self.url_list[space_delemited_url]=[]
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
        self.PR=self.pagerank()
        self.createPartial()
        self.mergePartial()


    def pagerank(self):
        self.url = list(self.url_list.keys())
        url_matrix = np.zeros((len(self.url), len(self.url)))
        for i, url in enumerate(self.url):
            for linked_url in self.url_list[url]:
                if linked_url in self.url:
                    j = self.url.index(linked_url)
                    url_matrix[i, j] = 1
        m = np.shape(url_matrix)[0]
        epsilon=1e-12
        T = url_matrix.copy()
        for i in range(m):
            s = np.sum(T[i])
            # Normalize by the number of outgoing links to create transition probabilities
            # For websites with no outgoing links, set T[i,i]=1
            if s==0:
                T[i][i]=1
            else:
                T[i]=T[i]/s
        B = np.ones(np.shape(url_matrix))
        B=(1/m)*B
        G = (1-0.15)*T
        # assert np.all(np.abs(T.sum(axis=1) - 1.0) < 1e-12)
        # assert np.all(np.abs(G.sum(axis=1) - 1.0) < 1e-12)
        m = np.shape(G)[0]
        #print(P)
        pi = np.ones(m) / m
        #print(pi)
        diff = np.zeros(10000)
        #P=P.T
        for i in range(10000):
            #print(np.shape(pi))
            #P=P.T
            pi_n=pi@G+0.15
            #pi_n=np.linalg.solve(pi_n, temp)
            diff[i] = np.sum(np.abs(pi_n - pi))
            if diff[i] < epsilon:
                print('early_stop',i)
                pi=pi_n
                return pi
            pi=pi_n
            #print(pi)
        return pi

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
                        token, postings = pickle.load(file)
                        heapq.heappush(heap, (token, i, postings))
                    except EOFError:
                        break

        currentTerm = None
        currentPostings = []
        currentLetter = None
        seek_locations = {}

        output_directory = "IndexOfIndex"
        os.makedirs(output_directory, exist_ok=True)
        
        with open("MergedIndex.txt", "w", encoding="utf-8") as output_file:
            seek_position = output_file.tell()

            while heap:
                term, fileIndex, postings = heapq.heappop(heap)
                first_letter = term[0].lower()  # Determine the first letter of the term (case-insensitive)

                if term == currentTerm:
                    currentPostings.extend(postings)
                else:
                    if currentTerm is not None:
                        # Write the postings for the current term
                        posting_str = chr(0x1D).join(
                            f"{post.docId} {post.docName} {post.getTfidf(math.log(self.currentDocId / len(currentPostings), 10))} {post.tag_weight} {self.PR[self.url.index(post.docName)]}"
                            for post in currentPostings
                        )
                        output_file.write(f"{currentTerm} {posting_str}\n")
                        seek_locations[currentTerm] = seek_position
                        seek_position = output_file.tell()

                    # If the first letter of the term changes, dump the current seek_locations to a file
                    if currentLetter != first_letter:
                        if currentLetter is not None:
                            with open(f"IndexOfIndex/term_seek_locations_{currentLetter}.pkl", "wb") as seek_file:
                                pickle.dump(seek_locations, seek_file)
                        # Reset seek_locations for the new letter
                        seek_locations = {}
                        currentLetter = first_letter

                    currentPostings = postings
                    currentTerm = term

            # Dump the final term and its postings
            posting_str = chr(0x1D).join(
                f"{post.docId} {post.docName} {post.tf} {post.tag_weight}"
                for post in currentPostings
            )
            output_file.write(f"{currentTerm},{posting_str}\n")
            seek_locations[currentTerm] = seek_position

            # Dump the last seek_locations to a file
            if currentLetter is not None:
                with open(f"IndexOfIndex/term_seek_locations_{currentLetter}.pkl", "wb") as seek_file:
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


