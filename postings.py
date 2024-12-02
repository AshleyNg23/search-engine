
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
    
    def setTfidf(self,value):
        self.tfidf=value
    
    def __eq__(self, value):
        if isinstance(value, Postings):
            if self.docName==value.docName and self.docId==value.docId:
                tf=self.tfidf+value.tfidf
                value.tfidf=tf
                self.tfidf=tf
                return True
        return False
    
    def __hash__(self):
        return hash((self.docId,self.docName))
    
    def __lt__(self,value):
        if isinstance(value, Postings):
            if self.tfidf<value.tfidf:
                return True
            elif self.tfidf==value.tfidf:
                if self.docId>value.docId:
                    return True
        else:
            return False
