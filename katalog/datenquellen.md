# Datenquellen

Alle Quellen sind frei erfundene Beispieldaten (Startwert 42). Die ersten fünf sind identisch mit den Projekten `ki-nutzung-kosten-analytics` und `ki-nutzung-kosten-lakehouse`. Die letzten sechs sind für diesen Katalog neu.

## usage_events.csv
Inhalt: Jede KI-Anfrage mit Nutzer, Anwendungsfall, Modell, Token, Status. 55.861 Zeilen, davon 139 doppelt.
Zuständig: Quellsystem / IT
Aktualisierung: täglich (Beispiel)
Bekannte Probleme: Duplikate, fehlende Anwendungsfälle, Nutzung nach Austritt.
Genutzt in: kosten-je-abteilung, aktive-nutzer, kosten-je-anwendungsfall, datenqualitaet, anbieter-datenstandort

## users.csv
Inhalt: 220 Nutzer mit Abteilung, Eintritt, Austritt.
Zuständig: Personal / Stammdaten
Aktualisierung: bei Eintritt und Austritt
Bekannte Probleme: 5 Nutzer mit unbekannter Abteilung.
Genutzt in: kosten-je-abteilung, aktive-nutzer, datenqualitaet, ungenutzte-lizenzen, schulungsquote

## departments.csv
Inhalt: 8 Abteilungen mit Kostenstelle.
Zuständig: Controlling
Aktualisierung: selten
Bekannte Probleme: keine.
Genutzt in: kosten-je-abteilung, budget-gegen-ist

## use_cases.csv
Inhalt: 15 Anwendungsfälle mit Risikoklasse, Status, Freigabedatum, Dokumentationsstand.
Zuständig: KI-Verantwortliche
Aktualisierung: bei Freigabe
Bekannte Probleme: Risikoklassen in den Beispieldaten zufällig vergeben.
Genutzt in: freigabe-konformitaet, kosten-je-anwendungsfall, schulungsquote

## ai_models.csv
Inhalt: 3 Modelle mit Preis je 1.000 Eingabe- und Ausgabe-Token. Das ist die Preisliste.
Zuständig: Einkauf
Aktualisierung: bei Preisänderung
Bekannte Probleme: keine.
Genutzt in: kosten-je-abteilung, kosten-je-anwendungsfall, anbieter-datenstandort

## budgets.csv
Inhalt: Monatsbudget je Abteilung für 2025. 93 Zeilen.
Zuständig: Controlling
Aktualisierung: jährlich
Bekannte Probleme: Für Personal fehlen Oktober bis Dezember.
Genutzt in: budget-gegen-ist

## ai_providers.csv
Inhalt: 3 Anbieter mit Datenstandort, AVV-Status und Vertragsende.
Zuständig: Einkauf und Datenschutz
Aktualisierung: bei Vertragsänderung
Bekannte Probleme: keine. Die Angaben sind erfunden.
Genutzt in: anbieter-datenstandort

## model_providers.csv
Inhalt: Zuordnung der 3 Modelle zu ihrem Anbieter.
Zuständig: Einkauf
Aktualisierung: bei neuem Modell
Bekannte Probleme: keine.
Genutzt in: anbieter-datenstandort

## licenses.csv
Inhalt: 119 vergebene Lizenzen mit Nutzer, Vergabe, letztem Login und Monatspreis.
Zuständig: IT-Einkauf (Lizenzverwaltung)
Aktualisierung: täglich (Beispiel)
Bekannte Probleme: 4 Nutzer mit zwei Lizenzen, 13 Lizenzen für ausgetretene Personen.
Genutzt in: ungenutzte-lizenzen, gesamtkosten

## training_courses.csv
Inhalt: 3 Kurse mit Pflichtkennzeichen und Gültigkeit in Monaten.
Zuständig: Personalentwicklung
Aktualisierung: selten
Bekannte Probleme: keine.
Genutzt in: schulungsquote

## training_completions.csv
Inhalt: Abgeschlossene Kurse je Person mit Datum. 349 Zeilen.
Zuständig: Personalentwicklung
Aktualisierung: laufend (Beispiel)
Bekannte Probleme: 3 Nachweise für unbekannte Nutzer, 5 doppelt erfasst.
Genutzt in: schulungsquote
