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
                            # matching_docs[search_tokens.index(token)].add((t.docId,t.docName))
                            matching_docs[search_tokens.index(token)].add(t)
                        token = ""
                    if item in search_tokens:
                        # if we found a matching keyword, save the word so we can collect its posting on the next iteration
                        token = item
        except EOFError:
            intersect = set.intersection(*matching_docs) if len(matching_docs) > 1 else matching_docs[0]

            if not intersect:
                return [{"title": "No Results", "url": "N/A"}]

            # sort results by tf idf
            sorted_results = sorted(intersect, key=lambda p: p.getTfidf(), reverse=True)

            results = []
            for inf in sorted_results:
                url = getUrl(inf.getDocName())
                results.append({
                    "title": f"Doc Id: {inf.getDocId()} (TF-IDF: {inf.getTfidf():.2f})",
                    "url": url
                })

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