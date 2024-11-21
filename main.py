from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('search_home.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = return_results(query)  # Replace with your search engine logic
    return render_template('results.html', query=query, results=results)

def return_results(query):
    # Dummy search logic
    return [{"title": f"Result for {query}", "url": "#"}]

if __name__ == '__main__':
    app.run(debug=True)