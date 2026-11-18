---
id: freigabe-konformitaet
titel: Welche KI-Anwendungsfälle sind freigegeben und dokumentiert?
kurzantwort: Bei Hochrisiko-Anwendungsfällen ist nur 1 von 4 freigegeben und vollständig dokumentiert (25,0 %). Bei minimalem Risiko sind es alle (4 von 4).
fuer: [Compliance & Datenschutz]
status: verlaessig
status_hinweis: Die Risikoklassen der Beispieldaten sind zufällig vergeben und keine echte Einstufung.
seit: 2026-11-12
aktualisiert: 2026-11-18
zustaendig_fachlich: Compliance und KI-Verantwortliche
zustaendig_zahlen: BI-Team
rueckfragen: "#ki-daten-hilfe"
technischer_name: ki_nutzung.gold.mart_anwendungsfaelle_konformitaet (Lakehouse-Projekt)
herkunft:
  - {station: Anwendungsfall-Register, text: "Jeder Anwendungsfall hat Risikoklasse, Status und Dokumentationsstand."}
  - {station: Filter, text: "Eingestellte Anwendungsfälle werden nicht gezählt."}
  - {station: Prüfen, text: "Konform = Status freigegeben und Dokumentation vollständig."}
  - {station: Dein Bericht, text: "Anzahl und Anteil je Risikoklasse."}
beispielfragen:
  - Wie viele Hochrisiko-Anwendungsfälle sind konform?
  - Was heißt konform?
  - Zählen Pilotprojekte als konform?
nicht_verwechseln:
  - "Freigegeben: Status laut Register. Freigegeben allein genügt nicht, es braucht auch die vollständige Dokumentation."
  - "Rechtliche Einstufung: Die Klassen sind an die Stufen des EU AI Act angelehnt, ersetzen aber keine Rechtsprüfung."
werte:
  konform_minimal_anzahl: "4 von 4"
  konform_begrenzt_anzahl: "2 von 5"
  konform_hoch_anzahl: "1 von 4"
  konform_hoch_prozent: "25,0"
  konform_begrenzt_prozent: "40,0"
  konform_minimal_prozent: "100,0"
---

## Das sagt die Zahl

Anteil der Anwendungsfälle, die **freigegeben und vollständig dokumentiert** sind, je Risikoklasse:

- minimal: **4 von 4** (100,0 %)
- begrenzt: **2 von 5** (40,0 %)
- hoch: **1 von 4** (25,0 %)

Je höher das Risiko, desto weniger ist erledigt.

## Darf ich mich darauf verlassen?

**Ja für die Rechnung, nein als Rechtsaussage.** Die Zahl ist nachgerechnet. Aber:

- Die Risikoklassen der Beispieldaten sind zufällig vergeben. Beispiel: "Bewerbungs-Vorauswahl" steht dort auf minimal, obwohl Personalauswahl im EU AI Act als Hochrisiko gilt.
- **Nicht geeignet für:** rechtliche Bewertung oder Nachweise gegenüber Behörden.

## So wird gerechnet

Konform = Status "freigegeben" **und** Dokumentation vollständig. Eingestellte Anwendungsfälle zählen nicht. Piloten zählen mit, sind aber noch nicht freigegeben und daher nie konform.

## Wer hilft?

- **Fachlich:** Compliance und KI-Verantwortliche
- **Zur Berechnung:** BI-Team
- **Kanal:** #ki-daten-hilfe

## Was hat sich geändert?

- 18.11.2026: Karte neu geschrieben, Zahlen nachgerechnet.
- 12.11.2026: Erste Fassung im Lakehouse-Projekt.
