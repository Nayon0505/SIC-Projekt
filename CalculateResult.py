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

        
        
