
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




    def getTokens(self, docName):
        # get the tokens from the document with their frequency
        # return {token: freq}
        pass

    def logTokens(self, token, docId, frequency):
        # key = token
        # value = (docId, frequency)
        # self.invertex_index[key] array, append value tuple
        pass

    def printReport(self):
         print("Indexed Documents: " + self.currentDocId)
         print("Unique Tokens: " + self.inverted_index.keys().length())
         print("Total Size: ")
         # maybe print top 10 most frequent tokens
         # print the most common document?
