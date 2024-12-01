from flask import Flask, request, render_template
import pickle
from postings import Postings
import json
from nltk import PorterStemmer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('search_home.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = return_results(query)
    return render_template('results.html', query=query, results=results, num_results=len(results))

def return_results(query):
    ps = PorterStemmer()

    # break query into tokens
    search_tokens = query.lower().split(" ")
    search_tokens = [ ps.stem(token) for token in search_tokens ]
    set1={}
    set1=set(set1)
    matching_docs=[]

    # keep each posting result in a different index so we can track intersection
    matching_docs = [set1 for _ in range(len(search_tokens))]
    for _ in range(len(search_tokens)):
        matching_docs.append(set1)
    with open('FinalIndex.pkl', "rb") as file:
        try:
            while True: 
                # load each pair
                # each line is expected to be a pair of a token (string) and its postings
                line = pickle.load(file)
                token = ""
                for item in line:
                    # item can be token or postings, its weird so this is the only way to iterate through our pickle file
                    if token:
                        # if the token was found, then item = posting, add to the matched docs list
                        for t in item:
                            #matching_docs[search_tokens.index(token)].add((t.docId,t.docName))
                            matching_docs[search_tokens.index(token)].add(t)
                        token = ""
                    if item in search_tokens:
                        # if we found a matching keyword, save the word so we can collect its posting on the next iteration
                        token = item
        except EOFError:
            contains_all_words = []
            if len(matching_docs) > 1:
                # TODO: Make this work for queries with more than one word
                intersect=matching_docs[0]
                for l in range(1,len(matching_docs)):
                    intersect=set((intersect) & matching_docs[l])
                # contains_all_words = [
                #     posting for posting in matching_docs
                #     if all(posting.getDocId() in {p.getDocId() for p in all_postings} for all_postings in matching_docs[1:])
                # ]
                file.close()
                if intersect == []:
                    return {"title": "No Results", "url": "N/A"}
                results = []
                intersect=sorted(intersect,reverse=True)
                for inf in intersect:
                    url = getUrl(inf.getDocName())
                    # format title and url for front-end
                    results.append({"title": f"Doc Id: {inf.getDocId()} (TF-IDF: {inf.getTfidf():.2f})","url": url})
                return results
                #return [convert_to_link(p) for p in contains_all_words]
            else:
                file.close()
                # query was one word, so just convert the single list of postings to link
                #return convert_to_link(matching_docs[0])
                if matching_docs[0] == set({}):
                    return {"title": "No Results", "url": "N/A"}
                results = []
                matching_docs[0]=sorted(matching_docs,reverse=True)
                for inf in matching_docs[0]:
                    url = getUrl(inf.getDocName())
                    # format title and url for front-end
                    results.append({"title": f"Doc Id: {inf.getDocId()} (TF-IDF: {inf.getTfidf():.2f})","url": url})
                return results

def convert_to_link(posting):
    if posting == []:
        return {"title": "No Results", "url": "N/A"}
    results = []
    for post in posting[0]:
        url = getUrl(post.getDocName())
        # format title and url for front-end
        results.append({"title": f"Doc Id: {post.getDocId()}", "url": f"{url}"})
    return results

def getUrl(docName):
    with open(docName, "r") as docFile:
        data = json.load(docFile)
        url = data.get('url')
        docFile.close()
        return url

if __name__ == '__main__':
    app.run(debug=True)