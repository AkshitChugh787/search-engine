from flask import Flask, render_template, request
from tabulate import tabulate
import pandas as pd

app = Flask(__name__)

def search_dataframe(df, keywords):
    all_columns = df.apply(lambda x: ' '.join(x.astype(str)), axis=1)
    mask = all_columns.str.contains(keywords, case=False)
    return df[mask]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    df = pd.read_csv('HR Manager Payer Test cases.csv')
    keywords = request.form['keywords']
    results = search_dataframe(df, keywords)

    if len(results) > 0:
        headers = list(results.columns)
        rows = [list(row) for i, row in results.iterrows()]
        table = tabulate(rows, headers=headers, showindex=True, tablefmt="html")
        return render_template('results.html', table=table)
    else:
        message = "No results found for the search keywords."
        return render_template('results.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
