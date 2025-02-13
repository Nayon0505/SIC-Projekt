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


Quellen:

https://www.youtube.com/watch?v=71EU8gnZqZQ Login
Packages: pip install flask flask_sqlalchemy flask_login flask_bcrypt flask_wtf wtforms email_validator
Bootstrap:
https://getbootstrap.com/docs/5.3/utilities/link/

Login:
https://stackoverflow.com/questions/6463035/wtforms-getting-the-errors/20644520#20644520 Error Messages
https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.security.generate_password_hash passwort encrypting
Bootswatch:
https://bootswatch.com/pulse/
