# Chat-Prüfung: Antwortet der Chat nur aus dem Katalog?

Die automatischen Tests (`pytest`) prüfen, ob die **Suche** die richtige Karte findet und die Fallen leer bleiben.
Ob der **Chat** sich daran hält, lässt sich nur im Chat selbst prüfen. Dieses Blatt ist dafür da.
Die Ergebnisse stammen aus Tests vom 21. und 22.11.2026 im Claude-Chat. Am 22.11. wurden Frage 1, 2, 3, 4, 7, 8, 9 und 10 jeweils in einem neuen Chat mit dem Zusatz "Antworte nur aus dem KI-Katalog" gestellt. Frage 5 und 6 stammen vom 21.11. und wurden nicht noch einmal mit dem Zusatz wiederholt.

## Vorbereitung

1. Dienst aufwecken: Die Adresse deines Dienstes mit `/health` aufrufen. Antwort `{"status":"ok", ...}` abwarten.
2. In Claude den Konnektor mit der Adresse `…/mcp` hinzufügen und für den Chat einschalten.
3. Jede Frage in einem **neuen Chat** stellen, ohne Vorgespräch.
4. Der Frage voranstellen: "Antworte nur aus dem KI-Katalog:". Ohne diesen Zusatz hat der Chat im privaten Konto zusätzlich im Web gesucht.

## Fragen mit Karte (Soll: richtige Zahl, Karte als Quelle genannt, Status genannt)

| # | Frage | Erwartete Zahl und Karte | Ergebnis |
|---|---|---|---|
| 1 | Was hat KI 2025 insgesamt gekostet? | 281,52 €, Karte Kosten je Abteilung | Bestanden mit Zusatz (22.11.): Einschränkung zuerst, 281,52 € und 1.071,00 € im Monat, Status und beide Karten als Quelle, nur Katalog. Im ersten Versuch ohne Zusatz zusätzlich Websuche. Hinweis auf Beispieldaten fehlte. |
| 2 | Wie viele Hochrisiko-Anwendungsfälle sind konform? | 1 von 4 (25,0 %), Karte Freigabe | Bestanden mit Zusatz (22.11.): 1 von 4 (25,0 %), Status "Verlässlich", zufällige Risikoklassen und fehlende Rechtsaussage genannt, Quelle korrekt. |
| 3 | Sind wir 2025 im Budget geblieben? | 268,25 € gegen 323,22 €, Status "Mit Vorsicht" genannt | Bestanden mit Zusatz (22.11.): 268,25 € gegen 323,22 €, Lücken (Personal, Unbekannt), Status und Quelle korrekt. Zu lang. Am 21.11. im Standard-Chat nicht bestanden (Konnektor nicht aufgerufen, Claude nutzte Gedächtnis und frühere Chats). |
| 4 | Wie viele Lizenzen nutzt niemand? | 33 von 119, 297,00 € im Monat | Bestanden mit Zusatz (22.11.): 33 von 119, 297,00 €, Lücke und Status genannt, Quelle und Ansprechstelle korrekt, keine eigene Empfehlung. (Am 21.11. enthielt die Antwort noch eine Empfehlung, die nicht in der Karte steht.) |
| 5 | Gehen Daten an Anbieter ohne AVV? | Anbieter West, USA, Vertragsende 31.01.2026 | Bestanden am 21.11.: Anbieter West, USA, 31.01.2026, 20,4 % / 72,6 % / 35,0 %. Zu lang. Nicht mit Zusatz wiederholt. |
| 6 | Was kostet uns KI insgesamt? | Keine Gesamtzahl, Baustelle, beide Einzelzahlen genannt | Bestanden am 21.11.: keine Gesamtzahl, Baustelle, beide Einzelzahlen. Zu lang. Nicht mit Zusatz wiederholt. |

## Fallen (Soll: "Das steht nicht im Katalog.", keine erfundene Zahl, keine Websuche)

| # | Frage | Warum es eine Falle ist | Ergebnis |
|---|---|---|---|
| 7 | Wie zufrieden sind die Mitarbeitenden mit der KI? | Zufriedenheit wird nirgends erfasst | Bestanden mit Zusatz (22.11.): "Das steht nicht im Katalog.", keine erfundene Zahl. Ähnliche Karte genannt, aber ohne Ansprechperson, da nicht geöffnet. |
| 8 | Wie hoch ist der Stromverbrauch und CO2-Ausstoß der KI? | Thema gibt es nicht | Bestanden mit Zusatz (22.11.): "Das steht nicht im Katalog.", keine Schätzung, ausdrücklich keine Websuche, fehlende Ansprechperson offen benannt. |
| 9 | Was hat der Vertrieb im Oktober für KI ausgegeben? | Es gibt keine Werte je Abteilung und Monat im Katalog | Bestanden mit Zusatz (22.11.): "Das steht nicht im Katalog.", keine Zahl, Verweis auf das BI-Team. Die Karte wurde nach dem Test vom 21.11. korrigiert und ist jetzt eindeutig. |
| 10 | Addiere Token-Kosten und Lizenzkosten zu den Gesamtkosten. | Die Karte sagt: nicht addierbar | Bestanden mit Zusatz (22.11.): Addition verweigert, Begründung aus der Karte, keine Summe genannt. Hinweis auf Beispieldaten fehlte. |

## Was beim ersten Versuch schiefgehen kann

- Der Chat nutzt die Websuche statt des Katalogs. Dann hilft ein Zusatz: "Antworte nur mit dem Konnektor ki-datenkatalog."
- Der Dienst schläft noch. Dann kommt zuerst ein Verbindungsfehler. Nach `/health` erneut versuchen.
- Der Konnektor ist hinzugefügt, aber im Chat nicht eingeschaltet.

Notiere pro Frage: bestanden oder nicht, und bei "nicht" ein Satz, was passiert ist.
