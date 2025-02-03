class CalculateResult:
    
    def __init__(self, test_type, form_data):
        self.test_type = test_type
        self.form_data = form_data
        
        self.bewertungskriterien = [
            ## Schnelltest
            (form_data.get('TSE'), ["ja", "unsicher"], 5),
            (form_data.get('Beleg'), ["ja"], 5),
            (form_data.get('Pruefung'), ["ja"], 5),
            (form_data.get('Trennung'), ["ja"], 5),
            (form_data.get('Einnahmen'), ["ja"], 5),
            (form_data.get('Steuererklärungen'), ["ja"], 5),
            (form_data.get('Nachforderungen'), ["nein"], 5),
            (form_data.get('Trinkgelder'), ["ja"], 5),
            (form_data.get('Schulung'), ["ja"], 5),
            ## Form 1
            (form_data.get('Betrieb'), ["restaurant", "cafe", "bar", "imbiss", "catering", "hotel", "sonstiges"], 0),  
            (form_data.get('StandortZahl'), ["1", "2", "3-5", "Mehr als 5"], 0), 
            (form_data.get('MitarbeiterZahl'), ["zahl"], 0),  
            (form_data.get('Jahresumsatz'), ["zahl"], 0), 
            (form_data.get('BarumsatzAnteil'), ["0-25 %", "26-50 %", "51-75 %", "Über 75%"], 0),
            ## Form 2
            (form_data.get('Kassensystem'), ["Ja, für alle Standorte", "Teilweise"], 5), 
            (form_data.get('KassensystemPruefung'), ["Innerhalb der letzten 12 Monate", "Vor mehr als 12 Monaten"], 5),   
            (form_data.get('Beleg'), ["Ja immer", "Teilweise"], 5),
            (form_data.get('BelegsAnforderungen'), ["Ja", "Teilweise"], 5),  
            (form_data.get('Kassendaten'), ["Täglich", "Wöchentlich"], 5),  
            ## Form 3
            (form_data.get('Trennung'), ["Ja", "Teilweise", ], 5),  
            (form_data.get('Buchhaltungssystem'), ["Ja, vollständig integriert"], 10), 
            (form_data.get('EinnahmenTrennung'), ["Ja", "Teilweise"], 5), 
            (form_data.get('Umsatzsteuerzahlung'), ["zahl"], 0),  
            (form_data.get('Nachforderungen'), ["Ja"], 10),  
            ## Form 4
            (form_data.get('SteuererklärungFristgerecht'), ["Ja, immer"], 10),  
            (form_data.get('EinnahmenDokumentation'), ["Ja", "Teilweise"], 5),  
            (form_data.get('UmsatzsteuerSatz'), ["Ja, getrennt", "Teilweise", "Nein"], 0),  
            (form_data.get('Steuerpruefung'), ["Ja, mehrmals", "Ja, einmal"], 5),  
            (form_data.get('NachforderungenDokumentation'), ["Detailliert", "Manuell"], 5),  
            (form_data.get('InterneAudits'), ["Ja, monatlich", "Ja, jährlich", "Nein"], 5),  
            ## Form 5
            (form_data.get('TrinkgelderDokumentation'), ["Ja, vollständig", "Teilweise"], 5), 
            (form_data.get('TrinkgelderLohnversteuerung'), ["Nein"], -5),  
            (form_data.get('SchulungMitarbeitende'), ["Ja"], 5), 
   
        ]

    def calcResults(self):
        pos_answers = sum(punkte for wert, gültige_werte, punkte in self.bewertungskriterien if wert in gültige_werte)
        ampelfarbe = 'rot'
        if (self.test_type == 'Schnell'):
            if (pos_answers < 30) :       #Insgesamt 50 Punkte erreichbar
                ampelfarbe = "rot"                
            elif (pos_answers < 40):
                ampelfarbe = "gelb"
            else:
                ampelfarbe = "grün"
        elif(self.test_type == 'Ausführlich'):
                if (pos_answers < 100) :       #Insgesamt 145 Punkte erreichbar
                    ampelfarbe = "rot"
                elif (pos_answers <= 130):
                    ampelfarbe = "gelb"
                else:
                    ampelfarbe = "grün"
        return ampelfarbe

        
        
