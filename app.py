from flask import Flask, render_template

app = Flask(__name__) #__name__ is convention

@app.route('/', methods=['GET', 'POST'])   #Homepage
def index():
    return render_template('index.html')

#flask run in terminal um die seite aufzurufen, flask run --reload damit man nicht immer neustarten muss

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/mein-bereich')
def meinBereich():
    return render_template('meinBereich.html')