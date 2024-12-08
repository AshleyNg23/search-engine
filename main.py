from flask import Flask, request, render_template
import pickle
from postings import Postings
import json
from nltk import PorterStemmer
import math
import os
import time
from functools import reduce
from concurrent.futures import ThreadPoolExecutor


app = Flask(__name__)




@app.route('/')
def home():
    return render_template('search_home.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    query = request.form['query'] if request.method == 'POST' else request.args.get('query', '')  # Handle form and query params
    page = int(request.args.get('page', 1))  # Get the current page from the query string
    per_page = 10  # Number of results per page


    start_time = time.time()


    # Get all results based on the query
    all_results = return_results(query)


    end_time = time.time()
    elapsed_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds


    # Calculate pagination
    start = (page - 1) * per_page
   
    end = start + per_page
    try:
        paginated_results = all_results[start:end]  # Slice results for pagination
    except KeyError:
        paginated_results = all_results


    # Calculate total pages
    total_pages = math.ceil(len(all_results) / per_page)


    # Debugging output
    print(start_time, end_time, elapsed_time)
    print(f'{end_time} - {start_time} = {elapsed_time}')


    # Render the results template with pagination and other info
    return render_template(
        'results.html',
        query=query,
        results=paginated_results,
        num_results=len(all_results),
        elapsed_time=elapsed_time,
        current_page=page,
        total_pages=total_pages
    )




def fetch_postings(token):
    """Fetch postings list for a token from the appropriate file."""
    file_path = f"IndexOfIndex/IndexesWith{token[0]}"
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            file_dict = pickle.load(file)
            return file_dict.get(token, [])
    return []


# Parallel processing for token lookups
def get_matching_docs_parallel(search_tokens):
    matching_docs = []
    with ThreadPoolExecutor() as executor:
        # Map each token to the fetch_postings function
        results = list(executor.map(fetch_postings, search_tokens))
        matching_docs.append(results)
    return matching_docs


# Intersection of results
# def find_total_sum(search_tokens):
#     matching_docs = get_matching_docs_parallel(search_tokens)
#     print(matching_docs)
#     # Filter empty lists and find intersection
#     results = {}
#     for values in matching_docs[0]:
#         if values.getDocId() in results:
#             matching_docs[values.getDocId()] += values.getTfidf()
#         else:
#             matching_docs[values.getDocId()] = values.getTfidf()
#     return results






def return_results(query):
    start_time = time.time()
    ps = PorterStemmer()


    # break query into tokens
    search_tokens = query.lower().split(" ")
    search_tokens = { ps.stem(token) for token in search_tokens }
   


    # keep each posting result in a different index so we can track intersection
    # matching_docs = [set1 for _ in range(len(search_tokens))]
   
    #Find if the tokens in the SEARCH QUERY are in our Index
    #IF not in file then append an empty list.
    
    intersection = get_matching_docs_parallel(search_tokens)
    intersection=intersection[0]
    #print(intersection)
    intersection=tf_idf(intersection)
    intersection=sorted(intersection,reverse=True)
    end_time = time.time()
    print("Parallel Time:", end_time - start_time)

                       
        # try:
        #     while True:
        #         # load each pair
        #         # each line is expected to be a pair of a token (string) and its postings
        #         line = pickle.load(file)
        #         print(type(line))
        #         token = ""
        #         for item in line:
        #             # item can be token or postings, its weird so this is the only way to iterate through our pickle file
        #             if token:
        #                 # if the token was found, then item = posting, add to the matched docs list
        #                 for t in item:
        #                     #matching_docs[search_tokens.index(token)].add((t.docId,t.docName))
        #                     matching_docs[search_tokens.index(token)].add(t)
        #                 token = ""
        #             if item in search_tokens:
        #                 # if we found a matching keyword, save the word so we can collect its posting on the next iteration
        #                 token = item
        # except EOFError:
    if len(intersection) > 0:
        results = []
        for inf in intersection:
            url = inf.getDocName()
            # format title and url for front-end
            results.append({"title": f"Doc Id: {inf.getDocId()} (TF-IDF: {inf.getTfidf():.4f})","url": url})
        return results
    else:
        return [{"title": "No Results", "url": "N/A"}]
           


# def convert_to_link(posting):
#     if posting == []:
#         return {"title": "No Results", "url": "N/A"}
#     results = []
#     for post in posting[0]:
#         url = getUrl(post.getDocName())
#         # format title and url for front-end
#         results.append({"title": f"Doc Id: {post.getDocId()}", "url": f"{url}"})
#     return results


def getUrl(docName):
    docName = docName.replace("\\", "/")
    with open(docName, "r") as docFile:
        data = json.load(docFile)
        url = data.get('url')
        docFile.close()
        return url


def tf_idf(matching_docs):
    for i in matching_docs:
        for j in i:
            # print(j.getTfidf())
            tf=(1+math.log(j.getTfidf(),10))*math.log(55394/len(i),10)
            tf=tf*j.getWeight()
            j.setTfidf(tf)
    union_set=set()
    for s in matching_docs:
        union_set=union_set.union(s)
    return union_set






if __name__ == '__main__':
    app.run(debug=True)
