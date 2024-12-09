from flask import Flask, request, render_template
import pickle
from postings import Postings
import json
from nltk import PorterStemmer
import math
import os
import time
import re
from functools import reduce
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache




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
    with open(f"term_seek_locations.pkl", "rb") as file:
        data = pickle.load(file)
        return
    file_path = f"IndexOfIndex/IndexesWith{token[0]}"
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            file_dict = pickle.load(file)
            return file_dict.get(token, [])
    return []




# Parallel processing for token lookups
def get_matching_docs_parallel(search_tokens):
    matching_docs = []
    MergedIndex = open("MergedIndex.txt", "r", encoding = "utf-8")
    for tokens in search_tokens:
        with open(f"IndexOfIndex/term_seek_locations_{tokens[0]}.pkl", "rb") as file:
            data = pickle.load(file)
            if tokens in data:
                MergedIndex.seek(data[tokens])
                line = MergedIndex.readline()
                matching_docs.append(line[len(tokens) + 1::].split(chr(0x1D)))
            else:
                matching_docs.append([])
    return matching_docs
            

    # with open(f"term_seek_locations.pkl", "rb") as file:
    #     data = pickle.load(file)
    #     for tokens in search_tokens:
    #         if tokens in data:
    #             MergedIndex = open("MergedIndex.txt", "r", encoding = "utf-8")
    #             MergedIndex.seek(data[tokens])
    #             line = MergedIndex.readline()
    #             matching_docs.append(line[len(tokens) + 1::].split(chr(0x1D)))
    #         else:
    #             matching_docs.append([])
    # return matching_docs




# Intersection of results
def find_total_sum(search_tokens):
    matching_docs = get_matching_docs_parallel(search_tokens)
    # Filter empty lists and find intersection
    results = {}
    for lists in matching_docs:
        for values in lists:
            value = values.split(" ")
            if value[1] in results:
                results[value[1]] += float(value[2])
                results[value[1]] += 2*float(value[4])
            else:
                results[value[1]] = float(value[2])
                results[value[1]] += 2*float(value[4])
    return results












def return_results(query):
    start_time = time.time()
    ps = PorterStemmer()




    # break query into tokens
    search_tokens = query.strip().lower().split(" ")
    search_tokens = { ps.stem(token.strip()) for token in search_tokens }
   
    if '' in search_tokens and len(search_tokens) == 1:
        return [{"title": "No Results", "url": "N/A"}]
   
    if '' in search_tokens:
        search_tokens.remove('')






    # keep each posting result in a different index so we can track intersection
    # matching_docs = [set1 for _ in range(len(search_tokens))]
   
    #Find if the tokens in the SEARCH QUERY are in our Index
    #IF not in file then append an empty list.
   
    intersection = find_total_sum(search_tokens)
    intersection = dict(sorted(intersection.items(), key=lambda item: item[1], reverse = True))
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
        for docName, tfIDF in intersection.items():
           
            # format title and url for front-end
            results.append({"title": f"(TF-IDF: {tfIDF:.4f})","url": docName})
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












if __name__ == '__main__':
    app.run(debug=True)