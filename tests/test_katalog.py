"""Tests für den KI-Datenkatalog.

Sie prüfen drei Dinge:
  1. Jede Zahl im Katalog stimmt mit der Nachrechnung aus den Beispieldaten überein.
  2. Der Katalog ist vollständig und frei von toten Verweisen.
  3. Suche und Server beantworten die Testfragen wie festgelegt, auch die Fallen.
"""

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest
import yaml

WURZEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WURZEL))
sys.path.insert(0, str(WURZEL / "scripts"))

import kennzahlen  # noqa: E402
from server import app as serverapp  # noqa: E402
from server import katalog, seite  # noqa: E402


@pytest.fixture(scope="session")
def daten(tmp_path_factory) -> Path:
    ziel = tmp_path_factory.mktemp("raw")
    for skript in ("generate_data.py", "generate_zusatzdaten.py"):
        subprocess.run([sys.executable, str(WURZEL / "scripts" / skript), "--out", str(ziel)],
                       check=True, capture_output=True)
    return ziel


@pytest.fixture(scope="session")
def werte(daten) -> dict:
    return kennzahlen.berechne(daten)


# ---------- 1. Zahlen ----------

def test_bekannte_zahlen_stimmen_mit_den_anderen_projekten(werte):
    """Diese Zahlen stehen auch in ki-nutzung-kosten-analytics und ki-nutzung-kosten-lakehouse."""
    assert werte["anfragen_geliefert"] == "55.861"
    assert werte["anfragen_ohne_duplikate"] == "55.722"
    assert werte["anfragen_erfolgreich"] == "54.098"
    assert werte["kosten_gesamt_eur"] == "281,52"
    assert werte["kosten_summe_gerundet_eur"] == "281,49"
    assert (werte["dq_doppelte"], werte["dq_ohne_anwendungsfall"], werte["dq_nach_austritt"],
            werte["dq_unbekannte_abteilung"]) == ("139", "1.102", "174", "5")
    assert werte["konform_hoch_anzahl"] == "1 von 4"


def test_kennzahlen_json_ist_aktuell(werte):
    gespeichert = json.loads((WURZEL / "katalog" / "kennzahlen.json").read_text(encoding="utf-8"))
    assert gespeichert == werte, "katalog/kennzahlen.json ist veraltet: python scripts/kennzahlen.py ausführen"


@pytest.mark.parametrize("karte", list(katalog.karten().values()), ids=lambda k: k.id)
def test_zahlen_der_karte_stimmen(karte, werte):
    for schluessel, wert in karte.meta["werte"].items():
        assert schluessel in werte, f"{karte.id}: unbekannter Wert {schluessel}"
        assert werte[schluessel] == wert, f"{karte.id}: {schluessel} ist {werte[schluessel]}, Karte sagt {wert}"
        text = " ".join([karte.rumpf, karte.meta["kurzantwort"], *karte.meta["nicht_verwechseln"]]).replace("\u2212", "-")
        assert wert in text, f"{karte.id}: {wert} steht nicht im Text der Karte"


# ---------- 2. Aufbau ----------

PFLICHT = ["id", "titel", "kurzantwort", "fuer", "status", "seit", "aktualisiert", "zustaendig_fachlich",
           "zustaendig_zahlen", "rueckfragen", "technischer_name", "herkunft", "beispielfragen",
           "nicht_verwechseln", "werte"]


@pytest.mark.parametrize("karte", list(katalog.karten().values()), ids=lambda k: k.id)
def test_karte_ist_vollstaendig(karte):
    m = karte.meta
    for feld in PFLICHT:
        assert m.get(feld), f"{karte.id}: Feld {feld} fehlt"
    assert karte.pfad.stem == m["id"]
    assert m["status"] in katalog.STATUS
    assert set(m["fuer"]) <= set(katalog.ROLLEN)
    assert isinstance(m["aktualisiert"], date)
    assert len(m["herkunft"]) >= 3
    for a in katalog.ABSCHNITTE:
        assert karte.abschnitte.get(a), f"{karte.id}: Abschnitt '{a}' fehlt"
    if m["status"] != "verlaessig":
        assert m.get("status_hinweis"), f"{karte.id}: Status ohne Hinweis"


def test_glossar_verweist_nur_auf_vorhandene_karten():
    for e in katalog.glossar():
        assert e.text and e.abgrenzung, f"Glossar {e.name}: Text oder Abgrenzung fehlt"
        for kid in e.siehe:
            assert kid in katalog.karten(), f"Glossar {e.name}: Karte {kid} gibt es nicht"


def test_datenquellen_verweisen_nur_auf_vorhandene_karten():
    text = (WURZEL / "katalog" / "datenquellen.md").read_text(encoding="utf-8")
    for zeile in text.splitlines():
        if zeile.startswith("Genutzt in:"):
            for kid in [x.strip() for x in zeile[11:].split(",")]:
                assert kid in katalog.karten(), f"Datenquellen: Karte {kid} gibt es nicht"


def test_jede_neue_csv_ist_beschrieben(daten):
    text = (WURZEL / "katalog" / "datenquellen.md").read_text(encoding="utf-8")
    for csv_datei in daten.glob("*.csv"):
        assert f"## {csv_datei.name}" in text, f"{csv_datei.name} fehlt in datenquellen.md"


def test_abzeichen_werden_nur_bei_erfuelltem_kriterium_vergeben():
    karte = katalog.karten()["gesamtkosten"]
    namen = [n for n, _ in karte.abzeichen(heute=date(2030, 1, 1))]
    assert "Aktuell" not in namen
    assert "Lücke benannt" not in namen  # Baustelle, nicht "mit Vorsicht"
    assert "Nachgerechnet" in namen


# ---------- 3. Testfragen ----------

FRAGEN = yaml.safe_load((WURZEL / "tests" / "testfragen.yaml").read_text(encoding="utf-8"))


@pytest.mark.parametrize("f", FRAGEN["treffer"], ids=lambda f: f["frage"][:50])
def test_frage_findet_richtige_karte(f):
    ergebnis = katalog.suche(f["frage"])
    assert ergebnis, f"Keine Karte gefunden für: {f['frage']}"
    assert ergebnis[0]["id"] == f["karte"], f"Erste Karte ist {ergebnis[0]['id']}, erwartet {f['karte']}"
    text = serverapp.karte_anzeigen(f["karte"])
    for z in f["muss_enthalten"]:
        assert z in text, f"'{z}' fehlt in der Karte {f['karte']}"


@pytest.mark.parametrize("f", FRAGEN["fallen"], ids=lambda f: f["frage"][:50])
def test_falle_bleibt_ohne_antwort(f):
    assert katalog.suche(f["frage"]) == []
    assert serverapp.katalog_durchsuchen(f["frage"]).startswith("Das steht nicht im Katalog.")


def test_unbekannte_karte_und_begriff():
    assert serverapp.karte_anzeigen("gibt-es-nicht").startswith("Das steht nicht im Katalog.")
    assert serverapp.begriff_erklaeren("Raumschiff").startswith("Das steht nicht im Katalog.")
    assert "Auftragsverarbeitungsvertrag" in serverapp.begriff_erklaeren("Datenschutzvertrag")


def test_alle_auswertungen_nach_rolle():
    assert "budget-gegen-ist" in serverapp.alle_auswertungen("Controlling")
    assert "schulungsquote" not in serverapp.alle_auswertungen("Controlling")
    assert serverapp.alle_auswertungen("Hausmeister").startswith("Das steht nicht im Katalog.")


def test_karte_nennt_status_und_quelle():
    text = serverapp.karte_anzeigen("ungenutzte-lizenzen")
    assert "Status: Mit Vorsicht" in text
    assert "katalog/auswertungen/ungenutzte-lizenzen.md" in text


# ---------- Webseite ----------

def test_seiten_werden_gerendert():
    assert "Woher kommt diese Zahl?" in seite.startseite()
    for kid in katalog.karten():
        html = seite.kartenseite(kid)
        assert html and katalog.karten()[kid].titel in html
    assert seite.kartenseite("gibt-es-nicht") is None
    assert "Lizenz" in seite.glossarseite()
    assert "Das steht nicht im Katalog." in seite.suchseite("Zufriedenheit der Mitarbeitenden")
    assert "<script>alert" not in seite.suchseite("<script>alert(1)</script>")
    assert "Über diesen Katalog" in seite.ueberseite()
