---
id: ungenutzte-lizenzen
titel: Welche bezahlten KI-Lizenzen werden nicht genutzt?
kurzantwort: Zum Stichtag 31.12.2025 sind 33 von 119 Lizenzen (27,7 %) ungenutzt. Das kostet 297,00 € im Monat.
fuer: [Einkauf & IT, Controlling]
status: mit-vorsicht
status_hinweis: 4 Nutzer haben zwei Lizenzen, 13 Lizenzen gehören ausgetretenen Personen.
seit: 2026-11-18
aktualisiert: 2026-11-18
zustaendig_fachlich: IT-Einkauf (Lizenzverwaltung)
zustaendig_zahlen: BI-Team
rueckfragen: "#ki-daten-hilfe"
technischer_name: licenses.csv (neue Quelle, noch nicht im Lakehouse-Projekt eingebunden)
herkunft:
  - {station: Lizenzverwaltung, text: "Die Verwaltung führt je bezahltem Platz Nutzer, Vergabedatum und letzten Login."}
  - {station: Stichtag, text: "Bewertet wird zum 31.12.2025."}
  - {station: Regel, text: "Ungenutzt = letzter Login mehr als 90 Tage vor dem Stichtag oder nie eingeloggt."}
  - {station: Preis, text: "Jede Lizenz kostet 9,00 € im Monat."}
  - {station: Dein Bericht, text: "Zahl und Anteil ungenutzter Lizenzen, Kosten je Monat."}
beispielfragen:
  - Wie viele Lizenzen nutzt niemand?
  - Was kosten uns ungenutzte Lizenzen?
  - Haben ausgetretene Mitarbeitende noch Lizenzen?
nicht_verwechseln:
  - "Aktive Nutzer: Aktiv zählt Anfragen, ungenutzt zählt Logins in der Lizenzverwaltung. Die Zahlen können abweichen."
  - "Token-Kosten: Lizenzkosten sind ein fester Betrag je Platz, Token-Kosten hängen von der Nutzung ab."
werte:
  lizenzen_gesamt: "119"
  lizenzen_ungenutzt: "33"
  lizenzen_ungenutzt_prozent: "27,7"
  lizenzen_ungenutzt_kosten_monat_eur: "297,00"
  lizenzen_kosten_monat_eur: "1.071,00"
  lizenzen_preis_eur: "9,00"
  lizenzen_nie_genutzt: "17"
  lizenzen_ausgetretene: "13"
  lizenzen_nutzer_doppelt: "4"
---

## Das sagt die Zahl

Von **119** bezahlten Lizenzen sind zum Stichtag 31.12.2025 **33** ungenutzt (**27,7 %**). Bei **9,00 €** je Platz und Monat kosten diese 33 Plätze **297,00 €** im Monat. **17** Lizenzen wurden noch nie benutzt. Alle 119 Lizenzen zusammen kosten **1.071,00 €** im Monat.

## Darf ich mich darauf verlassen?

**Mit Vorsicht.**

- **4 Nutzer** haben zwei Lizenzen. Die zweite ist doppelt bezahlt.
- **13 Lizenzen** gehören Personen, die das Unternehmen verlassen haben.
- Der letzte Login stammt aus der Lizenzverwaltung und ist nicht dasselbe wie die Nutzung über Schnittstellen. Wer nur über eine andere Anwendung KI nutzt, kann als ungenutzt erscheinen.
- Das ist ein Stand zum Stichtag, keine Entwicklung über die Zeit.
- **Nicht geeignet für:** Kündigung von Lizenzen ohne Rückfrage bei den betroffenen Personen.

## So wird gerechnet

Ungenutzt = kein Login in den 90 Tagen bis zum Stichtag, oder noch nie eingeloggt. Kosten = Anzahl × 9,00 € je Monat. Doppelte Lizenzen zählen als zwei Lizenzen.

## Wer hilft?

- **Fachlich:** IT-Einkauf (Lizenzverwaltung)
- **Zur Berechnung:** BI-Team
- **Kanal:** #ki-daten-hilfe

## Was hat sich geändert?

- 18.11.2026: Karte neu im Katalog. Die Lizenzdatei ist eine neue Quelle.
