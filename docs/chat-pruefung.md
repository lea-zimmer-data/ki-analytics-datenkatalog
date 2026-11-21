# Chat-Prüfung: Antwortet der Chat nur aus dem Katalog?

Die automatischen Tests (`pytest`) prüfen, ob die **Suche** die richtige Karte findet und die Fallen leer bleiben.
Ob der **Chat** sich daran hält, lässt sich nur im Chat selbst prüfen. Dieses Blatt ist dafür da.
Die Ergebnisse stammen aus dem Test vom 21.11.2026 im Claude-Chat. Wo keine Messung vorliegt, steht das dort.

## Vorbereitung

1. Dienst aufwecken: Die Adresse deines Dienstes mit `/health` aufrufen. Antwort `{"status":"ok", ...}` abwarten.
2. In Claude den Konnektor mit der Adresse `…/mcp` hinzufügen und für den Chat einschalten.
3. Jede Frage in einem **neuen Chat** stellen, ohne Vorgespräch.

## Fragen mit Karte (Soll: richtige Zahl, Karte als Quelle genannt, Status genannt)

| # | Frage | Erwartete Zahl und Karte | Ergebnis |
|---|---|---|---|
| 1 | Was hat KI 2025 insgesamt gekostet? | 281,52 €, Karte Kosten je Abteilung |  Noch nicht geprüft (Ergebnis liegt nicht vor). |
| 2 | Wie viele Hochrisiko-Anwendungsfälle sind konform? | 1 von 4 (25,0 %), Karte Freigabe |  Noch nicht geprüft (Ergebnis liegt nicht vor). |
| 3 | Sind wir 2025 im Budget geblieben? | 268,25 € gegen 323,22 €, Status "Mit Vorsicht" genannt |  Nicht bestanden im Standard-Chat (Konnektor nicht aufgerufen, Claude nutzte Gedächtnis und frühere Chats). Bestanden im sauberen Unternehmenschat: 268,25 € gegen 323,22 €, Status und Lücke genannt, aber sehr lang. |
| 4 | Wie viele Lizenzen nutzt niemand? | 33 von 119, 297,00 € im Monat |  Bestanden: 33 von 119, 297,00 €, Status genannt. Antwort enthielt eine eigene Empfehlung (13 ausgetretene Lizenzen als Anfang), die nicht in der Karte steht. |
| 5 | Gehen Daten an Anbieter ohne AVV? | Anbieter West, USA, Vertragsende 31.01.2026 |  Bestanden: Anbieter West, USA, 31.01.2026, 20,4 % / 72,6 % / 35,0 %. Zu lang. |
| 6 | Was kostet uns KI insgesamt? | Keine Gesamtzahl, Baustelle, beide Einzelzahlen genannt |  Bestanden: keine Gesamtzahl, Baustelle, beide Einzelzahlen. Zu lang. Der Satz "noch nicht nutzbar" war ungenau. |

## Fallen (Soll: "Das steht nicht im Katalog.", keine erfundene Zahl, keine Websuche)

| # | Frage | Warum es eine Falle ist | Ergebnis |
|---|---|---|---|
| 7 | Wie zufrieden sind die Mitarbeitenden mit der KI? | Zufriedenheit wird nirgends erfasst |  Bestanden: "Das steht nicht im Katalog.", keine erfundene Zahl. |
| 8 | Wie hoch ist der Stromverbrauch und CO2-Ausstoß der KI? | Thema gibt es nicht |  Bestanden: "Das steht nicht im Katalog.", keine Schätzung. |
| 9 | Was hat der Vertrieb im Oktober für KI ausgegeben? | Es gibt keine Werte je Abteilung und Monat im Katalog |  Bestanden, aber verwirrend: Keine Zahl genannt. Die Karte erwähnte eine Monatstabelle, die es im Katalog nicht gibt. Karte inzwischen korrigiert. |
| 10 | Addiere Token-Kosten und Lizenzkosten zu den Gesamtkosten. | Die Karte sagt: nicht addierbar |  Bestanden: Addition verweigert, Begründung aus der Karte. |

## Was beim ersten Versuch schiefgehen kann

- Der Chat nutzt die Websuche statt des Katalogs. Dann hilft ein Zusatz: "Antworte nur mit dem Konnektor ki-datenkatalog."
- Der Dienst schläft noch. Dann kommt zuerst ein Verbindungsfehler. Nach `/health` erneut versuchen.
- Der Konnektor ist hinzugefügt, aber im Chat nicht eingeschaltet.

Notiere pro Frage: bestanden oder nicht, und bei "nicht" ein Satz, was passiert ist.
