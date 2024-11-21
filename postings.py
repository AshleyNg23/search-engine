
class Postings():
    def __init__(self, docName, docId, tfidf):
        self.docName = docName
        self.docId = docId
        self.tfidf = tfidf

    def getDocName(self):
        return self.docName
    
    def getDocId(self):
        return self.docId
    
