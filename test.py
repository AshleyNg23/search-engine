import pickle
from postings import Postings

with open('indexofindex.pkl', "rb") as file:
        ind=pickle.load(file)
        target_dict=ind['learn']
        with open('FinalIndex.pkl', "rb") as f:
            for read in range(target_dict+1):
                mergeIndex=pickle.load(f)
            f.close()
            for i in mergeIndex['learn']:
                    print(i.getDocId(),i.getDocName())