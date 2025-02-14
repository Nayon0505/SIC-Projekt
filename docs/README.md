# 1. Python Interpreter installieren
## Windows:
    Python von python.org installieren:
    Lade Python von python.org herunter und installiere es.

Öffne CMD und führe folgenden Befehl aus:

python -V
Es sollte die Python-Version angezeigt werden.
macOS:
## Python via Homebrew installieren:
Installiere Homebrew, falls noch nicht installiert, mit:

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Installiere Python mit:

brew install python3
Verifizierung:
Öffne Terminal und führe aus:
python3 -V
Die Python-Version sollte angezeigt werden.

# 3. Installiere Git
Folge den Anweisungen auf der Seite:
https://git-scm.com/book/de/v2/Erste-Schritte-Git-installieren

# 4. Visual Studio Code einrichten
Projektordner erstellen:
Erstelle einen Ordner für dein Projekt, z. B. /webapp.
Visual Studio Code installieren:
Lade Visual Studio Code von VS Code herunter und installiere es.
Erweiterungen installieren:
Installiere die Erweiterungen „Python“ und „Better Jinja“ über den Extension Marketplace.
Projektordner als Workspace öffnen:
Öffne den Ordner /webapp in VS Code als Workspace.

In VS Code, öffne das Terminal (strg, shift, ö) und kopiere das Repository mit:
git clone https://github.com/Nayon0505/SIC-Projekt.git


# 5. Virtuelle Umgebung erstellen und Packages installieren
Virtuelle Umgebung erstellen:

Öffne das Terminal und führe folgenden Befehl aus:
Windows:
python -m venv venv

macOS:
python3 -m venv venv


Aktiviere die virtuelle Umgebung und installiere die erforderliche Pakete:
Terminal:
pip install -r requirements.txt

# Flask run

Wir öffnen das Terminal und verwenden den Befehl:
flask run

Nun können wir in einem beliegen Browser unter der Webadresse: http://127.0.0.1:5000/
unsere App verwenden

(Falls die Datenbank nicht aktiv ist schreibe ins Terminal: flask init-db)

Es sei angemerkt, wir haben die Kommentare und das Debugging zur Bewertung drin gelassen um unsere Problemlösungsmethoden nachempfindbar zu machen.


### Quellen:

**Allgemein:**
Home (o. D.): Full-Stack Web Dev @HWR Berlin, [online] https://hwrberlin.github.io/fswd/.
(wir haben auch verlinkte Ressourcen verwendet)
Code with Josh (2024): Flask Full Course: Build stunning web Apps Fast | Python Flask Tutorial, [YouTube] https://www.youtube.com/watch?v=45P3xQPaYxc.
Matthes, Eric (2023): Python Crash Course, 3rd Edition: A Hands-On, Project-Based Introduction to Programming, No Starch Press.

**Bootstrap:**
Contributors, Mark Otto Jacob Thornton, And Bootstrap (o. D.): Link, [online] https://getbootstrap.com/docs/5.3/utilities/link/.
Bootswatch: Pulse (o. D.): [online] https://bootswatch.com/pulse/.

**Login:**
Arpan Neupane (2021): Python Flask Authentication Tutorial - Learn Flask Login, [YouTube] https://www.youtube.com/watch?v=71EU8gnZqZQ.
Utilities — Werkzeug Documentation (3.1.x) (o. D.): [online] https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.security.generate_password_hash. (passwort encrypting)
WTForms getting the errors (o. D.): Stack Overflow, [online] https://stackoverflow.com/questions/6463035/wtforms-getting-the-errors/20644520#20644520. (Error Messages)

**Docs**
Class diagrams | Mermaid (o. D.): [online] https://mermaid.js.org/syntax/classDiagram.html.

KI:
OpenAI (2024) ChatGPT (Version Feb 14). Verfügbar unter: https://chat.openai.com
(Wir haben ChatGPT zur Rechereche benutzt(z.B. suchen passender Librarys), Code Formatierung, Verstandnis, Fehlersuche bzw. um die Bedeutung von Fehlermeldungen zu verstehen)