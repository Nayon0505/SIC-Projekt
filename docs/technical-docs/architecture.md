---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
Nayon Lenz

{: .no_toc }
# Architecture

<!-- {: .attention }
> This page describes how the application is structured and how important parts of the app work. It should give a new-joiner sufficient technical knowledge for contributing to the codebase.
> 
> See [this blog post](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) for an explanation of the concept and these examples:
>
> + <https://github.com/rust-lang/rust-analyzer/blob/master/docs/dev/architecture.md>
> + <https://github.com/Uriopass/Egregoria/blob/master/ARCHITECTURE.md>
> + <https://github.com/davish/obsidian-full-calendar/blob/main/src/README.md>
> 
> For structural and behavioral illustration, you might want to leverage [Mermaid](../ui-components.md), e.g., by charting common [C4](https://c4model.com/) or [UML](https://www.omg.org/spec/UML) diagrams.
> 
>
> You may delete this `attention` box. -->

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

Unsere App ermöglicht es dem Nutzer zwei Checks für deren Steuersituation auszuführen. Wir haben einen SchnellCheckForm, welcher ohne Anmeldung zugänglich ist und einen Ausführlichen Check, welcher eine Anmeldung benötigt. Sobald der Nutzer angemeldet ist, werden seine Checks in einer Datenbank gespeichert. Die Checks werden mit einem Punktesystem ausgewertet und mit einer Ampel bewertet (Rot, Schlecht; Gelb, Okay; Grün, Gut). Der Nutzer bekommt sein Ergebnis und hat die Möglichkeit sein Ergebnis als PDF herunterzuladen. Die PDF wird mithilfe der Nutzereingaben individuell erstellt. Ergebnisse (Nachhaltigkeitsberichte) werden in der Datenbank gespeichert und der Nutzer bekommt in einem Privaten Bereich die Möglichkeit frühere Checks einzusehen, herunterzuladen und zu löschen.

<!-- Die User Journey sieht wie folgt aus:

```mermaid
journey
    title SchnellCheckForm
    section Nicht angemeldet
      Check wählen: 6
      Check ausfüllen: 4
      Ergebnisse einholen: 3
    section Angemeldet
      Checks einsehen: 2
      Checks bearbeiten: 5
``` -->



<!-- [Give a high-level overview of what your app does and how it achieves it: similar to the value proposition, but targeted at a fellow developer who wishes to contribute.] -->

## Codemap

### 1. Datamodel
Alle Datenmodell-Klassen und Datenbankoperationen befinden sich in `db.py`:
- class User 
- class Report

### 2. Forms
Bearbeitung jeglicher Forms kann an folgenden Stellen vorgenommen werden:

`AusführlicherCheckForm.py`:
- class AusführlicherCheckForm1
- class AusführlicherCheckForm2
- class AusführlicherCheckForm3
- class AusführlicherCheckForm4
- class AusführlicherCheckForm5

`SchnellCheckForm.py`:
- class SchnellCheckForm

`db.py`:
- class RegisterForm
- class LoginForm

### Logik der Checks
Das Test Limit kann in app.py bestimt werden in der Variable "MAX_REPORTS_PER_USER"

**Schnellcheck:**
- `app.py`, app.route('schnelltest')
- `PDFGenerator.py`
- `CalculateResult.py`
**Ausführlicher Check:**
- `app.py`, app.route('ausführlicherTest')
- `PDFGenerator.py`
- `CalculateResult.py`

### Handhaben von Reports

**Generieren:**
- `PDFGernerator.py`

**Herunterladen:**
- `app.py`, app.route('/download/<'Filename'>'), (Direkt nach den Tests)
- `app.py`, @app.route('/download_pdf/<'int:report_id'>'), (In "Mein Bereich" von der Datenbank aus)

**Löschen**
- `app.py`, app.route('/deleteReport')

**Speichern in der Datenbank:**
- `app.py`, app.route('schnelltest')
- `app.py`, app.route('ausführlicherTest')

## Architecture Invariants

### 1. Trennung von Verantwortlichkeiten
- Alle datenbankbezogenen Operationen befinden sich in `db.py`.
- Formularlogik ist in separate Dateien ausgelagert, um Modularität und Wartbarkeit zu gewährleisten.
- Routen sind in `app.py` definiert und verweisen auf Hilfsklassen für Berechnungen, PDF-Erstellung und Datenbankoperationen.

### 2. State Management
- **Session Management:** Die Flask-Session wird verwendet, um Check-Daten und Status (Schnell oder Ausführlich) zwischen Routen zu speichern.
- **Datenbank:** Angemeldete Nutzer können ihre Berichte abrufen, da diese persistiert werden.

### 3. Fehlerbehandlung
- **Formulare:** Validierungslogik (z. B. maximale Berichte pro Nutzer) ist zentral in den Formular-Klassen definiert.
- **PDF-Fehler:** Falls bei der Generierung ein Fehler auftritt, wird dies dem Nutzer mit einer klaren Fehlermeldung angezeigt.


<!-- Unsere App läuft wie folgt ab:
### 1. Homepage
 Auf der Index Route (Die Startseite) bekommt der Nutzer einige Informationen und die Möglichkeit sich anzumelden, zu registrieren, den Schnelltest zu starten und unter der Bedingung, das er angemeldet ist den ausführlichen Test zu starten (Wenn nicht angemeldet wird er zum login weitergeleitet). Falls der Nutzer bereits angemeldet ist, kann er ebenfalls in der navbar zu "Mein Bereich" navigieren oder sich abmelden. 

### 2. Schnelltest
Der Nutzer wird sobald er den Schnelltest button drückt mit der Schnelltest Route, zum weitergeleitet. Falls der Nutzer angemeldet ist, wird gecheckt ob er das Limit an Tests pro Nutzer überschitten hat. Falls dies der Fall ist, wird eine Fehlermeldung geflashed und er wird zu "Mein Bereich" weitergeleitet um Tests zu löschen. Falls nicht, kommt er zum Test. Dort kann er den Schnelltest in form eines WTForms ausfüllen. Nachdem alles ausgefüllt ist und der Nutzer auf "Fertig" drückt, berechnet die Schnelltest Route das Ergebnis mit einem Punktesystem und gibt eine Ampelfarbe aus. Zudem werden die Testart (Ausfürhlich/Schnell), die Formulardaten, die Ampelfarbe in einer Session gespeichert. Eine PDF wird generiert mit der generate_pdf Methode aus der PDFGenerator Klasse. Das alles wird an die Route "Result" übergeben.
Falls der nutzer angemeldet ist, wird die Testart, die PDF und das Datum in die "db.sqlite" Datenbank eingefügt mit der Parent Id vom derzeitigen Nutzer (Die PDFs werden dem Nutzer zugeschrieben). Dann wird der Nutzer ebenfalls zu "Result" weitergeleitet.

### 3. Login und Registrierung
Das Login/Register System ist sehr simpel gehalten. Mit den Routes "login" und "register" kommt man zu einer Seite mit jeweils einem WTForm und die Logik der Forms ist in db.py definiert. Wir verwenden Flasks "LoginManager" um alles zu handhaben
**Registrieren**: Der Nutzer muss Nutzernamen, Passwort und Passwort bestätigen als input eingeben. Das ist selbsterklärend. Der Nutzername darf nicht vergeben sein, die Passwörter müssen übereinstimmen und beides muss eine bestimmte Buchstabenlänge haben. Die Logik ist in der "validate..." Methode der db.RegisterForm Klasse definiert. Wenn alles stimmt, wird der Nutzer in die Datenbank eingetragen.
**Login**:

### Ausführlicher Test

### Mein Bereich -->

[Describe how your app is structured. Don't aim for completeness, rather describe *just* the most important parts.]

## Cross-cutting concerns

Die Tests sind in zwei aufgeiteilt (Schnell/Ausführlich) und während der Schnelle aus einem Formular besteht, ist der zweite aus mehreren Formularen. Die Daten werden zwischen gespeichert mit `flask_session`. Wir verwenden Schritte in ``app.py`` um darzustellen bei welchem Formular wir uns derzeit befinden.


[Describe anything that is important for a solid understanding of your codebase. Most likely, you want to explain the behavior of (parts of) your application. In this section, you may also link to important [design decisions](../design-decisions.md).]
