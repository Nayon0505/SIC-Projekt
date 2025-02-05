
from flask import Flask, flash, redirect, render_template, url_for, request, send_file, session
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user
from CalculateResult import CalculateResult
from SchnellCheckFormular import SchnellCheckFormular
from AusführlicherCheckFormular import *

from PdfGenerator import PdfGenerator

import logging

# app.logger.setLevel(logging.DEBUG)  # Setze den Log-Level auf DEBUG
# app.logger.debug("Das ist eine Debug-Nachricht.")
# app.logger.info("Das ist eine Info-Nachricht.")
# app.logger.warning("Das ist eine Warnung.")


app = Flask(__name__) 
bcrypt = Bcrypt(app)
pdf_generator = PdfGenerator()

app.logger.setLevel(logging.DEBUG)  # Setze den Log-Level auf DEBUG


app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)

bootstrap = Bootstrap5(app)

from db import db, User, RegisterForm, LoginForm


@app.route('/', methods=['GET', 'POST'])   #Homepage
def index():
    # session['step'] = 1
    session.pop('form_data', default= None)
    session.pop('step', default= None)

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
    test_type = 'Schnell'
    session['test_type'] = test_type
    
    form = SchnellCheckFormular() 
    if form.validate_on_submit():
        
        
        session['form_data'] = {field.name: field.data for field in form}  
        app.logger.debug(f'Form data Schnelltest: {session['form_data']} Test Type: {test_type}-----------------------------------')


        calculator = CalculateResult(test_type, session['form_data'])  
        app.logger.debug(f'Calculator inputs, testtype: {test_type}, form data: {session['form_data']}------------------------------------')

        ampelfarbe, _ = calculator.calcResults() 
        _, punkte = calculator.calcResults()
        session['ampelfarbe'] = ampelfarbe
        app.logger.debug(f'Ampelfarbe result: {ampelfarbe}, session ampelfarbe: {session['ampelfarbe']},  Punkte: {punkte} ------------------------------------------')

        filename = pdf_generator.generate_pdf(session['form_data'])
        
        return redirect(url_for('result', filename=filename))

    return render_template('schnelltest.html', form=form)


@app.route('/ausführlicherTest', methods=['GET', 'POST'])
def ausführlicherTest():
    test_type = 'Ausführlich'
    session['test_type'] = test_type
    app.logger.debug(f'Session Data1: {session}')

    if 'step' not in session:     #Step wird bei Index definiert, deswegen geht er hier eigtl nicht rein
        session['step'] = 1
        session['form_data'] = {}
        app.logger.debug(f'Session Data3: {session['form_data']}')



    form_classes = [AusführlicherCheck1, AusführlicherCheck2, AusführlicherCheck3, 
                    AusführlicherCheck4, AusführlicherCheck5]

    if 1 <= session['step'] <= 5:
 
        form = form_classes[session['step'] - 1]()
        if form.validate_on_submit():
            session['form_data'].update({field.name: field.data for field in form})
            app.logger.debug(f'Form Data: {session['form_data']}')
            if session['step'] == 5:
                calculator = CalculateResult(test_type, session['form_data'])  
                app.logger.debug(f'Calculator inputs, testtype: {test_type}, form data: {session['form_data']}------------------------------------')

                ampelfarbe, _ = calculator.calcResults() 
                _, punkte = calculator.calcResults()
                session['ampelfarbe'] = ampelfarbe
                app.logger.debug(f'Ampelfarbe result: {ampelfarbe}, session ampelfarbe: {session['ampelfarbe']},  Punkte: {punkte} ------------------------------------------')

              
                filename = pdf_generator.generate_pdf(session['form_data'])
                app.logger.debug(f'Filename-------------------------------------------------------------------------------------------------------:')
                return redirect(url_for('result', filename = filename))
            else:
                session['step'] += 1
                app.logger.debug(f'Session Step:------------------------------------------------------------------------ {session['step']}')
                return redirect(url_for('ausführlicherTest'))
    else:
        filename = pdf_generator.generate_pdf(session['form_data'])
        app.logger.debug(f'Filename-------------------------------------------------------------------------------------------------------:')

        return redirect(url_for('result', filename=filename))
        
        
    return render_template('ausführlicherTest.html', form=form)



@app.route("/result")
def result():
    filename = request.args.get('filename')

    return render_template("result.html", filename=filename, ampelfarbe = session['ampelfarbe'])


@app.route("/download/<filename>")
def download_pdf(filename):
    return send_file(filename, as_attachment=True)






if __name__ == "__main__":
    app.run(debug=True) 

