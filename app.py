from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def query_form():
    return render_template('query.html')

@app.route('/process_query', methods=['POST'])
def process_query():
    query = request.form['query']
    result = run_query_classifier(query)
    return render_template('result.html', result=result)

def run_query_classifier(query):
    result = subprocess.run(['python', 'query_classifier.py', query], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 5000, debug=True)
#check