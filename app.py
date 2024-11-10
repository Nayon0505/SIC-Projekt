from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

#flask run in terminal um die seite aufzurufen