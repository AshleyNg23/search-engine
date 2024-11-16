
class Postings():
    def __init__(self, docName, docId, tfidf):
        self.docName = docName
        self.docId = docId
        self.tfidf = tfidf

    def __lt__(self, other):
        if isinstance(other, Postings):
            return self.docId < other.docId
