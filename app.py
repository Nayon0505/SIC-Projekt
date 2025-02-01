
from flask import Flask, flash, redirect, render_template, url_for, request, send_file, jsonify, session
from flask_bootstrap import Bootstrap5
import os
import json
from io import BytesIO
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from Formular import SchnellCheckFormular


from reportlab.pdfgen import canvas 
from reportlab.lib.pagesizes import letter 
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from PdfGenerator import PdfGenerator

app = Flask(__name__) 
bcrypt = Bcrypt(app)
pdf_generator = PdfGenerator()



app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)

bootstrap = Bootstrap5(app)

from db import db, User, insert_sample, RegisterForm, LoginForm


@app.route('/', methods=['GET', 'POST'])   #Homepage
def index():
    return render_template('index.html')

#flask run in terminal um die seite aufzurufen, flask run --reload damit man nicht immer neustarten muss
@app.route('/ausführlicherTest', methods=['GET', 'POST'])   #Homepage
def ausführlicherTest():
    return render_template('ausführlicherTest.html')

@app.route('/insert/sample')
def run_insert_sample():
    insert_sample()
    return 'Database flushed and populated with some sample data.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                
                return redirect(url_for('meinBereich', name=user.username))
            else: 
                flash("Falsches Passwort")
        else:
            flash("Der Nutzer existiert nicht.")

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

@app.route('/mein-bereich/<string:name>', methods=['GET', 'POST'])
@login_required
def meinBereich(name):
    return render_template('meinBereich.html', content=name)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
def home():
    logout_user()
    return redirect(url_for('index'))


@app.route('/schnelltest', methods=['GET', 'POST'])
def schnelltest(): 
    form = SchnellCheckFormular()
    if form.validate_on_submit():
    
        data = {
            'Betrieb': form.betrieb.data,
            'TSE': form.tse.data,
            'Beleg': form.beleg.data,
            'Pruefung': form.pruefung.data,
            'Trennung': form.trennung.data,
            'Einnahmen': form.einnahmen.data,
            'Steuererklärungen': form.steuererklärungen.data,
            'Nachforderungen': form.nachforderungen.data,
            'Trinkgelder': form.trinkgelder.data,
            'Schulung': form.schulung.data
        }
        filename = pdf_generator.generate_pdf(form)
        return redirect(url_for('download_confirmation', filename=filename))

    return render_template('schnelltest.html', form=form)



@app.route("/download_confirmation")
def download_confirmation():
    filename = request.args.get('filename')
    form_data = session.get('form_data')
    ampelfarbe = session.get('ampelfarbe')
    
    if form_data is None:
        return "Fehler: Formulardaten nicht gefunden."
    
    pos_answers = 0
    if form_data['TSE'] == "ja" or form_data['TSE'] == "unsicher":
        pos_answers += 10
    if form_data['Beleg'] == "ja":
        pos_answers += 9
    if form_data['Pruefung'] == "ja":
        pos_answers += 8
    if form_data['Trennung'] == "ja":
        pos_answers += 10
    if form_data['Einnahmen'] == "ja":
        pos_answers += 10
    if form_data['Steuererklärungen'] == "ja":
        pos_answers += 8
    if form_data['Nachforderungen'] == "nein":
        pos_answers += 9
    if form_data['Trinkgelder'] == "ja":
        pos_answers += 8
    if form_data['Schulung'] == "ja":
        pos_answers += 7

    if (pos_answers < 50) :       
        ampelfarbe = "rot"
    elif (pos_answers <= 68):
        ampelfarbe = "gelb"
    else:
        ampelfarbe = "grün"
    
    return render_template("download_confirmation.html", filename=filename, form_data=form_data, ampelfarbe=ampelfarbe)




@app.route("/download/<filename>")
def download_pdf(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True) 

