class Postings():


    def __init__(self, filePath, url, docId, tf, tag_weight):
        self.docName = url
        self.docId = docId
        self.tfidf = tf
        self.filePath = filePath
        self.tf = tf
        self.tag_weight = tag_weight


    def getDocName(self):
        return self.docName
   
    def getDocId(self):
        return self.docId
   
    def getTfidf(self, idf):
        return self.tf * idf * self.tag_weight


   
    def setTfidf(self,value):
        self.tfidf=value


    def getWeight(self):
        return self.tag_weight


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