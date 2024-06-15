import subprocess
import pandas as pd
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

import validators

def load_csv_data(filename):
    try:
        filepath = os.path.join('datalog', filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            # Process LinkedIn URLs, ensuring they are valid before converting to HTML links
            if 'LinkedIn' in df.columns:
                df['LinkedIn'] = df['LinkedIn'].apply(lambda x: f'<a href="{x}">{x}</a>' if validators.url(x) else x)
            # Continue with 'scholar_url' as you have been, assuming these are generally valid
            if 'scholar_url' in df.columns:
                df['scholar_url'] = df['scholar_url'].apply(lambda x: f'<a href="{x}">{x}</a>')
            return df.to_html(classes='table table-striped', escape=False, index=False, border=0)
        else:
            return f"<p>File does not exist: {filepath}</p>"
    except Exception as e:
        return f"<p>Error loading file: {str(e)}</p>"



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'query' in request.form:
            query = request.form['query']
            try:
                result = subprocess.run(
                    ['python', 'query_classifier.py', query],
                    text=True,
                    capture_output=True,
                    check=True
                )
                output = result.stdout
                flash('YAY , CSVs updated', 'success')
            except subprocess.CalledProcessError as e:
                flash('Failed to execute the script: ' + str(e), 'error')
            return redirect(url_for('index'))

        elif 'filename' in request.form:
            filename = request.form['filename']
            csv_html = load_csv_data(filename)
            return render_template('index.html', csv_html=csv_html)

    return render_template('index.html')
from flask import send_from_directory

@app.route('/download/<filename>')
def download_file(filename):
    # Define the directory where your CSV files are stored
    directory = os.path.join(app.root_path, 'datalog')
    try:
        return send_from_directory(directory, filename, as_attachment=True)
    except FileNotFoundError:
        flash('File not found!', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
