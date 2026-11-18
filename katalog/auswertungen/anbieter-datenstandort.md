---
id: anbieter-datenstandort
titel: Wohin gehen unsere Daten, und ist der Vertrag in Ordnung?
kurzantwort: 20,4 % der erfolgreichen Anfragen gehen an Anbieter West (Datenstandort USA, kein Auftragsverarbeitungsvertrag). Das sind 72,6 % der Kosten. Der Vertrag endet am 31.01.2026.
fuer: [Compliance & Datenschutz, Einkauf & IT]
status: verlaessig
status_hinweis: Vertragsdaten sind eine erfundene Beispielliste, in der Praxis müssten Einkauf und Datenschutz sie bestätigen.
seit: 2026-11-18
aktualisiert: 2026-11-18
zustaendig_fachlich: Einkauf und Datenschutz
zustaendig_zahlen: BI-Team
rueckfragen: "#ki-daten-hilfe"
technischer_name: ai_providers.csv, model_providers.csv und usage_events (neue Quellen, noch nicht im Lakehouse-Projekt eingebunden)
herkunft:
  - {station: Anbieterliste, text: "Einkauf pflegt je Anbieter Datenstandort, Vertragsende und ob ein Auftragsverarbeitungsvertrag (AVV) unterschrieben ist."}
  - {station: Modellzuordnung, text: "Jedes KI-Modell gehört zu genau einem Anbieter."}
  - {station: Nutzungsprotokoll, text: "Jede Anfrage nennt das Modell und damit den Anbieter."}
  - {station: Dein Bericht, text: "Anteil der Anfragen und Kosten je Anbieter, mit Standort und AVV-Status."}
beispielfragen:
  - Gehen Daten an Anbieter ohne AVV?
  - Wann läuft der Vertrag mit Anbieter West aus?
  - Wie viel der Hochrisiko-Nutzung geht an Anbieter ohne AVV?
nicht_verwechseln:
  - "Datenstandort: Er sagt, wo Daten verarbeitet werden. Er ersetzt keinen Vertrag."
  - "Kostenanteil: Anbieter West hat nur 20,4 % der Anfragen, aber 72,6 % der Kosten, weil das große Modell teuer ist."
werte:
  anbieter_anzahl: "3"
  anbieter_ohne_avv: "Anbieter West"
  anbieter_ohne_avv_standort: "USA"
  anbieter_ohne_avv_vertragsende: "31.01.2026"
  anfragen_ohne_avv_prozent: "20,4"
  kosten_ohne_avv_prozent: "72,6"
  hochrisiko_ohne_avv_prozent: "35,0"
  anfragen_P1_prozent: "42,5"
  anfragen_P2_prozent: "37,1"
  anfragen_P3_prozent: "20,4"
---

## Das sagt die Zahl

Es gibt **3** Anbieter. Zwei (Anbieter Nord und Anbieter Mitte, Standort EU) haben einen Auftragsverarbeitungsvertrag. **Anbieter West** hat keinen, der Datenstandort ist **USA**, der Vertrag endet am **31.01.2026**.

- Anteil der erfolgreichen Anfragen: Nord **42,5 %**, Mitte **37,1 %**, West **20,4 %**
- An Anbieter West gehen **20,4 %** aller Anfragen und **72,6 %** der Kosten
- Bei Hochrisiko-Anwendungsfällen gehen **35,0 %** der Anfragen an Anbieter West

## Darf ich mich darauf verlassen?

**Ja für die Rechnung.** Die Zahlen sind nachgerechnet. Aber:

- Anbieter, Standorte und Verträge sind erfunden. In der Praxis müssen Einkauf und Datenschutz sie bestätigen.
- Der Katalog sagt nicht, welche Daten in den Anfragen steckten, also auch nicht, ob personenbezogene Daten dabei waren.
- **Nicht geeignet für:** rechtliche Bewertung der Verträge.

## So wird gerechnet

Anteil = erfolgreiche Anfragen je Anbieter geteilt durch alle erfolgreichen Anfragen (54.098). Kostenanteil = Kosten der Anfragen an den Anbieter geteilt durch Gesamtkosten (281,52 €). Zuordnung über das Modell.

## Wer hilft?

- **Fachlich:** Einkauf und Datenschutz
- **Zur Berechnung:** BI-Team
- **Kanal:** #ki-daten-hilfe

## Was hat sich geändert?

- 18.11.2026: Karte neu im Katalog. Die Anbieterlisten sind neue Quellen.
