---
id: schulungsquote
titel: Wer ist für die KI-Nutzung geschult?
kurzantwort: 26,2 % der Mitarbeitenden haben beide Pflichtschulungen gültig (53 von 202). Von den Personen, die im Dezember Hochrisiko-Anwendungsfälle genutzt haben, fehlt bei 66 die gültige Grundlagenschulung.
fuer: [Personal, Compliance & Datenschutz]
status: mit-vorsicht
status_hinweis: 3 Schulungsnachweise gehören zu Nutzer-Nummern, die es nicht gibt.
seit: 2026-11-18
aktualisiert: 2026-11-18
zustaendig_fachlich: Personalentwicklung
zustaendig_zahlen: BI-Team
rueckfragen: "#ki-daten-hilfe"
technischer_name: training_courses.csv und training_completions.csv (neue Quellen, noch nicht im Lakehouse-Projekt eingebunden)
herkunft:
  - {station: Schulungsverwaltung, text: "Jeder abgeschlossene Kurs wird mit Person und Datum erfasst."}
  - {station: Bereinigung, text: "Doppelt erfasste Nachweise zählen einmal, Nachweise für unbekannte Nutzer werden nicht gezählt."}
  - {station: Gültigkeit, text: "KI-Grundlagen gilt 24 Monate, Datenschutz bei KI-Nutzung 12 Monate, gerechnet bis zum Stichtag 31.12.2025."}
  - {station: Dein Bericht, text: "Anteil der Mitarbeitenden mit gültiger Schulung."}
beispielfragen:
  - Wie viele Mitarbeitende haben die Pflichtschulungen?
  - Wie viele Hochrisiko-Nutzer haben keine gültige Grundlagenschulung?
  - Wie lange ist eine Schulung gültig?
nicht_verwechseln:
  - "Teilnahme: Ein Kurs, der länger als die Gültigkeit zurückliegt, zählt als abgelaufen und nicht als absolviert."
  - "Ausgetretene: Sie zählen nicht zur Grundgesamtheit (202 Personen im Haus, nicht 220)."
werte:
  schulung_nutzer_im_haus: "202"
  schulung_c1_prozent: "67,3"
  schulung_c2_prozent: "41,6"
  schulung_beide_anzahl: "53"
  schulung_beide_prozent: "26,2"
  schulung_unbekannte_nutzer: "3"
  schulung_doppelt_erfasst: "5"
  hochrisiko_nutzer_dezember: "202"
  hochrisiko_ohne_grundlagen: "66"
  hochrisiko_ohne_grundlagen_prozent: "32,7"
---

## Das sagt die Zahl

Zum Stichtag 31.12.2025 sind **202** Personen im Unternehmen.

- **67,3 %** haben die gültige Schulung **KI-Grundlagen**
- **41,6 %** haben die gültige Schulung **Datenschutz bei KI-Nutzung**
- **26,2 %** (53 Personen) haben **beide** Pflichtschulungen gültig

Besonders wichtig für Compliance: Von den **202** Personen, die im Dezember einen Hochrisiko-Anwendungsfall genutzt haben, fehlt **66** (**32,7 %**) die gültige Grundlagenschulung.

## Darf ich mich darauf verlassen?

**Mit Vorsicht.**

- **3 Nachweise** gehören zu Nutzer-Nummern, die es nicht gibt, und werden nicht gezählt. **5 Nachweise** sind doppelt erfasst.
- In den Beispieldaten haben praktisch alle Personen im Dezember einen Hochrisiko-Anwendungsfall genutzt, weil die Anwendungsfälle zufällig verteilt sind. In der Praxis wäre die Gruppe kleiner.
- Der Katalog nennt Pflichtschulungen im Sinn des internen Programms. Das ist keine Rechtsaussage zum EU AI Act.
- **Nicht geeignet für:** personenbezogene Einzelentscheidungen. Die Auswertung zeigt Zahlen, keine Namen.

## So wird gerechnet

Grundgesamtheit: Personen ohne Austrittsdatum. Eine Schulung gilt als **gültig**, wenn der Abschluss weniger Monate zurückliegt als die Gültigkeit (24 Monate bei KI-Grundlagen, 12 bei Datenschutz), gerechnet bis zum Stichtag. Die Quote ist gültige Schulungen geteilt durch Personen im Haus.

## Wer hilft?

- **Fachlich:** Personalentwicklung
- **Zur Berechnung:** BI-Team
- **Kanal:** #ki-daten-hilfe

## Was hat sich geändert?

- 18.11.2026: Karte neu im Katalog. Die Schulungsdateien sind neue Quellen.
