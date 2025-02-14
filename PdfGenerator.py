from flask import session
from reportlab.lib.pagesizes import letter 
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.pagesizes import letter

class PdfGenerator():
    def __init__(self):
        pass
    def generate_pdf(self, form):

        test_type = "Ausführlich" if 'kassensystem' in form else "Schnell"
        filename = "Nachhaltigkeitsbericht.pdf"
        document = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()

        #Styles von ChatGPT generiert
        h1_style = ParagraphStyle(
            "h1ueberschrift", 
            parent=styles["Normal"],
            fontName="Helvetica-Bold", 
            fontSize=24,
            spaceAfter=26,
            alignment=1 
        )

        h2_style = ParagraphStyle(
            "h2ueberschrift", 
            parent=styles["Normal"],
            fontName="Helvetica-Bold", 
            fontSize=14, 
            alignment=1
        )

        blocksatz_style = ParagraphStyle(
            "blocksatz", 
            parent=styles["Normal"],  
            alignment=4,
            fontSize=11,
            leading=16,
            spaceAfter=8
        )

        story = []

        # je nachdem welchen Test man wählt soll der Titel gewählt werden
        title = "Ausführlicher Check Report" if test_type == "Ausführlich" else "SchnellCheck Report"
        story.append(Paragraph(f"<b>{title}</b>", h1_style))
        story.append(Spacer(1, 10))

        # Ampelfarbe hinzufügen
        ampelfarbe = session['ampelfarbe']
        ampelfarbe_dict = {
            "rot": colors.red,
            "gelb": colors.yellow,
            "grün": colors.green
        }
        ampelfarbe_paragraph = f"<font color={ampelfarbe_dict[ampelfarbe]}><b>Ampelfarbe: {ampelfarbe.capitalize()}</b></font>"
        story.append(Paragraph(ampelfarbe_paragraph, styles["Normal"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Um die Links aufzurufen, kopieren Sie am besten die URL aus den Klammern und fügen sie dann im Browser ein, danke!",blocksatz_style))
        story.append(Spacer(1, 10))

        # Damit zwischen den test Typen unterschieden werden kann, also ob Schneller oder Ausführlicher
        if test_type == "Schnell":
            self._add_schnelltest_sections(form, story, h2_style, blocksatz_style)
        else:
            self._add_ausfuehrlich_sections(form, story, h2_style, blocksatz_style)

        document.build(story)
        return filename

    def _add_schnelltest_sections(self, form, story, h2_style, blocksatz_style):

        betrieb = form.get('betrieb')
        TSE = form.get('tse')
        Beleg = form.get('beleg')
        Pruefung = form.get('prüfung')
        Trennung = form.get('trennung')
        Einnahmen = form.get('einnahmen')
        Steuererklärungen = form.get('steuererklärungen')
        Nachforderungen = form.get('nachforderungen')
        Trinkgelder = form.get('trinkgelder')
        Schulung = form.get('schulung')

        
        
        # hier die Hinweise bzw. das was ausgegeben werden soll je nachdem was der User wählt
        betrieb_hinweise = {
            "restaurant": "Ein Restaurant muss bei seiner Steuertransparenz zahlreiche gesetzliche Vorgaben einhalten. Zunächst ist es wichtig, dass alle Einnahmen und Ausgaben in einem manipulationssicheren Kassensystem erfasst werden. Das schreibt die Kassensicherungsverordnung (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html) vor, die sicherstellen soll, dass keine Umsätze „vergessen“ werden können. Manipulationssichere Kassensysteme müssen zertifiziert sein und alle Buchungen digital speichern. Außerdem gibt es die Belegausgabepflicht, die verlangt, dass jedem Kunden ein Kassenbon ausgehändigt wird. Diese Pflicht gilt unabhängig davon, ob der Kunde den Bon möchte oder nicht (https://www.gesetze-im-internet.de/ao_1977/BJNR006130976.html). Restaurants müssen auch bei der Umsatzsteuer gut aufpassen. Für Speisen gilt meistens der ermäßigte Steuersatz von 7 %, aber für Getränke und andere Zusatzleistungen, wie Catering oder Lieferdienste, gilt der volle Satz von 19 % (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Eine häufige Fehlerquelle ist die korrekte Trennung dieser Steuersätze, die sorgfältig dokumentiert werden muss. Zusätzlich müssen Trinkgelder korrekt behandelt werden. Sie sind steuerfrei, wenn sie freiwillig vom Kunden direkt an die Mitarbeiter gegeben werden. Werden Trinkgelder über das Kassensystem gesammelt oder an das Team verteilt, können andere Regelungen gelten (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html). Auch die Dokumentation des Wareneinsatzes ist wichtig, um sicherzustellen, dass die verbrauchten Lebensmittel zu den Einnahmen passen – das Finanzamt prüft solche Abweichungen.",  # Keep your existing restaurant text
            "cafe": "In einem Café müssen selbst kleine Beträge, wie der Verkauf von Kaffee, Tee oder Gebäck, lückenlos erfasst werden. Dazu ist ein elektronisches Kassensystem Pflicht, das den Vorgaben der Kassensicherungsverordnung (KassenSichV) entspricht. Jedes Café ist außerdem verpflichtet, jedem Kunden einen Kassenbon auszuhändigen, egal ob die Bestellung klein oder groß ist (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html).Ein kritischer Punkt für Cafés ist die Umsatzsteuer. Wenn ein Kunde seinen Kaffee mitnimmt, gilt der ermäßigte Steuersatz von 7 %. Trinkt der Kunde seinen Kaffee im Café, fällt jedoch der volle Steuersatz von 19 % an. Diese Unterscheidung ist essenziell, da sie Auswirkungen auf die Steuerabrechnung hat (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Außerdem müssen Cafés darauf achten, ihre Verpackungskosten korrekt zu berücksichtigen. Seit dem 1. Januar 2024 gelten neue Anforderungen an die Angaben auf Kassenbons. So müssen beispielsweise Umweltkosten für Mehrweg- oder Einwegverpackungen ausgewiesen werden (https://www.hwk.de/neuepflichtangaben-fuer-kassenbonsab-2024/).",        # Keep your existing cafe text
            "bar":"Bars stehen vor der Herausforderung, dass sie oft mit hohen Bargeldeinnahmen arbeiten, die besonders streng kontrolliert werden. Nach der Kassensicherungsverordnung (KassenSichV) ist auch hier ein zertifiziertes Kassensystem Pflicht. Um die Einnahmen korrekt zu erfassen, ist es wichtig, dass die Bons bei jedem Verkauf automatisch erstellt und gespeichert werden (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Ein weiterer wichtiger Punkt ist die Umsatzsteuer. Alkoholische Getränke werden generell mit 19 % Umsatzsteuer belegt, während Snacks oder kleine Speisen, die eventuell angeboten werden, nur 7 % unterliegen können (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Veranstaltungen wie Happy Hours oder Events erfordern besondere Sorgfalt, da Rabatte oder Sonderpreise in der Buchhaltung nachvollziehbar dokumentiert werden müssen. Auch Trinkgelder spielen in Bars eine große Rolle. Diese sind steuerfrei, wenn sie freiwillig direkt vom Gast an das Personal gegeben werden. Werden Trinkgelder zentral erfasst oder weiterverteilt, müssen sie jedoch korrekt in der Lohnabrechnung berücksichtigt werden (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html).",
            "imbiss":"Imbisse arbeiten oft mit kleinen Beträgen und schnellem Kundenkontakt. Auch hier ist die Verwendung eines manipulationssicheren Kassensystems Pflicht (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Besonders wichtig ist die Unterscheidung der Umsatzsteuer: Für Speisen, die mitgenommen werden, gilt der ermäßigte Steuersatz von 7 %, während der Verzehr vor Ort mit 19 % besteuert wird (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Imbissbetriebe müssen außerdem die Belegausgabepflicht beachten. Auch wenn viele Kunden ihre Bons nicht mitnehmen möchten, muss ein Beleg erstellt und dem Kunden angeboten werden (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html).",
            "catering":"Catering-Unternehmen haben oft umfangreiche Geschäftsbeziehungen, die sauber dokumentiert werden müssen. Jede Einnahme und Ausgabe muss in einem manipulationssicheren Kassensystem oder einer Buchhaltungssoftware erfasst werden (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Besonders wichtig ist die Abgrenzung der Umsatzsteuer: Während Dienstleistungen wie die Bereitstellung von Servicekräften dem vollen Steuersatz von 19 % unterliegen, können reine Speisenlieferungen ermäßigt besteuert werden (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Zusätzlich müssen Reisekosten und Materialaufwendungen für das Catering genau erfasst werden. Bewirtungskosten, etwa für Geschäftskunden, müssen zwischen abzugsfähigen und nicht abzugsfähigen Kosten unterschieden werden.",
            "hotel":"Hotels mit gastronomischem Angebot müssen die Einnahmen aus Übernachtungen und Gastronomie getrennt erfassen. Für Übernachtungen gilt der ermäßigte Umsatzsteuersatz von 7 %, für Speisen und Getränke jedoch der volle Satz von 19 % (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Für Veranstaltungen wie Bankette oder Tagungen ist es wichtig, diese korrekt in der Buchhaltung auszuweisen, da solche Leistungen meist vollständig dem 19%-Steuersatz unterliegen. Die Kassensicherungsverordnung (KassenSichV) verpflichtet Hotels zudem, manipulationssichere Kassensysteme zu verwenden, die sämtliche Einnahmen digital speichern und absichern (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html).",
            "sonstiges":"Betriebe wie Foodtrucks oder Pop-up-Restaurants unterliegen ebenfalls der Kassensicherungsverordnung (KassenSichV) und der Belegausgabepflicht. Für saisonale Geschäfte, wie Weihnachtsmarktstände, ist es besonders wichtig, die Einnahmen trotz des kurzen Betriebszeitraums vollständig zu dokumentieren (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html). Lieferdienste müssen Einnahmen aus Dienstleistungen und Speisen getrennt erfassen, da unterschiedliche Steuersätze gelten (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html). Trinkgelder, die vom Kunden freiwillig gegeben werden, sind steuerfrei, sofern sie direkt an die Mitarbeiter gehen (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html)."
        }
        TSE_hinweise = {
            "ja":"Ihr Kassensystem entspricht den gesetzlichen Anforderungen der Kassensicherungsverordnung (KassenSichV). Das bedeutet, dass alle Umsätze manipulationssicher erfasst werden und bei einer Prüfung durch das Finanzamt nachvollziehbar sind. Sie erfüllen somit eine der wichtigsten Voraussetzungen für steuerliche Transparenz. Es ist jedoch wichtig, die Funktionalität Ihrer TSE regelmäßig zu überprüfen. Beachten Sie, dass die Zertifizierung einer TSE zeitlich begrenzt ist und rechtzeitig erneuert werden muss. Auch die Software Ihres Kassensystems sollte geprüft werden, um sicherzustellen, dass sie alle gesetzlichen Anforderungen, wie die Belegausgabepflicht, vollständig erfüllt. Weitere Informationen hierzu finden Sie unter: https://www.ihk.de/nordschwarzwald/recht/aktuelles/steuerliche-anforderungen-anregistrierkassen-3178868.",
            "nein":"Falls Ihr Kassensystem nicht über eine zertifizierte technische Sicherheitseinrichtung (TSE) verfügt, ist dringender Handlungsbedarf geboten. Seit dem 1. Januar 2020 ist ein manipulationssicheres Kassensystem gesetzlich vorgeschrieben. Ohne eine TSE riskieren Sie erhebliche Konsequenzen, darunter Bußgelder und Steuernachzahlungen, falls eine Prüfung durch das Finanzamt erfolgt. In diesem Fall sollten Sie umgehend handeln: Lassen Sie Ihr Kassensystem aufrüsten oder investieren Sie in ein neues, gesetzeskonformes System. Bis ein TSE-konformes System installiert ist, müssen Sie Ihre Umsätze manuell und lückenlos dokumentieren. Weitere Informationen zu den Anforderungen und Hilfestellungen finden Sie unter: https://www.hwk.de/neuepflichtangaben-fuer-kassenbonsab-2024/.",
            "unsicher":"Falls Sie sich unsicher sind, ob Ihr Kassensystem die Anforderungen einer zertifizierten technischen Sicherheitseinrichtung (TSE) erfüllt, sollten Sie dies schnellstmöglich klären, um mögliche rechtliche Konsequenzen zu vermeiden. Beginnen Sie damit, die technische Dokumentation Ihres Kassensystems zu überprüfen. Dort sollte angegeben sein, ob eine TSE vorhanden ist und den gesetzlichen Vorgaben entspricht. Falls diese Information nicht klar ist oder fehlt, kontaktieren Sie den Hersteller oder Anbieter Ihres Kassensystems. Lassen Sie sich schriftlich bestätigen, dass das System konform ist und eine zertifizierte TSE verwendet wird. Alternativ können Sie auch Ihren Steuerberater konsultieren, der Ihnen dabei hilft, die Konformität Ihres Systems zu überprüfen und gegebenenfalls notwendige Maßnahmen zur Nachrüstung einzuleiten. Beachten Sie, dass gemäß § 146a der Abgabenordnung (AO) alle elektronischen Kassensysteme in Deutschland seit dem 1. Januar 2020 mit einer TSE ausgestattet sein müssen. Diese Einrichtung gewährleistet, dass alle Einnahmen manipulationssicher erfasst und gespeichert werden. Weitere Informationen zu den gesetzlichen Anforderungen finden Sie hier: https://www.gesetze-im-internet.de/ao_1977/BJNR006130976.html."
        }
        Beleg_hinweise = {
            "ja":"Wenn die Antwort „Ja“ lautet, bedeutet dies, dass für jede Transaktion, egal ob der Kunde den Beleg anfordert oder nicht, ein Kassenbeleg ausgestellt werden muss. Dies ist gemäß der Belegausgabepflicht in Deutschland erforderlich. Diese Verpflichtung betrifft alle bargeld- und kartenzahlenden Kunden und gilt unabhängig von der Art des Geschäfts, auch für Online-Transaktionen. Die Kassensicherungsverordnung (KassenSichV) fordert, dass jeder Kassenbeleg auf elektronisch erfassten Transaktionen basieren muss. Der Beleg muss die grundlegenden Informationen wie den Betrag, den Zeitpunkt und die Art der Transaktion beinhalten. Falls ein manueller Beleg oder eine handschriftliche Quittung ausgestellt wird, sind auch hier die Informationen zur Transaktion eindeutig festzuhalten (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Zusätzlich muss der Kassenbeleg die verwendete Zahlungsmethode (Barzahlung, EC, Kreditkarte etc.) sowie die vollständigen Umsatzsteuerangaben enthalten. Die Belege dürfen nicht manipuliert werden können, weshalb ein zertifiziertes Kassensystem erforderlich ist. Eine lückenlose Dokumentation ist auch für die Steuergerechtigkeit erforderlich, um dem Finanzamt nachweisen zu können, dass alle Einnahmen korrekt versteuert wurden (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html).",
            "teilweise":"Wenn die Antwort „Teilweise“ lautet, bedeutet dies, dass in bestimmten Fällen oder für bestimmte Arten von Transaktionen kein Beleg ausgestellt werden muss. Zum Beispiel könnte dies in Situationen zutreffen, in denen der Kunde auf den Beleg verzichtet, etwa bei kleinen Beträgen oder wiederkehrenden Kunden. Dennoch bleibt die Belegausgabepflicht grundsätzlich bestehen. In einigen Fällen, wie bei Online-Geschäften oder Transaktionen über elektronische Kassensysteme, kann der Beleg in elektronischer Form ausgegeben werden. Dabei muss jedoch sichergestellt werden, dass alle relevanten Informationen wie der Betrag, die Art der Transaktion, die verwendete Zahlungsmethode und der Steuersatz korrekt erfasst sind. Für den Fall, dass Belege nicht ausgestellt werden, sollte das Unternehmen in der Lage sein, durch andere Dokumentationsmittel nachzuweisen, dass die Transaktionen ordnungsgemäß erfasst wurden. Das bedeutet, dass auch für Transaktionen, bei denen keine Papierbelege ausgestellt werden, eine lückenlose Erfassung der Einnahmen im Kassensystem erforderlich ist. Dies entspricht den Anforderungen der Kassensicherungsverordnung (KassenSichV) und stellt sicher, dass keine Umsatzsteuerminderungen oder Steuerhinterziehungen vorgenommen werden (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Die Belegausgabepflicht verlangt, dass Unternehmen sicherstellen, dass dem Kunden der Beleg angeboten wird, auch wenn er diesen nicht immer annehmen möchte. Falls keine Belege ausgegeben werden, muss das Unternehmen jedoch einen anderen Nachweis erbringen, um die Einnahmen und Transaktionen korrekt zu dokumentieren (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html).",
            "nein":"Riskant! Ohne Belegausgabe machen Sie sich strafbar. Sofort ändern!"
        }
        Pruefung_hinweise = {
            "ja":"Wenn Ihr Kassensystem innerhalb der letzten 12 Monate geprüft oder zertifiziert wurde, erfüllen Sie bereits die Anforderungen der Kassensicherungsverordnung (KassenSichV), die sicherstellt, dass Ihre Kasse manipulationssicher ist. Nach der KassenSichV müssen elektronische Kassensysteme mit einer technischen Sicherheitseinrichtung (TSE) ausgestattet sein, die die Speicherung der Kassendaten sicherstellt. Diese Sicherheitsvorkehrungen verhindern, dass Daten verändert oder gelöscht werden können, was für eine ordnungsgemäße steuerliche Überprüfung notwendig ist (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Darüber hinaus sind Sie verpflichtet, die Belegausgabepflicht einzuhalten, die besagt, dass bei jedem Verkauf ein Kassenbeleg erstellt und dem Kunden zur Verfügung gestellt wird (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html). Falls Sie in den letzten 12 Monaten zusätzliche Anpassungen oder Änderungen vorgenommen haben (z. B. ein Update Ihres Kassensystems), sollten Sie sicherstellen, dass diese ebenfalls den geltenden gesetzlichen Anforderungen entsprechen. Stellen Sie sicher, dass Ihre Kassenbelege korrekt und vollständig sind. Seit dem 1. Januar 2024 müssen auch neue Pflichtangaben, wie z. B. Umweltkosten für Verpackungen, auf den Kassenbons erscheinen (https://www.hwk.de/neuepflichtangaben-fuer-kassenbonsab-2024/).",
            "nein":"Wenn Ihr Kassensystem innerhalb der letzten 12 Monate nicht geprüft oder zertifiziert wurde, müssen Sie sicherstellen, dass es den Anforderungen der Kassensicherungsverordnung (KassenSichV) entspricht. Das bedeutet, dass Ihr Kassensystem mit einer technischen Sicherheitseinrichtung (TSE) ausgestattet sein muss, die alle Kassendaten manipulationssicher speichert (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Zusätzlich sind Sie verpflichtet, die Belegausgabepflicht einzuhalten. Das bedeutet, dass Sie jedem Kunden bei jedem Kauf einen Kassenbeleg anbieten müssen, unabhängig davon, ob er diesen mitnimmt oder nicht (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html). Falls Ihr Kassensystem nicht den gesetzlichen Anforderungen entspricht, sollten Sie eine Überprüfung und gegebenenfalls eine Zertifizierung bei einem zugelassenen Anbieter durchführen lassen, um sicherzustellen, dass Sie den Vorschriften entsprechen und mögliche Steuerstrafen vermeiden. Zudem müssen Sie sicherstellen, dass ab dem 1. Januar 2024 neue Pflichtangaben auf den Kassenbons erscheinen, wie z. B. die Kosten für Verpackungen (https://www.hwk.de/neuepflichtangaben-fuer-kassenbonsab-2024/)."
        }
        Trennung_hinweise = {
            "ja":"Wenn Sie Speisen und Getränke korrekt in Ihrer Buchhaltung trennen, erfüllen Sie eine der grundlegenden Anforderungen der Steuertransparenz. Speisen unterliegen grundsätzlich dem ermäßigten Steuersatz von 7 %, während Getränke – unabhängig davon, ob sie vor Ort konsumiert oder mitgenommen werden – mit dem vollen Steuersatz von 19 % besteuert werden. Dies ist wichtig, um die korrekte Umsatzsteuerabführung zu gewährleisten und mögliche steuerliche Nachteile oder Strafen zu vermeiden. Um diese Trennung korrekt vorzunehmen, empfehlen wir, eine geeignete Buchhaltungssoftware zu verwenden oder manuell die Einnahmen aus Speisen und Getränken detailliert zu dokumentieren. Achten Sie darauf, dass Ihre Kassenbons und die digitale Aufzeichnung Ihrer Einnahmen diese Unterscheidung widerspiegeln. Beachten Sie auch die Vorgaben der Kassensicherungsverordnung (KassenSichV), die vorschreibt, dass alle Einnahmen ordnungsgemäß und manipulationssicher erfasst werden müssen (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html) und die Belegausgabepflicht (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html).",
            "nein":"Wenn Sie Speisen und Getränke nicht korrekt in Ihrer Buchhaltung trennen, kann dies zu Problemen bei der Steuerabrechnung führen. Da für Speisen grundsätzlich der ermäßigte Steuersatz von 7 % und für Getränke der volle Steuersatz von 19 % gilt, ist es wichtig, diese beiden Kategorien korrekt zu unterscheiden. Eine falsche Zuordnung kann dazu führen, dass das Finanzamt eine falsche Steuerberechnung vornimmt, was zu Nachzahlungen oder sogar Strafen führen kann. Für eine korrekte Buchführung sollten Sie sicherstellen, dass alle Einnahmen aus Speisen und Getränken in Ihrem Kassensystem oder Ihrer Buchhaltung eindeutig voneinander getrennt sind. Wenn Sie dies noch nicht tun, sollten Sie überlegen, entweder Ihre Buchhaltungssoftware entsprechend anzupassen oder einen Steuerberater hinzuzuziehen, um eine korrekte Trennung zu gewährleisten. Verstöße gegen die Kassensicherungsverordnung (KassenSichV) oder das Fehlen von Kassenbons können ebenfalls Konsequenzen haben (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html) (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html)."
        }
        Einnahmen_hinweise = {
            "ja":"Wenn Sie alle Einnahmen aus Barzahlungen, Kartenzahlungen und Lieferdiensten vollständig erfassen, halten Sie sich an die gesetzlichen Vorgaben zur Steuertransparenz. Die Kassensicherungsverordnung (KassenSichV) verlangt, dass alle Zahlungen, ob in bar oder mit Karte, lückenlos und ohne Manipulation in einem zertifizierten, manipulationssicheren Kassensystem erfasst werden. Dies stellt sicher, dass alle Einnahmen dokumentiert und dem Finanzamt korrekt gemeldet werden können. Besonders wichtig ist die vollständige Erfassung, um die Belegausgabepflicht einzuhalten. Unabhängig von der Zahlungsart müssen Sie jedem Kunden einen Kassenbon oder eine Quittung ausstellen, um Transparenz über den getätigten Umsatz zu gewährleisten. Dies ist eine Voraussetzung, um die steuerlichen Anforderungen zu erfüllen, wie sie in den § 146a der Abgabenordnung und der Kassensicherungsverordnung geregelt sind (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html) (https://www.gesetze-im-internet.de/ao_1977/BJNR006130976.html). Eine ordnungsgemäße Buchhaltung und die vollständige Erfassung aller Zahlungen, inklusive Lieferdienste und Kartenzahlungen, sind auch für die korrekte Berechnung der Umsatzsteuer entscheidend. Die korrekte Abgrenzung zwischen den verschiedenen Steuersätzen für die Lieferung und den Verzehr vor Ort ist von zentraler Bedeutung (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html).",
            "nein":"Wenn Sie Speisen und Getränke nicht korrekt in Ihrer Buchhaltung trennen, kann dies zu Problemen bei der Steuerabrechnung führen. Da für Speisen grundsätzlich der ermäßigte Steuersatz von 7 % und für Getränke der volle Steuersatz von 19 % gilt, ist es wichtig, diese beiden Kategorien korrekt zu unterscheiden. Eine falsche Zuordnung kann dazu führen, dass das Finanzamt eine falsche Steuerberechnung vornimmt, was zu Nachzahlungen oder sogar Strafen führen kann. Für eine korrekte Buchführung sollten Sie sicherstellen, dass alle Einnahmen aus Speisen und Getränken in Ihrem Kassensystem oder Ihrer Buchhaltung eindeutig voneinander getrennt sind. Wenn Sie dies noch nicht tun, sollten Sie überlegen, entweder Ihre Buchhaltungssoftware entsprechend anzupassen oder einen Steuerberater hinzuzuziehen, um eine korrekte Trennung zu gewährleisten. Verstöße gegen die Kassensicherungsverordnung (KassenSichV) oder das Fehlen von Kassenbons können ebenfalls Konsequenzen haben (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html) (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html)."
        }
        Steuererklärungen_hinweise = {
            "ja":"Wenn Sie Ihre Steuererklärungen immer fristgerecht einreichen, erfüllen Sie eine wichtige gesetzliche Pflicht und vermeiden mögliche Strafen oder Verzugszinsen. Das Einhalten der Fristen stellt sicher, dass Ihre Steuerschuld korrekt berechnet und rechtzeitig beglichen wird. Steuerpflichtige, die die Abgabetermine einhalten, schützen sich vor zusätzlichen Kosten wie Verspätungszuschlägen und Zinsen. Es ist wichtig, alle erforderlichen Unterlagen vollständig und korrekt einzureichen, um spätere Rückfragen oder Nachforderungen des Finanzamtes zu vermeiden. Weitere Informationen zur Steuererklärung und den relevanten Fristen finden Sie in der Abgabenordnung (AO), die die allgemeinen Regeln für steuerliche Pflichten festlegt (https://www.gesetze-im-internet.de/ao_1977/BJNR006130976.html), sowie im Umsatzsteuergesetz (UStG), das die spezifischen Regelungen für die Umsatzsteuer und deren Meldung enthält (https://usth.bundesfinanzministerium.de/usth/2023/A-Umsatzsteuergesetz/inhalt.html).",
            "nein":"Wenn Sie Ihre Steuererklärungen nicht fristgerecht einreichen, müssen Sie mit möglichen Konsequenzen rechnen. Das Finanzamt kann Verspätungszuschläge erheben, die Ihre Steuerlast deutlich erhöhen. Darüber hinaus können Verzugszinsen anfallen, die zusätzlich zur ursprünglichen Steuerschuld bezahlt werden müssen. In wiederholten Fällen, in denen Steuererklärungen nicht fristgerecht eingereicht werden, kann das Finanzamt auch ein Zwangsgeld ansetzen, um die Einreichung der Erklärung zu erzwingen. Es wird daher empfohlen, bei wiederholten Versäumnissen rechtzeitig die Unterstützung eines Steuerberaters zu suchen. Dieser kann Ihnen helfen, die Steuererklärungen korrekt und fristgerecht nachzureichen. Wenn Sie Steuererklärungen verspätet einreichen, kann dies auch dazu führen, dass der Steuerbescheid später ergeht und zusätzliche Zahlungen erforderlich werden. Weitere Informationen zu den rechtlichen Konsequenzen und Strafen bei verspäteter Abgabe finden Sie in der Abgabenordnung (AO) (https://www.gesetze-im-internet.de/ao_1977/BJNR006130976.html) sowie zu den Verspätungszuschlägen und Strafen unter (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html)."
        }
        Nachforderungen_hinweise = {
            "ja":"Wenn Sie in den letzten zwei Jahren eine Umsatzsteuer-Nachforderung erhalten haben, bedeutet das, dass das Finanzamt festgestellt hat, dass Sie zu wenig Umsatzsteuer abgeführt haben. In diesem Fall müssen Sie den Differenzbetrag nachzahlen und darauf achten, die Zahlungsfristen einzuhalten, um Säumniszuschläge oder Zinsen zu vermeiden. Falls die Nachforderung aufgrund von Fehlern in Ihrer Umsatzsteuererklärung entstanden ist, können Sie diese nachträglich berichtigen. Ein Steuerberater kann hierbei helfen. Wichtig ist auch, dass Ihre Buchhaltung und Kassensysteme den Anforderungen der Kassensicherungsverordnung (KassenSichV) entsprechen, die eine manipulationssichere Erfassung aller Einnahmen vorschreibt (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Falls Sie Schwierigkeiten bei der Begleichung der Nachforderung haben, können Sie beim Finanzamt eine Ratenzahlung beantragen. Achten Sie auch darauf, dass Trinkgelder korrekt erfasst werden, da diese steuerfrei sind, wenn sie direkt an das Personal gehen (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html).",
            "nein":"Wenn Sie in den letzten zwei Jahren keine Umsatzsteuer-Nachforderungen erhalten haben, ist dies ein gutes Zeichen dafür, dass Ihre steuerlichen Angelegenheiten gut organisiert sind. Um auch in Zukunft Probleme zu vermeiden, sollten Sie weiterhin sicherstellen, dass alle Umsatzsteuererklärungen korrekt abgegeben werden. Achten Sie darauf, dass Sie Belege für jede Transaktion ausstellen und die Belegausgabepflicht erfüllen (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html). Stellen Sie außerdem sicher, dass Ihre Kassensysteme den Vorgaben der Kassensicherungsverordnung (KassenSichV) entsprechen, um eine korrekte Erfassung der Einnahmen und Ausgaben sicherzustellen. So vermeiden Sie mögliche steuerliche Probleme bei einer späteren Betriebsprüfung (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Falls Sie unsicher sind, können Sie einen Steuerberater hinzuziehen, um Fehler zu vermeiden und Ihre steuerlichen Pflichten genau zu prüfen."
        }
        Trinkgelder_hinweise = {
            "ja":"Wenn Trinkgelder gemäß den steuerlichen Vorgaben dokumentiert werden müssen, müssen Sie sicherstellen, dass alle Trinkgelder korrekt erfasst und dokumentiert werden. Grundsätzlich sind Trinkgelder steuerfrei, wenn sie direkt und freiwillig vom Gast an die Mitarbeiter übergeben werden. Diese Trinkgelder müssen jedoch korrekt in der Buchhaltung und gegebenenfalls in der Lohnabrechnung berücksichtigt werden, besonders wenn sie über ein Kassensystem abgewickelt werden. Wenn Trinkgelder über das Kassensystem erfasst werden, etwa in einem Pool oder als Teil eines Servicezuschlags, gelten diese Trinkgelder als Betriebseinnahmen und müssen in der Buchhaltung als solche verbucht werden. In diesem Fall unterliegen die Trinkgelder der Umsatzsteuer und müssen in der Umsatzsteuererklärung berücksichtigt werden. Es ist wichtig, dass alle relevanten Belege und Nachweise aufbewahrt werden, um im Falle einer Steuerprüfung alle Einnahmen, einschließlich der Trinkgelder, nachweisen zu können. Die Kassensicherungsverordnung (KassenSichV) fordert, dass alle Einnahmen, auch Trinkgelder, ordnungsgemäß dokumentiert werden, wenn sie über das Kassensystem abgewickelt werden. Dies bedeutet, dass Sie bei der Verwendung eines Kassensystems sicherstellen müssen, dass alle Trinkgelder entsprechend der gesetzlichen Vorgaben erfasst und die Einnahmen korrekt verbucht werden (Kassensicherungsverordnung (KassenSichV)). Wenn Trinkgelder an Mitarbeiter weitergegeben werden, müssen diese in der Lohnabrechnung korrekt ausgewiesen werden, wenn sie aus einem Pool stammen oder als Teil des Gehalts behandelt werden. Auch wenn Trinkgelder steuerfrei sind, müssen sie ordnungsgemäß dokumentiert und in den Lohnabrechnungen berücksichtigt werden. Weitere Informationen zu den steuerlichen Regelungen zu Trinkgeldern finden Sie hier: Trinkgeldregelungen und Steuerfreiheit. Zudem müssen Sie die gesetzlichen Bestimmungen zur Belegausgabepflicht einhalten, die auch für Trinkgelder relevant sein kann, wenn sie über das Kassensystem erfasst werden. Weitere Details zur Belegausgabepflicht finden Sie auf der Webseite des Bundesministeriums der Finanzen: Belegausgabepflicht FAQ.",
            "nein":"Wenn Sie Trinkgelder nicht dokumentieren müssen, bezieht sich dies meist auf Fälle, in denen Trinkgelder direkt und freiwillig vom Gast an die Mitarbeiter gegeben werden, ohne dass diese über das Kassensystem oder die Buchhaltung des Unternehmens laufen. In diesem Fall gelten Trinkgelder als steuerfreie Einkünfte für die Mitarbeiter und müssen nicht in der Buchhaltung des Unternehmens erfasst werden. Es besteht keine Pflicht zur Dokumentation dieser Trinkgelder in den Steuererklärungen, solange sie nicht über das Kassensystem oder auf andere Weise in das Unternehmen integriert werden. Diese Trinkgelder unterliegen nicht der Umsatzsteuer und müssen nicht in der Umsatzsteuererklärung des Unternehmens berücksichtigt werden. Sie sind nur dann steuerpflichtig, wenn sie über das Kassensystem laufen oder als Teil eines Servicezuschlags in der Rechnung enthalten sind. Es ist daher wichtig zu verstehen, dass Trinkgelder, die direkt an die Mitarbeiter gegeben werden, als persönliche Zuwendung des Gastes gelten, die nicht der Umsatzsteuer unterliegt. Weitere Informationen finden Sie dazu im Umsatzsteuergesetz (UStG): Umsatzsteuergesetz (UStG). Auch wenn Trinkgelder nicht dokumentiert werden müssen, bleibt die Pflicht zur ordnungsgemäßen Nutzung eines Kassensystems bestehen. Die Kassensicherungsverordnung (KassenSichV) verlangt, dass alle Einnahmen, auch Trinkgelder, korrekt erfasst werden, wenn diese über das Kassensystem laufen. Daher sollten Sie sicherstellen, dass Sie alle gesetzlichen Anforderungen an Ihre Kassenführung einhalten, auch wenn die Trinkgelder nicht dokumentiert werden müssen (Kassensicherungsverordnung (KassenSichV)). Falls Trinkgelder in einem Pool gesammelt und unter den Mitarbeitern aufgeteilt werden, müssen diese korrekt in der Lohnbuchhaltung angegeben werden. In solchen Fällen müssen sie ebenfalls dokumentiert werden, da sie als Einnahmen gelten und in die Lohnabrechnung aufgenommen werden müssen. Weitere Informationen zur Steuerfreiheit von Trinkgeldern und den entsprechenden Regelungen finden Sie auf der Seite der VLH Trinkgeldregelungen."
        }
        Schulung_hinweise = {
            "ja":"Wenn Ihre Mitarbeitenden regelmäßig zu steuerlichen Vorgaben geschult werden, ist das ein sehr positiver Schritt, um sicherzustellen, dass alle relevanten Vorschriften eingehalten werden. Die regelmäßige Schulung hilft, Fehler zu vermeiden, die durch Unwissenheit oder Missverständnisse bei der Anwendung der Kassensicherungsverordnung (KassenSichV), der Trinkgeldregelung und anderen steuerlichen Anforderungen entstehen können. Ein wichtiger Bestandteil der Schulung sollte das Kassensystem und die Belegausgabepflicht sein. Mitarbeitende müssen wissen, dass alle Transaktionen korrekt in einem manipulationssicheren Kassensystem erfasst werden müssen. Dies ist durch die Kassensicherungsverordnung (KassenSichV) vorgeschrieben, die für Gastronomiebetriebe, einschließlich Restaurants, Cafés, Bars, Imbisse und Hotels, gilt. Das System sollte alle Buchungen digital und revisionssicher speichern, um Steuerhinterziehung zu verhindern. Die Belegausgabepflicht erfordert, dass jedem Kunden ein Kassenbon ausgestellt wird, unabhängig davon, ob der Kunde diesen tatsächlich mitnimmt oder nicht. Schulungen helfen sicherzustellen, dass alle Mitarbeitenden den gesetzlichen Anforderungen folgen (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Zusätzlich sollten Mitarbeitende über die Trinkgeldregelung informiert sein. Trinkgelder sind grundsätzlich steuerfrei, wenn sie direkt vom Gast an das Personal gegeben werden. Werden die Trinkgelder jedoch über das Kassensystem verwaltet oder an das Team verteilt, müssen sie steuerlich korrekt behandelt werden. Eine ordnungsgemäße Dokumentation ist entscheidend, um steuerliche und rechtliche Probleme zu vermeiden (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html).",
            "nein":"Wenn Ihre Mitarbeitenden noch nicht regelmäßig zu den steuerlichen Vorgaben geschult werden, könnte dies langfristig zu Problemen führen, insbesondere in Bezug auf die Einhaltung gesetzlicher Anforderungen. Insbesondere die Kassensicherungsverordnung (KassenSichV) und die Belegausgabepflicht müssen genau beachtet werden. Das Fehlen einer Schulung kann dazu führen, dass Transaktionen nicht korrekt erfasst werden, was das Risiko von Steuerhinterziehung oder Fehlern bei der Umsatzsteuermeldung erhöht. Die Kassensicherungsverordnung (KassenSichV) schreibt vor, dass alle Transaktionen in einem manipulationssicheren Kassensystem erfasst und digital gespeichert werden müssen. Ein nicht manipulierbares System schützt sowohl den Betrieb als auch die Mitarbeitenden vor rechtlichen Konsequenzen (https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html). Außerdem müssen alle Mitarbeitenden die Belegausgabepflicht verstehen und umsetzen. Jeder Kunde muss einen Beleg erhalten, auch wenn er diesen nicht mitnimmt. Das kann zu Strafen führen, wenn es bei den Aufzeichnungen oder der Bon-Ausgabe Versäumnisse gibt (https://www.bundesfinanzministerium.de/Content/DE/FAQ/FAQ-steuergerechtigkeitbelegpflicht.html). Zudem ist es wichtig, dass Ihre Mitarbeitenden die Trinkgeldregelung verstehen. Trinkgelder, die direkt vom Gast an die Mitarbeitenden gegeben werden, sind grundsätzlich steuerfrei. Werden Trinkgelder jedoch über das Kassensystem verwaltet oder verteilt, muss die steuerliche Behandlung korrekt erfolgen (https://www.vlh.de/arbeiten-pendeln/beruf/trinkgeld-ist-nicht-immer-steuerfrei.html). Es wird empfohlen, eine regelmäßige Schulung durchzuführen, um sicherzustellen, dass alle Mitarbeitenden über aktuelle steuerliche Regelungen informiert sind und Fehler in der täglichen Praxis vermieden werden."
        }
        # story füllen
        story.append(Paragraph(f"1. Gastronomiebetrieb: {betrieb}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(betrieb_hinweise.get(betrieb, ""), blocksatz_style))
        story.append(Spacer(1, 10))  

        story.append(Paragraph(f"2. TSE-Anforderungen: {TSE}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(TSE_hinweise.get(TSE, ""), blocksatz_style))
        story.append(Spacer(1, 10))  

        story.append(Paragraph(f"3. Belegausgabe: {Beleg}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(Beleg_hinweise.get(Beleg, ""), blocksatz_style))
        story.append(Spacer(1, 10))  

        story.append(Paragraph(f"4. Kassenprüfung: {Pruefung}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(Pruefung_hinweise.get(Pruefung, ""), blocksatz_style))
        story.append(Spacer(1, 10))  

        story.append(Paragraph(f"5. Trennung in der Buchhaltung: {Trennung}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(Trennung_hinweise.get(Trennung, ""), blocksatz_style))
        story.append(Spacer(1, 10))  

        story.append(Paragraph(f"6. Vollständige Erfassung der Einnahmen: {Einnahmen}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(Einnahmen_hinweise.get(Einnahmen, ""), blocksatz_style))
        story.append(Spacer(1, 10))  

        story.append(Paragraph(f"7. fristgerechte einreichung der Steuererklärung: {Steuererklärungen}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(Steuererklärungen_hinweise.get(Steuererklärungen, ""), blocksatz_style))
        story.append(Spacer(1, 10))  

        story.append(Paragraph(f"8. Umsatzsteuer-Nachforderungen innerhalb der letzten 2 Jahre erhalten: {Nachforderungen}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(Nachforderungen_hinweise.get(Nachforderungen, ""), blocksatz_style))
        story.append(Spacer(1, 10))  

        story.append(Paragraph(f"9. Dokumentation von Trinkgeldern gemäß steuerlichen Vorgaben: {Trinkgelder}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(Trinkgelder_hinweise.get(Trinkgelder, ""), blocksatz_style))
        story.append(Spacer(1, 10))  

        story.append(Paragraph(f"10. Schulung der Mitarbeiter: {Schulung}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(Schulung_hinweise.get(Schulung, ""), blocksatz_style))
        story.append(PageBreak())

    def _add_ausfuehrlich_sections(self, form, story, h2_style, blocksatz_style):
        
        betrieb = form.get('betrieb')
        standort_zahl = form.get('standort_zahl')
        mitarbeiter_zahl = form.get('mitarbeiter_zahl')
        jahresumsatz = form.get('jahresumsatz')
        trennung = form.get('trennung')
        kassensystem = form.get('kassensystem')
        kassensytem_prüfung = form.get('kassensytem_prüfung')
        tse1 = form.get('tse1')
        beleg = form.get('beleg')
        belegs_anforderungen = form.get('belegs_anforderungen')
        kassendaten = form.get('kassendaten')
        trennung_essen_trinken = form.get('trennung_essen_trinken')
        buchhaltungssystem = form.get('buchhaltungssystem')
        einnahme_erfassung = form.get('einnahme_erfassung')
        umsatzsteuer = form.get('umsatzsteuer')
        nachforderungen = form.get('nachforderungen')
        steuererklärungen = form.get('steuererklärungen')
        einkommensdokumentation = form.get('einkommensdokumentation')
        getrennte_steuersätze = form.get('getrennte_steuersätze')
        steuerprüfung = form.get('steuerprüfung')
        nachforderungsdokumentation = form.get('nachforderungsdokumentation')
        audits = form.get('audits')
        trinkgelder_dokumentation = form.get('trinkgelder_dokumentation')
        trinkgelder_steuer = form.get('trinkgelder_steuer')
        mitarbeiterschulungen = form.get('mitarbeiterschulungen')

        # für die behandlung von Integern
        if isinstance(mitarbeiter_zahl, int):
            if mitarbeiter_zahl <= 5:
                mitarbeiter_category = "1-5"
            elif 6 <= mitarbeiter_zahl <= 15:
                mitarbeiter_category = "6-15"
            else:
                mitarbeiter_category = "16+"
        else:
            mitarbeiter_category = mitarbeiter_zahl

        if isinstance(jahresumsatz, int):
            if jahresumsatz <= 50000:
                jahresumsatz_category = '0-50k'
            elif 50001 <= jahresumsatz <= 250000:
                jahresumsatz_category = '50k-250k'
            elif 250001 <= jahresumsatz <= 600000:
                jahresumsatz_category = '250k-600k'
            else:
                jahresumsatz_category = '600k+'
        else:
            jahresumsatz_category = jahresumsatz

        if isinstance(umsatzsteuer, int):
            if umsatzsteuer <= 100:
                umsatzsteuer_category = '0-100'
            elif 101 <= umsatzsteuer <= 500:
                umsatzsteuer_category = '101-500'
            elif 501 <= umsatzsteuer <= 2000:
                umsatzsteuer_category = '501-2000'
            elif 2001 <= umsatzsteuer <= 5000:
                umsatzsteuer_category = '2001-5000'
            else:
                umsatzsteuer_category = '5000+'
        else:
            umsatzsteuer_category = umsatzsteuer



        betrieb_hinweise = {
            "restaurant": "Für Restaurants gelten spezielle Regeln zur Kassensicherung. Sie müssen alle Umsätze genau dokumentieren, besonders wenn Sie Speisen und Getränke kombinieren. Gut zu wissen: Bei Speisen gilt ein reduzierter Mehrwertsteuersatz.[dehoga-nrw.de](https://www.dehoga-nrw.de/fachthemen/mehrwertsteuer-aenderungen-in-2024), [ihk.de](https://www.ihk.de/ostbrandenburg/zielgruppeneinstieg-gruender/hotellerie/existenzgruendung-im-gastgewerbe-2318136)",  
            "cafe": "In Cafés wird zwischen 'kalten' und 'warmen' Snacks unterschieden. Achten Sie darauf, Kaffee zum Mitnehmen und vor Ort getrennt zu buchen. Tipp: Für reine Kaffee-Verkäufe gelten einfachere Regeln. [ihk.de](https://www.ihk.de/ostbrandenburg/zielgruppeneinstieg-gruender/hotellerie/existenzgruendung-im-gastgewerbe-2318136)",       
            "bar":"Bei alkoholischen Getränken müssen Sie die gesetzlichen Ausweiskontrollen dokumentieren. Wichtig: Notieren Sie Sonderaktionen wie Happy Hour genau, da diese steuerlich relevant sind. [bundesfinanzministerium.de](https://www.bundesfinanzministerium.de/Content/DE/Glossareintraege/A/alkoholsteuer.html?view=renderHelp), [ihk.de](https://www.ihk.de/ostbrandenburg/zielgruppeneinstieg-gruender/hotellerie/existenzgruendung-im-gastgewerbe-2318136)",
            "imbiss":"Für Imbissbetriebe ist die Bonpflicht auch bei kleinen Beträgen wichtig. Einfacher Tipp: Nutzen Sie ein Kassensystem mit täglicher Umsatzübersicht für weniger Papierkram. [dross.blog](https://dross.blog/ueber-uns/leitfaden-fuer-die-eroeffnung-eines-imbissbetriebs/), [amberg.de](https://amberg.de/fileadmin/Ordnungsamt/Imbisswaegen_und_Imbissbetriebe_Merkblatt.pdf), [ihk.de](https://www.ihk.de/ostbrandenburg/zielgruppeneinstieg-gruender/hotellerie/existenzgruendung-im-gastgewerbe-2318136)",
            "catering":"Catering-Dienstleistungen müssen immer mit Rechnungen dokumentiert werden. Merken: Auch Fahrtkosten und Verpackungen gehören in die Steuerunterlagen. [catering-nimmersatt.de](https://www.catering-nimmersatt.de/blogs/guides/mehrwertsteuer-catering?srsltid=AfmBOoo927rwbyBLi8hwZbc7CR4fA80pmblN-xj_j8_5sHqqaVeUBCHA), [ihk.de](https://www.ihk.de/ostbrandenburg/zielgruppeneinstieg-gruender/hotellerie/existenzgruendung-im-gastgewerbe-2318136)",
            "hotel":"Trennen Sie genau zwischen Übernachtungs- und Verpflegungsumsätzen. Praktisch: Frühstück für Hotelgäste hat andere Steuerregeln als externe Restaurantgäste. [ihk.de](https://www.ihk.de/schwerin/standort-westmecklenburg/tourismus-und-gastgewerbe/rechtsfragen/steuersaetze-in-gastronomie-und-hotellerie-4835520), [ihk.de](https://www.ihk.de/ostbrandenburg/zielgruppeneinstieg-gruender/hotellerie/existenzgruendung-im-gastgewerbe-2318136)",
            "sonstiges":"Lassen Sie sich individuell beraten, da Sonderformen besondere Regeln haben können. Wichtig: Dokumentieren Sie alle Einnahmequellen genau. [ihk.de](https://www.ihk.de/ostbrandenburg/zielgruppeneinstieg-gruender/hotellerie/existenzgruendung-im-gastgewerbe-2318136)"
        }

        standort_zahl_hinweise = {
            "1":"Mit einem Standort haben Sie einfachere Steuerunterlagen. Sie müssen nur eine monatliche Umsatzsteuervoranmeldung machen.",
            "2":"Bei zwei Standorten müssen Sie für jeden separat Buch führen. Gut zu wissen: Sie können die Steuererklärung aber zusammengefasst abgeben.",
            "3-5":"Ab 3 Standorten empfiehlt sich eine digitale Buchhaltung. Wichtig: Prüfen Sie ob Sie für jeden Standort eine separate Gewerbeanmeldung brauchen.",
            "Mehr als 5":"Für mehrere Standorte benötigen Sie professionelle Buchhaltungssoftware. Tipp: Lassen Sie sich zur Gruppierungsoption bei der Umsatzsteuer beraten."
        }

        mitarbeiter_zahl_hinweise = {
            "1-5":"Kleine Teams profitieren von Pauschalbesteuerung bei Minijobbern. Dokumentieren Sie klar zwischen Festangestellten und Saisonhilfen.",
            "6-15":"Ab 6 Mitarbeitern wird monatliche Lohnsteueranmeldung pflichtig. Führen Sie getrennte Aufzeichnungen für Vollzeit/Teilzeit/Aushilfen. [elster.de](https://www.elster.de/eportal/start)",
            "16+":"Großbetriebe müssen elektronische Lohnsteueranmeldungen abgeben. Beachten Sie die Dokumentationspflichten nach Mindestlohngesetz und Arbeitszeitverordnung. [ihk.de](https://www.ihk.de/koblenz/unternehmensservice/recht/arbeitsrecht/mindestlohn-minijob-und-aushilfen/aufzeichnungspflichten-nach-dem-mindestlohngesetz-1478366)"
        }

        jahresumsatz_hinweise = {
            "0-50k":"Kleinunternehmerregelung möglich - Verzicht auf Umsatzsteuererhebung bei entsprechendem Antrag. Jährliche EÜR ausreichend. (https://www.ihk.de/stuttgart/fuer-unternehmen/recht-und-steuern/steuerrecht/umsatzsteuer-verbrauchssteuer/umsatzsteuer-national/kleinunternehmerregelung-in-der-umsatzsteuer-1843632)",
            "50k-250k":"Monatliche Umsatzsteuervoranmeldungen erforderlich. Quartalsweise Gewinnermittlung empfohlen.[accountable.de](https://www.accountable.de/blog/umsatzsteuervoranmeldung-elster/), [elster.de](https://www.elster.de/eportal/formulare-leistungen/alleformulare/ustvaeru)",
            "250k-600k":"Verpflichtung zur doppelten Buchführung. Einrichtung eines steuerlichen Beraterkontos für Vorsteuerabzug empfohlen.[gruenderplattform.de](https://gruenderplattform.de/unternehmen-gruenden/doppelte-buchfuehrung)",
            "600k+":"Automatische Einstufung als Großbetrieb mit täglicher Kassendifferenzmeldung. Externes Jahresaudit empfohlen. [ihk.de](https://www.ihk.de/berlin/service-und-beratung/recht-und-steuern/kaufmaennische-pflichten/veroeffentlichungs-offenlegungs-bekanntmachungspflichten-4336858)"
        }

        trennung_hinweise = {
            "0-25 %":"Geringe Barzahlungen bedeuten weniger Kontrollrisiko. Trotzdem wichtig: Bewahren Sie alle Kartenzahlungsbelege und Online-Buchungsbestätigungen auf. [gesetze-im-internet.de](https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html), [kassensichv.com](https://kassensichv.com), ",
            "26-50 %":"Documentieren Sie Barzahlungen besonders sorgfältig. Praktisch: Führen Sie ein Tageskassenbuch mit Unterschrift der Schichtverantwortlichen. [ready2order.com](https://ready2order.com/de/post/belegausgabepflicht/)",
            "51-75 %":"Bei hohen Barumsätzen sind Registrierkassen mit Speicherfunktion Pflicht. Tipp: Machen Sie tägliche Kassenstürze und notieren Sie Abweichungen sofort.",
            "Über 75%":"Sehr hohe Barumsätze werden vom Finanzamt besonders geprüft. Wichtig: Verwenden Sie ein zertifiziertes Kassensystem und lagern Sie Bons 10 Jahre. [ready2order.com](https://ready2order.com/de/post/belegausgabepflicht/)"
        }

        kassensystem_hinweise = {
            "Ja, für alle Standorte":"Super! Damit erfüllen Sie die gesetzlichen Vorgaben. Wichtig: Stellen Sie sicher, dass alle Kassen regelmäßig Updates erhalten. [kassensichv.com](https://kassensichv.com)",
            "Teilweise":"Achtung: Nicht konforme Kassen können Strafen nach sich ziehen. Tipp: Rüsten Sie alle Standorte innerhalb von 3 Monaten nach. [ihk.de](https://www.ihk.de/bayreuth/hauptnavigation/service/steuern/aktuelle-steuerinfos/steuermeldungen-news/letzte-frist-jetzt-unbedingt-die-kasse-nachruesten-4726124)",
            "Nein":"Das ist gesetzlich Pflicht! Handeln Sie schnell: Einfache Systeme gibt es schon ab 200€. Vermeiden Sie sonst hohe Nachzahlungen. [heimpel.com](https://www.heimpel.com/kassensysteme-strafen-bussgelder-sanktionen)"
        }

        kassensytem_prüfung_hinweise = {
            "Innerhalb der letzen 12 Monate":"Gut gemacht! Planen Sie die nächste Prüfung spätestens in 10 Monaten. Merken: Protokolle 5 Jahre aufbewahren. [BZSt.de](https://www.bzst.de/DE/Home/home_node.html)",
            "Vor mehr als 12 Monaten":"Das Risiko steigt - alte Systeme haben oft Sicherheitslücken. Tipp: Lassen Sie die Kasse innerhalb von 4 Wochen checken. [tuvit.de](https://www.tuvit.de/de/tuevit/elektronische-kassensysteme/)",
            "Nie":"Sehr riskant! Ohne Prüfung sind Strafen bis 25.000€ möglich. Dringend: Beauftragen Sie umgehend einen Fachbetrieb. [gesetze-im-internet.de ](https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html)"
        }

        tse1_hinweise = {
            "Ja":"Perfekt! Die TSE macht Ihre Kasse fälschungssicher. Einfacher Tipp: Kontrollieren Sie monatlich das TSE-Siegel. [bsi.bund.de](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Zertifizierung-und-Anerkennung/Listen/Zertifizierte-Produkte-nach-TR/Technische_Sicherheitseinrichtungen/TSE_node.html)",
            "Nein":"Das ist seit 2020 Pflicht! Handeln Sie jetzt: Nachrüstkits gibt es ab 150€. Sonst drohen Bußgelder.",
            "Unsicher":"Checken Sie das schnell: Öffnen Sie die Kasse - steht dort 'TSE' oder ein grünes Zertifikat? Wenn nein: Techniker rufen. [fiskaly.com](https://www.fiskaly.com/de/blog/fiskalcheck)"
        }

        beleg_hinweise = {
            "Ja immer":"Richtig so! Jeder Kunde muss einen Beleg erhalten. Praktisch: Hängen Sie einen Hinweis 'Bitte nehmen Sie Ihren Bon' sichtbar auf. [ready2order.com](https://ready2order.com/de/post/belegausgabepflicht/), [gesetze-im-internet.de](https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html)",
            "Teilweise":"Vorsicht: Fehlende Belege können als Steuerhinterziehung gewertet werden. Einfache Lösung: Kassensystem mit automatischer Bon-Ausgabe. [ready2order.com](https://ready2order.com/de/post/belegausgabepflicht/), [gesetze-im-internet.de](https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html",
            "Nein":"Das ist illegal! Sofort ändern: Nutzen Sie Notizblöcke, bis ein Kassensystem vorhanden ist. Bons müssen 10 Jahre archiviert werden. [bzst.de](https://www.bzst.de/DE/Unternehmen/Umsatzsteuer/ZusammenfassendeMeldung/Downloadbereich/downloadbereich_node.html), [ready2order.com](https://ready2order.com/de/post/belegausgabepflicht/), [gesetze-im-internet.de](https://www.gesetze-im-internet.de/kassensichv/BJNR351500017.html)"
        }
    
        belegs_anforderungen_hinweise = {
            "Ja":"Top! Ihre Belege müssen enthalten: Datum, Uhrzeit, Steuerbeträge und eine fortlaufende Nummer. Kontrollieren Sie das monatlich. [bundesfinanzministerium.de](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/2024-12-06-anpassung-vordruckmuster.html)",
            "Teilweise":"Überprüfen Sie Beispielbelege: Fehlen MwSt-Aufschlüsselung oder Firmenadresse? Dann nachbessern! Vorlagen gibt es online. [datev.de](https://www.datev.de/web/de/datev-shop/betriebliches-rechnungswesen/belege-online/)",
            "Nein":"Gefährlich! Ungültige Belege = Kein Nachweis fürs Finanzamt. Sofortmaßnahme: Lassen Sie Belegvorlagen von einem Steuerberater prüfen. [jochen-muth.de](http://www.jochen-muth.de/mandatsvermittlung.html)"
        }

        kassendaten_hinweise = {
            "Täglich":"Perfekt! Sichern Sie zusätzlich wöchentlich auf einer externen Festplatte. Einfacher Trick: Erinnerung im Kalender einstellen. [datev.de](https://www.datev.de/web/de/m/presse/im-fokus/themenreihen/kasse/kassendaten-sicher-archivieren-und-automatisiert-verarbeiten/), [comwer.de](https://www.comwer.de/Backup-Touch-Modelle.pdf)",
            "Wöchentlich":"Okay, aber riskant bei Stromausfällen. Besser: Cloud-Backup einrichten (kostet oft weniger als 10€/Monat). [datev.de](https://www.datev.de/web/de/m/presse/im-fokus/themenreihen/kasse/kassendaten-sicher-archivieren-und-automatisiert-verarbeiten/), [comwer.de](https://www.comwer.de/Backup-Touch-Modelle.pdf)",
            "Monatlich":"Zu lang! Bei Datenverlust müssen Sie alle Umsätze schätzen lassen. Mindestens: Wöchentliche Sicherung + Papierprotokolle. [datev.de](https://www.datev.de/web/de/m/presse/im-fokus/themenreihen/kasse/kassendaten-sicher-archivieren-und-automatisiert-verarbeiten/), [comwer.de](https://www.comwer.de/Backup-Touch-Modelle.pdf)",
            "Nicht regelmäßig":"Extrem riskant! Ohne Daten haben Sie keine Beweise bei Prüfungen. Starten Sie heute: Automatische Sicherung einrichten. [datev.de](https://www.datev.de/web/de/m/presse/im-fokus/themenreihen/kasse/kassendaten-sicher-archivieren-und-automatisiert-verarbeiten/), [comwer.de](https://www.comwer.de/Backup-Touch-Modelle.pdf)"
        }

        trennung_essen_trinken_hinweise = {
            "Ja":"Wichtig für die Steuer! Beispiel: Ein Kaffee zum Mitnehmen ist 19%, ein belegtes Brötchen 7%. Kontrollieren Sie wöchentlich die Buchung. [lexware.de](https://www.lexware.de/wissen/buchhaltung-finanzen/mehrwertsteuer-gastronomie/)",
            "Teilweise":"Vorsicht: Falsche Trennung führt zu Nachzahlungen. Einfache Hilfe: Farbige Etiketten für Speisen/Getränke an der Kasse. [datev.de](https://www.datev.de/dnlexom/v2/content/files/st9007200705405451_de.pdf)",
            "Nein":"Pauschale 19%-Besteuerung ist illegal. Sofort ändern: Lassen Sie sich vom Lieferanten die MwSt-Sätze der Produkte bestätigen."
        }

        buchhaltungssystem_hinweise = {
            "Ja, vollständig integriert":"Optimal! Automatische Steuerberechnung spart Zeit. Tipp: Exportieren Sie monatlich eine PDF-Übersicht fürs Finanzamt. [datev.de](https://www.datev.de/web/de/marktplatz/datev-schnittstellen-anbieter/)",
            "Teilweise digital":"Fehlerquelle! Nutzen Sie Apps wie Lexoffice oder SevDesk - die übernehmen sogar Foto-Belegeinsendungen. Papierbelege müssen gescannt und indexiert werden (§147 AO). Digitalisieren Sie binnen 6 Monaten vollständig. [ao.bundesfinanzministerium.de](https://ao.bundesfinanzministerium.de/ao/2021/Anhaenge/BMF-Schreiben-und-gleichlautende-Laendererlasse/Anhang-64/anhang-64.html)",
            "Nein, rein manuell":"Sehr fehleranfällig! Starten Sie mit kostenlosen Tools wie Wave Apps. Manuelle Buchungen dauern 3x länger!. Förderungen möglich. [foerderdatenbank.de](https://www.foerderdatenbank.de/FDB/Content/DE/Foerderprogramm/Bund/BMWi/digitalisierung-go-digital-bund.html)"
        }

        einnahme_erfassung_hinweise = {
            "Ja, vollständig":"Perfekt! Trennen Sie z.B. Lieferando, Bar und EC. Einfacher Check: Monatliche Abgleich mit Bankauszügen.",
            "Teilweise":"Problem: Unklare Quellen = Streit mit dem Finanzamt. Lösung: Getrennte Kassen-Schubladen für Bar/Karte.",
            "Nein":"Riskant! Ohne Trennung drohen pauschale Schätzungen. Sofort starten: Notizbuch für tägliche Zahlungsarten anlegen."
        }
#fehlt
        umsatzsteuer_hinweise = {
            "0-100":"Ihre monatliche Umsatzsteuerzahlung ist sehr niedrig. Falls Sie unter die Kleinunternehmerregelung fallen, beachten Sie bitte, dass Sie nur dann von dieser Regelung profitieren können, wenn Ihr Umsatz bestimmte Grenzen nicht überschreitet. Überprüfen Sie Ihre Umsätze und Belege, um sicherzugehen, dass alles korrekt erfasst ist. [ihk.de](https://www.ihk.de/blueprint/servlet/resource/blob/4838596/b06a94ca4bdbe751162cbb5292ae1c8f/checkliste-umsatzsteuersenkung-ab-1-7-2020-data.pdf)",
            "101-500":"Ihre Umsatzsteuerzahlungen liegen im niedrigen Bereich. Dies könnte auf einen moderaten Umsatz hindeuten. Achten Sie darauf, dass alle steuerlichen Vorgaben eingehalten werden und alle Abzüge korrekt berücksichtigt sind. [ihk.de](https://www.ihk.de/blueprint/servlet/resource/blob/4838596/b06a94ca4bdbe751162cbb5292ae1c8f/checkliste-umsatzsteuersenkung-ab-1-7-2020-data.pdf)",
            "501-2000":"Die Höhe Ihrer monatlichen Umsatzsteuerzahlungen liegt im mittleren Bereich. Es ist sinnvoll, regelmäßig zu prüfen, ob alle Vorsteuerbeträge und Abzüge vollständig und korrekt erfasst sind. Bei Unklarheiten kann eine Beratung durch einen Steuerexperten hilfreich sein. [ihk.de](https://www.ihk.de/blueprint/servlet/resource/blob/4838596/b06a94ca4bdbe751162cbb5292ae1c8f/checkliste-umsatzsteuersenkung-ab-1-7-2020-data.pdf)",
            "2001-5000":"Ihre Umsatzsteuerzahlungen sind relativ hoch. Stellen Sie sicher, dass Sie alle steuerlichen Abzüge optimal nutzen und alle Vorsteuerbeträge korrekt verbucht haben. Eine professionelle steuerliche Beratung könnte hier Optimierungspotenzial aufdecken. [ihk.de](https://www.ihk.de/blueprint/servlet/resource/blob/4838596/b06a94ca4bdbe751162cbb5292ae1c8f/checkliste-umsatzsteuersenkung-ab-1-7-2020-data.pdf)",
            "5000+":"Bei solch hohen Umsatzsteuerzahlungen sollten Sie Ihre Buchhaltung besonders sorgfältig überprüfen. Achten Sie darauf, dass alle steuerlichen Regelungen eingehalten werden und alle Abzüge sowie Vorsteuern korrekt erfasst sind. Es ist ratsam, in diesem Fall einen erfahrenen Steuerberater hinzuzuziehen, um Optimierungsmöglichkeiten zu identifizieren. [ihk.de](https://www.ihk.de/blueprint/servlet/resource/blob/4838596/b06a94ca4bdbe751162cbb5292ae1c8f/checkliste-umsatzsteuersenkung-ab-1-7-2020-data.pdf)"
        }

        nachforderungen_hinweise = {
            "Ja":"Handeln Sie: Lassen Sie die letzten 3 Jahre prüfen. Oft liegt der Fehler in falsch zugeordneten Beträgen (z.B. Catering vs. normale Verkäufe). [bundesfinanzministerium.de](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Weitere_Steuerthemen/Abgabenordnung/AO-Anwendungserlass/2024-03-11-aenderung-gobd.html)",
            "Nein":"Weiter so! Dokumentieren Sie besonders Sonderaktionen (z.B. Events) - diese prüft das Finanzamt oft extra. [bundesfinanzministerium.de](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Weitere_Steuerthemen/Abgabenordnung/AO-Anwendungserlass/2024-03-11-aenderung-gobd.html)"
        }
    
        steuererklärungen_hinweise = {
            "Ja, immer":"Das spart Ärger und Verspätungsgebühren! Tipp: Legen Sie einen Ordner mit allen Fristen an (z.B. 10. Mai für Umsatzsteuer).",
            "Manchmal verspätet":"Vorsicht: Jeder verspätete Monat kann 25€ Strafe kosten. Einfacher Trick: Stellen Sie Handy-Erinnerungen 2 Wochen vor Abgabetermin ein.",
            "Oft verspätet":"Riskant! Das Finanzamt kann Schätzungen vornehmen. Sofort handeln: Beauftragen Sie einen Steuerhelfer für die Grundbuchhaltung."
        }

        einkommensdokumentation_hinweise = {
            "Ja":"Perfekt! Speichern Sie Kassenbons, Lieferando-Berichte und EC-Auszüge zusammen ab. Beispiel: Ein Monat = Ein Ordner.",
            "Teilweise":"Fehlende Belege = Verdacht auf Schwarzarbeit. Lösung: Machen Sie täglich ein Handy-Foto von allen Einnahmequellen.",
            "Nein":"Sehr gefährlich! Starten Sie heute: Notieren Sie zumindest Tagesendsummen in einem Kalender an der Kasse."
        }

        getrennte_steuersätze_hinweise = {
            "Ja":"Wichtig bei Lieferungen: Essen zum Mitnehmen hat 7%, Getränke immer 19%. Kontrollieren Sie wöchentlich die Kassen-Einstellungen.",
            "Teilweise":"Achtung: Falsche Sätze führen zu Nachzahlungen. Test: Bestellen Sie selbst online - steht die richtige MwSt auf dem Bon?",
            "Nein":"Das kann teuer werden! Sofort ändern: Lassen Sie Ihr Kassensystem mit Steuerberater-Beratung einrichten."
        }

        steuerprüfung_hinweise = {
            "Ja, mehrmals":"Seien Sie vorbereitet: Halten Sie alle Unterlagen der letzten 7 Jahre griffbereit. Tipp: Scannen Sie wichtige Dokumente ein.",
            "Ja, einmal":"Lernen Sie daraus: Heben Sie besonders Quittungen für Großgeräte (z.B. neue Kühltheke) 10 Jahre auf.",
            "Nein":"Trotzdem vorbereiten: Legen Sie einen Musterordner mit Kassenbons, Lieferscheinen und Bankauszügen für 2023 an."
        }

        nachforderungsdokumentation_hinweise = {
            "Detailliert im Buchhaltungssystem":"Optimal! Fügen Sie immer das Finanzamt-Schreiben als PDF hinzu. Beispiel: 'Nachforderung_2023-04_Steuerberater.pdf'",
            "Manuell in separaten Unterlagen":"Übergangslösung: Kleben Sie Briefe in einen Schnellhefter mit Datums-Stichworten. Besser: Digitalisieren mit Handy-Scanner-Apps.",
            "Keine Dokumentation":"Problem: Bei Wiederholungsfall drohen höhere Strafen. Sofort starten: Sammeln Sie alle Briefe in einer Schuhschachtel."
        }

        audits_hinweise = {
            "Ja, monatlich":"Top! Prüfen Sie dabei immer: Kassenabschlüsse, Belegnummern-Lücken und MwSt-Zuordnung. Protokoll hilft bei Prüfungen.",
            "Ja, jährlich":"Gut, aber riskant: Fehler fallen erst spät auf. Besser: Machen Sie zusätzlich Stichproben vor Quartalsenden.",
            "Nein":"Starten Sie mit 3-Monats-Checks: Vergleichen Sie Kassen-Tagesberichte mit Bankeinzügen. Dauert nur 10 Minuten pro Woche."
        }

        trinkgelder_dokumentation_hinweise = {
            "Ja, vollständig":"Wichtig für Sozialabgaben! Beispiel: Notieren Sie täglich Trinkgeldverteilung im Schichtbuch - wer bekam wieviel?",
            "Teilweise":"Vorsicht: Nicht erfasste Trinkgelder können als Lohnbetrug gelten. Einfache Lösung: Transparente Trinkgeldbox mit Protokollblatt.",
            "Nein":"Gesetzliche Pflicht! Sofort ändern: Führen Sie ein A4-Blatt an der Pinnwand, wo jede Schicht ihr Trinkgeld einträgt."
        }

        trinkgelder_steuer_hinweise = {
            "Ja":"Korrekt: Über die Kasse gezahlte Trinkgelder gehören ins Gehalt. Check: Steht im Lohnzettel ein separater Posten 'Trinkgeld'? ",
            "Nein":"Das ist illegal! Ändern Sie die Lohnabrechnungen sofort. Tipp: Bargeld-Trinkgelder sind steuerfrei, wenn direkt an Mitarbeiter",
            "Unsicher":"Kontrollieren Sie: Wenn Trinkgeld über die Kasse läuft (z.B. Kartenzahlung), muss es versteuert werden. Sonst nicht."
        }

        mitarbeiterschulungen_hinweise = {
            "Ja":"Super! Halten Sie Teilnehmerlisten mit Unterschriften bereit. Praxis-Tipp: Machen Sie jährlich ein Quiz zu Kassenregeln.",
            "Nein":"Riskant: Fehler von Mitarbeitern werden Ihnen angelastet. Starten Sie mit 20-Minuten-Einweisungen zu Bon-Pflicht und TSE. [ihk.de](https://www.ihk.de/bodensee-oberschwaben/weiterbildung/seminare-und-lhrgaenge/ihk-hoc-online-trainings-1943526)",
        }

        story.append(Paragraph(f"1. Gastronomiebetrieb: {betrieb}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(betrieb_hinweise.get(betrieb, ""), blocksatz_style))
        story.append(Spacer(1, 10))  

        story.append(Paragraph(f"2. standort_zahl: {standort_zahl}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(standort_zahl_hinweise.get(standort_zahl, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"3. mitarbeiter_zahl: {mitarbeiter_zahl}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(mitarbeiter_zahl_hinweise.get(mitarbeiter_category), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"4. jahresumsatz: {jahresumsatz}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(jahresumsatz_hinweise.get(jahresumsatz_category), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"5. trennung: {trennung}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(trennung_hinweise.get(trennung, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"6. kassensystem: {kassensystem}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(kassensystem_hinweise.get(kassensystem, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"7. kassensytem_prüfung: {kassensytem_prüfung}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(kassensytem_prüfung_hinweise.get(kassensytem_prüfung, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"8. tse1: {tse1}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(tse1_hinweise.get(tse1, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"9. beleg: {beleg}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(beleg_hinweise.get(beleg, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"10. belegs_anforderungen: {belegs_anforderungen}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(belegs_anforderungen_hinweise.get(belegs_anforderungen, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"11. kassendaten: {kassendaten}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(kassendaten_hinweise.get(kassendaten, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"12. trennung_essen_trinken: {trennung_essen_trinken}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(trennung_essen_trinken_hinweise.get(trennung_essen_trinken, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"13. buchhaltungssystem: {buchhaltungssystem}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(buchhaltungssystem_hinweise.get(buchhaltungssystem, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"14. einnahme_erfassung: {einnahme_erfassung}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(einnahme_erfassung_hinweise.get(einnahme_erfassung, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"15. umsatzsteuer: {umsatzsteuer}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(umsatzsteuer_hinweise.get(umsatzsteuer_category), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"16. nachforderungen: {nachforderungen}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(nachforderungen_hinweise.get(nachforderungen, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"17. steuererklärungen: {steuererklärungen}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(steuererklärungen_hinweise.get(steuererklärungen, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"18. einkommensdokumentation: {einkommensdokumentation}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(einkommensdokumentation_hinweise.get(einkommensdokumentation, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"19. getrennte_steuersätze: {getrennte_steuersätze}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(getrennte_steuersätze_hinweise.get(getrennte_steuersätze, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"20. steuererklärungen: {steuererklärungen}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(steuererklärungen_hinweise.get(steuererklärungen, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"21. steuerprüfung: {steuerprüfung}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(steuerprüfung_hinweise.get(steuerprüfung, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"22. nachforderungsdokumentation: {nachforderungsdokumentation}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(nachforderungsdokumentation_hinweise.get(nachforderungsdokumentation, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"23. audits: {audits}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(audits_hinweise.get(audits, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"24. trinkgelder_dokumentation: {trinkgelder_dokumentation}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(trinkgelder_dokumentation_hinweise.get(trinkgelder_dokumentation, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"25. trinkgelder_steuer: {trinkgelder_steuer}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(trinkgelder_steuer_hinweise.get(trinkgelder_steuer, ""), blocksatz_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph(f"26. mitarbeiterschulungen: {mitarbeiterschulungen}", h2_style))
        story.append(Spacer(1, 10))  
        story.append(Paragraph(mitarbeiterschulungen_hinweise.get(mitarbeiterschulungen, ""), blocksatz_style))
        story.append(PageBreak())