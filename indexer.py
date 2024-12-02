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
        if self.inverted_index:
                self.createPartial()
        self.mergePartial()
            
    

    def createPartial(self):
        with open(f"PartialIndex{self.amountOfPartial}.pkl", "wb") as file:
            #for tokens, postings in sorted(self.inverted_index.items()):
            pickle.dump(self.inverted_index, file)
        self.amountOfPartial += 1
        self.inverted_index.clear()

    def mergePartial(self):
        # currentChunk = 0
        # listOfFiles = []
        # heap = []
        # for i in range(self.amountOfPartial):
        #     file = open(f"PartialIndex{i}.pkl", "rb")
        #     listOfFiles.append(file)
        #     try:
        #         token, postings = pickle.load(file)
        #         heapq.heappush(heap, (token, i, postings))
        #     except EOFError:
        #         file.close()
        
        # mergedIndex = {}
        # currentTerm = None
        # currentPostings = []
                
        # while heap:
        #     term, fileIndex, postings = heapq.heappop(heap)

        #     if term == currentTerm:
        #         currentPostings.extend(postings)
        #     else:
        #         if currentTerm != None:
        #             mergedIndex[currentTerm] = currentPostings
                
        #         #Keep track of the amount of unique tokens so we don't have to open the file to check.            
        #         currentPostings = postings
        #         currentTerm = term
        #         currentChunk += 1
            
        #     if currentChunk >= self.chunkSize:
        #         self.dumpFinal(mergedIndex)
        #         mergedIndex.clear()
            
        #     try:
        #         nextToken, nextPostings = pickle.load(listOfFiles[fileIndex])
        #         heapq.heappush(heap, (nextToken, fileIndex, nextPostings))
        #     except EOFError:
        #         listOfFiles[fileIndex].close()
        # self.dumpFinal(mergedIndex)
        index_index={}
        final={}
        part=0;
        number=0;
        while 1:
                empty=0
                decision=1
                dict_sum={}
                for index in range(0,self.amountOfPartial):
                    with open(f"PartialIndex{index}.pkl", "rb") as fi:
                            loaded_dict = pickle.load(fi)
                            if decision:
                                if len(loaded_dict)!=0:
                                        first_key = next(iter(loaded_dict))
                                        post=loaded_dict.pop(first_key)
                                        #print(type(post))
                                        if first_key in index_index:
                                            index_index[first_key].extend(post)
                                        else:
                                             index_index[first_key]=[]
                                             index_index[first_key].extend(post)
                                        # with open('report.txt', 'a') as file:
                                        #     file.write(f"token: {first_key}, post: {post}")
                                        #     file.close()
                                        decision=0
                                        fi.close()
                                        os.remove(f"PartialIndex{index}.pkl")
                                        with open(f"PartialIndex{index}.pkl", "wb") as f:
                                            pickle.dump(loaded_dict, f)
                                            f.close()
                                else:
                                        empty+=1
                                        continue
                            else:
                                if len(loaded_dict)!=0:
                                        if first_key in loaded_dict:
                                            post=loaded_dict.pop(first_key)
                                            fi.close()
                                            os.remove(f"PartialIndex{index}.pkl")
                                            with open(f"PartialIndex{index}.pkl", "wb") as f:
                                                    pickle.dump(loaded_dict, f)
                                                    f.close()
                                            #print(index_index[first_key])
                                            index_index[first_key].extend(post)
                                            # with open('report.txt', 'a') as file:
                                            #         file.write(f", {post}")
                                            #         file.close()
                            fi.close()
                number=number+1
                final[first_key]=part
                if number%1000==0:
                     self.dumpFinal(index_index)
                     index_index.clear()
                     part=part+1
                # with open('report.txt', 'a') as file:
                #     file.write(f"\n")
                #     file.close()
                if empty==self.amountOfPartial:
                    self.dumpFinal(index_index)
                    index_index.clear()
                    with open(f"indexofindex.pkl", "wb") as f:
                            pickle.dump(final, f)
                            f.close()
                    break


    def dumpFinal(self, mergedIndex, fileName = "FinalIndex.pkl"):
        with open(fileName, "ab") as file:
            # for token, post in mergedIndex.items():
            pickle.dump(mergedIndex, file)
            
         

    def logTokens(self, filePath, token, docId, frequency):
        # key = token
        # value = (docId, frequency)
        # self.invertex_index[key] array, append value tuple
        if token not in self.inverted_index:
            self.inverted_index[token] = []
        self.inverted_index[token].append(Postings(filePath, docId, frequency))
        pass

    def printReport(self):
        unique_tokens = 0
        total_size = 0
        with open("FinalIndex.pkl", "rb") as file:
            token= pickle.load(file)
            for dict1 in token:
                try:
                    unique_tokens+=len(dict1)
                    total_size += sys.getsizeof(dict1)
                except EOFError:
                    break  # End of file reached
            print("Indexed Documents: " + str(self.currentDocId))
            print("Unique Tokens: " + str(unique_tokens))
            print("Total Size: " + str(round((total_size)/1024,2)) + "kb")
