import logging


logger = logging.getLogger(__name__)


class CalculateResult:
    
    def __init__(self, test_type, form_data):
        self.test_type = test_type
        self.form_data = form_data
        logger.debug(f'CALCULATE RESULTS CLASS Form Data: {form_data}')

        self.bewertungskriterien = [
            ## Schnelltest
            (form_data.get('tse'), ["ja"], 5),
            (form_data.get('beleg'), ["ja"], 5),
            (form_data.get('pruefung'), ["ja"], 5),
            (form_data.get('trennung'), ["ja"], 5),
            (form_data.get('einnahmen'), ["ja"], 5),
            (form_data.get('steuererklärungen'), ["ja"], 5),
            (form_data.get('nachforderungen'), ["nein"], 5),
            (form_data.get('trinkgelder'), ["ja"], 5),
            (form_data.get('schulung'), ["ja"], 5),
            ## Form 1
            (form_data.get('betrieb'), ["restaurant", "cafe", "bar", "imbiss", "catering", "hotel", "sonstiges"], 0),  
            (form_data.get('standortZahl'), ["1", "2", "3-5", "Mehr als 5"], 0), 
            (form_data.get('mitarbeiterZahl'), ["zahl"], 0),  
            (form_data.get('jahresumsatz'), ["zahl"], 0), 
            (form_data.get('barumsatzAnteil'), ["0-25 %", "26-50 %", "51-75 %", "Über 75%"], 0),
            ## Form 2
            (form_data.get('kassensystem'), ["Ja, für alle Standorte", "Teilweise"], 5), 
            (form_data.get('kassensytem_prüfung'), ["Innerhalb der letzten 12 Monate", "Vor mehr als 12 Monaten"], 5),   
            (form_data.get('beleg'), ["Ja immer", "Teilweise"], 5),
            (form_data.get('tse1'), ["Ja", "Unsicher"], 5),
            (form_data.get('belegs_anforderungen'), ["Ja", "Teilweise"], 5),  
            (form_data.get('kassendaten'), ["Täglich", "Wöchentlich"], 5),  
            ## Form 3
            (form_data.get('trennung_essen_trinken'), ["Ja", "Teilweise"], 5), 
            (form_data.get('buchhaltungssystem'), ["Ja, vollständig integriert"], 10), 
            (form_data.get('einnahme_erfassung'), ["Ja, vollständig", "Teilweise"], 5), 
            (form_data.get('umsatzsteuer'), ["zahl"], 0), 
            (form_data.get('nachforderungen'), ["Nein"], 10), 

            ## Form 4
            (form_data.get('steuererklärungen'), ["Ja, immer"], 10),  
            (form_data.get('einkommensdokumentation'), ["Ja", "Teilweise"], 5),  
            (form_data.get('getrennte_steuersätze'), ["Ja, getrennt", "Teilweise"], 5),  
            (form_data.get('steuerprüfung'), ["Ja, mehrmals", "ja, einmal"], 5),  
            (form_data.get('nachforderungsdokumentation'), ["Detailliert im Buchhaltungssystem", "Manuell in separaten Unterlagen"], 5),  
            (form_data.get('audits'), ["Ja, monatlich"], 10),  

            ## Form 5
            (form_data.get('trinkgelder_dokumentation'), ["Ja, vollständig", "Teilweise"], 5),  
            (form_data.get('trinkgelder_steuer'), ["Nein"], -5),  
            (form_data.get('mitarbeiterschulungen'), ["Ja"], 5), 
   
        ]

    def calcResults(self):
        pos_answers = sum(punkte for wert, gültige_werte, punkte in self.bewertungskriterien if wert in gültige_werte)        
        logger.debug(f'CALCULATE RESULTS CLASS Form Data: {self.form_data}')

        ampelfarbe = 'rot'
        if (self.test_type == 'Schnell'):
            if (pos_answers < 30) :       #Insgesamt 45 Punkte erreichbar
                ampelfarbe = "rot"                
            elif (pos_answers < 40):
                ampelfarbe = "gelb"
            else:
                ampelfarbe = "grün"
        elif(self.test_type == 'Ausführlich'):
                if (pos_answers < 75) :       #Insgesamt 110 Punkte erreichbar
                    ampelfarbe = "rot"
                elif (pos_answers <= 90):
                    ampelfarbe = "gelb"
                else:
                    ampelfarbe = "grün"
        return ampelfarbe, pos_answers

        
        
