
from flask import Flask, flash, redirect, render_template, url_for, request, send_file, session
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user
from CalculateResult import CalculateResult
from SchnellCheckFormular import SchnellCheckFormular
from AusführlicherCheckFormular import *

from PdfGenerator import PdfGenerator

app = Flask(__name__) 
bcrypt = Bcrypt(app)
pdf_generator = PdfGenerator()



app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)

bootstrap = Bootstrap5(app)

from db import db, User, RegisterForm, LoginForm


@app.route('/', methods=['GET', 'POST'])   #Homepage
def index():
    session['step'] = 1
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
        return redirect(url_for('result', filename=filename))

    return render_template('schnelltest.html', form=form)



@app.route("/result")
def result():
    filename = request.args.get('filename')
    form_data = session.get('form_data')
    test_type = session.get('test_type') 
    
    if form_data is None:
        return "Fehler: Formulardaten nicht gefunden."
    if test_type is None:
        return "Fehler: Testtyp nicht definiert."

    calculator = CalculateResult(test_type, form_data)  
    ampelfarbe = calculator.calcResults() 

    return render_template("result.html", filename=filename, form_data=form_data, ampelfarbe=ampelfarbe)


@app.route("/download/<filename>")
def download_pdf(filename):
    return send_file(filename, as_attachment=True)


@app.route('/ausführlicherTest', methods=['GET', 'POST'])
def ausführlicherTest():
    test_type = 'Ausführlich'
    session['test_type'] = test_type

    if 'step' not in session:
        session['step'] = 1
        session['form_data'] = {}

    form_classes = [AusführlicherCheck1, AusführlicherCheck2, AusführlicherCheck3, 
                    AusführlicherCheck4, AusführlicherCheck5]

    if 1 <= session['step'] <= 5:
        form = form_classes[session['step'] - 1]()
        if form.validate_on_submit():
            session['form_data'].update({field.name: field.data for field in form})
            if session['step'] == 5:
                return redirect(url_for('result'))
            else:
                session['step'] += 1
                return redirect(url_for('ausführlicherTest'))
    else:
        filename = pdf_generator.generate_pdf(form)
        return redirect(url_for('result', filename=filename))
        
        
    return render_template('ausführlicherTest.html', form=form)



if __name__ == "__main__":
    app.run(debug=True) 

