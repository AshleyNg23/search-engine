
class Postings():
    def __init__(self, docName, docId, tfidf):
        self.docName = docName
        self.docId = docId
        self.tfidf = tfidf

    def getDocName(self):
        return self.docName
    
    def getDocId(self):
        return self.docId
    
    def getTfidf(self):
        return self.tfidf
    
    def __eq__(self, value):
        if isinstance(value, Postings):
            if self.docName==value.docName and self.docId==value.docId:
                if self.tfidf>value.tfidf:
                    self.tfidf=value.tfidf
                else:
                    value.tfidf=self.tfidf
                return True
        return False
    
    def __hash__(self):
        return hash((self.docId,self.docName))
    
