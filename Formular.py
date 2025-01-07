from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired

class SchnellCheckFormular(FlaskForm):
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
     tse = RadioField('Erfüllt Ihr Kassensystem die Anforderungen einer zertifizierten technischen Sicherheitseinrichtung (TSE)?',
                     choices=[('ja', 'Ja'), ('nein', 'Nein'), ('unsicher', 'Unsicher')],
                     validators=[DataRequired()])
     #Frage 3
     beleg = RadioField('Geben Sie für jede Transaktion einen Beleg aus?',
                       choices=[('ja', 'Ja'), ('teilweise', 'Teilweise')],
                       validators=[DataRequired()])
     #Frage 4
     pruefung = RadioField('Wurde Ihr Kassensystem innerhalb der letzten 12 Monate geprüft oder zertifiziert?',
                          choices=[('ja', 'Ja'), ('nein', 'Nein')],
                          validators=[DataRequired()])
     #Frage 5
     trennung = RadioField('Trennen Sie Speisen (7% MwSt.) und Getränke (19% MwSt.) korrekt in Ihrer Buchhaltung?',
                          choices=[('ja', 'Ja'), ('nein', 'Nein')],
                          validators=[DataRequired()])
     #Frage 6
     einnahmen = RadioField('Erfassen Sie alle Einnahmen aus Barzahlungen, Kartenzahlungen und Lieferdiensten vollständig?',
                           choices=[('ja', 'Ja'), ('nein', 'Nein')],
                           validators=[DataRequired()])
     #Frage 7
     steuererklärungen = RadioField('Reichen Sie Ihre Steuererklärungen immer fristgerecht ein?',
                                   choices=[('ja', 'Ja'), ('nein', 'Nein')],
                                   validators=[DataRequired()])
     #Frage 8
     nachforderungen = RadioField('Haben Sie in den letzten 2 Jahren Umsatzsteuer-Nachforderungen erhalten?',
                                 choices=[('ja', 'Ja'), ('nein', 'Nein')],
                                 validators=[DataRequired()])
     #Frage 9
     trinkgelder = RadioField('Dokumentieren Sie Trinkgelder gemäß den steuerlichen Vorgaben?',
                             choices=[('ja', 'Ja'), ('nein', 'Nein')],
                             validators=[DataRequired()])
     #Frage 10
     schulung = RadioField('Werden Ihre Mitarbeitenden regelmäßig zu steuerlichen Vorgaben geschult (z.B. Kassensicherungsverordnung, Trinkgeldregelung)?',
                          choices=[('ja', 'Ja'), ('nein', 'Nein')],
                          validators=[DataRequired()])
     
     #Einreichen
     submit = SubmitField('Fertig')
     
     
