"""MCP-Server und Webseite des KI-Datenkatalogs in einer Anwendung.

Der Server liest nur den Katalog (Markdown-Dateien). Er braucht keine Datenbank und keine
Zugangsdaten. Er gibt nur Katalogtexte weiter, nennt die Quelle und sagt, wenn etwas nicht
im Katalog steht.

Start lokal:   python -m server.app
Start Render:  uvicorn server.app:app --host 0.0.0.0 --port $PORT
Adressen:      /          Webseite
               /mcp       MCP-Endpunkt (Streamable HTTP) für den Chat
               /health    Lebenszeichen für Render
"""

import os

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from server import katalog, seite

ANWEISUNG = """\
Du beantwortest Fragen von Fachbereichen zu KI-Nutzung und KI-Kosten ausschließlich aus diesem Katalog.

1. Rufe zuerst katalog_durchsuchen auf und danach karte_anzeigen für die passende Karte.
2. Nenne bei jeder Zahl den Titel der Karte als Quelle.
3. Nenne den Status der Karte. Bei "Mit Vorsicht" und bei "Baustelle" nennst du die Einschränkung, bevor du die Zahl nennst.
4. Steht die Antwort nicht im Katalog, sage genau: "Das steht nicht im Katalog." Nenne, falls es eine ähnliche Karte gibt, diese Karte und wer dort helfen kann. Rate nicht, rechne nicht selbst und nutze keine Websuche.
5. Alle Zahlen sind frei erfundene Beispieldaten für das Jahr 2025, keine Live-Werte.
6. Antworte in einfacher Sprache ohne Fachbegriffe aus der Datentechnik.
7. Antworte kurz, so wie ein Controller es lesen will: Zuerst ein bis zwei Sätze mit der Antwort (bei "Mit Vorsicht" und "Baustelle" mit der Einschränkung zuerst). Danach höchstens drei Stichpunkte mit Zahlen. Zum Schluss eine Zeile mit Quelle (Titel der Karte) und Ansprechperson mit Kanal. Liefere nichts Zusätzliches, solange nicht danach gefragt wird.
8. Gib nur Zahlen und Aussagen wieder, die in der Karte stehen. Eigene Empfehlungen und Vermutungen gehören nicht in die Antwort.
"""

NUR_LESEN = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)

mcp = FastMCP(
    "ki-datenkatalog",
    instructions=ANWEISUNG,
    host="0.0.0.0",
    stateless_http=True,
    json_response=True,
    # Der Katalog ist öffentlich und enthält nur erfundene Beispieldaten. Ohne diese Zeile
    # lehnt der Server Anfragen mit der Render-Adresse als Host ab.
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)

NICHT_IM_KATALOG = "Das steht nicht im Katalog."


@mcp.tool(annotations=NUR_LESEN)
def katalog_durchsuchen(frage: str) -> str:
    """Sucht in den Karten des Katalogs nach einer Frage in Alltagssprache, zum Beispiel
    "Was kostet KI pro Abteilung?". Gibt passende Karten mit Kurzantwort und Status zurück.
    Wenn nichts passt, lautet die Antwort "Das steht nicht im Katalog."."""
    treffer = katalog.suche(frage)
    if not treffer:
        return NICHT_IM_KATALOG + " Es gibt keine Karte zu dieser Frage. Mit alle_auswertungen siehst du, was der Katalog enthält."
    zeilen = [f"Passende Karten ({len(treffer)}):"]
    for t in treffer:
        zeilen.append(f"- {t['id']} | {t['titel']} | Status: {t['status']}\n  Kurzantwort: {t['kurzantwort']}")
    zeilen.append("Rufe karte_anzeigen mit der Karten-ID auf, bevor du eine Zahl nennst.")
    return "\n".join(zeilen)


@mcp.tool(annotations=NUR_LESEN)
def karte_anzeigen(karte_id: str) -> str:
    """Zeigt eine vollständige Karte: Kurzantwort, Status, ob man sich darauf verlassen darf,
    Rechenregel, Herkunft der Zahl, Zuständige. Die Karten-ID kommt aus katalog_durchsuchen."""
    k = katalog.karten().get(karte_id)
    if not k:
        return f"{NICHT_IM_KATALOG} Die Karten-ID '{karte_id}' gibt es nicht. Gültig sind: {', '.join(katalog.karten())}."
    return k.volltext()


@mcp.tool(annotations=NUR_LESEN)
def herkunft_der_zahl(karte_id: str) -> str:
    """Beantwortet "Woher kommt diese Zahl?" für eine Karte als Folge von Stationen
    von der Quelle bis zum Bericht."""
    k = katalog.karten().get(karte_id)
    if not k:
        return f"{NICHT_IM_KATALOG} Die Karten-ID '{karte_id}' gibt es nicht."
    z = [f"Herkunft der Zahl: {k.titel}"]
    z += [f"{i}. {s['station']}: {s['text']}" for i, s in enumerate(k.meta["herkunft"], 1)]
    z.append(f"Quelle im Katalog: katalog/auswertungen/{k.id}.md")
    return "\n".join(z)


@mcp.tool(annotations=NUR_LESEN)
def wer_hilft(karte_id: str) -> str:
    """Nennt die Zuständigen und den Kanal für Rückfragen zu einer Karte."""
    k = katalog.karten().get(karte_id)
    if not k:
        return f"{NICHT_IM_KATALOG} Die Karten-ID '{karte_id}' gibt es nicht."
    m = k.meta
    return (f"{k.titel}\nFachlich zuständig: {m['zustaendig_fachlich']}\nFür die Berechnung: {m['zustaendig_zahlen']}\n"
            f"Rückfragen im Kanal: {m['rueckfragen']}\n(Rollen und Kanal sind in den Beispieldaten erfunden.)")


@mcp.tool(annotations=NUR_LESEN)
def begriff_erklaeren(begriff: str) -> str:
    """Erklärt einen Begriff aus dem Glossar, zum Beispiel "Token", "Konform" oder "AVV",
    und sagt, womit er nicht zu verwechseln ist."""
    e = katalog.finde_begriff(begriff)
    if not e:
        return f"{NICHT_IM_KATALOG} Der Begriff '{begriff}' steht nicht im Glossar."
    return e.volltext()


@mcp.tool(annotations=NUR_LESEN)
def alle_auswertungen(fuer: str = "") -> str:
    """Listet alle Karten des Katalogs. Optional gefiltert nach Rolle: Controlling,
    Abteilungsleitung, Compliance & Datenschutz, Personal oder Einkauf & IT."""
    karten = katalog.alle_fuer(fuer or None)
    if not karten:
        return f"{NICHT_IM_KATALOG} Für '{fuer}' gibt es keine Karten. Rollen: {', '.join(katalog.ROLLEN)}."
    return "\n".join(f"- {k.id} | {k.titel} | Status: {katalog.STATUS[k.status][0]}" for k in karten)


# ---------------- Webseite ----------------

@mcp.custom_route("/", methods=["GET"])
async def start(request: Request) -> HTMLResponse:
    return HTMLResponse(seite.startseite())


@mcp.custom_route("/karte/{karte_id}", methods=["GET"])
async def karte(request: Request) -> HTMLResponse:
    html = seite.kartenseite(request.path_params["karte_id"])
    return HTMLResponse(html or seite.nicht_gefunden(), status_code=200 if html else 404)


@mcp.custom_route("/glossar", methods=["GET"])
async def glossar(request: Request) -> HTMLResponse:
    return HTMLResponse(seite.glossarseite())


@mcp.custom_route("/ueber", methods=["GET"])
async def ueber(request: Request) -> HTMLResponse:
    return HTMLResponse(seite.ueberseite())


@mcp.custom_route("/suche", methods=["GET"])
async def suche(request: Request) -> HTMLResponse:
    return HTMLResponse(seite.suchseite(request.query_params.get("q", "")))


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "karten": len(katalog.karten()), "begriffe": len(katalog.glossar())})


app = mcp.streamable_http_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
