# KI-Datenkatalog für Fachbereiche

**Woher kommt diese Zahl? Der Katalog sagt es, und ein Chat kann ihn befragen.**

Ein Beispielkatalog zu KI-Nutzung und KI-Kosten, geschrieben für Fachbereiche und nicht für Informatiker. Zu jeder Zahl steht: was sie bedeutet, wie sie berechnet wird, woher sie kommt, ob man sich darauf verlassen darf und wer helfen kann.

Dazu gehört ein kleiner MCP-Server. Damit kann ein Chat wie Claude den Katalog lesen und Fragen daraus beantworten. Er nennt die Karte als Quelle und sagt "Das steht nicht im Katalog.", wenn etwas fehlt.

*Von Lea Zimmer · [LinkedIn](https://www.linkedin.com/in/leazimmer)*

## Das Wichtigste in drei Punkten

1. **Zehn Karten, jede passt auf einen Bildschirm.** Fragen als Titel, Status mit klarer Bedeutung (Verlässlich, Mit Vorsicht, Baustelle), Herkunft der Zahl in vier bis fünf Stationen.
2. **Jede Zahl ist nachgerechnet.** Ein Test rechnet alle Zahlen aus den Beispieldaten neu und vergleicht sie mit dem Text der Karten.
3. **Der Chat darf nicht raten.** Testfragen mit vorher festgelegten Antworten, darunter vier Fallen, prüfen das.

## Was im Katalog steht

| Karte | Frage | Status |
|---|---|---|
| Kosten je Abteilung | Was kostet KI pro Abteilung und Monat? | Mit Vorsicht |
| Aktive Nutzer | Wie viele Mitarbeitende nutzen KI wirklich aktiv? | Verlässlich |
| Freigabe und Konformität | Welche Anwendungsfälle sind freigegeben und dokumentiert? | Verlässlich |
| Kosten je Anwendungsfall | Welche Anwendungsfälle sind je Anfrage am teuersten? | Mit Vorsicht |
| Datenqualität | Wo sind die Daten unsauber? | Verlässlich |
| Budget gegen Ist | Liegen wir mit den KI-Kosten im Budget? | Mit Vorsicht |
| Ungenutzte Lizenzen | Welche bezahlten Lizenzen werden nicht genutzt? | Mit Vorsicht |
| Schulungsquote | Wer ist für die KI-Nutzung geschult? | Mit Vorsicht |
| Anbieter und Datenstandort | Wohin gehen unsere Daten, und ist der Vertrag in Ordnung? | Verlässlich |
| Gesamtkosten | Was kostet uns KI insgesamt? | Baustelle |

Dazu ein Glossar mit 21 Begriffen (jeder nennt, womit er nicht zu verwechseln ist) und eine Beschreibung aller elf Datenquellen.

Die Karten stehen als Markdown-Dateien in [`katalog/auswertungen/`](katalog/auswertungen). Man kann sie direkt auf GitHub lesen.

## Datenbasis

Alle Daten sind frei erfundene Beispieldaten für das Jahr 2025 (Startwert 42). Es gibt keinen Bezug zu realen Unternehmen, Anbietern oder Personen.

- **Fünf Quellen** sind identisch mit den Projekten [ki-nutzung-kosten-analytics](https://github.com/lea-zimmer-data/ki-nutzung-kosten-analytics) (Snowflake, dbt) und [ki-nutzung-kosten-lakehouse](https://github.com/lea-zimmer-data/ki-nutzung-kosten-lakehouse) (Databricks): Nutzungsereignisse, Nutzer, Abteilungen, Anwendungsfälle, Modelle mit Preisen. Das Skript `scripts/generate_data.py` ist von dort übernommen und unverändert. Die bekannten Zahlen (281,52 € Kosten, 54.098 erfolgreiche Anfragen, 139 / 1.102 / 174 / 5 Datenqualitätsfunde) stimmen deshalb mit den beiden Projekten überein, und ein Test prüft das.
- **Sechs Quellen** sind für diesen Katalog neu (`scripts/generate_zusatzdaten.py`): Budgets, Anbieter mit Datenstandort und Vertrag, Modell-Zuordnung, Lizenzen, Schulungskurse und Schulungsnachweise. Sie liegen nur als CSV vor und sind in den beiden anderen Projekten noch nicht eingebunden.

In die neuen Quellen sind bewusst Probleme eingebaut, die der Katalog offen nennt: Budgetlücke bei Personal (Oktober bis Dezember), doppelte Lizenzen, Schulungsnachweise für unbekannte Nutzer.

## Ausprobieren

```bash
git clone https://github.com/lea-zimmer-data/ki-analytics-datenkatalog
cd ki-analytics-datenkatalog
pip install -r requirements-dev.txt

python scripts/generate_data.py          # schreibt data/raw/
python scripts/generate_zusatzdaten.py   # ergänzt data/raw/
python scripts/kennzahlen.py             # rechnet alle Zahlen des Katalogs neu

pytest                                   # 45 Tests: Zahlen, Aufbau, Testfragen, Fallen
python -m server.app                     # Webseite auf http://localhost:8000, MCP auf /mcp
```

Der Server selbst braucht die Daten nicht. Er liest nur den Ordner `katalog/`.

## Den Chat anschließen

1. **Server auf Render einrichten:** Repository mit Render verbinden, "New → Blueprint", `render.yaml` wird erkannt (Gratis-Tarif, Frankfurt). Nach dem Deployment die Adresse des Dienstes aufrufen: Die Webseite erscheint.
2. **Aufwecken:** Im Gratis-Tarif schläft der Dienst nach 15 Minuten. Vor einem Test `…/health` aufrufen und auf `{"status":"ok"}` warten.
3. **In Claude** (claude.ai oder Claude Desktop, VS Code wird dafür nicht gebraucht): Anpassen › Konnektoren, Plus, "Benutzerdefinierten Konnektor hinzufügen", Name vergeben und die Adresse `https://<dein-dienst>.onrender.com/mcp` eintragen. Das geht in allen Tarifen, im Gratis-Tarif mit einem Konnektor. Danach den Konnektor im Chat einschalten. Claude verbindet sich aus der Cloud von Anthropic, nicht von deinem Rechner.
   *Alternative im Terminal oder in VS Code mit Claude Code:* `claude mcp add --transport http ki-datenkatalog https://<dein-dienst>.onrender.com/mcp`
4. **Fragen stellen**, zum Beispiel: "Sind wir 2025 im Budget geblieben?" Das Prüfblatt mit zehn Fragen steht in [`docs/chat-pruefung.md`](docs/chat-pruefung.md).

Der Server hat sechs Werkzeuge, alle nur lesend: `katalog_durchsuchen`, `karte_anzeigen`, `herkunft_der_zahl`, `wer_hilft`, `begriff_erklaeren`, `alle_auswertungen`. Er hat keine Zugangsdaten und keine Datenbank. Der Katalog ist öffentlich, deshalb ist die Prüfung des Host-Namens abgeschaltet (sonst würden Anfragen über die Render-Adresse abgelehnt).

## Aufbau

```
katalog/
  auswertungen/*.md     die zehn Karten (Kopf mit Status, Herkunft, Zuständigen, Zahlen)
  glossar.md            Begriffe mit Abgrenzung
  datenquellen.md       alle elf Quellen
  kennzahlen.json       nachgerechnete Zahlen (erzeugt von scripts/kennzahlen.py)
scripts/                Generatoren und Nachrechnung
server/                 MCP-Server und Webseite (ein Dienst)
tests/                  Tests und Testfragen mit festen Antworten
docs/chat-pruefung.md   Prüfblatt für den Chat
render.yaml             Blueprint für Render
```

## Ehrliche Einordnung

- **Der Chat ist ein Machbarkeitsnachweis, kein fertiges Produkt.** In einer Firma würde die BI oder IT den Anschluss einmal einrichten, der Server müsste dauerhaft laufen, und der Chat-Anbieter ist austauschbar.
- **Der Katalog liefert keine Live-Zahlen.** Er erklärt Zahlen. Die Werte stehen als Beispiel auf den Karten und stammen aus den Beispieldaten.
- **Die Pflege der Texte ist die eigentliche Arbeit.** Wer erklärt, was eine Zahl bedeutet, wer aktuell hält und wer bei Lücken zuständig ist, entscheidet, ob ein Katalog nützt. Die Technik ist dagegen klein.
- **Erfunden sind:** alle Daten, Anbieter, Verträge, Rollen und der Kanal `#ki-daten-hilfe`.
- **Bewusst nicht gebaut:** Sterne, Punkte und Beliebtheitslisten. Ohne echte Nutzung dahinter wären sie erfunden. "Für dich" und "Zuletzt angesehen" bleiben im Browser der Besucherin.
- **Rechtliches:** Risikoklassen, Pflichtschulungen und Verträge sind angelehnt an Begriffe aus dem EU AI Act und dem Datenschutz. Der Katalog ersetzt keine Rechtsprüfung.

## Entstehung

Den Code hat Claude geschrieben. Die Fachfragen, die Regeln und die Entscheidung, was eine Zahl bedeutet, kamen von Lea Zimmer.

## Lizenz

MIT, siehe [LICENSE](LICENSE).
