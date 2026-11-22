"""Liest den Katalog aus den Markdown-Dateien und beantwortet Suchanfragen.

Der Katalog liegt als Text im Ordner `katalog/`. Dieser Code liest nur, er rechnet nichts
und erfindet nichts. Wenn etwas nicht im Katalog steht, sagt er das.
"""

from __future__ import annotations

import re
from datetime import date
from functools import lru_cache
from pathlib import Path

import yaml

KATALOG = Path(__file__).resolve().parent.parent / "katalog"
ABSCHNITTE = [
    "Das sagt die Zahl",
    "Darf ich mich darauf verlassen?",
    "So wird gerechnet",
    "Wer hilft?",
    "Was hat sich geändert?",
]
STATUS = {
    "verlaessig": ("Verlässlich", "Nachgerechnet, keine bekannte Lücke, die die Zahl verändert."),
    "mit-vorsicht": ("Mit Vorsicht", "Nachgerechnet, aber mit einer benannten Lücke. Lies den Abschnitt dazu."),
    "baustelle": ("Baustelle", "Noch nicht nutzbar. Die Karte erklärt, was fehlt."),
}
ROLLEN = ["Controlling", "Abteilungsleitung", "Compliance & Datenschutz", "Personal", "Einkauf & IT"]
STOPWOERTER = set("""
aber alle als also auch auf aus bei bin bis das dass dem den der des die dies diese doch dort durch ein eine
einem einen einer eines for gibt hab habe haben hat hier ihr ich ist ihre kann kein keine man mehr mein mit nach
nicht noch nur oder ohne sind soll uns und unser unsere von war warum was wer wie wir wird wo wurde zum zur
wieviel viele viel gab gibt gehen geht welche welcher welches wann wenn muss
""".split())


def normalisiere(text: str) -> str:
    t = text.lower()
    for a, b in (("ä", "a"), ("ö", "o"), ("ü", "u"), ("ß", "ss"), ("ae", "a"), ("oe", "o"), ("ue", "u")):
        t = t.replace(a, b)
    return t


def stamm(wort: str) -> str:
    for suffix in ("ungen", "ung", "heit", "keit", "et", "en", "er", "es", "st", "e", "n", "s", "t"):
        if wort.endswith(suffix) and len(wort) - len(suffix) >= 4:
            return wort[: -len(suffix)]
    return wort


def woerter(text: str) -> list[str]:
    roh = re.findall(r"[a-z0-9]+", normalisiere(text))
    return [stamm(w) for w in roh if len(w) >= 3 and w not in STOPWOERTER]


def passt(a: str, b: str) -> bool:
    if a == b:
        return True
    k, l = (a, b) if len(a) <= len(b) else (b, a)
    return len(k) >= 5 and l.startswith(k)


class Karte:
    def __init__(self, pfad: Path):
        text = pfad.read_text(encoding="utf-8")
        _, kopf, rumpf = text.split("---", 2)
        self.meta: dict = yaml.safe_load(kopf)
        self.rumpf = rumpf.strip()
        self.pfad = pfad
        self.abschnitte: dict[str, str] = {}
        for teil in re.split(r"^## ", self.rumpf, flags=re.M)[1:]:
            titel, _, inhalt = teil.partition("\n")
            self.abschnitte[titel.strip()] = inhalt.strip()

    id = property(lambda s: s.meta["id"])
    titel = property(lambda s: s.meta["titel"])
    status = property(lambda s: s.meta["status"])

    def abzeichen(self, heute: date | None = None) -> list[tuple[str, str]]:
        """Abzeichen werden nur vergeben, wenn die Bedingung wirklich erfüllt ist."""
        heute = heute or date.today()
        m = self.meta
        liste = []
        baustelle = m["status"] == "baustelle"
        if m.get("werte"):
            if baustelle:
                # Bei einer Baustelle gibt es keine fertige Zahl. Nachgerechnet sind nur die Einzelzahlen.
                liste.append(("Einzelzahlen nachgerechnet", "Die Einzelzahlen dieser Karte werden von einem Test nachgerechnet. Eine Gesamtzahl gibt es noch nicht."))
            else:
                liste.append(("Nachgerechnet", "Alle Zahlen dieser Karte werden von einem Test aus den Daten nachgerechnet."))
        if m.get("zustaendig_fachlich") and m.get("zustaendig_zahlen"):
            liste.append(("Ansprechpersonen benannt", "Fachlich und für die Berechnung ist eine Rolle benannt."))
        # Bei einer Baustelle wäre "Vollständig beschrieben" irreführend: Die Karte ist nicht nutzbar.
        if not baustelle and all(a in self.abschnitte for a in ABSCHNITTE):
            liste.append(("Vollständig beschrieben", "Alle fünf Abschnitte sind ausgefüllt."))
        if (heute - m["aktualisiert"]).days <= 30:
            liste.append(("Aktuell", "In den letzten 30 Tagen aktualisiert."))
        if m["status"] == "mit-vorsicht":
            liste.append(("Lücke benannt", "Die bekannte Einschränkung steht offen auf der Karte."))
        elif baustelle:
            liste.append(("Lücke benannt", "Die Karte sagt offen, was fehlt."))
        return liste

    def volltext(self) -> str:
        m = self.meta
        name, bedeutung = STATUS[m["status"]]
        zeilen = [
            f"# {m['titel']}",
            f"Kurzantwort: {m['kurzantwort']}",
            f"Status: {name}. {bedeutung} {m.get('status_hinweis', '')}".strip(),
            "",
        ]
        for a in ABSCHNITTE[:3]:
            zeilen += [f"## {a}", self.abschnitte[a], ""]
        zeilen += ["## Woher kommt die Zahl?"]
        for i, s in enumerate(m["herkunft"], 1):
            zeilen.append(f"{i}. {s['station']}: {s['text']}")
        zeilen += ["", "## Nicht zu verwechseln mit"] + [f"- {x}" for x in m.get("nicht_verwechseln", [])]
        zeilen += ["", "## Wer hilft?", self.abschnitte["Wer hilft?"], ""]
        zeilen += [f"Technischer Name (für die IT): {m['technischer_name']}",
                   f"Stand der Karte: {m['aktualisiert']:%d.%m.%Y}",
                   f"Quelle im Katalog: katalog/auswertungen/{m['id']}.md"]
        return "\n".join(zeilen)

    def suchtext(self) -> dict[str, str]:
        m = self.meta
        return {
            "titel": m["titel"],
            "kurz": m["kurzantwort"],
            "fragen": " ".join(m.get("beispielfragen", [])),
            "abgrenzung": " ".join(m.get("nicht_verwechseln", [])),
            "rumpf": self.rumpf,
        }


class Eintrag:
    def __init__(self, name: str, synonyme: list[str], text: str, abgrenzung: str, siehe: list[str]):
        self.name, self.synonyme, self.text, self.abgrenzung, self.siehe = name, synonyme, text, abgrenzung, siehe

    def volltext(self) -> str:
        z = [f"# {self.name}", self.text]
        if self.synonyme:
            z.append(f"Auch genannt: {', '.join(self.synonyme)}")
        if self.abgrenzung:
            z.append(f"Nicht zu verwechseln mit: {self.abgrenzung}")
        if self.siehe:
            z.append(f"Mehr dazu in den Karten: {', '.join(self.siehe)}")
        return "\n".join(z)


@lru_cache(maxsize=1)
def karten() -> dict[str, Karte]:
    k = [Karte(p) for p in sorted((KATALOG / "auswertungen").glob("*.md"))]
    return {x.id: x for x in k}


@lru_cache(maxsize=1)
def glossar() -> list[Eintrag]:
    text = (KATALOG / "glossar.md").read_text(encoding="utf-8")
    eintraege = []
    for teil in re.split(r"^### ", text, flags=re.M)[1:]:
        name, _, rest = teil.partition("\n")
        syn, abgr, siehe, inhalt = [], "", [], []
        for zeile in rest.strip().splitlines():
            if zeile.startswith("Synonyme:"):
                syn = [s.strip() for s in zeile[9:].split(",") if s.strip()]
            elif zeile.startswith("Nicht zu verwechseln mit:"):
                abgr = zeile[len("Nicht zu verwechseln mit:"):].strip()
            elif zeile.startswith("Siehe:"):
                siehe = [s.strip() for s in zeile[6:].split(",") if s.strip()]
            elif zeile.strip():
                inhalt.append(zeile.strip())
        eintraege.append(Eintrag(name.strip(), syn, " ".join(inhalt), abgr, siehe))
    return eintraege


def suche(frage: str, grenze: int = 3) -> list[dict]:
    """Findet passende Karten. Leere Liste heißt: steht nicht im Katalog."""
    q = list(dict.fromkeys(woerter(frage)))
    if not q:
        return []
    gewicht = {"titel": 4, "fragen": 3, "kurz": 2, "abgrenzung": 1, "rumpf": 1}
    punkte: dict[str, float] = {}
    treffer: dict[str, set[str]] = {}
    for karte in karten().values():
        felder = {k: set(woerter(v)) for k, v in karte.suchtext().items()}
        for wort in q:
            beste = 0
            for feld, menge in felder.items():
                if any(passt(wort, w) for w in menge):
                    beste = max(beste, gewicht[feld])
            if beste:
                punkte[karte.id] = punkte.get(karte.id, 0) + beste
                treffer.setdefault(karte.id, set()).add(wort)
    # Begriffe aus dem Glossar verweisen auf Karten
    for e in glossar():
        for n in [e.name] + e.synonyme:
            nw = woerter(n)
            if nw and all(any(passt(x, w) for w in q) for x in nw):
                for kid in e.siehe:
                    if kid in karten():
                        punkte[kid] = punkte.get(kid, 0) + 3
                        treffer.setdefault(kid, set()).update(w for w in q if any(passt(x, w) for x in nw))
                break
    ergebnis = [(kid, p) for kid, p in punkte.items() if p >= 3 and len(treffer[kid]) >= min(2, len(q))]
    ergebnis.sort(key=lambda t: -t[1])
    return [
        {"id": kid, "titel": karten()[kid].titel, "kurzantwort": karten()[kid].meta["kurzantwort"],
         "status": STATUS[karten()[kid].status][0], "punkte": p}
        for kid, p in ergebnis[:grenze]
    ]


def finde_begriff(begriff: str) -> Eintrag | None:
    b = normalisiere(begriff).strip()
    ws = woerter(begriff)
    for e in glossar():
        if b == normalisiere(e.name) or b in [normalisiere(s) for s in e.synonyme]:
            return e
    for e in glossar():
        namen = [e.name] + e.synonyme
        for n in namen:
            nw = woerter(n)
            if ws and nw and all(any(passt(w, x) for x in nw) for w in ws):
                return e
    return None


def alle_fuer(rolle: str | None = None) -> list[Karte]:
    k = list(karten().values())
    if rolle:
        k = [x for x in k if rolle in x.meta.get("fuer", [])]
    return k
