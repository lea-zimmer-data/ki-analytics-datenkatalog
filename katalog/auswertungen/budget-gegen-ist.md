---
id: budget-gegen-ist
titel: Liegen wir mit den KI-Kosten im Budget?
kurzantwort: Über das Jahr liegen die Abteilungen mit 268,25 € unter dem geplanten Budget von 323,22 €. In 31 von 93 Abteilungsmonaten wurde das Monatsbudget trotzdem überschritten, ab Mai 2025.
fuer: [Controlling, Abteilungsleitung]
status: mit-vorsicht
status_hinweis: Für Personal fehlt das Budget von Oktober bis Dezember. Unbekannt hat nie ein Budget.
seit: 2026-11-18
aktualisiert: 2026-11-18
zustaendig_fachlich: Controlling
zustaendig_zahlen: BI-Team
rueckfragen: "#ki-daten-hilfe"
technischer_name: budgets.csv und mart_kosten_je_abteilung_monat (Budgetdatei im Lakehouse-Projekt noch nicht eingebunden)
herkunft:
  - {station: Budgetplanung, text: "Controlling plant je Abteilung ein Jahresbudget und verteilt es gleichmäßig auf zwölf Monate."}
  - {station: Ist-Kosten, text: "Token-Kosten je Abteilung und Monat, wie in der Karte Kosten je Abteilung."}
  - {station: Abgleich, text: "Je Abteilung und Monat: Ist minus Plan. Nur Monate mit Budget werden verglichen."}
  - {station: Dein Bericht, text: "Abweichung in Euro und Zahl der Monate über Budget."}
beispielfragen:
  - Sind wir 2025 im Budget geblieben?
  - Welche Abteilung hat ihr Budget am häufigsten überschritten?
  - Warum fehlt das Budget für Personal im vierten Quartal?
nicht_verwechseln:
  - "Kosten: Die Kosten stehen in der Karte Kosten je Abteilung. Hier geht es um den Abgleich mit dem Plan."
  - "Jahresbilanz und Monatsbild: Das Jahr kann im Plus liegen, obwohl einzelne Monate darüber liegen. Das liegt an der gleichmäßigen Verteilung bei wachsender Nutzung."
werte:
  budget_gesamt_eur: "323,22"
  budget_ist_eur: "268,25"
  budget_abweichung_eur: "-54,97"
  budget_monate_ueber_anzahl: "31"
  budget_monate_geplant: "93"
  budget_erster_monat_ueber: "Mai 2025"
  budget_abteilungen_mit_luecke: "Personal"
  budget_luecke_monate: "3"
  budget_ist_ohne_budget_eur: "6,73"
  budget_abteilung_meiste_ueberschreitungen: "Vertrieb"
  budget_abteilung_meiste_ueberschreitungen_monate: "6"
---

## Das sagt die Zahl

Vergleich der KI-Kosten mit dem Budget je Abteilung und Monat (nur Token-Kosten).

- Budget für 2025 laut Plan: **323,22 €**
- Tatsächliche Kosten in den Monaten mit Budget: **268,25 €**
- Abweichung: **−54,97 €**, also unter Plan

Das Bild je Monat ist weniger gut: In **31 von 93** Abteilungsmonaten lagen die Kosten über dem Monatsbudget, zum ersten Mal im **Mai 2025**. **Vertrieb** hat das Budget in **6** Monaten überschritten, am häufigsten.

## Darf ich mich darauf verlassen?

**Mit Vorsicht.**

- Für die Abteilung **Personal** fehlt das Budget für **3 Monate** (Oktober bis Dezember). Diese 3 Monate sind in "93 geplant" nicht enthalten.
- Die Kosten der drei Personal-Monate ohne Budget betragen **6,73 €** und sind im Vergleich nicht enthalten. Die Abteilung "Unbekannt" (6,54 €) hat nie ein Budget.
- Das Monatsbudget ist ein Zwölftel des Jahresbudgets. Weil die Nutzung über das Jahr wächst, liegen späte Monate eher darüber.
- **Nicht geeignet für:** Freigabe von Zusatzbudget ohne Rückfrage beim Controlling.

## So wird gerechnet

Abweichung = Ist-Kosten minus Budget, je Abteilung und Monat. Ein Monat gilt als überschritten, wenn die Ist-Kosten über dem Monatsbudget liegen. Monate ohne Budget werden nicht verglichen.

## Wer hilft?

- **Fachlich:** Controlling
- **Zur Berechnung:** BI-Team
- **Kanal:** #ki-daten-hilfe

## Was hat sich geändert?

- 18.11.2026: Karte neu im Katalog. Die Budgetdatei ist eine neue Quelle.
