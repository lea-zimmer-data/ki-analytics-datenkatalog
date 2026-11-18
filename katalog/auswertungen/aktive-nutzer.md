---
id: aktive-nutzer
titel: Wie viele Mitarbeitende nutzen KI wirklich aktiv?
kurzantwort: "Im Dezember 2025 waren 202 Personen aktiv, im Januar 212. Aktiv heißt: mindestens eine erfolgreiche Anfrage im Monat."
fuer: [Abteilungsleitung, Personal]
status: verlaessig
status_hinweis: Anfragen nach dem Austritt zählen nicht mit.
seit: 2026-11-12
aktualisiert: 2026-11-18
zustaendig_fachlich: KI-Verantwortliche
zustaendig_zahlen: BI-Team
rueckfragen: "#ki-daten-hilfe"
technischer_name: ki_nutzung.gold.mart_aktive_nutzer_monat (Lakehouse-Projekt)
herkunft:
  - {station: Nutzungsprotokoll, text: "Jede erfolgreiche KI-Anfrage nennt den Nutzer."}
  - {station: Bereinigung, text: "Doppelte Anfragen zählen einmal, Anfragen nach dem Austritt werden ausgeschlossen."}
  - {station: Zählen, text: "Je Monat wird jede Person einmal gezählt, egal wie oft sie fragt."}
  - {station: Dein Bericht, text: "Aktive Nutzer je Abteilung und Monat."}
beispielfragen:
  - Wie viele Leute haben im Dezember KI benutzt?
  - Darf ich die Monatswerte über das Jahr addieren?
  - Zählen Anfragen von ausgetretenen Mitarbeitenden?
nicht_verwechseln:
  - "Mitarbeitende mit Lizenz: Wer eine Lizenz hat, muss nicht aktiv sein. Siehe Karte Ungenutzte Lizenzen."
  - "Nutzer gesamt: 220 Personen sind in den Stammdaten, davon 18 ausgetreten."
werte:
  aktive_nutzer_dezember: "202"
  aktive_nutzer_januar: "212"
  nutzer_gesamt: "220"
---

## Das sagt die Zahl

Wie viele verschiedene Personen in einem Monat mindestens eine erfolgreiche KI-Anfrage gestellt haben. Im **Dezember 2025** waren es **202**, im **Januar 212**. Die Zahl sinkt, obwohl die Nutzung steigt: 18 Personen sind im Jahresverlauf ausgetreten.

## Darf ich mich darauf verlassen?

**Ja.** Die Zahl ist nachgerechnet. Zu wissen ist:

- Anfragen nach dem Austrittsdatum zählen nicht. Davon gibt es 174, sie stehen in der Karte Datenqualität.
- Wer nur fehlgeschlagene Anfragen hatte, gilt nicht als aktiv.
- Es sind Beispieldaten für 2025.

## So wird gerechnet

Je Monat werden die verschiedenen Personen mit mindestens einer erfolgreichen Anfrage gezählt. Die Zuordnung zur Abteilung erfolgt über die Stammdaten.

**Achtung beim Summieren:** Monatswerte dürfen nicht über das Jahr addiert werden. Wer im Januar und im Februar aktiv war, würde doppelt gezählt.

## Wer hilft?

- **Fachlich:** KI-Verantwortliche
- **Zur Berechnung:** BI-Team
- **Kanal:** #ki-daten-hilfe

## Was hat sich geändert?

- 18.11.2026: Karte neu geschrieben, Zahlen nachgerechnet.
- 12.11.2026: Erste Fassung im Lakehouse-Projekt.
