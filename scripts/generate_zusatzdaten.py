"""Erzeugt die zusätzlichen, vollständig synthetischen Beispieldaten für den Datenkatalog.

Voraussetzung: `python scripts/generate_data.py` ist gelaufen (liefert Abteilungen,
Nutzer, Anwendungsfälle, Modelle und Nutzungsereignisse mit Startwert 42). Dieses
Skript ändert diese Dateien nicht, es ergänzt nur vier weitere Quellen:

  1. Budgets je Abteilung und Monat                  -> budgets.csv
  2. KI-Anbieter, Datenstandort, Verträge            -> ai_providers.csv, model_providers.csv
  3. KI-Lizenzen (bezahlte Plätze)                   -> licenses.csv
  4. KI-Schulungen                                   -> training_courses.csv, training_completions.csv

Alle Namen, Beträge und Mengen sind frei erfunden.

Aufruf:
    python scripts/generate_zusatzdaten.py                 # liest und schreibt data/raw/
    python scripts/generate_zusatzdaten.py --seed 7

Bewusst eingebaute Datenprobleme (damit der Katalog "Bekannte Einschränkungen" ehrlich nennen kann):
  A. Für die Abteilung Personal fehlt das Budget für Oktober bis Dezember.
  B. Einige Nutzer haben zwei Lizenzen (doppelt bezahlt).
  C. Schulungsnachweise für Nutzer-Nummern, die es nicht gibt.
  D. Eine Schulung ist doppelt erfasst.
"""

import argparse
import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

STICHTAG = date(2025, 12, 31)
JAHRESSTART = date(2025, 1, 1)
LIZENZ_PREIS_EUR = 9.00

PROVIDERS = [
    ("P1", "Anbieter Nord", "EU", "true", "2026-06-30"),
    ("P2", "Anbieter Mitte", "EU", "true", "2027-03-31"),
    ("P3", "Anbieter West", "USA", "false", "2026-01-31"),
]
MODEL_PROVIDERS = [("M1", "P1"), ("M2", "P2"), ("M3", "P3")]

COURSES = [
    ("C1", "KI-Grundlagen", "true", 24),
    ("C2", "Datenschutz bei KI-Nutzung", "true", 12),
    ("C3", "Prompting für Fortgeschrittene", "false", 36),
]


def lese(pfad: Path) -> list[dict]:
    with open(pfad, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def schreibe(pfad: Path, kopf: list[str], zeilen: list) -> None:
    with open(pfad, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(kopf)
        w.writerows(zeilen)


def kosten_je_abteilung(d: Path) -> dict[str, float]:
    """Jahreskosten (erfolgreiche Anfragen, ohne Duplikate) je Abteilung. Nur für die Budgetplanung."""
    nutzer = {u["user_id"]: u["department_id"] for u in lese(d / "users.csv")}
    preise = {m["model_id"]: (float(m["price_per_1k_input_eur"]), float(m["price_per_1k_output_eur"]))
              for m in lese(d / "ai_models.csv")}
    gesehen: set[str] = set()
    summe: dict[str, float] = {}
    for e in lese(d / "usage_events.csv"):
        if e["event_id"] in gesehen:
            continue
        gesehen.add(e["event_id"])
        if e["status"] != "erfolg":
            continue
        pi, po = preise[e["model_id"]]
        k = int(e["input_tokens"]) * pi / 1000 + int(e["output_tokens"]) * po / 1000
        dep = nutzer[e["user_id"]]
        summe[dep] = summe.get(dep, 0.0) + k
    return summe


def main(seed: int, d: Path) -> None:
    rng = random.Random(seed + 1000)  # eigener Zufallsstrom, die Basisdaten bleiben unberührt
    users = lese(d / "users.csv")
    abteilungen = [r["department_id"] for r in lese(d / "departments.csv")]

    # 1. Budgets: Jahresbudget = Kosten des Jahres x Faktor, gleichmäßig auf zwölf Monate verteilt.
    #    Weil die Nutzung über das Jahr wächst, liegen die Abteilungen im Jahresverlauf irgendwann darüber.
    kosten = kosten_je_abteilung(d)
    budgets = []
    for dep in abteilungen:
        jahr = kosten.get(dep, 0.0) * rng.uniform(0.85, 1.35)
        monat = round(jahr / 12, 2)
        for m in range(1, 13):
            if dep == "D05" and m >= 10:  # Problem A: Planungslücke
                continue
            budgets.append([dep, date(2025, m, 1).isoformat(), f"{monat:.2f}"])
    schreibe(d / "budgets.csv", ["department_id", "budget_month", "budget_eur"], budgets)

    # 2. Anbieter und Zuordnung der Modelle
    schreibe(d / "ai_providers.csv",
             ["provider_id", "provider_name", "data_location", "dpa_signed", "contract_end_date"], PROVIDERS)
    schreibe(d / "model_providers.csv", ["model_id", "provider_id"], MODEL_PROVIDERS)

    # 3. Lizenzen: etwa die Hälfte der Nutzer hat einen bezahlten Platz.
    lizenzen = []
    lid = 0
    for u in users:
        if rng.random() >= 0.5:
            continue
        hired = date.fromisoformat(u["hired_date"])
        left = date.fromisoformat(u["left_date"]) if u["left_date"] else None
        assigned = max(hired, JAHRESSTART + timedelta(days=rng.randint(-300, 250)))
        r = rng.random()
        if r < 0.72:
            login = STICHTAG - timedelta(days=rng.randint(0, 20))
        elif r < 0.87:
            login = JAHRESSTART + timedelta(days=rng.randint(0, 270))
        else:
            login = None  # nie benutzt
        if login is not None and left is not None:
            login = min(login, left - timedelta(days=rng.randint(0, 30)))
        if login is not None and login < assigned:
            login = assigned
        lid += 1
        lizenzen.append([f"L{lid:04d}", u["user_id"], "KI-Assistent Plus", assigned.isoformat(),
                         login.isoformat() if login else "", f"{LIZENZ_PREIS_EUR:.2f}"])
    # Problem B: vier Nutzer mit zweiter Lizenz
    for row in rng.sample(lizenzen, 4):
        lid += 1
        lizenzen.append([f"L{lid:04d}", row[1], row[2], row[3], row[4], row[5]])
    rng.shuffle(lizenzen)
    schreibe(d / "licenses.csv",
             ["license_id", "user_id", "product", "assigned_date", "last_login_date", "monthly_price_eur"],
             lizenzen)

    # 4. Schulungen
    schreibe(d / "training_courses.csv", ["course_id", "course_name", "mandatory", "valid_months"], COURSES)
    abschluesse = []
    for u in users:
        hired = date.fromisoformat(u["hired_date"])
        if rng.random() < 0.72:
            tag = max(hired, date(2023, 7, 1) + timedelta(days=rng.randint(0, 900)))
            abschluesse.append([u["user_id"], "C1", min(tag, STICHTAG).isoformat()])
        if rng.random() < 0.58:
            tag = max(hired, date(2024, 10, 1) + timedelta(days=rng.randint(0, 440)))
            abschluesse.append([u["user_id"], "C2", min(tag, STICHTAG).isoformat()])
        if rng.random() < 0.20:
            tag = date(2024, 6, 1) + timedelta(days=rng.randint(0, 570))
            abschluesse.append([u["user_id"], "C3", min(tag, STICHTAG).isoformat()])
    # Problem C: Nachweise für unbekannte Nutzer
    for i in range(3):
        abschluesse.append([f"U{9101 + i}", "C1", date(2025, 3, 10 + i).isoformat()])
    # Problem D: doppelt erfasst
    for row in rng.sample(abschluesse, 5):
        abschluesse.append(list(row))
    rng.shuffle(abschluesse)
    schreibe(d / "training_completions.csv", ["user_id", "course_id", "completed_date"], abschluesse)

    print(f"budgets={len(budgets)} licenses={len(lizenzen)} completions={len(abschluesse)} -> {d}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=Path, default=Path("data/raw"))
    args = ap.parse_args()
    main(args.seed, args.out)
