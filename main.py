from flask import Flask, request, render_template
import pickle
from postings import Postings
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('search_home.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = return_results(query)
    return render_template('results.html', query=query, results=results)

def return_results(query):
    # break query into tokens
    search_tokens = query.split(" ");
    # keep each posting result in a different index so we can track intersection
    matching_docs = [[] * len(search_tokens)]
    with open('FinalIndex.pkl', "rb") as file:
        try:
            while True: 
                # load each pair
                line = pickle.load(file)
                token = ""
                for item in line:
                    # item can be token or postings, its weird so this is the only way to iterate through our pickle file
                    if token != "":
                        # if the token was found, then item = posting, add to the matched docs list
                        matching_docs[search_tokens.index(token)].append(item)
                        token = ""
                    if item in search_tokens:
                        # if we found a matching keyword, save the word so we can collect its posting on the next iteration
                        token = item
        except EOFError:
            contains_all_words = []
            if len(matching_docs) > 1:
                # TODO: Make this work for queries with more than one word
                contains_all_words = [
                    posting for posting in matching_docs
                    if all(posting.getDocId() in {p.getDocId() for p in all_postings} for all_postings in matching_docs[1:])
                ]
                file.close()
                return [convert_to_link(p) for p in contains_all_words]
            else:
                file.close()
                # query was one word, so just convert the single list of postings to link
                return convert_to_link(matching_docs[0])

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