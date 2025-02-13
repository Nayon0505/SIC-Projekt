---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
Nayon Lenz

{: .no_toc }
# Data model

![Datenmodel](/docs/assets/images/sic-datamodel.png)



<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Entitäten
### User:
Stellt den Nutzer als Objekt dar.

**Atribute:**
- Id
- Name
- Passwort

### Report:
Stellt den Nachhaltigkeitsbericht als Objekt dar.

**Atribute:**
- Id 
- Testdatum
- Testtyp (Ausführlich oder Schnell)
- PDF-file für den Report

## Relationships

Ein User kann n Reports haben und n Reports können genau einen User haben.
Es herrscht eine 1 zu n beziehung zwischen den beiden, was bedeutet, dass im Übergang zum Relationsmodell wird die UserID ein Foreignkey in der Reporttabelle.
Dadurch können wir jeden Report einen Nutzer zuweisen und jedem Nutzer alle seine Reports zuweisen.

