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
            elif 6 <= mitarbeiter <= 10:
                self.form_data['mitarbeiter_zahl'] = '6-10'
            elif 11 <= mitarbeiter <= 20:
                self.form_data['mitarbeiter_zahl'] = '11-20'
            else:
                self.form_data['mitarbeiter_zahl'] = '21+'

        # Jahresumsatz Kategorizieren
        umsatz = self.form_data.get('jahresumsatz')
        if isinstance(umsatz, int):
            if umsatz <= 100000:
                self.form_data['jahresumsatz'] = '0-100k'
            elif 100001 <= umsatz <= 500000:
                self.form_data['jahresumsatz'] = '100k-500k'
            else:
                self.form_data['jahresumsatz'] = '500k+'

        # Umsatzsteuer Kategorizieren
        ust = self.form_data.get('umsatzsteuer')
        if isinstance(ust, int):
            if ust <= 1000:
                self.form_data['umsatzsteuer'] = '0-1000'
            elif 1001 <= ust <= 5000:
                self.form_data['umsatzsteuer'] = '1001-5000'
            else:
                self.form_data['umsatzsteuer'] = '5000+'

    def _build_bewertungskriterien(self):
        """Define scoring rules for different test types"""
        if self.test_type == "Schnell":
            self.bewertungskriterien = [
                (self.form_data.get('tse'), ["ja"], 5),
                (self.form_data.get('beleg'), ["ja"], 5),
                (self.form_data.get('pruefung'), ["ja"], 5),
                (self.form_data.get('trennung'), ["ja"], 5),
                (self.form_data.get('einnahmen'), ["ja"], 5),
                (self.form_data.get('steuererklärungen'), ["ja"], 5),
                (self.form_data.get('nachforderungen'), ["nein"], 5),
                (self.form_data.get('trinkgelder'), ["ja"], 5),
                (self.form_data.get('schulung'), ["ja"], 5),
            ]
        else:
            self.bewertungskriterien = [
                # Step 1: Allgemeine Informationen
                (self.form_data.get('betrieb'), ['restaurant'], 5),
                (self.form_data.get('betrieb'), ['cafe', 'hotel'], 4),
                (self.form_data.get('betrieb'), ['bar', 'catering'], 3),
                (self.form_data.get('betrieb'), ['imbiss'], 2),
                (self.form_data.get('betrieb'), ['sonstiges'], 1),
                
                (self.form_data.get('standort_zahl'), ['1'], 5),
                (self.form_data.get('standort_zahl'), ['2'], 4),
                (self.form_data.get('standort_zahl'), ['3-5'], 3),
                (self.form_data.get('standort_zahl'), ['Mehr als 5'], 2),
                
                (self.form_data.get('mitarbeiter_zahl'), ['1-5'], 5),
                (self.form_data.get('mitarbeiter_zahl'), ['6-10'], 4),
                (self.form_data.get('mitarbeiter_zahl'), ['11-20'], 3),
                (self.form_data.get('mitarbeiter_zahl'), ['21+'], 2),
                
                (self.form_data.get('jahresumsatz'), ['0-100k'], 5),
                (self.form_data.get('jahresumsatz'), ['100k-500k'], 4),
                (self.form_data.get('jahresumsatz'), ['500k+'], 3),
                
                (self.form_data.get('trennung'), ['0-25 %'], 5),
                (self.form_data.get('trennung'), ['26-50 %'], 4),
                (self.form_data.get('trennung'), ['51-75 %'], 3),
                (self.form_data.get('trennung'), ['Über 75%'], 2),

                # Step 2: Kassensystem
                (self.form_data.get('kassensystem'), ['Ja, für alle Standorte'], 5),
                (self.form_data.get('kassensystem'), ['Teilweise'], 3),
                (self.form_data.get('kassensystem'), ['Nein'], 1),
                
                (self.form_data.get('kassensytem_prüfung'), ['Innerhalb der letzen 12 Monate'], 5),
                (self.form_data.get('kassensytem_prüfung'), ['Vor mehr als 12 Monaten'], 3),
                (self.form_data.get('kassensytem_prüfung'), ['Nie'], 1),
                
                (self.form_data.get('tse1'), ['Ja'], 5),
                (self.form_data.get('tse1'), ['Unsicher'], 2),
                (self.form_data.get('tse1'), ['Nein'], 1),
                
                (self.form_data.get('beleg'), ['Ja immer'], 5),
                (self.form_data.get('beleg'), ['Teilweise'], 3),
                (self.form_data.get('beleg'), ['Nein'], 1),
                
                (self.form_data.get('belegs_anforderungen'), ['Ja'], 5),
                (self.form_data.get('belegs_anforderungen'), ['Teilweise'], 3),
                (self.form_data.get('belegs_anforderungen'), ['Nein'], 1),
                
                (self.form_data.get('kassendaten'), ['Täglich'], 5),
                (self.form_data.get('kassendaten'), ['Wöchentlich'], 4),
                (self.form_data.get('kassendaten'), ['Monatlich'], 3),
                (self.form_data.get('kassendaten'), ['Nicht regelmäßig'], 1),

                # Step 3: Buchhaltung
                (self.form_data.get('trennung_essen_trinken'), ['Ja'], 5),
                (self.form_data.get('trennung_essen_trinken'), ['Teilweise'], 3),
                (self.form_data.get('trennung_essen_trinken'), ['Nein'], 1),
                
                (self.form_data.get('buchhaltungssystem'), ['Ja, vollständig integriert'], 5),
                (self.form_data.get('buchhaltungssystem'), ['Teilweise digital'], 3),
                (self.form_data.get('buchhaltungssystem'), ['Nein, rein manuell'], 1),
                
                (self.form_data.get('einnahme_erfassung'), ['Ja, vollständig'], 5),
                (self.form_data.get('einnahme_erfassung'), ['Teilweise'], 3),
                (self.form_data.get('einnahme_erfassung'), ['Nein'], 1),
                
                (self.form_data.get('umsatzsteuer'), ['0-1000'], 5),
                (self.form_data.get('umsatzsteuer'), ['1001-5000'], 4),
                (self.form_data.get('umsatzsteuer'), ['5000+'], 3),
                
                (self.form_data.get('nachforderungen'), ['Nein'], 5),
                (self.form_data.get('nachforderungen'), ['Ja'], 1),

                # Step 4: Steuerdokumentation
                (self.form_data.get('steuererklärungen'), ['Ja, immer'], 5),
                (self.form_data.get('steuererklärungen'), ['Manchmal verspätet'], 3),
                (self.form_data.get('steuererklärungen'), ['Oft verspätet'], 1),
                
                (self.form_data.get('einkommensdokumentation'), ['Ja'], 5),
                (self.form_data.get('einkommensdokumentation'), ['Teilweise'], 3),
                (self.form_data.get('einkommensdokumentation'), ['Nein'], 1),
                
                (self.form_data.get('getrennte_steuersätze'), ['Ja'], 5),
                (self.form_data.get('getrennte_steuersätze'), ['Teilweise'], 3),
                (self.form_data.get('getrennte_steuersätze'), ['Nein'], 1),
                
                (self.form_data.get('steuerprüfung'), ['Nein'], 5),
                (self.form_data.get('steuerprüfung'), ['Ja, einmal'], 3),
                (self.form_data.get('steuerprüfung'), ['Ja, mehrmals'], 1),
                
                (self.form_data.get('nachforderungsdokumentation'), ['Detailliert im Buchhaltungssystem'], 5),
                (self.form_data.get('nachforderungsdokumentation'), ['Manuell in separaten Unterlagen'], 3),
                (self.form_data.get('nachforderungsdokumentation'), ['Keine Dokumentation'], 1),
                
                (self.form_data.get('audits'), ['Ja, monatlich'], 5),
                (self.form_data.get('audits'), ['Ja, jährlich'], 4),
                (self.form_data.get('audits'), ['Nein'], 1),

                # Step 5: Trinkgelder & Schulungen
                (self.form_data.get('trinkgelder_dokumentation'), ['Ja, vollständig'], 5),
                (self.form_data.get('trinkgelder_dokumentation'), ['Teilweise'], 3),
                (self.form_data.get('trinkgelder_dokumentation'), ['Nein'], 1),
                
                (self.form_data.get('trinkgelder_steuer'), ['Ja'], 5),
                (self.form_data.get('trinkgelder_steuer'), ['Unsicher'], 2),
                (self.form_data.get('trinkgelder_steuer'), ['Nein'], 1),
                
                (self.form_data.get('mitarbeiterschulungen'), ['Ja'], 5),
                (self.form_data.get('mitarbeiterschulungen'), ['Nein'], 1)
            ]

    def calcResults(self):
        pos_answers = sum(
            punkte 
            for wert, gültige_werte, punkte in self.bewertungskriterien 
            if wert in gültige_werte
        )
        
        logger.debug(f'Total points calculated: {pos_answers}')

        if self.test_type == "Schnell":
            if pos_answers < 30:   
                ampelfarbe = "rot"
            elif pos_answers < 40:
                ampelfarbe = "gelb"
            else:
                ampelfarbe = "grün"
        else:  # AusführlicherTest
            if pos_answers < 75:    
                ampelfarbe = "rot"
            elif pos_answers <= 90:
                ampelfarbe = "gelb"
            else:
                ampelfarbe = "grün"

        return ampelfarbe, pos_answers
        
