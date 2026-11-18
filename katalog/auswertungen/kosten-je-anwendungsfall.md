---
id: kosten-je-anwendungsfall
titel: Welche KI-Anwendungsfälle sind je Anfrage am teuersten?
kurzantwort: Am teuersten ist Textzusammenfassung mit 0,0083 € je erfolgreicher Anfrage, am günstigsten Wissensdatenbank-Antworten mit 0,0040 €.
fuer: [Controlling, Compliance & Datenschutz]
status: mit-vorsicht
status_hinweis: 1.102 Anfragen haben keinen Anwendungsfall und fehlen in dieser Auswertung.
seit: 2026-11-12
aktualisiert: 2026-11-18
zustaendig_fachlich: KI-Verantwortliche
zustaendig_zahlen: BI-Team
rueckfragen: "#ki-daten-hilfe"
technischer_name: ki_nutzung.gold.mart_kosten_je_anwendungsfall (Lakehouse-Projekt)
herkunft:
  - {station: Nutzungsprotokoll, text: "Jede Anfrage nennt, wenn angegeben, den Anwendungsfall."}
  - {station: Kosten, text: "Kosten je Anfrage wie in der Karte Kosten je Abteilung."}
  - {station: Gruppieren, text: "Pro Anwendungsfall mit mindestens 100 Anfragen werden Kosten und erfolgreiche Anfragen gezählt."}
  - {station: Dein Bericht, text: "Kosten geteilt durch erfolgreiche Anfragen, vier Nachkommastellen."}
beispielfragen:
  - Welcher Anwendungsfall ist am teuersten?
  - Warum fehlen Anfragen in dieser Auswertung?
  - Sind teure Anwendungsfälle auch Hochrisiko?
nicht_verwechseln:
  - "Gesamtkosten je Anwendungsfall: Hier steht der Preis je Anfrage, nicht die Summe."
werte:
  teuerster_anwendungsfall: "Textzusammenfassung"
  teuerster_anwendungsfall_risiko: "hoch"
  teuerster_anwendungsfall_je_anfrage_eur: "0,0083"
  guenstigster_anwendungsfall: "Wissensdatenbank-Antworten"
  guenstigster_anwendungsfall_je_anfrage_eur: "0,0040"
  dq_ohne_anwendungsfall: "1.102"
---

## Das sagt die Zahl

Was eine erfolgreiche KI-Anfrage im Durchschnitt kostet, je Anwendungsfall. **Textzusammenfassung** ist mit **0,0083 €** am teuersten (Risikoklasse hoch). **Wissensdatenbank-Antworten** sind mit **0,0040 €** am günstigsten.

## Darf ich mich darauf verlassen?

**Mit Vorsicht.**

- **1.102 Anfragen** haben keinen Anwendungsfall. Ihre Kosten sind in den Gesamtkosten enthalten, aber hier nicht zuordenbar.
- Es zählen nur Anwendungsfälle mit mindestens 100 Anfragen.
- Dass teure Anwendungsfälle selten freigegeben sind, liegt in den Beispieldaten am Generator: Große, teure Modelle werden dort bei Hochrisiko-Fällen häufiger genutzt.

## So wird gerechnet

Kosten des Anwendungsfalls ÷ Zahl seiner erfolgreichen Anfragen. Fehlgeschlagene Anfragen kosten nichts und zählen nicht im Nenner.

## Wer hilft?

- **Fachlich:** KI-Verantwortliche
- **Zur Berechnung:** BI-Team
- **Kanal:** #ki-daten-hilfe

## Was hat sich geändert?

- 18.11.2026: Karte neu geschrieben, Zahlen nachgerechnet.
- 12.11.2026: Erste Fassung im Lakehouse-Projekt.
