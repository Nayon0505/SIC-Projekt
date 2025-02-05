
from flask import session
from reportlab.lib.pagesizes import letter 
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter

class PdfGenerator():
    def __init__(self):
        pass
        

    def generate_pdf(self, form):
        filename = "Nachhaltigkeitsbericht.pdf"
        document = SimpleDocTemplate(filename, pagesize=letter)

        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]

        h1_style = ParagraphStyle(
        "h1ueberschrift", 
        parent=normal_style,
        fontName="Helvetica-Bold", 
        fontSize=24,
        spaceAfter=26,
        alignment=1 
    )

        abstand_style = ParagraphStyle(
        "abstand", 
        parent=styles["Normal"],  
        spaceBefore=10, 
        spaceAfter=10,   
    )
        
        blocksatz_style = ParagraphStyle(
        "blocksatz", 
        parent=normal_style,  
        alignment=4,              # Blocksatz (Justify)
        fontName="Times-Roman",   # Elegantere Schriftart für Fließtext
        fontSize=11,              # Leicht kleinere Schrift für besseres Layout
        leading=16,               # Angenehmer Zeilenabstand (1.5x)
        spaceAfter=8,             # Mehr Abstand nach Absätzen
        firstLineIndent=0,       # Deutliche Einrückung der ersten Zeile
        leftIndent=5,             # Leichter linker Rand für bessere Struktur
        rightIndent=5,            # Leichter rechter Rand für Symmetrie
        textColor=colors.black,   # Schwarzer Text für hohe Kontraste
        backColor=None,           # Kein Hintergrund für saubere Optik
        borderPadding=0,          # Kein zusätzlicher Innenabstand
        wordWrap='LTR',           # Wörter umbrechen (von links nach rechts)
        allowOrphans=0,           # Verhindert, dass einzelne Zeilen am Ende einer Seite hängenbleiben
        allowWidows=0,            # Verhindert einzelne Zeilen am Anfang einer neuen Seite
    )
        
        h2_style = ParagraphStyle(
        "h2ueberschrift", 
        parent=normal_style,
        fontName="Helvetica-Bold", 
        fontSize=14, 
        alignment=1 
    )

    
        form_data = {
            'Betrieb': form.get('betrieb'),
            'TSE': form.get('tse'),
            'Beleg': form.get('beleg'),
            'Pruefung': form.get('prüfung'),
            'Trennung': form.get('trennung'),
            'Einnahmen': form.get('einnahmen'),
            'Steuererklärungen': form.get('steuererklärungen'),
            'Nachforderungen': form.get('nachforderungen'),
            'Trinkgelder': form.get('trinkgelder'),
            'Schulung': form.get('schulung'),
        }
        
        session['form_data'] = form_data

        story = []

        story.append(Paragraph("<b>SchnellCheck Report</b>", h1_style))

        story.append(Paragraph("", abstand_style))

        ampelfarbe = session['ampelfarbe']
        

        ampelfarbe_dict = {
            "rot": colors.red,
            "gelb": colors.yellow,
            "grün": colors.green
        }

        ampelfarbe_paragraph = f"<font color={ampelfarbe_dict[ampelfarbe]}><b>Ampelfarbe: {ampelfarbe.capitalize()}</b></font>"
        story.append(Paragraph(ampelfarbe_paragraph, normal_style))

        story.append(Paragraph("", abstand_style))

        story.append(Paragraph(f"1. Gastronomiebetrieb: {form.get('betrieb')}", h2_style))

        story.append(Paragraph("", abstand_style))
        
        # Spezifische Hinweise für Gastronomiebetrieb
        if form.get('betrieb') == "restaurant":
            hinweis_betrieb = "Ein Restaurant muss bei seiner Steuertransparenz zahlreiche gesetzliche Vorgaben einhalten. Zunächst ist es wichtig, dass alle Einnahmen und Ausgaben in einem manipulationssicheren Kassensystem erfasst werden. Das schreibt die Kassensicherungsverordnung (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html) vor, die sicherstellen soll, dass keine Umsätze „vergessen“ werden können. Manipulationssichere Kassensysteme müssen zertifiziert sein und alle Buchungen digital speichern. Außerdem gibt es die Belegausgabepflicht, die verlangt, dass jedem Kunden ein Kassenbon ausgehändigt wird. Diese Pflicht gilt unabhängig davon, ob der Kunde den Bon möchte oder nicht (https://www.gesetze-im-internet.de/ao_1977/BJNR006130976.html). Restaurants müssen auch bei der Umsatzsteuer gut aufpassen. Für Speisen gilt meistens der ermäßigte Steuersatz von 7 %, aber für Getränke und andere Zusatzleistungen, wie Catering oder Lieferdienste, gilt der volle Satz von 19 % (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Eine häufige Fehlerquelle ist die korrekte Trennung dieser Steuersätze, die sorgfältig dokumentiert werden muss. Zusätzlich müssen Trinkgelder korrekt behandelt werden. Sie sind steuerfrei, wenn sie freiwillig vom Kunden direkt an die Mitarbeiter gegeben werden. Werden Trinkgelder über das Kassensystem gesammelt oder an das Team verteilt, können andere Regelungen gelten (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html). Auch die Dokumentation des Wareneinsatzes ist wichtig, um sicherzustellen, dass die verbrauchten Lebensmittel zu den Einnahmen passen – das Finanzamt prüft solche Abweichungen."
            story.append(Paragraph(hinweis_betrieb, blocksatz_style))
        elif form.get('betrieb') == "cafe":
            hinweis_betrieb = "In einem Café müssen selbst kleine Beträge, wie der Verkauf von Kaffee, Tee oder Gebäck, lückenlos erfasst werden. Dazu ist ein elektronisches Kassensystem Pflicht, das den Vorgaben der Kassensicherungsverordnung (KassenSichV) entspricht. Jedes Café ist außerdem verpflichtet, jedem Kunden einen Kassenbon auszuhändigen, egal ob die Bestellung klein oder groß ist (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html).Ein kritischer Punkt für Cafés ist die Umsatzsteuer. Wenn ein Kunde seinen Kaffee mitnimmt, gilt der ermäßigte Steuersatz von 7 %. Trinkt der Kunde seinen Kaffee im Café, fällt jedoch der volle Steuersatz von 19 % an. Diese Unterscheidung ist essenziell, da sie Auswirkungen auf die Steuerabrechnung hat (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Außerdem müssen Cafés darauf achten, ihre Verpackungskosten korrekt zu berücksichtigen. Seit dem 1. Januar 2024 gelten neue Anforderungen an die Angaben auf Kassenbons. So müssen beispielsweise Umweltkosten für Mehrweg- oder Einwegverpackungen ausgewiesen werden (https://www.hwk.de/neuepflichtangaben-fuer-kassenbonsab-2024/)."
            story.append(Paragraph(hinweis_betrieb, blocksatz_style))
        elif form.get('betrieb') == "bar":
            hinweis_betrieb = "Bars stehen vor der Herausforderung, dass sie oft mit hohen Bargeldeinnahmen arbeiten, die besonders streng kontrolliert werden. Nach der Kassensicherungsverordnung (KassenSichV) ist auch hier ein zertifiziertes Kassensystem Pflicht. Um die Einnahmen korrekt zu erfassen, ist es wichtig, dass die Bons bei jedem Verkauf automatisch erstellt und gespeichert werden (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Ein weiterer wichtiger Punkt ist die Umsatzsteuer. Alkoholische Getränke werden generell mit 19 % Umsatzsteuer belegt, während Snacks oder kleine Speisen, die eventuell angeboten werden, nur 7 % unterliegen können (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Veranstaltungen wie Happy Hours oder Events erfordern besondere Sorgfalt, da Rabatte oder Sonderpreise in der Buchhaltung nachvollziehbar dokumentiert werden müssen. Auch Trinkgelder spielen in Bars eine große Rolle. Diese sind steuerfrei, wenn sie freiwillig direkt vom Gast an das Personal gegeben werden. Werden Trinkgelder zentral erfasst oder weiterverteilt, müssen sie jedoch korrekt in der Lohnabrechnung berücksichtigt werden (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html)."
            story.append(Paragraph(hinweis_betrieb, blocksatz_style))
        elif form.get('betrieb') == "imbiss":
            hinweis_betrieb = "Imbisse arbeiten oft mit kleinen Beträgen und schnellem Kundenkontakt. Auch hier ist die Verwendung eines manipulationssicheren Kassensystems Pflicht (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Besonders wichtig ist die Unterscheidung der Umsatzsteuer: Für Speisen, die mitgenommen werden, gilt der ermäßigte Steuersatz von 7 %, während der Verzehr vor Ort mit 19 % besteuert wird (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Imbissbetriebe müssen außerdem die Belegausgabepflicht beachten. Auch wenn viele Kunden ihre Bons nicht mitnehmen möchten, muss ein Beleg erstellt und dem Kunden angeboten werden (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html)."
            story.append(Paragraph(hinweis_betrieb, blocksatz_style))
        elif form.get('betrieb') == "catering":
            hinweis_betrieb = "Catering-Unternehmen haben oft umfangreiche Geschäftsbeziehungen, die sauber dokumentiert werden müssen. Jede Einnahme und Ausgabe muss in einem manipulationssicheren Kassensystem oder einer Buchhaltungssoftware erfasst werden (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Besonders wichtig ist die Abgrenzung der Umsatzsteuer: Während Dienstleistungen wie die Bereitstellung von Servicekräften dem vollen Steuersatz von 19 % unterliegen, können reine Speisenlieferungen ermäßigt besteuert werden (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Zusätzlich müssen Reisekosten und Materialaufwendungen für das Catering genau erfasst werden. Bewirtungskosten, etwa für Geschäftskunden, müssen zwischen abzugsfähigen und nicht abzugsfähigen Kosten unterschieden werden."
            story.append(Paragraph(hinweis_betrieb, blocksatz_style))
        elif form.get('betrieb') == "hotel":
            hinweis_betrieb = "Hotels mit gastronomischem Angebot müssen die Einnahmen aus Übernachtungen und Gastronomie getrennt erfassen. Für Übernachtungen gilt der ermäßigte Umsatzsteuersatz von 7 %, für Speisen und Getränke jedoch der volle Satz von 19 % (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Für Veranstaltungen wie Bankette oder Tagungen ist es wichtig, diese korrekt in der Buchhaltung auszuweisen, da solche Leistungen meist vollständig dem 19%-Steuersatz unterliegen. Die Kassensicherungsverordnung (KassenSichV) verpflichtet Hotels zudem, manipulationssichere Kassensysteme zu verwenden, die sämtliche Einnahmen digital speichern und absichern (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html)."
            story.append(Paragraph(hinweis_betrieb, blocksatz_style))
        elif form.get('betrieb') == "sonstiges":
            hinweis_betrieb = "Betriebe wie Foodtrucks oder Pop-up-Restaurants unterliegen ebenfalls der Kassensicherungsverordnung (KassenSichV) und der Belegausgabepflicht. Für saisonale Geschäfte, wie Weihnachtsmarktstände, ist es besonders wichtig, die Einnahmen trotz des kurzen Betriebszeitraums vollständig zu dokumentieren (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html). Lieferdienste müssen Einnahmen aus Dienstleistungen und Speisen getrennt erfassen, da unterschiedliche Steuersätze gelten (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Trinkgelder, die vom Kunden freiwillig gegeben werden, sind steuerfrei, sofern sie direkt an die Mitarbeiter gehen (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html)."
            story.append(Paragraph(hinweis_betrieb, blocksatz_style))
        story.append(Paragraph("", abstand_style))

        # 2. Frage: TSE (Technische Sicherheitseinrichtung)
        story.append(Paragraph(f"2. TSE-Anforderungen: {form.get('tse')}", h2_style))
        story.append(Paragraph("", abstand_style))

        if form.get('tse') == "ja":
            hinweis_tse = "Ihr Kassensystem entspricht den gesetzlichen Anforderungen der Kassensicherungsverordnung (KassenSichV). Das bedeutet, dass alle Umsätze manipulationssicher erfasst werden und bei einer Prüfung durch das Finanzamt nachvollziehbar sind. Sie erfüllen somit eine der wichtigsten Voraussetzungen für steuerliche Transparenz. Es ist jedoch wichtig, die Funktionalität Ihrer TSE regelmäßig zu überprüfen. Beachten Sie, dass die Zertifizierung einer TSE zeitlich begrenzt ist und rechtzeitig erneuert werden muss. Auch die Software Ihres Kassensystems sollte geprüft werden, um sicherzustellen, dass sie alle gesetzlichen Anforderungen, wie die Belegausgabepflicht, vollständig erfüllt. Weitere Informationen hierzu finden Sie unter: https://www.ihk.de/nordschwarzwald/recht/aktuelles/steuerliche-anforderungen-anregistrierkassen-3178868."
            story.append(Paragraph(hinweis_tse, blocksatz_style))
        elif form.get('tse') == "nein":
            hinweis_tse = "Falls Ihr Kassensystem nicht über eine zertifizierte technische Sicherheitseinrichtung (TSE) verfügt, ist dringender Handlungsbedarf geboten. Seit dem 1. Januar 2020 ist ein manipulationssicheres Kassensystem gesetzlich vorgeschrieben. Ohne eine TSE riskieren Sie erhebliche Konsequenzen, darunter Bußgelder und Steuernachzahlungen, falls eine Prüfung durch das Finanzamt erfolgt. In diesem Fall sollten Sie umgehend handeln: Lassen Sie Ihr Kassensystem aufrüsten oder investieren Sie in ein neues, gesetzeskonformes System. Bis ein TSE-konformes System installiert ist, müssen Sie Ihre Umsätze manuell und lückenlos dokumentieren. Weitere Informationen zu den Anforderungen und Hilfestellungen finden Sie unter: https://www.hwk.de/neuepflichtangaben-fuer-kassenbonsab-2024/."
            story.append(Paragraph(hinweis_tse, blocksatz_style))
        elif form.get('tse') == "unsicher":
            hinweis_tse = "Falls Sie sich unsicher sind, ob Ihr Kassensystem die Anforderungen einer zertifizierten technischen Sicherheitseinrichtung (TSE) erfüllt, sollten Sie dies schnellstmöglich klären, um mögliche rechtliche Konsequenzen zu vermeiden. Beginnen Sie damit, die technische Dokumentation Ihres Kassensystems zu überprüfen. Dort sollte angegeben sein, ob eine TSE vorhanden ist und den gesetzlichen Vorgaben entspricht. Falls diese Information nicht klar ist oder fehlt, kontaktieren Sie den Hersteller oder Anbieter Ihres Kassensystems. Lassen Sie sich schriftlich bestätigen, dass das System konform ist und eine zertifizierte TSE verwendet wird. Alternativ können Sie auch Ihren Steuerberater konsultieren, der Ihnen dabei hilft, die Konformität Ihres Systems zu überprüfen und gegebenenfalls notwendige Maßnahmen zur Nachrüstung einzuleiten. Beachten Sie, dass gemäß § 146a der Abgabenordnung (AO) alle elektronischen Kassensysteme in Deutschland seit dem 1. Januar 2020 mit einer TSE ausgestattet sein müssen. Diese Einrichtung gewährleistet, dass alle Einnahmen manipulationssicher erfasst und gespeichert werden. Weitere Informationen zu den gesetzlichen Anforderungen finden Sie hier: https://www.gesetze-im-internet.de/ao_1977/BJNR006130976.html."
            story.append(Paragraph(hinweis_tse, blocksatz_style))
        story.append(Paragraph("", abstand_style))

        # 3. Frage
        story.append(Paragraph(f"3. Belegausgabe: {form.get('beleg')}", h2_style))
        story.append(Paragraph("", abstand_style))

        if form.get('beleg') == "ja":
            hinweis_beleg = "Wenn die Antwort „Ja“ lautet, bedeutet dies, dass für jede Transaktion, egal ob der Kunde den Beleg anfordert oder nicht, ein Kassenbeleg ausgestellt werden muss. Dies ist gemäß der Belegausgabepflicht in Deutschland erforderlich. Diese Verpflichtung betrifft alle bargeld- und kartenzahlenden Kunden und gilt unabhängig von der Art des Geschäfts, auch für Online-Transaktionen. Die Kassensicherungsverordnung (KassenSichV) fordert, dass jeder Kassenbeleg auf elektronisch erfassten Transaktionen basieren muss. Der Beleg muss die grundlegenden Informationen wie den Betrag, den Zeitpunkt und die Art der Transaktion beinhalten. Falls ein manueller Beleg oder eine handschriftliche Quittung ausgestellt wird, sind auch hier die Informationen zur Transaktion eindeutig festzuhalten (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Zusätzlich muss der Kassenbeleg die verwendete Zahlungsmethode (Barzahlung, EC, Kreditkarte etc.) sowie die vollständigen Umsatzsteuerangaben enthalten. Die Belege dürfen nicht manipuliert werden können, weshalb ein zertifiziertes Kassensystem erforderlich ist. Eine lückenlose Dokumentation ist auch für die Steuergerechtigkeit erforderlich, um dem Finanzamt nachweisen zu können, dass alle Einnahmen korrekt versteuert wurden (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html)."
            story.append(Paragraph(hinweis_beleg, blocksatz_style))
        elif form.get('beleg') == "teilweise":
            hinweis_beleg = "Wenn die Antwort „Teilweise“ lautet, bedeutet dies, dass in bestimmten Fällen oder für bestimmte Arten von Transaktionen kein Beleg ausgestellt werden muss. Zum Beispiel könnte dies in Situationen zutreffen, in denen der Kunde auf den Beleg verzichtet, etwa bei kleinen Beträgen oder wiederkehrenden Kunden. Dennoch bleibt die Belegausgabepflicht grundsätzlich bestehen. In einigen Fällen, wie bei Online-Geschäften oder Transaktionen über elektronische Kassensysteme, kann der Beleg in elektronischer Form ausgegeben werden. Dabei muss jedoch sichergestellt werden, dass alle relevanten Informationen wie der Betrag, die Art der Transaktion, die verwendete Zahlungsmethode und der Steuersatz korrekt erfasst sind. Für den Fall, dass Belege nicht ausgestellt werden, sollte das Unternehmen in der Lage sein, durch andere Dokumentationsmittel nachzuweisen, dass die Transaktionen ordnungsgemäß erfasst wurden. Das bedeutet, dass auch für Transaktionen, bei denen keine Papierbelege ausgestellt werden, eine lückenlose Erfassung der Einnahmen im Kassensystem erforderlich ist. Dies entspricht den Anforderungen der Kassensicherungsverordnung (KassenSichV) und stellt sicher, dass keine Umsatzsteuerminderungen oder Steuerhinterziehungen vorgenommen werden (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Die Belegausgabepflicht verlangt, dass Unternehmen sicherstellen, dass dem Kunden der Beleg angeboten wird, auch wenn er diesen nicht immer annehmen möchte. Falls keine Belege ausgegeben werden, muss das Unternehmen jedoch einen anderen Nachweis erbringen, um die Einnahmen und Transaktionen korrekt zu dokumentieren (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html)."
            story.append(Paragraph(hinweis_beleg, blocksatz_style))
        story.append(Paragraph("", abstand_style))
        
        # 4. Frage
        story.append(Paragraph(f"4. Kassenprüfung: {form.get('prüfung')}", h2_style))
        story.append(Paragraph("", abstand_style))
        
        if form.get('prüfung') == "ja":
            hinweis_pruefung = "Wenn Ihr Kassensystem innerhalb der letzten 12 Monate geprüft oder zertifiziert wurde, erfüllen Sie bereits die Anforderungen der Kassensicherungsverordnung (KassenSichV), die sicherstellt, dass Ihre Kasse manipulationssicher ist. Nach der KassenSichV müssen elektronische Kassensysteme mit einer technischen Sicherheitseinrichtung (TSE) ausgestattet sein, die die Speicherung der Kassendaten sicherstellt. Diese Sicherheitsvorkehrungen verhindern, dass Daten verändert oder gelöscht werden können, was für eine ordnungsgemäße steuerliche Überprüfung notwendig ist (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Darüber hinaus sind Sie verpflichtet, die Belegausgabepflicht einzuhalten, die besagt, dass bei jedem Verkauf ein Kassenbeleg erstellt und dem Kunden zur Verfügung gestellt wird (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html). Falls Sie in den letzten 12 Monaten zusätzliche Anpassungen oder Änderungen vorgenommen haben (z. B. ein Update Ihres Kassensystems), sollten Sie sicherstellen, dass diese ebenfalls den geltenden gesetzlichen Anforderungen entsprechen. Stellen Sie sicher, dass Ihre Kassenbelege korrekt und vollständig sind. Seit dem 1. Januar 2024 müssen auch neue Pflichtangaben, wie z. B. Umweltkosten für Verpackungen, auf den Kassenbons erscheinen (https://www.hwk.de/neuepflichtangaben-fuer-kassenbonsab-2024/)."
            story.append(Paragraph(hinweis_pruefung, blocksatz_style))
        elif form.get('prüfung') == "nein":
            hinweis_pruefung = "Wenn Ihr Kassensystem innerhalb der letzten 12 Monate nicht geprüft oder zertifiziert wurde, müssen Sie sicherstellen, dass es den Anforderungen der Kassensicherungsverordnung (KassenSichV) entspricht. Das bedeutet, dass Ihr Kassensystem mit einer technischen Sicherheitseinrichtung (TSE) ausgestattet sein muss, die alle Kassendaten manipulationssicher speichert (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Zusätzlich sind Sie verpflichtet, die Belegausgabepflicht einzuhalten. Das bedeutet, dass Sie jedem Kunden bei jedem Kauf einen Kassenbeleg anbieten müssen, unabhängig davon, ob er diesen mitnimmt oder nicht (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html). Falls Ihr Kassensystem nicht den gesetzlichen Anforderungen entspricht, sollten Sie eine Überprüfung und gegebenenfalls eine Zertifizierung bei einem zugelassenen Anbieter durchführen lassen, um sicherzustellen, dass Sie den Vorschriften entsprechen und mögliche Steuerstrafen vermeiden. Zudem müssen Sie sicherstellen, dass ab dem 1. Januar 2024 neue Pflichtangaben auf den Kassenbons erscheinen, wie z. B. die Kosten für Verpackungen (https://www.hwk.de/neuepflichtangaben-fuer-kassenbonsab-2024/)."
            story.append(Paragraph(hinweis_pruefung, blocksatz_style))
        story.append(Paragraph("", abstand_style))
        
        # 5. Frage
        story.append(Paragraph(f"5. Trennung in der Buchhaltung: {form.get('trennung')}", h2_style))
        story.append(Paragraph("", abstand_style))

        if form.get('trennung') == "ja":
            hinweis_trennung = "Wenn Sie Speisen und Getränke korrekt in Ihrer Buchhaltung trennen, erfüllen Sie eine der grundlegenden Anforderungen der Steuertransparenz. Speisen unterliegen grundsätzlich dem ermäßigten Steuersatz von 7 %, während Getränke – unabhängig davon, ob sie vor Ort konsumiert oder mitgenommen werden – mit dem vollen Steuersatz von 19 % besteuert werden. Dies ist wichtig, um die korrekte Umsatzsteuerabführung zu gewährleisten und mögliche steuerliche Nachteile oder Strafen zu vermeiden. Um diese Trennung korrekt vorzunehmen, empfehlen wir, eine geeignete Buchhaltungssoftware zu verwenden oder manuell die Einnahmen aus Speisen und Getränken detailliert zu dokumentieren. Achten Sie darauf, dass Ihre Kassenbons und die digitale Aufzeichnung Ihrer Einnahmen diese Unterscheidung widerspiegeln. Beachten Sie auch die Vorgaben der Kassensicherungsverordnung (KassenSichV), die vorschreibt, dass alle Einnahmen ordnungsgemäß und manipulationssicher erfasst werden müssen (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html) und die Belegausgabepflicht (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html)."
            story.append(Paragraph(hinweis_trennung, blocksatz_style))
        elif form.get('trennung') == "nein":
            hinweis_trennung = "Wenn Sie Speisen und Getränke nicht korrekt in Ihrer Buchhaltung trennen, kann dies zu Problemen bei der Steuerabrechnung führen. Da für Speisen grundsätzlich der ermäßigte Steuersatz von 7 % und für Getränke der volle Steuersatz von 19 % gilt, ist es wichtig, diese beiden Kategorien korrekt zu unterscheiden. Eine falsche Zuordnung kann dazu führen, dass das Finanzamt eine falsche Steuerberechnung vornimmt, was zu Nachzahlungen oder sogar Strafen führen kann. Für eine korrekte Buchführung sollten Sie sicherstellen, dass alle Einnahmen aus Speisen und Getränken in Ihrem Kassensystem oder Ihrer Buchhaltung eindeutig voneinander getrennt sind. Wenn Sie dies noch nicht tun, sollten Sie überlegen, entweder Ihre Buchhaltungssoftware entsprechend anzupassen oder einen Steuerberater hinzuzuziehen, um eine korrekte Trennung zu gewährleisten. Verstöße gegen die Kassensicherungsverordnung (KassenSichV) oder das Fehlen von Kassenbons können ebenfalls Konsequenzen haben (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html) (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html)."
            story.append(Paragraph(hinweis_trennung, blocksatz_style))
        story.append(Paragraph("", abstand_style))

        # 6. Frage
        story.append(Paragraph(f"6. Vollständige Erfassung der Einnahmen: {form.get('einnahmen')}", h2_style))
        story.append(Paragraph("", abstand_style))

        if form.get('einnahmen') == "ja":
            hinweis_einnahmen = "Wenn Sie alle Einnahmen aus Barzahlungen, Kartenzahlungen und Lieferdiensten vollständig erfassen, halten Sie sich an die gesetzlichen Vorgaben zur Steuertransparenz. Die Kassensicherungsverordnung (KassenSichV) verlangt, dass alle Zahlungen, ob in bar oder mit Karte, lückenlos und ohne Manipulation in einem zertifizierten, manipulationssicheren Kassensystem erfasst werden. Dies stellt sicher, dass alle Einnahmen dokumentiert und dem Finanzamt korrekt gemeldet werden können. Besonders wichtig ist die vollständige Erfassung, um die Belegausgabepflicht einzuhalten. Unabhängig von der Zahlungsart müssen Sie jedem Kunden einen Kassenbon oder eine Quittung ausstellen, um Transparenz über den getätigten Umsatz zu gewährleisten. Dies ist eine Voraussetzung, um die steuerlichen Anforderungen zu erfüllen, wie sie in den § 146a der Abgabenordnung und der Kassensicherungsverordnung geregelt sind (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html) (https://www.gesetze-im-internet.de/ao_1977/BJNR006130976.html). Eine ordnungsgemäße Buchhaltung und die vollständige Erfassung aller Zahlungen, inklusive Lieferdienste und Kartenzahlungen, sind auch für die korrekte Berechnung der Umsatzsteuer entscheidend. Die korrekte Abgrenzung zwischen den verschiedenen Steuersätzen für die Lieferung und den Verzehr vor Ort ist von zentraler Bedeutung (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html)."
            story.append(Paragraph(hinweis_einnahmen, blocksatz_style))
        elif form.get('einnahmen') == "nein":
            hinweis_einnahmen = "Wenn Sie Speisen und Getränke nicht korrekt in Ihrer Buchhaltung trennen, kann dies zu Problemen bei der Steuerabrechnung führen. Da für Speisen grundsätzlich der ermäßigte Steuersatz von 7 % und für Getränke der volle Steuersatz von 19 % gilt, ist es wichtig, diese beiden Kategorien korrekt zu unterscheiden. Eine falsche Zuordnung kann dazu führen, dass das Finanzamt eine falsche Steuerberechnung vornimmt, was zu Nachzahlungen oder sogar Strafen führen kann. Für eine korrekte Buchführung sollten Sie sicherstellen, dass alle Einnahmen aus Speisen und Getränken in Ihrem Kassensystem oder Ihrer Buchhaltung eindeutig voneinander getrennt sind. Wenn Sie dies noch nicht tun, sollten Sie überlegen, entweder Ihre Buchhaltungssoftware entsprechend anzupassen oder einen Steuerberater hinzuzuziehen, um eine korrekte Trennung zu gewährleisten. Verstöße gegen die Kassensicherungsverordnung (KassenSichV) oder das Fehlen von Kassenbons können ebenfalls Konsequenzen haben (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html) (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html)."
            story.append(Paragraph(hinweis_einnahmen, blocksatz_style))
        story.append(Paragraph("", abstand_style))

        # 7. Frage
        story.append(Paragraph(f"7. fristgerechte einreichung der Steuererklärung: {form.get('steuererklärungen')}", h2_style))
        story.append(Paragraph("", abstand_style))

        if form.get('steuererklärungen') == "ja":
            hinweis_steuererklärungen = "Wenn Sie Ihre Steuererklärungen immer fristgerecht einreichen, erfüllen Sie eine wichtige gesetzliche Pflicht und vermeiden mögliche Strafen oder Verzugszinsen. Das Einhalten der Fristen stellt sicher, dass Ihre Steuerschuld korrekt berechnet und rechtzeitig beglichen wird. Steuerpflichtige, die die Abgabetermine einhalten, schützen sich vor zusätzlichen Kosten wie Verspätungszuschlägen und Zinsen. Es ist wichtig, alle erforderlichen Unterlagen vollständig und korrekt einzureichen, um spätere Rückfragen oder Nachforderungen des Finanzamtes zu vermeiden. Weitere Informationen zur Steuererklärung und den relevanten Fristen finden Sie in der Abgabenordnung (AO), die die allgemeinen Regeln für steuerliche Pflichten festlegt (https://www.gesetze-im-internet.de/ao_1977/BJNR006130976.html), sowie im Umsatzsteuergesetz (UStG), das die spezifischen Regelungen für die Umsatzsteuer und deren Meldung enthält (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html)."
            story.append(Paragraph(hinweis_steuererklärungen, blocksatz_style))
        elif form.get('steuererklärungen') == "nein":
            hinweis_steuererklärungen = "Wenn Sie Ihre Steuererklärungen nicht fristgerecht einreichen, müssen Sie mit möglichen Konsequenzen rechnen. Das Finanzamt kann Verspätungszuschläge erheben, die Ihre Steuerlast deutlich erhöhen. Darüber hinaus können Verzugszinsen anfallen, die zusätzlich zur ursprünglichen Steuerschuld bezahlt werden müssen. In wiederholten Fällen, in denen Steuererklärungen nicht fristgerecht eingereicht werden, kann das Finanzamt auch ein Zwangsgeld ansetzen, um die Einreichung der Erklärung zu erzwingen. Es wird daher empfohlen, bei wiederholten Versäumnissen rechtzeitig die Unterstützung eines Steuerberaters zu suchen. Dieser kann Ihnen helfen, die Steuererklärungen korrekt und fristgerecht nachzureichen. Wenn Sie Steuererklärungen verspätet einreichen, kann dies auch dazu führen, dass der Steuerbescheid später ergeht und zusätzliche Zahlungen erforderlich werden. Weitere Informationen zu den rechtlichen Konsequenzen und Strafen bei verspäteter Abgabe finden Sie in der Abgabenordnung (AO) (https://www.gesetze-im-internet.de/ao_1977/BJNR006130976.html) sowie zu den Verspätungszuschlägen und Strafen unter (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html)."
            story.append(Paragraph(hinweis_steuererklärungen, blocksatz_style))
        story.append(Paragraph("", abstand_style))

        # 8. Frage
        story.append(Paragraph(f"8. Umsatzsteuer-Nachforderungen innerhalb der letzten 2 Jahre erhalten: {form.get('nachforderungen')}", h2_style))
        story.append(Paragraph("", abstand_style))

        if form.get('nachforderungen') == "ja":
            hinweis_nachforderungen = "Wenn Sie in den letzten zwei Jahren eine Umsatzsteuer-Nachforderung erhalten haben, bedeutet das, dass das Finanzamt festgestellt hat, dass Sie zu wenig Umsatzsteuer abgeführt haben. In diesem Fall müssen Sie den Differenzbetrag nachzahlen und darauf achten, die Zahlungsfristen einzuhalten, um Säumniszuschläge oder Zinsen zu vermeiden. Falls die Nachforderung aufgrund von Fehlern in Ihrer Umsatzsteuererklärung entstanden ist, können Sie diese nachträglich berichtigen. Ein Steuerberater kann hierbei helfen. Wichtig ist auch, dass Ihre Buchhaltung und Kassensysteme den Anforderungen der Kassensicherungsverordnung (KassenSichV) entsprechen, die eine manipulationssichere Erfassung aller Einnahmen vorschreibt (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Falls Sie Schwierigkeiten bei der Begleichung der Nachforderung haben, können Sie beim Finanzamt eine Ratenzahlung beantragen. Achten Sie auch darauf, dass Trinkgelder korrekt erfasst werden, da diese steuerfrei sind, wenn sie direkt an das Personal gehen (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html)."
            story.append(Paragraph(hinweis_nachforderungen, blocksatz_style))
        elif form.get('nachforderungen') == "nein":
            hinweis_nachforderungen = "Wenn Sie in den letzten zwei Jahren keine Umsatzsteuer-Nachforderungen erhalten haben, ist dies ein gutes Zeichen dafür, dass Ihre steuerlichen Angelegenheiten gut organisiert sind. Um auch in Zukunft Probleme zu vermeiden, sollten Sie weiterhin sicherstellen, dass alle Umsatzsteuererklärungen korrekt abgegeben werden. Achten Sie darauf, dass Sie Belege für jede Transaktion ausstellen und die Belegausgabepflicht erfüllen (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html). Stellen Sie außerdem sicher, dass Ihre Kassensysteme den Vorgaben der Kassensicherungsverordnung (KassenSichV) entsprechen, um eine korrekte Erfassung der Einnahmen und Ausgaben sicherzustellen. So vermeiden Sie mögliche steuerliche Probleme bei einer späteren Betriebsprüfung (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Falls Sie unsicher sind, können Sie einen Steuerberater hinzuziehen, um Fehler zu vermeiden und Ihre steuerlichen Pflichten genau zu prüfen."
            story.append(Paragraph(hinweis_nachforderungen, blocksatz_style))
        story.append(Paragraph("", abstand_style))

        # 9. Frage
        story.append(Paragraph(f"9. Dokumentation von Trinkgeldern gemäß steuerlichen Vorgaben: {form.get('trinkgelder')}", h2_style))
        story.append(Paragraph("", abstand_style))

        if form.get('trinkgelder') == "ja":
            hinweis_trinkgelder = "Wenn Trinkgelder gemäß den steuerlichen Vorgaben dokumentiert werden müssen, müssen Sie sicherstellen, dass alle Trinkgelder korrekt erfasst und dokumentiert werden. Grundsätzlich sind Trinkgelder steuerfrei, wenn sie direkt und freiwillig vom Gast an die Mitarbeiter übergeben werden. Diese Trinkgelder müssen jedoch korrekt in der Buchhaltung und gegebenenfalls in der Lohnabrechnung berücksichtigt werden, besonders wenn sie über ein Kassensystem abgewickelt werden. Wenn Trinkgelder über das Kassensystem erfasst werden, etwa in einem Pool oder als Teil eines Servicezuschlags, gelten diese Trinkgelder als Betriebseinnahmen und müssen in der Buchhaltung als solche verbucht werden. In diesem Fall unterliegen die Trinkgelder der Umsatzsteuer und müssen in der Umsatzsteuererklärung berücksichtigt werden. Es ist wichtig, dass alle relevanten Belege und Nachweise aufbewahrt werden, um im Falle einer Steuerprüfung alle Einnahmen, einschließlich der Trinkgelder, nachweisen zu können. Die Kassensicherungsverordnung (KassenSichV) fordert, dass alle Einnahmen, auch Trinkgelder, ordnungsgemäß dokumentiert werden, wenn sie über das Kassensystem abgewickelt werden. Dies bedeutet, dass Sie bei der Verwendung eines Kassensystems sicherstellen müssen, dass alle Trinkgelder entsprechend der gesetzlichen Vorgaben erfasst und die Einnahmen korrekt verbucht werden (Kassensicherungsverordnung (KassenSichV)). Wenn Trinkgelder an Mitarbeiter weitergegeben werden, müssen diese in der Lohnabrechnung korrekt ausgewiesen werden, wenn sie aus einem Pool stammen oder als Teil des Gehalts behandelt werden. Auch wenn Trinkgelder steuerfrei sind, müssen sie ordnungsgemäß dokumentiert und in den Lohnabrechnungen berücksichtigt werden. Weitere Informationen zu den steuerlichen Regelungen zu Trinkgeldern finden Sie hier: Trinkgeldregelungen und Steuerfreiheit. Zudem müssen Sie die gesetzlichen Bestimmungen zur Belegausgabepflicht einhalten, die auch für Trinkgelder relevant sein kann, wenn sie über das Kassensystem erfasst werden. Weitere Details zur Belegausgabepflicht finden Sie auf der Webseite des Bundesministeriums der Finanzen: Belegausgabepflicht FAQ."
            story.append(Paragraph(hinweis_trinkgelder, blocksatz_style))
        elif form.get('trinkgelder') == "nein":
            hinweis_trinkgelder = "Wenn Sie Trinkgelder nicht dokumentieren müssen, bezieht sich dies meist auf Fälle, in denen Trinkgelder direkt und freiwillig vom Gast an die Mitarbeiter gegeben werden, ohne dass diese über das Kassensystem oder die Buchhaltung des Unternehmens laufen. In diesem Fall gelten Trinkgelder als steuerfreie Einkünfte für die Mitarbeiter und müssen nicht in der Buchhaltung des Unternehmens erfasst werden. Es besteht keine Pflicht zur Dokumentation dieser Trinkgelder in den Steuererklärungen, solange sie nicht über das Kassensystem oder auf andere Weise in das Unternehmen integriert werden. Diese Trinkgelder unterliegen nicht der Umsatzsteuer und müssen nicht in der Umsatzsteuererklärung des Unternehmens berücksichtigt werden. Sie sind nur dann steuerpflichtig, wenn sie über das Kassensystem laufen oder als Teil eines Servicezuschlags in der Rechnung enthalten sind. Es ist daher wichtig zu verstehen, dass Trinkgelder, die direkt an die Mitarbeiter gegeben werden, als persönliche Zuwendung des Gastes gelten, die nicht der Umsatzsteuer unterliegt. Weitere Informationen finden Sie dazu im Umsatzsteuergesetz (UStG): Umsatzsteuergesetz (UStG). Auch wenn Trinkgelder nicht dokumentiert werden müssen, bleibt die Pflicht zur ordnungsgemäßen Nutzung eines Kassensystems bestehen. Die Kassensicherungsverordnung (KassenSichV) verlangt, dass alle Einnahmen, auch Trinkgelder, korrekt erfasst werden, wenn diese über das Kassensystem laufen. Daher sollten Sie sicherstellen, dass Sie alle gesetzlichen Anforderungen an Ihre Kassenführung einhalten, auch wenn die Trinkgelder nicht dokumentiert werden müssen (Kassensicherungsverordnung (KassenSichV)). Falls Trinkgelder in einem Pool gesammelt und unter den Mitarbeitern aufgeteilt werden, müssen diese korrekt in der Lohnbuchhaltung angegeben werden. In solchen Fällen müssen sie ebenfalls dokumentiert werden, da sie als Einnahmen gelten und in die Lohnabrechnung aufgenommen werden müssen. Weitere Informationen zur Steuerfreiheit von Trinkgeldern und den entsprechenden Regelungen finden Sie auf der Seite der VLH Trinkgeldregelungen."
            story.append(Paragraph(hinweis_trinkgelder, blocksatz_style))
        story.append(Paragraph("", abstand_style))

        # 10. Frage
        story.append(Paragraph(f"10. Schulung der Mitarbeiter: {form.get('schulung')}", h2_style))
        story.append(Paragraph("", abstand_style))

        if form.get('schulung') == "ja":
            hinweis_schulung = "Wenn Ihre Mitarbeitenden regelmäßig zu steuerlichen Vorgaben geschult werden, ist das ein sehr positiver Schritt, um sicherzustellen, dass alle relevanten Vorschriften eingehalten werden. Die regelmäßige Schulung hilft, Fehler zu vermeiden, die durch Unwissenheit oder Missverständnisse bei der Anwendung der Kassensicherungsverordnung (KassenSichV), der Trinkgeldregelung und anderen steuerlichen Anforderungen entstehen können. Ein wichtiger Bestandteil der Schulung sollte das Kassensystem und die Belegausgabepflicht sein. Mitarbeitende müssen wissen, dass alle Transaktionen korrekt in einem manipulationssicheren Kassensystem erfasst werden müssen. Dies ist durch die Kassensicherungsverordnung (KassenSichV) vorgeschrieben, die für Gastronomiebetriebe, einschließlich Restaurants, Cafés, Bars, Imbisse und Hotels, gilt. Das System sollte alle Buchungen digital und revisionssicher speichern, um Steuerhinterziehung zu verhindern. Die Belegausgabepflicht erfordert, dass jedem Kunden ein Kassenbon ausgestellt wird, unabhängig davon, ob der Kunde diesen tatsächlich mitnimmt oder nicht. Schulungen helfen sicherzustellen, dass alle Mitarbeitenden den gesetzlichen Anforderungen folgen (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Zusätzlich sollten Mitarbeitende über die Trinkgeldregelung informiert sein. Trinkgelder sind grundsätzlich steuerfrei, wenn sie direkt vom Gast an das Personal gegeben werden. Werden die Trinkgelder jedoch über das Kassensystem verwaltet oder an das Team verteilt, müssen sie steuerlich korrekt behandelt werden. Eine ordnungsgemäße Dokumentation ist entscheidend, um steuerliche und rechtliche Probleme zu vermeiden (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html)."
            story.append(Paragraph(hinweis_schulung, blocksatz_style))
        elif form.get('schulung') == "nein":
            hinweis_schulung = "Wenn Ihre Mitarbeitenden noch nicht regelmäßig zu den steuerlichen Vorgaben geschult werden, könnte dies langfristig zu Problemen führen, insbesondere in Bezug auf die Einhaltung gesetzlicher Anforderungen. Insbesondere die Kassensicherungsverordnung (KassenSichV) und die Belegausgabepflicht müssen genau beachtet werden. Das Fehlen einer Schulung kann dazu führen, dass Transaktionen nicht korrekt erfasst werden, was das Risiko von Steuerhinterziehung oder Fehlern bei der Umsatzsteuermeldung erhöht. Die Kassensicherungsverordnung (KassenSichV) schreibt vor, dass alle Transaktionen in einem manipulationssicheren Kassensystem erfasst und digital gespeichert werden müssen. Ein nicht manipulierbares System schützt sowohl den Betrieb als auch die Mitarbeitenden vor rechtlichen Konsequenzen (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Außerdem müssen alle Mitarbeitenden die Belegausgabepflicht verstehen und umsetzen. Jeder Kunde muss einen Beleg erhalten, auch wenn er diesen nicht mitnimmt. Das kann zu Strafen führen, wenn es bei den Aufzeichnungen oder der Bon-Ausgabe Versäumnisse gibt (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html). Zudem ist es wichtig, dass Ihre Mitarbeitenden die Trinkgeldregelung verstehen. Trinkgelder, die direkt vom Gast an die Mitarbeitenden gegeben werden, sind grundsätzlich steuerfrei. Werden Trinkgelder jedoch über das Kassensystem verwaltet oder verteilt, muss die steuerliche Behandlung korrekt erfolgen (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html). Es wird empfohlen, eine regelmäßige Schulung durchzuführen, um sicherzustellen, dass alle Mitarbeitenden über aktuelle steuerliche Regelungen informiert sind und Fehler in der täglichen Praxis vermieden werden."
            story.append(Paragraph(hinweis_schulung, blocksatz_style))
        
        document.build(story)

        return filename