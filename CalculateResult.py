import logging

logger = logging.getLogger(__name__)

class CalculateResult:
    
    def __init__(self, test_type, form_data):
        self.test_type = test_type
        self.form_data = form_data.copy()  # arbeiten mit Kopie, damit es nicht zu schwierighkeiten kommt
        logger.debug(f'CALCULATE RESULTS CLASS Form Data: {form_data}')

        # vorher numerische Felder zu kategorien machen (AusführlicherTest)
        if self.test_type == "Ausführlich":
            self._preprocess_ausfuehrlich_data()
        
        self._build_bewertungskriterien()

    def _preprocess_ausfuehrlich_data(self):
        """Convert numerical answers to categorical ranges for scoring"""
        # Mitarbeiterzahl Kategorizieren
        mitarbeiter = self.form_data.get('mitarbeiter_zahl')
        if isinstance(mitarbeiter, int):
            if mitarbeiter <= 5:
                self.form_data['mitarbeiter_zahl'] = '1-5'
            elif 6 <= mitarbeiter <= 15:
                self.form_data['mitarbeiter_zahl'] = '6-15'
            else:
                self.form_data['mitarbeiter_zahl'] = '16+'

        # Jahresumsatz Kategorizieren
        umsatz = self.form_data.get('jahresumsatz')
        if isinstance(umsatz, int):
            if umsatz <= 50000:
                self.form_data['jahresumsatz'] = '0-50k'
            elif 50001 <= umsatz <= 250000:
                self.form_data['jahresumsatz'] = '50k-250k'
            elif 250001 <= umsatz <= 600000:
                self.form_data['jahresumsatz'] = '250k-600k'
            else:
                self.form_data['jahresumsatz'] = '600k+'

        # Umsatzsteuer Kategorizieren
        ust = self.form_data.get('umsatzsteuer')
        if isinstance(ust, int):
            if ust <= 100:
                self.form_data['umsatzsteuer'] = '0-100'
            elif 101 <= ust <= 500:
                self.form_data['umsatzsteuer'] = '101-500'
            elif 501 <= ust <= 2000:
                self.form_data['umsatzsteuer'] = '501-2000'
            elif 2001 <= ust <= 5000:
                self.form_data['umsatzsteuer'] = '2001-5000'
            else:
                self.form_data['umsatzsteuer'] = '5000+'

    def _build_bewertungskriterien(self):
        """Define scoring rules for different test types"""
        if self.test_type == "Schnell":
            #für den SchnellCheck
            #62
            self.bewertungskriterien = [
                (self.form_data.get('tse'), ["ja"], 10),
                (self.form_data.get('beleg'), ["ja"], 9),
                (self.form_data.get('pruefung'), ["ja"], 7),
                (self.form_data.get('trennung'), ["ja"], 8),
                (self.form_data.get('einnahmen'), ["ja"], 10),
                (self.form_data.get('steuererklärungen'), ["ja"], 6),
                (self.form_data.get('nachforderungen'), ["nein"], 5),
                (self.form_data.get('trinkgelder'), ["ja"], 3),
                (self.form_data.get('schulung'), ["ja"], 4),
            ]
        else:
            #für den AusführlichenCheck
            #132
            self.bewertungskriterien = [
                # Step 1: Allgemeine Informationen
                (self.form_data.get('betrieb'), ['restaurant'], 0),
                (self.form_data.get('betrieb'), ['cafe', 'hotel'], 0),
                (self.form_data.get('betrieb'), ['bar', 'catering'], 0),
                (self.form_data.get('betrieb'), ['imbiss'], 0),
                (self.form_data.get('betrieb'), ['sonstiges'], 0),
                
                (self.form_data.get('standort_zahl'), ['1'], 0),
                (self.form_data.get('standort_zahl'), ['2'], 0),
                (self.form_data.get('standort_zahl'), ['3-5'], 0),
                (self.form_data.get('standort_zahl'), ['Mehr als 5'], 0),
                
                (self.form_data.get('mitarbeiter_zahl'), ['1-5'], 0),
                (self.form_data.get('mitarbeiter_zahl'), ['6-10'], 0),
                (self.form_data.get('mitarbeiter_zahl'), ['11-20'], 0),
                (self.form_data.get('mitarbeiter_zahl'), ['21+'], 0),
                
                (self.form_data.get('jahresumsatz'), ['0-100k'], 0),
                (self.form_data.get('jahresumsatz'), ['100k-500k'], 0),
                (self.form_data.get('jahresumsatz'), ['500k+'], 3),
                
                (self.form_data.get('trennung'), ['0-25 %'], 0),
                (self.form_data.get('trennung'), ['26-50 %'], 0),
                (self.form_data.get('trennung'), ['51-75 %'], 0),
                (self.form_data.get('trennung'), ['Über 75%'], 0),

                # Step 2: Kassensystem
                (self.form_data.get('kassensystem'), ['Ja, für alle Standorte'], 10),
                (self.form_data.get('kassensystem'), ['Teilweise'], 5),
                (self.form_data.get('kassensystem'), ['Nein'], 0),
                
                (self.form_data.get('kassensytem_prüfung'), ['Innerhalb der letzen 12 Monate'], 8),
                (self.form_data.get('kassensytem_prüfung'), ['Vor mehr als 12 Monaten'], 5),
                (self.form_data.get('kassensytem_prüfung'), ['Nie'], 0),
                
                (self.form_data.get('tse1'), ['Ja'], 10),
                (self.form_data.get('tse1'), ['Unsicher'], 5),
                (self.form_data.get('tse1'), ['Nein'], 0),
                
                (self.form_data.get('beleg'), ['Ja immer'], 9),
                (self.form_data.get('beleg'), ['Teilweise'], 4),
                (self.form_data.get('beleg'), ['Nein'], 0),
                
                (self.form_data.get('belegs_anforderungen'), ['Ja'], 8),
                (self.form_data.get('belegs_anforderungen'), ['Teilweise'], 4),
                (self.form_data.get('belegs_anforderungen'), ['Nein'], 0),
                
                (self.form_data.get('kassendaten'), ['Täglich'], 7),
                (self.form_data.get('kassendaten'), ['Wöchentlich'], 6),
                (self.form_data.get('kassendaten'), ['Monatlich'], 5),
                (self.form_data.get('kassendaten'), ['Nicht regelmäßig'], 2),

                # Step 3: Buchhaltung
                (self.form_data.get('trennung_essen_trinken'), ['Ja'], 10),
                (self.form_data.get('trennung_essen_trinken'), ['Teilweise'], 4),
                (self.form_data.get('trennung_essen_trinken'), ['Nein'], 0),
                
                (self.form_data.get('buchhaltungssystem'), ['Ja, vollständig integriert'], 9),
                (self.form_data.get('buchhaltungssystem'), ['Teilweise digital'], 7),
                (self.form_data.get('buchhaltungssystem'), ['Nein, rein manuell'], 5),
                
                (self.form_data.get('einnahme_erfassung'), ['Ja, vollständig'], 8),
                (self.form_data.get('einnahme_erfassung'), ['Teilweise'], 6),
                (self.form_data.get('einnahme_erfassung'), ['Nein'], 5),
                
                (self.form_data.get('umsatzsteuer'), ['0-1000'], 0),
                (self.form_data.get('umsatzsteuer'), ['1001-5000'], 0),
                (self.form_data.get('umsatzsteuer'), ['5000+'], 0),
                
                (self.form_data.get('nachforderungen'), ['Nein'], 5),
                (self.form_data.get('nachforderungen'), ['Ja'], 0),

                # Step 4: Steuerdokumentation
                (self.form_data.get('steuererklärungen'), ['Ja, immer'], 7),
                (self.form_data.get('steuererklärungen'), ['Manchmal verspätet'], 3),
                (self.form_data.get('steuererklärungen'), ['Oft verspätet'], 1),
                
                (self.form_data.get('einkommensdokumentation'), ['Ja'], 10),
                (self.form_data.get('einkommensdokumentation'), ['Teilweise'], 5),
                (self.form_data.get('einkommensdokumentation'), ['Nein'], 0),
                
                (self.form_data.get('getrennte_steuersätze'), ['Ja'], 8),
                (self.form_data.get('getrennte_steuersätze'), ['Teilweise'], 4),
                (self.form_data.get('getrennte_steuersätze'), ['Nein'], 0),
                
                (self.form_data.get('steuerprüfung'), ['Nein'], 2),
                (self.form_data.get('steuerprüfung'), ['Ja, einmal'], 1),
                (self.form_data.get('steuerprüfung'), ['Ja, mehrmals'], 0),
                
                (self.form_data.get('nachforderungsdokumentation'), ['Detailliert im Buchhaltungssystem'], 4),
                (self.form_data.get('nachforderungsdokumentation'), ['Manuell in separaten Unterlagen'], 3),
                (self.form_data.get('nachforderungsdokumentation'), ['Keine Dokumentation'], 0),
                
                (self.form_data.get('audits'), ['Ja, monatlich'], 2),
                (self.form_data.get('audits'), ['Ja, jährlich'], 1),
                (self.form_data.get('audits'), ['Nein'], 0),

                # Step 5: Trinkgelder & Schulungen
                (self.form_data.get('trinkgelder_dokumentation'), ['Ja, vollständig'], 4),
                (self.form_data.get('trinkgelder_dokumentation'), ['Teilweise'], 2),
                (self.form_data.get('trinkgelder_dokumentation'), ['Nein'], 0),
                
                (self.form_data.get('trinkgelder_steuer'), ['Ja'], 7),
                (self.form_data.get('trinkgelder_steuer'), ['Unsicher'], 3),
                (self.form_data.get('trinkgelder_steuer'), ['Nein'], 0),
                
                (self.form_data.get('mitarbeiterschulungen'), ['Ja'], 4),
                (self.form_data.get('mitarbeiterschulungen'), ['Nein'], 0)
            ]

    def calcResults(self):
        pos_answers = sum(
            punkte 
            for wert, gültige_werte, punkte in self.bewertungskriterien 
            if wert in gültige_werte
        )
        
        logger.debug(f'Total points calculated: {pos_answers}')

        if self.test_type == "Schnell":
            if pos_answers < 42:   
                ampelfarbe = "rot"
            elif pos_answers < 52:
                ampelfarbe = "gelb"
            else:
                ampelfarbe = "grün"
        else:  # AusführlicherTest
            if pos_answers < 107:    
                ampelfarbe = "rot"
            elif pos_answers <= 119:
                ampelfarbe = "gelb"
            else:
                ampelfarbe = "grün"

        return ampelfarbe, pos_answers
        