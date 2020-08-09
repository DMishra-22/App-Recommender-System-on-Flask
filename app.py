import pandas as pd
from flask import Flask, request, render_template
from model import get_rec

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods = ['POST'])
def recommend():
    '''
    For rendering results on HTML GUI
    '''

    input_app = request.form['input']
    recommended_apps = get_rec(input_app)
    recommended_apps.rename("App Name", inplace = True)
    return render_template('index.html', recommendations_table = pd.DataFrame(recommended_apps).to_html())

if __name__ == "__main__":
    app.run(debug = True)
