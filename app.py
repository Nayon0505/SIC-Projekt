from flask import Flask, redirect, render_template, url_for
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__) #__name__ is convention
bcrypt = Bcrypt(app)




app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
)

from db import db, User, insert_sample, RegisterForm, LoginForm


@app.route('/', methods=['GET', 'POST'])   #Homepage
def index():
    return render_template('index.html')

#flask run in terminal um die seite aufzurufen, flask run --reload damit man nicht immer neustarten muss

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('meinBereich'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
     form = RegisterForm()
     if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))  
     return render_template('register.html', form = form)

@app.route('/mein-bereich', methods=['GET', 'POST'])
@login_required
def meinBereich():
    return render_template('meinBereich.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))