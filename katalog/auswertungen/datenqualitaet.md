---
id: datenqualitaet
titel: Wo sind die Daten unsauber?
kurzantwort: Vier Prüfungen melden Auffälligkeiten. Zwei sind rot (zu viele Anfragen ohne Anwendungsfall, Nutzer mit unbekannter Abteilung), zwei gelb.
fuer: [Einkauf & IT, Compliance & Datenschutz]
status: verlaessig
status_hinweis: Die Prüfungen reparieren nichts still, sie zählen und melden.
seit: 2026-11-12
aktualisiert: 2026-11-18
zustaendig_fachlich: BI-Team
zustaendig_zahlen: BI-Team
rueckfragen: "#ki-daten-hilfe"
technischer_name: ki_nutzung.gold.mart_datenqualitaet und mart_datenqualitaet_details (Lakehouse-Projekt)
herkunft:
  - {station: Rohdaten, text: "Alle gelieferten Daten bleiben unverändert erhalten."}
  - {station: Prüfregeln, text: "Vier Regeln zählen Auffälligkeiten: Doppelte, ohne Anwendungsfall, nach Austritt, unbekannte Abteilung."}
  - {station: Ampel, text: "grün = nichts gefunden, gelb = unter 1 % betroffen, rot = 1 % oder mehr."}
  - {station: Dein Bericht, text: "Übersicht mit Erklärung, Empfehlung und Zuständigkeit."}
beispielfragen:
  - Welche Datenprobleme gibt es?
  - Was bedeutet die rote Ampel?
  - Wer kümmert sich um Nutzung nach dem Austritt?
nicht_verwechseln:
  - "Fehlgeschlagene Anfragen: Das sind technische Fehler bei der KI-Nutzung, kein Datenqualitätsproblem."
werte:
  dq_doppelte: "139"
  dq_ohne_anwendungsfall: "1.102"
  dq_nach_austritt: "174"
  dq_unbekannte_abteilung: "5"
---

## Das sagt die Zahl

| Prüfung | Betroffen | Ampel | Zuständig |
|---|---:|---|---|
| Doppelte Ereignisse | 139 | gelb | Quellsystem / IT |
| Ereignisse ohne Anwendungsfall | 1.102 | rot | Fachbereich / KI-Verantwortliche |
| Nutzung nach dem Austritt | 174 | gelb | IT / Personal |
| Nutzer mit unbekannter Abteilung | 5 | rot | Personal / Stammdaten |

## Darf ich mich darauf verlassen?

**Ja.** Die Zahlen sind nachgerechnet. Die Auswertung repariert nichts still: Auffällige Zeilen bleiben drin und werden gezählt, ein Mensch entscheidet.

## So wird gerechnet

Betroffene Zeilen geteilt durch geprüfte Zeilen. Gelb ist unter 1 %, rot ab 1 %. Die Grundgesamtheit unterscheidet sich je Prüfung: alle gelieferten Anfragen (55.861), Anfragen ohne Duplikate (55.722) oder alle Nutzer (220).

## Wer hilft?

- **Fachlich:** BI-Team
- **Kanal:** #ki-daten-hilfe

## Was hat sich geändert?

- 18.11.2026: Karte neu geschrieben, Zahlen nachgerechnet.
- 12.11.2026: Erste Fassung im Lakehouse-Projekt.
