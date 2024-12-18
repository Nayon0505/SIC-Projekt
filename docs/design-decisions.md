---
title: Design Decisions
nav_order: 3
---

{: .label }
[Nayon Lenz]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: [Standart SQL oder SQLAlechemy]

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 04-12-2024

### Problem statement

Wir müssen Nutzerdaten, sowie unsere Fragebögen und Nachhaltigkeitsberichte in einer Datenbank speichern. Wir haben nun die Wahl zwischen standart SQL oder SQLAlchemy. SQL würde uns einfacher fallen, da wir schon einige Kenntnisse haben, jedoch wäre für später geplanter Ausbau der Applikation SQLAlchemy besser.
<!-- [Describe the problem to be solved or the goal to be achieved. Include relevant context information.] -->

### Decision

Wir entschieden uns für SQLAlchemy um der zukünftigen Notwendigkeit einer komplexeren Datenbank vorzubeugen. Zudem möchten wir Erfahrungen mit anderen Datenbank-Modellen machen. Diese Entscheidung wurde von Nayon getroffen.
<!-- [Describe **which** design decision was taken for **what reason** and by **whom**.] -->

### Regarded options

Wir betrachteten folgende Optionen:

+Standard SQL
+SQLAlchemy

| Kriterium | Standart SQL | SQLAlchemy |
| --- | --- | --- |
| **Know-how** | ✔️ Wir kennen bereits SQL | ❌ Wir müssen SQLAlchemy von Grund auf lernen |
| **Change DB schema** | ❌ Unordentliches SQL | ✔️ Ordentlich überschaubare Klassen |
| **Switch DB engine** | ❌ Man benötigt einen anderen SQL-Dialekt | ✔️ Einfacher wechsel |

---

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
