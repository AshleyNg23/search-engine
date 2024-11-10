from postings import Postings
from tokenizer import tokenizer, computeWordFrequencies
import os
from bs4 import BeautifulSoup
import re

class Index(object):
    def __init__(self):
          self.inverted_index = {}
          # {token_name = [(docId, docFrequency), (1, 7), (2, 3)]}
          self.base_directory = ""
          self.currentDocId = 1
    
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
            for files in os.listdir(folders):
                filePath = os.path.join(files)
                # Open the HTML file
                with open(filePath, "r") as file:
                    html_content = file.read()

                # Create a BeautifulSoup object
                soup = BeautifulSoup(html_content, "lxml")

                text = soup.get_text()
                space_delemited_text = re.sub('\s+',' ',text)

                # Now you can use BeautifulSoup methods to extract data from the file
                # For example, to get all the links:
                tokens = tokenizer(space_delemited_text)
                freq = computeWordFrequencies(tokens)
                # Iterate through the tokens to log them into our inverted Index O(N) run-time O(N) space comp
                for key,values in freq.items():
                    self.logTokens(key, self.currentDocId, values)
                self.currentDocId += 1
            

         




    def getTokens(self, docName):
        # get the tokens from the document with their frequency
        # return {token: freq}
        pass

    def logTokens(self, token, docId, frequency):
        # key = token
        # value = (docId, frequency)
        # self.invertex_index[key] array, append value tuple
        if token not in self.inverted_index:
            self.inverted_index[token] = []
        self.inverted_index[token].append(Postings(docId, frequency))

        '''
        Someway to write this into a list.
        Lecture went over Partial Merge.
        '''
        pass

    def printReport(self):
         print("Indexed Documents: " + self.currentDocId)
         print("Unique Tokens: " + self.inverted_index.keys().length())
         print("Total Size: ")
         # maybe print top 10 most frequent tokens
         # print the most common document?
