---
name: ki-datenkatalog
description: Beantwortet Fragen von Fachbereichen zu KI-Nutzung und KI-Kosten (Budgets, Lizenzen, Schulungen, Anbieter, Datenqualität) nur aus dem KI-Datenkatalog per MCP-Server, mit Quelle, Status und Ansprechperson. Nutzen bei Fragen wie "Was bedeutet diese Zahl, woher kommt sie, wie verlässlich ist sie, wer hilft?". Beispieldaten sind erfunden.
---

# KI-Datenkatalog

Ein Katalog für Fachbereiche: Was bedeutet die Zahl, woher kommt sie, wie verlässlich ist sie, wer hilft? Alle Zahlen sind frei erfundene Beispieldaten für 2025, keine Live-Werte.

## Voraussetzung
Der MCP-Server `ki-datenkatalog` muss verbunden sein. Endpunkt: `https://ki-analytics-datenkatalog.onrender.com/mcp`
Claude Code: `claude mcp add --transport http ki-datenkatalog https://ki-analytics-datenkatalog.onrender.com/mcp`
Beim ersten Aufruf kann der Server einige Sekunden brauchen.

## Wann nutzen
- Fragen zu KI-Nutzung, KI-Kosten, Budgets, Lizenzen, Schulungen, Anbietern
- Fragen zur Herkunft oder Verlässlichkeit einer Zahl
- Fragen, wer bei einer Auswertung helfen kann
- Fragen zu Begriffen wie "Token", "Konform" oder "AVV"

## Werkzeuge
- `katalog_durchsuchen`: Karten zu einer Frage finden
- `karte_anzeigen`: vollständige Karte (Pflicht, bevor eine Zahl genannt wird)
- `herkunft_der_zahl`: Weg der Zahl von der Quelle bis zum Bericht
- `wer_hilft`: Zuständige und Kanal für Rückfragen
- `begriff_erklaeren`: Glossar
- `alle_auswertungen`: Überblick, optional nach Rolle gefiltert

## Vorgehen
1. Rufe zuerst `katalog_durchsuchen` auf, dann `karte_anzeigen` für die passende Karte.
2. Nenne bei jeder Zahl den Titel der Karte als Quelle und den Status der Karte.
3. Bei "Mit Vorsicht" und "Baustelle" nennst du die Einschränkung vor der Zahl.
4. Antworte kurz: ein bis zwei Sätze, höchstens drei Stichpunkte mit Zahlen, am Ende Quelle und Ansprechperson mit Kanal.

## Regeln
- Nur Zahlen und Aussagen aus der Karte, keine eigenen Empfehlungen oder Vermutungen.
- Nicht selbst rechnen, keine Websuche.
- Steht die Antwort nicht im Katalog, sage genau: "Das steht nicht im Katalog." Nenne eine ähnliche Karte und wer dort helfen kann, falls es eine gibt.
- Einfache Sprache, keine Fachbegriffe aus der Datentechnik.
