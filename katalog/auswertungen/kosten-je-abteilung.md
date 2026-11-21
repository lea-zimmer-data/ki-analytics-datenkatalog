---
id: kosten-je-abteilung
titel: Was kostet KI pro Abteilung und Monat?
kurzantwort: Die Nutzung hat 2025 insgesamt 281,52 € gekostet. Am meisten entfällt auf Kundenservice (68,76 €).
fuer: [Controlling, Abteilungsleitung]
status: mit-vorsicht
status_hinweis: 6,54 € gehören zu Nutzern ohne bekannte Abteilung und stehen unter "Unbekannt".
seit: 2026-11-12
aktualisiert: 2026-11-21
zustaendig_fachlich: Controlling (IT-Kostenstellen)
zustaendig_zahlen: BI-Team
rueckfragen: "#ki-daten-hilfe"
technischer_name: ki_nutzung.gold.mart_kosten_je_abteilung_monat und fct_usage_events (Lakehouse-Projekt)
herkunft:
  - {station: Nutzungsprotokoll, text: "Jede KI-Anfrage wird beim Anbieter protokolliert und geliefert (55.861 Zeilen)."}
  - {station: Bereinigung, text: "Doppelt gelieferte Anfragen zählen nur einmal (55.722 bleiben)."}
  - {station: Preisliste, text: "Kosten je Anfrage = Eingabe-Token × Preis + Ausgabe-Token × Preis. Fehlgeschlagene Anfragen kosten 0."}
  - {station: Zuordnung, text: "Jede Anfrage wird über den Nutzer einer Abteilung zugeordnet. Ohne bekannte Abteilung: Unbekannt."}
  - {station: Dein Bericht, text: "Summe je Abteilung und Monat."}
beispielfragen:
  - Was hat KI 2025 insgesamt gekostet?
  - Welche Abteilung verursacht die höchsten KI-Kosten?
  - Warum ist die Summe der Monatswerte nicht genau gleich den Gesamtkosten?
nicht_verwechseln:
  - "Lizenzkosten: Sie stehen nicht in dieser Zahl. Siehe Karte Ungenutzte Lizenzen."
  - "Budget: Das Budget ist eine Planzahl. Siehe Karte Budget gegen Ist."
werte:
  kosten_gesamt_eur: "281,52"
  kosten_teuerste_abteilung: "Kundenservice"
  kosten_teuerste_abteilung_eur: "68,76"
  kosten_unbekannt_eur: "6,54"
  kosten_summe_gerundet_eur: "281,49"
  kosten_januar_eur: "11,90"
  kosten_dezember_eur: "38,82"
---

## Das sagt die Zahl

Die Token-Kosten der KI-Nutzung, aufgeteilt nach Abteilung und Monat. In den Beispieldaten für 2025 sind das **281,52 €**. Die höchsten Kosten hat **Kundenservice** mit 68,76 €. Die Nutzung wächst über das Jahr: Im Januar waren es 11,90 €, im Dezember 38,82 €.

## Darf ich mich darauf verlassen?

**Mit Vorsicht.** Die Zahlen sind nachgerechnet, aber:

- **6,54 €** gehören zu Nutzern, deren Abteilung in den Stammdaten fehlt. Sie stehen unter "Unbekannt" und fehlen in jeder Abteilungssumme.
- **Lizenzkosten sind nicht enthalten.** Hier geht es nur um Token.
- Es sind Beispieldaten für 2025, keine Live-Daten.
- **Nicht geeignet für:** Rechnungsabgleich oder Buchhaltungsabschluss.

## So wird gerechnet

Kosten je Anfrage = Eingabe-Token × Eingabepreis ÷ 1.000 + Ausgabe-Token × Ausgabepreis ÷ 1.000. Fehlgeschlagene Anfragen kosten nichts. Doppelt gelieferte Anfragen zählen einmal.

**Achtung beim Summieren:** Im Bericht ist jede Zeile je Abteilung und Monat auf zwei Stellen gerundet. Die Summe der Zeilen ergibt deshalb 281,49 €, die genauen Gesamtkosten sind 281,52 €. Für Gesamtsummen die genaue Zahl verwenden.

**Was der Katalog nicht enthält:** Die einzelnen Werte je Abteilung und Monat stehen im Bericht, nicht im Katalog. Der Katalog erklärt die Zahl, er liefert nicht jede Zeile. Einzelwerte, zum Beispiel Vertrieb im Oktober, liefert das BI-Team.

## Wer hilft?

- **Fachlich:** Controlling (IT-Kostenstellen)
- **Zur Berechnung:** BI-Team
- **Kanal:** #ki-daten-hilfe

## Was hat sich geändert?

- 21.11.2026: Klargestellt, dass die Werte je Abteilung und Monat im Bericht stehen und nicht im Katalog.
- 18.11.2026: Karte neu geschrieben, Zahlen mit dem Katalog-Test nachgerechnet.
- 12.11.2026: Erste Fassung im Lakehouse-Projekt.
