from flask import Flask

app = Flask(__name__) #__name__ is convention

@app.route('/')
def index():
    return 'ejwiopjfi!'

#flask run in terminal um die seite aufzurufen, flask run --reload damit man nicht immer neustarten muss