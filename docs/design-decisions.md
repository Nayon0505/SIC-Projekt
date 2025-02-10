---
title: Design Decisions
nav_order: 3
---

{: .label }
Nayon Lenz

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
