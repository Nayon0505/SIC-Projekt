---
title: Design Decisions
nav_order: 3
---

{: .label }
Anil Öker, Nayon Lenz

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: Standart SQL oder SQLAlechemy

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 04-12-2024

### Problem statement

Wir müssen Nutzerdaten, sowie unsere Fragebögen und Nachhaltigkeitsberichte in einer Datenbank speichern. Wir haben nun die Wahl zwischen standart SQL oder SQLAlchemy. SQL würde uns einfacher fallen, da wir schon einige Kenntnisse haben, jedoch wäre für später geplanter Ausbau der Applikation SQLAlchemy besser.
<!-- [Describe the problem to be solved or the goal to be achieved. Include relevant context information.] -->

### Decision

Wir entschieden uns für SQLAlchemy um der zukünftigen Notwendigkeit einer komplexeren Datenbank vorzubeugen. Zudem möchten wir Erfahrungen mit anderen Datenbank-Modellen machen. 
*Entscheindung wurde getroffen von* github.com/nayon0505
<!-- [Describe **which** design decision was taken for **what reason** and by **whom**.] -->

### Regarded options

Wir betrachteten folgende Optionen:

+Standard SQL
+SQLAlchemy

---

## 02: Das stylen unserer Website - Bootstrap oder standart CSS

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 3-Jan-2025

### Problem statement

Sollten wir Bootstrap oder CSS für das Stylen unserer Website verwenden?
CSS ist uns bekannt und hat weniger Lernbedarf. Bootstrap ist eine neue herangehensweise, welche wir dadurch erlernen können.


Deshalb werden wir:

+ Bootstrap erstmals benutzen um die neuen Erfahrungen zusammeln
+ Falls wir nicht weiterkommen CSS einbinden

### Decision

Wir verwenden Bootstrap

Bootstrap bietet uns neue Kenntnisse und im Rahmen eines Kurses, in welchen wir versuchen, das Fullstack Web developing zu lernen, erscheint uns diese Herangehensweise am sinnvollsten.
*Entscheindung wurde getroffen von* github.com/nayon0505

### Regarded options

Wir zogen diese beiden Optionen in Betracht

+ CSS
+ Bootstrap

| Kriterien | CSS | BOOTSTRAP |
| --- | --- | --- |
| **Know-how** | ✔️ Wir kennen CSS | ❌ Wir müssen Bootstrap von grundauf lernen |
| **Simplizität** | ❌ CSS | ✔️ Bootstrap gibt eine komplette Stylevorlage |



---

## 03: Das Nutzen einer Navbar - Ja oder Nein

### Meta

Status
: Work in **progress** - Decided - Obsolete

Updated
: 7-Jan-2025

### Problem statement

Sollten wir eine Nav-bar für schnelle Navigation zwischen unseren Seiten verwenden? Bis her würden wir nur anmelden und registrieren als Optionen auf ihr haben, deshalb evaluieren wir wichtigkeit und Aufwand.  Im späteren Verlauf könnten wir jedoch ein FAQ, Impressum, usw. haben.


Deshalb werden wir wahrschieinlich:

+ im Verlauf schauen ob es villeicht mehr Anwendungsmöglichkeiten gibt

## 04: Nutzen von Werkzeug oder Bcrypt für Passwortencrypting

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 10-Feb-2025

### Problem statement

Nutzen wir weiterhin Bcrypt oder Werkzeug für Passwortencrypting? Wir nutzten bisher Bcrypt jedoch ist Bcrypt ein weiteres Package, was unsere App "schwerer" macht und deshalb werden wir womöglich auf das bereits installierte package Werkzeug zurückgreifen, denn es hat das gleiche feature.

### Decision

Wir wechseln auf Werkzeug encrypiting

Wir haben nun Erfahrungen mit Werkzeug encrypting gemacht und gemerkt, dass es genau das gleiche macht wie Bcrypt. Zudem ist es bereits Teil unserer App, was bedeutet wir brauchen kein neues package zu installieren.
*Entscheindung wurde getroffen von* github.com/nayon0505

### Regarded options

Wir zogen diese beiden Optionen in Betracht

+ Flask Bcrypt
+ Werkzeug security helpers

| Kriterien | BCrypt | Werkzeug encrypting |
| --- | --- | --- |
| **Funktion** | ✔️  | ✔️ |
| **Speicher** | ❌ Muss installiert werden | ✔️ Ist bereits in Nutzung, daher installiert |


---
## 05: SQLALchemy ``session.query API`` vs ``session.execute API``

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 14-Feb-2025

### Problem statement

Verwenden wir für ``READ`` Operationen in unsere ``SQLAlchemy`` Datenbank weiterhin ``session.query()`` oder ``session.execute()``?
### Decision

Wir wechseln auf ``session.execute()``

Seit ``SQLAlchemy 2.0``, gab es ein großes rework, was die  ``session.query() API`` durch ``session.execute() API`` ersetzte. Um nachhaltiger zu programmieren wechseln wir auf ``session.execute()``, obwohl uns persönlich ``session.query()`` einfacher scheint.
*Entscheindung wurde getroffen von* github.com/nayon0505

### Regarded options

Wir zogen diese beiden Optionen in Betracht

+ session.query()
+ session.execute()

| Kriterien | session.query() | session.execute() |
| --- | --- | --- |
| **Simplizität** | ✔️  | ❌ Nicht so simpel wir `session.query()` |
| **Nachhaltigkeit** | ❌ Veraltet | ✔️ Neu seit ``SQLAlchemy 2.0``|


---

## 06: Ausführlicher Check, wie wir das 5 Stufige Formular erstellen möchten - Eine Dynamische html,mit Steps oder mehrere html, eine pro Formular Abschnitt

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 13-Feb-2025

### Problem statement

Bei der Entwicklung des Ausführlichen Checks musste eine entscheidung bezüglich der Architektur für die Umsetzung der 5 Formularsektionen getroffen werden. 
Die Hauptaufgabe die wir hier gesehen haben, besteht darin, die sektionen Nutzerfreundlich und gleichzeitig Technisch effizient abzubilden, ohne die Wartbarkeit und User Experience zu beeinträchtigen.
Zusammengefasst bestand die Herausforderung darin, zwischen einem *Multi-HTML-Page-Ansatz*(eine Seite pro Sektion) und einem *Single-Page-Ansatz mit Dynamischen Steps*(alle Sektionen auf einer Seite) zu wählen.

### Regarded options

#### 1. **Multi-HTML-Page-Ansatz**
*Beschreibung:*
Jede der 5 Sektionen soll als seperate HTML-Seite implementiert werden.
Der User soll vor und zurück navigieren können.

*Vorteile:*
- Einfache Umsetzung, da jede Sektion seperat betrachtet werden kann
- Kein State-Management zwischen den Seiten erforderlich

*Nachteile:*
- Häufige Page-Reloads könnten die User Experience beeinträchtigen
- Komplexeres Session bzw. Datenmanagement über mehrere Seiten hinweg

#### 2. **Single-Page-Ansatz mit Dynamischen Steps**
*Beschreibung:*
Alle 5 Sektionen werden auf einer einzigen HTML-Seite geladen, hierbei sollen die Sektionen durch Bedingungen dynamisch ein- und ausgeblendet werden. 
Der User soll vor und zurück navigieren können.

*Vorteile:*
- Flüssigere Nutzerführung ohne Page-Reloads
- Einfacherre Validierung und Speicherung von Daten
- Zentrales State-Management

*Nachteile:*
- Höhere komplexität
- Möglicherweise längere Ladezeiten der initialen Seite
---

### Decision

Wir haben uns für den *Single-Page-Ansatz mit Dynamischen Steps* entschieden.

Die Entscheidung beruht darauf, dass wir die anfängliche Komplexität bewusst in kaufnehmen, um eine langfristige Wartbarkeit und nutzerzufriedenheit zu sichern, 
darüberhinaus ist es kurz gesagt skalierbarer, Neue Sektionen oder Änderungen lassen sich ohne problem Zentral ergänzen. 
Außerdem fand ich den grundgedanken für "einen Check" mehrere HTML-Seiten zu verwenden unschön.
*Entscheindung wurde getroffen von* github.com/Emircan1122

## 07: Erstellung der Formulare und deren Validierung

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 01-Jan-2025

### Problem statement

Um die Steuertransparenz zu prüfen, müssen wir eine Lösung zur Formularerstellung und Validierung implementieren.
Unsere Anforderungen hierbei sind die Wartbarkeit, Nutzerfreudnlichkeit und Datenintegrität.
Die Hauptfrage die wir uns gestellt haben lautet, wie können wir Formulare effizient, siccher und nutzerorientiert validieren, ohne das wir die Codebasis unnötig verkomplizieren.

### Regarded options

#### 1. **Manuelle Formulare mit Custom Validation**
*Beschreibung:*
Hierbei würden wir unsere Formulare direkt in HTML schreiben, die Validierung würde folgend über zugehörigen Python code erfolgen.

*Vorteile:*
- Volle Kontrolle über HTML-Struktur und Validierungslogik
- Keine externen Abhängigkeiten

*Nachteile:*
- Hoher Aufwand und warscheinlich sehr repetetiver Code für jedes Formular
- schwer skalierbar
- vermutlich ziemlich Fehleranfällig

#### 2. **WTForms/Flask-WTF**
*Beschreibung:*
 Nutzung der Bibliothek WTForms (mit Flask-Integration via Flask-WTF) zur Formularerstellung.

*Vorteile:*
- wiederverwendbare Field-Komponenten 
- Einfache Fehlerrückmeldung in Templates.
- Im Unterricht behandelt

*Nachteile:*
- Datenzwischenspeicherung bei Multi-Page-Forms können sich schwer gestalten.
- Bootstrap Styling schwerer anzuwenden
---

### Decision

Wir haben uns für den *WTForms/Flask-WTF* entschieden.

Die simple Einbindung in Jinja2-Templates z.B. {{ form.hidden_tag() }}, {{ form.field.label }} und wiederverwendbarkeit der Formularklassen und die Custom-Validatoren ermöglichen uns alles was wir im Rahmen unseres Projektes benötigen.
*Entscheindung wurde getroffen von* github.com/Emircan1122

## 08: Wählen des PDF-Generierungs Tools

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 01-Jan-2025

### Problem statement

Da wir uns als Aufgabe gesetzt haben die personalisierten Lösungen mit Hinweisen in From einer PDF auszugeben, beruhend auf den Eingaben des Users, müssen wir ein Tool wählen zum dynamischen ,generieren der jeweiligen PDF.
Die Frage die wir uns hier Gestellt haben lautet, Welche Bibliothek bietet für uns die beste Balance zwischen Felxibilität, Performance und Integration in Flask?

### Regarded options

#### 1. **ReportLab**
*Beschreibung:*
Ist eine Python Bibliothek zur erstellung von PDF's.

*Vorteile:*
- Volle Kontrolle über jedes Element (Position, Schriftart, Farben, usw.)
- Server-seitige Generierung ohne externe Abhängigkeiten (nur Python)

*Nachteile:*
- Layout erstellung etwas kompliziert

#### 2. ** WeasyPrint**
*Beschreibung:*
Konvertiert HTML/CSS in PDF.

*Vorteile:*
- Einfache Integration mit Flask-Templates (Jinja2 → HTML → PDF)
- Relativ Vertraute Syntax

*Nachteile:*
- Begrenzte Kontrolle über Seitenumbrüche oder Header/Footer
---

### Decision

Wir haben uns für den *ReportLab* entschieden.

Beim Ausprobieren, gab es Schwierigkeiten mit WeasyPrint, weshalb schnell klar wurde, das es nicht zu uns passt. ReportLab hingegen konnte einfach fast schon ideal in Flask Routen eingebaut werden, 
das aussehen der PDF kann einfach nach unserem bedarf Strukturiert oder Umstrukturiert werden, Formulardaten aus WTForms können nahtlos in die PDF eingebunden werden und zuletzt ist es einfach überschaubar wie wir finden.

*Entscheindung wurde getroffen von* github.com/Emircan1122

<!--
### Decision steht aus

We stick with plain SQL.

Our team still has to come to grips with various technologies new to us, like Python and CSS. Adding another element to our stack will slow us down at the moment.

Also, it is likely we will completely re-write the app after MVP validation. This will create the opportunity to revise tech choices in roughly 4-6 months from now.
*Decision was taken by:* github.com/joe, github.com/jane, github.com/maxi

### Regarded options

We regarded two alternative options:

+ Plain SQL
+ SQLAlchemy-->





<!-- ## [Example, delete this section] 01: How to access the database - SQL or SQLAlchemy 

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 30-Jun-2024

### Problem statement

Should we perform database CRUD (create, read, update, delete) operations by writing plain SQL or by using SQLAlchemy as object-relational mapper?

Our web application is written in Python with Flask and connects to an SQLite database. To complete the current project, this setup is sufficient.

We intend to scale up the application later on, since we see substantial business value in it.



Therefore, we will likely:
Therefore, we will likely:
Therefore, we will likely:

+ Change the database schema multiple times along the way, and
+ Switch to a more capable database system at some point.

### Decision

We stick with plain SQL.

Our team still has to come to grips with various technologies new to us, like Python and CSS. Adding another element to our stack will slow us down at the moment.

Also, it is likely we will completely re-write the app after MVP validation. This will create the opportunity to revise tech choices in roughly 4-6 months from now.
*Decision was taken by:* github.com/joe, github.com/jane, github.com/maxi

### Regarded options

We regarded two alternative options:

+ Plain SQL
+ SQLAlchemy

| Criterion | Plain SQL | SQLAlchemy |
| --- | --- | --- |
| **Know-how** | ✔️ We know how to write SQL | ❌ We must learn ORM concept & SQLAlchemy |
| **Change DB schema** | ❌ SQL scattered across code | ❔ Good: classes, bad: need Alembic on top |
| **Switch DB engine** | ❌ Different SQL dialect | ✔️ Abstracts away DB engine |

--- -->
