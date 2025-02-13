
from flask import Flask, flash, redirect, render_template, url_for, request, send_file, session
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func
import werkzeug

from CalculateResult import CalculateResult
from SchnellCheckForm import SchnellCheckForm
from AusführlicherCheckForm import *

from PdfGenerator import PdfGenerator

import logging


app = Flask(__name__) 
bcrypt = Bcrypt(app)
pdf_generator = PdfGenerator()
app.logger.setLevel(logging.DEBUG)  

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)

from db import *


bootstrap = Bootstrap5(app)

MAX_REPORTS_PER_USER = 3


@app.route('/', methods=['GET', 'POST'])   #Homepage
def index():
    # session['step'] = 1
    session.pop('form_data', default= None)
    session.pop('step', default= None)

    if current_user.is_authenticated:
        return render_template('index.html',hide_login_register = True)
    else:
        return render_template('index.html',hide_mein_bereich = True, hide_logout = True)
    

#flask run in terminal um die seite aufzurufen, flask run --reload damit man nicht immer neustarten muss


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)  # Benutzer anmelden
        return redirect(url_for('meinBereich', name=form.user.username, id=form.user.id))

    return render_template('login.html', form=form, hide_mein_bereich=True, hide_logout = True, hide_login_register=True)
                     
@app.route('/register', methods=['GET', 'POST'])       
def register():          
     print("Request-Methode:", request.method)  # Debugging

   
     if request.method == 'POST':  # Prüfen, ob POST-Request ankommt
        print("POST-Request erhalten!")

     form = RegisterForm()
     print("Fehler:", form.errors) 
     if form.validate_on_submit():    
        
            app.logger.debug('Validating...')
            #hashed_password = bcrypt.generate_password_hash(form.password.data)
            hashed_password = werkzeug.security.generate_password_hash(form.password.data, method='scrypt', salt_length=16)
            app.logger.debug(f'Hashed pw {hashed_password}') 
            new_user = User(username=form.username.data, password=hashed_password)
            app.logger.debug(f'New User {new_user}')
            db.session.add(new_user)
            app.logger.debug(f'Adding... {new_user}')
            db.session.commit()
            app.logger.debug(f'Comitted.')
            return redirect(url_for('meinBereich'))            
     else:
        print("❌ Formularvalidierung fehlgeschlagen!")
        print("Fehler:" ) # Zeigt, welche Fehler es gibt)
     return render_template('register.html', form = form,hide_mein_bereich = True,hide_login_register = True, hide_logout = True)

@app.route('/mein-bereich', methods=['GET', 'POST'])
@login_required  
def meinBereich():            
    user_name = current_user.username
    user_reports = Report.query.filter_by(parent_id=current_user.id).all()
    app.logger.debug(f'Past Checks:{user_reports}')

    return render_template('meinBereich.html', name=user_name, reports = user_reports,hide_login_register = True)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():    
    logout_user()
    return redirect(url_for('index'))
 
@app.route('/home')
def home():
    return redirect(url_for('index'))



@app.route('/schnelltest', methods=['GET', 'POST'])
def schnelltest(): 
    test_type = 'Schnell'
    session['test_type'] = test_type
    
    form = SchnellCheckForm() 
    if form.validate_on_submit():                       
        
        
        session['form_data'] = {field.name: field.data for field in form}  
        app.logger.debug(f'Form data Schnelltest: {session['form_data']} Test Type: {test_type}-----------------------------------')


        calculator = CalculateResult(test_type, session['form_data'])  
        app.logger.debug(f'Calculator inputs, testtype: {test_type}, form data: {session['form_data']}------------------------------------')

        ampelfarbe, punkte = calculator.calcResults() 
        session['ampelfarbe'] = ampelfarbe
        app.logger.debug(f'Ampelfarbe result: {ampelfarbe}, session ampelfarbe: {session['ampelfarbe']},  Punkte: {punkte} ------------------------------------------')

        filename = pdf_generator.generate_pdf(session['form_data'])  
                                    
        with open(filename, 'rb') as file:
            pdf_data = file.read() 
            if current_user.is_authenticated:
            
                report = Report(parent_id=current_user.id, file=pdf_data, test_type = test_type)
                db.session.add(report)
                db.session.commit() 

        # damit die antworten in der html angezeigt werden
        user_answers = {
            'Wie ist Ihr Gastronomiebetrieb strukturiert?': form.betrieb.data,
            'Erfüllt Ihr Kassensystem die Anforderungen einer zertifizierten technischen Sicherheitseinrichtung (TSE)?': form.tse.data,
            'Geben Sie für jede Transaktion einen Beleg aus?': form.beleg.data,
            'Wurde Ihr Kassensystem innerhalb der letzten 12 Monate geprüft oder zertifiziert?': form.pruefung.data,
            'Trennen Sie Speisen (7% MwSt.) und Getränke (19% MwSt.) korrekt in Ihrer Buchhaltung?': form.trennung.data,
            'Erfassen Sie alle Einnahmen aus Barzahlungen, Kartenzahlungen und Lieferdiensten vollständig?': form.einnahmen.data,
            'Reichen Sie Ihre Steuererklärungen immer fristgerecht ein?': form.steuererklärungen.data,
            'Haben Sie in den letzten 2 Jahren Umsatzsteuer-Nachforderungen erhalten?': form.nachforderungen.data,
            'Dokumentieren Sie Trinkgelder gemäß den steuerlichen Vorgaben?': form.trinkgelder.data,
            'Werden Ihre Mitarbeitenden regelmäßig zu steuerlichen Vorgaben geschult (z.B. Kassensicherungsverordnung, Trinkgeldregelung)?': form.schulung.data,
        }
    
        eingaben = [] 

        for frage, user_answer in user_answers.items():
            eingaben.append({
                'question': frage, 
                'user_answer': user_answer,       
            }) 
        
        session['form_eingaben'] = eingaben
  
        return redirect(url_for('result', filename = filename))

    if current_user.is_authenticated:
        user_report_count = db.session.query(func.count(Report.id)).filter_by(parent_id=current_user.id).scalar() + 1
        if user_report_count >= MAX_REPORTS_PER_USER:
            flash("Sie haben das Limit an gespeicherten Berichten erreicht. Löschen sie einen um einen neuen zu starten.", "danger")
            return redirect(url_for('meinBereich'))
        return render_template('schnelltest.html', form=form, hide_login_register = True)
    
    else:
        return render_template('schnelltest.html', form=form,hide_mein_bereich = True, hide_logout = True)

@app.route('/ausführlicherTest', methods=['GET', 'POST'])
@login_required 
def ausführlicherTest():   
    test_type = 'Ausführlich'
    session['test_type'] = test_type
    app.logger.debug(f'Session Data1: {session}')

    if 'step' not in session:     #Step wird bei Index definiert, deswegen geht er hier eigtl nicht rein
        session['step'] = 1
        session[f'form_data'] = {}
        app.logger.debug(f'Session Data3: {session['form_data']}')

    form_classes = [AusführlicherCheckForm1, AusführlicherCheckForm2, AusführlicherCheckForm3, 
                    AusführlicherCheckForm4, AusführlicherCheckForm5]
    form1 = AusführlicherCheckForm1()
    form2 = AusführlicherCheckForm2()
    form3 = AusführlicherCheckForm3()
    form4 = AusführlicherCheckForm4()  
    form5 = AusführlicherCheckForm5()   

    if 1 <= session['step'] <= 5:         
 
        form = form_classes[session['step'] - 1]()
        if form.validate_on_submit():
     
            session['form_data'].update({field.name: field.data for field in form}) 
                             
            # damit die antworten in der html angezeigt werden
            user_answers = {
                    'Wie ist Ihr Gastronomiebetrieb strukturiert?': form1.betrieb.data,
                    'Wie viele Standorte betreiben Sie?': form1.standort_zahl.data,
                    'Anzahl der Mitarbeitenden in Ihrem Betrieb?': form1.mitarbeiter_zahl.data,
                    'Wie hoch war Ihr Jahresumsatz im letzten Geschäftsjahr?': form1.jahresumsatz.data,
                    'Wie hoch war Ihr Anteil an Barumsätzen im letzten Geschäftsjahr?': form1.trennung.data,
                    'Nutzen Sie Kassensysteme mit digitaler Aufzeichnungspflicht?': form2.kassensystem.data,
                    'Wann wurde Ihr Kassensystem zuletzt geprüft?': form2.kassensytem_prüfung.data,
                    'Erfüllt Ihr Kassensystem die Anforderungen einer TSE?': form2.tse1.data,
                    'Geben Sie für jede Transaktion einen Beleg aus?': form2.beleg.data,
                    'Entsprechen die Belege allen gesetzlichen Anforderungen?': form2.belegs_anforderungen.data,
                    'Wie oft sichern Sie Ihre Kassendaten?': form2.kassendaten.data,
                    'Trennen Sie Speisen (7% MwSt.) und Getränke (19% MwSt.) korrekt?': form3.trennung_essen_trinken.data,
                    'Nutzen Sie ein digitales Buchhaltungssystem?': form3.buchhaltungssystem.data,
                    'Erfassen Sie Einnahmen aus verschiedenen Quellen getrennt?': form3.einnahme_erfassung.data,
                    'Wie hoch war Ihre durchschnittliche monatliche Umsatzsteuerzahlung?': form3.umsatzsteuer.data,
                    'Haben Sie in den letzten 2 Jahren Umsatzsteuer-Nachforderungen erhalten?': form3.nachforderungen.data,
                    'Reichen Sie Ihre Steuererklärungen immer fristgerecht ein?': form4.steuererklärungen.data,
                    'Werden alle Einnahmen vollständig dokumentiert?': form4.einkommensdokumentation.data,
                    'Nutzen Sie getrennte Umsatzsteuer-Sätze für Take-Away?': form4.getrennte_steuersätze.data,
                    'Wurde Ihr Betrieb in den letzten 5 Jahren steuerlich geprüft?': form4.steuerprüfung.data,
                    'Wie dokumentieren Sie Nachforderungen durch das Finanzamt?': form4.nachforderungsdokumentation.data,
                    'Führen Sie regelmäßige interne Steuer-Audits durch?': form4.audits.data,
                    'Werden Trinkgelder korrekt dokumentiert?': form5.trinkgelder_dokumentation.data,
                    'Sind Trinkgelder über das Kassensystem korrekt lohnversteuert?': form5.trinkgelder_steuer.data,
                    'Werden Mitarbeitende regelmäßig zu steuerlichen Vorgaben geschult?': form5.mitarbeiterschulungen.data,
                }

            eingaben = []

            for frage, user_answer in user_answers.items():
                eingaben.append({
                    'question': frage,
                    'user_answer': user_answer,
                })
        
            session['form_eingaben'] = eingaben      

            app.logger.debug(f'Form Data: {session['form_data']}')

            if session['step'] == 5:
                calculator = CalculateResult(test_type, session['form_data'])  
                app.logger.debug(f'Calculator inputs, testtype: {test_type}, form data: {session['form_data']}------------------------------------')

                ampelfarbe, punkte = calculator.calcResults() 
                session['ampelfarbe'] = ampelfarbe
                app.logger.debug(f'Ampelfarbe result: {ampelfarbe}, session ampelfarbe: {session['ampelfarbe']},  Punkte: {punkte} ------------------------------------------')

                filename = pdf_generator.generate_pdf(session['form_data'])

                with open(filename, 'rb') as file:
                            pdf_data = file.read()

                            if current_user.is_authenticated:
                                # Benutzer ist eingeloggt
                                report = Report(parent_id=current_user.id, file=pdf_data, test_type = test_type)
                                db.session.add(report)
                                db.session.commit()
                            else:
                                # Fehlerbehandlung, falls der Benutzer nicht eingeloggt ist
                                flash("Bitte melden Sie sich an.", "danger")
                                return redirect(url_for('login'))  # Beispiel für Weiterleitung zur Login-Seite
                            
                            # report = Report(user_id = session['user_id'], file = pdf_data)
                            # app.logger.debug(f'User Id: {session['user_id']} ----------------------------+++++++++++++++++++++++++++--------------')
                            # db.session.add(report)
                            # db.session.commit()

                return redirect(url_for('result', filename = filename))
            else:
                session['step'] += 1
                app.logger.debug(f'Session Step:------------------------------------------------------------------------ {session['step']}')
                return redirect(url_for('ausführlicherTest'))
    else:
        filename = pdf_generator.generate_pdf(session['form_data'])
        app.logger.debug(f'Filename-------------------------------------------------------------------------------------------------------:')

        return redirect(url_for('result', filename=filename))
        
    if current_user.is_authenticated:
        user_report_count = db.session.query(func.count(Report.id)).filter_by(parent_id=current_user.id).scalar() + 1
        app.logger.debug(f'Reportscount: {user_report_count}')
        if user_report_count >= MAX_REPORTS_PER_USER:
            app.logger.debug(f'Entereded If clause: {user_report_count}')
            flash("Sie haben das Limit an gespeicherten Berichten erreicht.", "danger")
            return redirect(url_for('meinBereich')) 
        return render_template('ausführlicherTest.html', form=form, hide_login_register = True)
    else: 
        return render_template('ausführlicherTest.html', form=form,hide_mein_bereich = True, hide_logout = True)
 
 
@app.route("/result")
def result():  
    filename = request.args.get('filename')
    form_eingaben = session.get('form_eingaben')
 
    if not form_eingaben: 
        return "Fehler: daten nicht gefunden."
    
    if current_user.is_authenticated:
        return render_template("result.html", filename=filename, form_eingaben = form_eingaben, ampelfarbe = session['ampelfarbe'], hide_login_register = True)
    else:
        return render_template("result.html", filename=filename, form_eingaben = form_eingaben, ampelfarbe = session['ampelfarbe'],hide_mein_bereich = True, hide_logout = True)

@app.route("/download/<filename>")     
def download_pdf(filename):
    return send_file(filename, as_attachment=True)

from flask import send_file, abort
import io

@app.route('/download_pdf/<int:report_id>')
@login_required
def download_pdf_meinBereich(report_id):        
    reportRow = db.session.execute(db.select(Report).filter_by(id=report_id))
    report = reportRow.scalar_one_or_none()

    if not report or report.parent_id != current_user.id:
        abort(403)     
             
    if report.file:                   
        pdf_stream = io.BytesIO(report.file)    
        pdf_stream.seek(0)   
  
        return send_file(pdf_stream, download_name=f"report_{report_id}.pdf", as_attachment=True, mimetype="application/pdf")
    else:       
        abort(404)       

@app.route('/deleteReport', methods=['POST'])
@login_required
def delReport():
         report_id = request.form.get('report_id')  
         if not report_id:
            flash("Ungültige Anfrage: Keine Report-ID angegeben", "danger")
            return redirect(url_for('meinBereich')) 

         reportRow = db.session.execute(db.select(Report).filter_by(id=report_id))
         report = reportRow.scalar_one_or_none()

         if not report or report.parent_id != current_user.id:
                flash("Fehler: Zugriff verweigert oder Bericht nicht gefunden.", "danger")
                return redirect(url_for('meinBereich'))

         db.session.delete(report)
         db.session.commit() 
         flash(f"Bericht {report_id} wurde erfolgreich gelöscht.", "success")

         return redirect(url_for('meinBereich'))
        
 

   
if __name__ == "__main__":
    app.run(debug=True)    

