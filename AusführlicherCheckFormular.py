from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, StringField, SubmitField
from wtforms.validators import DataRequired

class AusführlicherCheck1(FlaskForm): 

     #Frage 1
     betrieb = RadioField('Wie ist Ihr Gastronomiebetrieb strukturiert?',
                         choices=[('restaurant', 'Restaurant'),
                                  ('cafe', 'Café'),
                                  ('bar', 'Bar'),
                                  ('imbiss', 'Imbiss'),
                                  ('catering', 'Catering'),
                                  ('hotel', 'Hotel mit Gastronomie'),
                                  ('sonstiges', 'Sonstiges')],
                         validators=[DataRequired()])
                         
     #Frage 2
     standort_zahl = RadioField('Wie viele Standorte betreiben Sie?',
                     choices=[('1'), ('2'), ('3-5'), ('Mehr als 5')],
                     validators=[DataRequired()])
     
     #Frage 3
     mitarbeiter_zahl = IntegerField('Anzahl der Mitarbeitenden in Ihrem Betrieb (inkl. Teilzeit und Aushilfen)?',
                       validators=[DataRequired()])
     #Frage 4
     jahresumsatz = IntegerField('Wie hoch war Ihr Jahresumsatz im letzten Geschäftsjahr?',
                          validators=[DataRequired()])
     #Frage 5
     trennung = RadioField('Wie hoch war Ihr Anteil an Barumsätzen im letzten Geschäftsjahr?',
                          choices=[('0-25 %'), ('26-50 %'), ('51-75 %'), ('Über 75%')],
                          validators=[DataRequired()])
     
     submit = SubmitField('Weiter')


class AusführlicherCheck2(FlaskForm): 

     #Frage 1
     kassensystem = RadioField('Nutzen Sie für den Verkauf Kassensysteme mit digitaler Aufzeichnungspicht (nach Kassensicherungsverordnung)?',
                         choices=[('Ja, für alle Standorte'),
                                  ('Teilweise'),
                                  ('Nein')],
                         validators=[DataRequired()])
                         
     #Frage 2
     kassensytem_prüfung = RadioField('Wann wurde Ihr Kassensystem zuletzt geprüft oder zertiziert?',
                     choices=[('Innerhalb der letzen 12 Monate'), ('Vor mehr als 12 Monaten'), ('Nie')],
                     validators=[DataRequired()])
     
     #Frage 3
     tse1 = RadioField('Erfüllt Ihr Kassensystem die Anforderungen einer zertizierten technischen Sicherheitseinrichtung (TSE)?',
                     choices=[('Ja'), ('Nein'), ('Unsicher')],
                     validators=[DataRequired()])
     #Frage 4
     beleg = RadioField('Geben Sie für jede Transaktion einen Beleg aus?',
                               choices=[('Ja immer'), ('Teilweise'), ('Nein')],
                               validators=[DataRequired()])
     #Frage 5
     belegs_anforderungen = RadioField('Entsprechen die Belege Ihres Kassensystems allen gesetzlichen Anforderungen (Konkret)?',
                          choices=[('Ja'), ('Teilweise'), ('Nein')],
                          validators=[DataRequired()])
     
      #Frage 6
     kassendaten = RadioField('Wie oft sichern Sie Ihre Kassendaten?',
                          choices=[('Täglich'), ('Wöchentlich'), ('Monatlich'), ('Nicht regelmäßig')],
                          validators=[DataRequired()])

     submit = SubmitField('Weiter')


class AusführlicherCheck3(FlaskForm): 
    # Frage 1
    trennung_essen_trinken = RadioField('Trennen Sie Speisen (7% MwSt.) und Getränke (19% MwSt.) korrekt in Ihrer Buchhaltung?',
                                            choices=[('Ja'), 
                                                     ('Teilweise'), 
                                                     ('Nein')],
                                            validators=[DataRequired()])
    
    # Frage 2
    buchhaltungssystem = RadioField('Nutzen Sie ein digitales Buchhaltungssystem?',
                                             choices=[('Ja, vollständig integriert'), 
                                                      ('Teilweise digital'), 
                                                      ('Nein, rein manuell')],
                                             validators=[DataRequired()])
    
    # Frage 3
    einnahme_erfassung = RadioField('Erfassen Sie Einnahmen aus verschiedenen Quellen (z.B. Barzahlung, Kartenzahlung, Lieferdienste) getrennt?',
                                    choices=[('Ja, vollständig'), 
                                             ('Teilweise'), 
                                             ('Nein')],
                                    validators=[DataRequired()])
    
    # Frage 4
    umsatzsteuer = IntegerField('Wie hoch war Ihre durchschnittliche monatliche Umsatzsteuerzahlung in den letzten 12 Monaten? (€)',
                                                 validators=[DataRequired()])
    
    # Frage 5
    nachforderungen = RadioField('Haben Sie in den letzten 2 Jahren Umsatzsteuer-Nachforderungen erhalten?',
                                 choices=[('Ja'), 
                                          ('Nein')],
                                 validators=[DataRequired()])
    
    submit = SubmitField('Weiter')

class AusführlicherCheck4(FlaskForm): 
    # Frage 1
    steuererklärungen = RadioField('Reichen Sie Ihre Steuererklärungen immer fristgerecht ein?',
                                   choices=[('Ja, immer'), 
                                            ('Manchmal verspätet'), 
                                            ('Oft verspätet')],
                                   validators=[DataRequired()])
    
    # Frage 2
    einkommensdokumentation = RadioField('Werden die Einnahmen aus allen Quellen (z. B. Barumsatz, Kartenzahlungen, Lieferdienste) vollständig dokumentiert?',
                                         choices=[('Ja'), 
                                                  ('Teilweise'), 
                                                  ('Nein')],
                                         validators=[DataRequired()])
    
    # Frage 3
    getrennte_steuersätze = RadioField('Nutzen Sie getrennte Umsatzsteuer-Sätze für Lieferungen oder Take-Away-Geschäft?',
                                             choices=[('Ja'), 
                                                      ('Teilweise'), 
                                                      ('Nein')],
                                             validators=[DataRequired()])
    
    # Frage 4
    steuerprüfung = RadioField('Wurde Ihr Betrieb in den letzten 5 Jahren steuerlich geprüft?',
                                choices=[('Ja, mehrmals'), 
                                         ('Ja, einmal'), 
                                         ('Nein')],
                                validators=[DataRequired()])
    
    # Frage 5
    nachforderungsdokumentation = RadioField('Wie dokumentieren Sie Nachforderungen durch das Finanzsystem?',
                                             choices=[('Detailliert im Buchhaltungssystem'), 
                                                      ('Manuell in separaten Unterlagen'), 
                                                      ('Keine Dokumentation')],
                                             validators=[DataRequired()])
    
    # Frage 6
    audits = RadioField('Führen Sie regelmäßige interne Audits zu steuerlichen Anforderungen durch?',
                                choices=[('Ja, monatlich'), 
                                         ('Ja, jährlich'), 
                                         ('Nein')],
                                validators=[DataRequired()])
    
    submit = SubmitField('Weiter')


class AusführlicherCheck5(FlaskForm): 
    # Frage 1
    trinkgelder_dokumentation = RadioField('Werden Trinkgelder korrekt dokumentiert?',
                                           choices=[('Ja, vollständig'), 
                                                    ('Teilweise'), 
                                                    ('Nein')],
                                           validators=[DataRequired()])
    
    # Frage 2
    trinkgelder_steuer = RadioField('Sind Trinkgelder, die über das Kassensystem erfasst werden, korrekt lohnversteuert?',
                                    choices=[('Ja'), 
                                             ('Nein'), 
                                             ('Unsicher')],
                                    validators=[DataRequired()])
     
    # Frage 3
    mitarbeiterschulungen = RadioField('Werden Ihre Mitarbeitenden regelmäßig zu steuerlichen Vorgaben geschult?',
                                      choices=[('Ja'), 
                                               ('Nein')],
                                      validators=[DataRequired()])
    
    submit = SubmitField('Fertigstellen')
