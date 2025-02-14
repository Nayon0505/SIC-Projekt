---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
Anil Öker

{: .no_toc }
# Reference documentation

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Benutzerauthentifizierung

### `index()`

**Route:** `/`

**Methods:** `GET`

**Purpose:** Zeigt die Homepage an und verwaltet Session-Status.

**Sample output:**  
NONE (Rendert index.html Template)

---

### `login()`

**Route:** `/login`

**Methods:** `GET` `POST`

**Purpose:** Verarbeitet Benutzeranmeldung mit Flask-Login.

**Sample output:**  
Redirect zu `/mein-bereich` bei Erfolg

---

### `register()`

**Route:** `/register`

**Methods:** `GET` `POST`

**Purpose:** Registriert neue Benutzer mit Passwort-Hashing.

**Sample output:**  
Redirect zu `/mein-bereich` nach erfolgreicher Registrierung

---

### `logout()`

**Route:** `/logout`

**Methods:** `GET`

**Purpose:** Meldet Benutzer ab und leitet zur Homepage weiter.

**Sample output:**  
Redirect zu `/`

---

## Persönlicher Bereich

### `meinBereich()`

**Route:** `/mein-bereich`

**Methods:** `GET`

**Purpose:** Zeigt Benutzerprofil und gespeicherte Berichte an.

**Sample output:**  
Rendert `meinBereich.html` mit Benutzername und Report-Liste

---

## Check-Funktionen

### `schnelltest()`

**Route:** `/schnelltest`

**Methods:** `GET` `POST`

**Purpose:** Verarbeitet Schnellcheck-Formular und generiert PDF-Report.

**Sample output:**  
Redirect zu `/result` mit generiertem PDF

---

### `ausführlicherTest()`

**Route:** `/ausführlicherTest`

**Methods:** `GET` `POST`

**Purpose:** Mehrstufiges Formular für detaillierte Steuerprüfung.

**Sample output:**  
Rendert Template mit Schritt-für-Schritt Formularen

---

## Ergebnisverarbeitung

### `result()`

**Route:** `/result`

**Methods:** `GET`

**Purpose:** Zeigt Prüfergebnis und Benutzereingaben an.

**Sample output:**  
Rendert `result.html` mit Ampelfarbe und Antworten

---

## Dateioperationen

### `download_pdf()`

**Route:** `/download/<filename>`

**Methods:** `GET`

**Purpose:** Ermöglicht PDF-Download des Berichts.

**Sample output:**  
Sendet PDF als Dateianhang

---

### `download_pdf_meinBereich()`

**Route:** `/download_pdf/<int:report_id>`

**Methods:** `GET`

**Purpose:** Lädt gespeicherte PDF-Reports aus der Datenbank.

**Sample output:**  
PDF-File-Stream mit Report-Inhalten

---

## Datenbankverwaltung

### `init()`

**Route:** CLI Command `init-db`

**Methods:** CLI

**Purpose:** Initialisiert Datenbankstruktur.

**Sample output:**  
Terminal: "Database has been initialized."

---

## Hilfsfunktionen

### `CalculateResult.calcResults()`

**Purpose:** Berechnet Risikobewertung basierend auf Benutzerantworten.

**Sample output:**  
Return-Tuple: `("grün", 85)`

---

### `PdfGenerator.generate_pdf()`

**Purpose:** Erstellt strukturierte PDF-Reports mit ReportLab.

**Sample output:**  
Generiert `Nachhaltigkeitsbericht.pdf`

---

### `load_user()`

**Purpose:** Lädt Benutzerobjekt für Flask-Login.

**Sample output:**  
User-Objekt oder `None`

---