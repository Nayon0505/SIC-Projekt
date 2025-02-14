
from flask import Flask, flash, redirect, render_template, url_for, request, send_file, session
from flask_bootstrap import Bootstrap5
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func
import werkzeug

from CalculateResult import CalculateResult
from SchnellCheckForm import SchnellCheckForm
from AusführlicherCheckForm import *

from PdfGenerator import PdfGenerator

import logging


app = Flask(__name__) 
pdf_generator = PdfGenerator()
app.logger.setLevel(logging.DEBUG)  

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)
 
from db import *


bootstrap = Bootstrap5(app)

MAX_REPORTS_PER_USER = 4


@app.route('/', methods=['GET', 'POST'])  
def index():
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
        login_user(form.user) 
        return redirect(url_for('meinBereich', name=form.user.username, id=form.user.id))

    return render_template('login.html', form=form, hide_mein_bereich=True, hide_logout = True, hide_login_register=True)
                     
@app.route('/register', methods=['GET', 'POST'])       
def register():          
     print("Request-Methode:", request.method)  

   
     if request.method == 'POST': 
        print("POST-Request erhalten!")

     form = RegisterForm()
     print("Fehler:", form.errors) 
     if form.validate_on_submit():    
        
            app.logger.debug('Validating...')
            hashed_password = werkzeug.security.generate_password_hash(form.password.data, method='scrypt', salt_length=16)
            app.logger.debug(f'Hashed pw {hashed_password}') 
            new_user = User(username=form.username.data, password=hashed_password)
            app.logger.debug(f'New User {new_user}')
            db.session.add(new_user)
            app.logger.debug(f'Adding... {new_user}')
            db.session.commit()
            app.logger.debug(f'Comitted.')
            login_user(new_user)
            return redirect(url_for('meinBereich'))            
     else:
        print("Formularvalidierung fehlgeschlagen!")
        print("Fehler:" ) 
     return render_template('register.html', form = form,hide_mein_bereich = True,hide_login_register = True, hide_logout = True)

@app.route('/mein-bereich', methods=['GET', 'POST'])
@login_required  
def meinBereich():            
    user_name = current_user.username
    user_reports = db.session.execute(
    db.select(Report).filter_by(parent_id=current_user.id)).scalars().all()

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
        user_report_count = db.session.execute(
            db.select(func.count(Report.id)).filter_by(parent_id=current_user.id)).scalar() + 1    
        if user_report_count >= MAX_REPORTS_PER_USER:
            flash("Sie haben das Limit an gespeicherten Berichten erreicht. Löschen sie einen um einen neuen zu starten.", "danger")
            return redirect(url_for('meinBereich'))
        return render_template('schnelltest.html', form=form, hide_login_register = True)
    else:
        return render_template('schnelltest.html', form=form,hide_mein_bereich = True, hide_logout = True)
    
@app.route('/ausführlicherTest', methods=['GET', 'POST'])
def ausführlicherTest():
    session.setdefault('form_data_ausführlich', {})
    session.setdefault('step', 1)
    
    current_step = session['step']
    form_data = session['form_data_ausführlich']

    form_classes = {
        1: AusführlicherCheckForm1,
        2: AusführlicherCheckForm2,
        3: AusführlicherCheckForm3,
        4: AusführlicherCheckForm4,
        5: AusführlicherCheckForm5
    }

    if current_step not in form_classes:
        session['step'] = 1
        return redirect(url_for('ausführlicherTest'))

    form = form_classes[current_step](formdata=request.form if request.method == 'POST' else None)

    if request.method == 'POST':
        direction = request.form.get('direction')

        if direction == 'next':
            if form.validate():
                form_data.update(form.data)
                form_data.pop('csrf_token', None)
                form_data.pop('submit', None)
                session['form_data_ausführlich'] = form_data
                session['step'] = min(current_step + 1, 5)
                return redirect(url_for('ausführlicherTest'))
        elif direction == 'back':
            session['step'] = max(current_step - 1, 1)
            return redirect(url_for('ausführlicherTest'))
        elif direction == 'submit':
            if form.validate():
                form_data.update(form.data)
                form_data.pop('csrf_token', None)
                form_data.pop('submit', None)
                
                calculator = CalculateResult('Ausführlich', form_data)
                ampelfarbe, _ = calculator.calcResults()
                session['ampelfarbe'] = ampelfarbe
                
                filename = pdf_generator.generate_pdf(form_data)
                
                # wenn eingeloggt, wird das halt auf die db gesaved
                if current_user.is_authenticated:
                    with open(filename, 'rb') as f:
                        report = Report(parent_id=current_user.id, 
                                      file=f.read(),
                                      test_type='Ausführlich')
                        db.session.add(report)
                        db.session.commit()
                
                user_answers = {
                    'betrieb': 'Wie ist Ihr Gastronomiebetrieb strukturiert?',
                    'standort_zahl': 'Wie viele Standorte betreiben Sie?',
                    'mitarbeiter_zahl': 'Anzahl der Mitarbeitenden in Ihrem Betrieb (inkl. Teilzeit und Aushilfen)?',
                    'jahresumsatz': 'Wie hoch war Ihr Jahresumsatz im letzten Geschäftsjahr?',
                    'trennung': 'Wie hoch war Ihr Anteil an Barumsätzen im letzten Geschäftsjahr?',
                    'kassensystem': 'Nutzen Sie für den Verkauf Kassensysteme mit digitaler Aufzeichnungspicht (nach Kassensicherungsverordnung)?',
                    'kassensytem_prüfung': 'Wann wurde Ihr Kassensystem zuletzt geprüft oder zertiziert?',
                    'tse1': 'Erfüllt Ihr Kassensystem die Anforderungen einer zertizierten technischen Sicherheitseinrichtung (TSE)?',
                    'beleg': 'Geben Sie für jede Transaktion einen Beleg aus?',
                    'belegs_anforderungen': 'Entsprechen die Belege Ihres Kassensystems allen gesetzlichen Anforderungen (Konkret)?',
                    'kassendaten': 'Wie oft sichern Sie Ihre Kassendaten?',
                    'trennung_essen_trinken': 'Trennen Sie Speisen (7% MwSt.) und Getränke (19% MwSt.) korrekt in Ihrer Buchhaltung?',
                    'buchhaltungssystem': 'Nutzen Sie ein digitales Buchhaltungssystem?',
                    'einnahme_erfassung': 'Erfassen Sie Einnahmen aus verschiedenen Quellen (z.B. Barzahlung, Kartenzahlung, Lieferdienste) getrennt?',
                    'umsatzsteuer': 'Wie hoch war Ihre durchschnittliche monatliche Umsatzsteuerzahlung in den letzten 12 Monaten? (€)',
                    'nachforderungen': 'Haben Sie in den letzten 2 Jahren Umsatzsteuer-Nachforderungen erhalten?',
                    'steuererklärungen': 'Reichen Sie Ihre Steuererklärungen immer fristgerecht ein?',
                    'einkommensdokumentation': 'Werden die Einnahmen aus allen Quellen (z. B. Barumsatz, Kartenzahlungen, Lieferdienste) vollständig dokumentiert?',
                    'getrennte_steuersätze': 'Nutzen Sie getrennte Umsatzsteuer-Sätze für Lieferungen oder Take-Away-Geschäft?',
                    'steuerprüfung': 'Wurde Ihr Betrieb in den letzten 5 Jahren steuerlich geprüft?',
                    'nachforderungsdokumentation': 'Wie dokumentieren Sie Nachforderungen durch das Finanzsystem?',
                    'audits': 'Führen Sie regelmäßige interne Audits zu steuerlichen Anforderungen durch?',
                    'trinkgelder_dokumentation': 'Werden Trinkgelder korrekt dokumentiert?',
                    'trinkgelder_steuer': 'Sind Trinkgelder, die über das Kassensystem erfasst werden, korrekt lohnversteuert?',
                    'mitarbeiterschulungen': 'Werden Ihre Mitarbeitenden regelmäßig zu steuerlichen Vorgaben geschult?',
                }
                # damit die fragen in der richtigen Reihenfolge erscheinen statt einfach random
                question_order = [
                    'betrieb', 'standort_zahl', 'mitarbeiter_zahl', 'jahresumsatz', 'trennung',
                    'kassensystem', 'kassensytem_prüfung', 'tse1', 'beleg', 'belegs_anforderungen', 'kassendaten',
                    'trennung_essen_trinken', 'buchhaltungssystem', 'einnahme_erfassung', 'umsatzsteuer', 'nachforderungen',
                    'steuererklärungen', 'einkommensdokumentation', 'getrennte_steuersätze', 'steuerprüfung', 'nachforderungsdokumentation', 'audits',
                    'trinkgelder_dokumentation', 'trinkgelder_steuer', 'mitarbeiterschulungen'
                ] 
 
                eingaben = [] 
                for field in question_order:
                    if field in form_data:
                        eingaben.append({
                            'question': user_answers.get(field, field),
                            'user_answer': form_data[field]
                        })
                
                session['form_eingaben'] = eingaben
                session.pop('form_data_ausführlich', None) 
                session.pop('step', None)
                
                return redirect(url_for('result', filename=filename))

    for field in form:
        if field.name in form_data:
            field.data = form_data[field.name]
            
    if current_user.is_authenticated:
        user_report_count = db.session.execute(
            db.select(func.count(Report.id)).filter_by(parent_id=current_user.id)
        ).scalar() + 1        
        app.logger.debug(f'Reportscount: {user_report_count}')
        if user_report_count >= MAX_REPORTS_PER_USER:
            app.logger.debug(f'Entereded If clause: {user_report_count}')
            flash("Sie haben das Limit an gespeicherten Berichten erreicht.", "danger")
            return redirect(url_for('meinBereich')) 
        return render_template('ausführlicherTest.html', form=form, current_step=current_step, total_steps=5, hide_login_register = True)
    else: 
        return render_template('ausführlicherTest.html', form=form, current_step=current_step, total_steps=5, hide_mein_bereich = True, hide_logout = True)

 
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

