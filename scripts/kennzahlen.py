"""Berechnet alle Beispielwerte, die im Katalog vorkommen, direkt aus den CSV-Dateien.

Zweck: Jede Zahl im Katalog lässt sich nachrechnen. Die Tests vergleichen die Zahlen in den
Karten (Feld `werte`) mit diesem Skript. Rechenregeln wie in den Gold-Tabellen des Projekts
ki-nutzung-kosten-lakehouse.

Aufruf:
    python scripts/kennzahlen.py            # liest data/raw/, schreibt katalog/kennzahlen.json
"""

import csv
import json
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

STICHTAG = date(2025, 12, 31)
LIZENZ_INAKTIV_TAGE = 90


def lese(pfad: Path) -> list[dict]:
    with open(pfad, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def de(zahl: float, stellen: int = 2) -> str:
    """Deutsche Schreibweise: 1.234,56"""
    s = f"{zahl:,.{stellen}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def monate_zurueck(heute: date, bis: date) -> int:
    return (heute.year - bis.year) * 12 + (heute.month - bis.month) - (1 if heute.day < bis.day else 0)


def berechne(d: Path) -> dict:
    abt = {r["department_id"]: r["department_name"] for r in lese(d / "departments.csv")}
    users = {r["user_id"]: r for r in lese(d / "users.csv")}
    cases = {r["use_case_id"]: r for r in lese(d / "use_cases.csv")}
    preise = {r["model_id"]: (float(r["price_per_1k_input_eur"]), float(r["price_per_1k_output_eur"]))
              for r in lese(d / "ai_models.csv")}

    # ---- Faktentabelle: jede Anfrage einmal ----
    roh = lese(d / "usage_events.csv")
    gesehen, fct = set(), []
    for e in roh:
        if e["event_id"] in gesehen:
            continue
        gesehen.add(e["event_id"])
        u = users.get(e["user_id"])
        dep_id = u["department_id"] if u else None
        pi, po = preise[e["model_id"]]
        erfolg = e["status"] == "erfolg"
        tag = datetime.fromisoformat(e["event_ts"]).date()
        fct.append({
            "user": e["user_id"],
            "dept": abt.get(dep_id, "Unbekannt"),
            "monat": (tag.year, tag.month),
            "uc": e["use_case_id"],
            "model": e["model_id"],
            "erfolg": erfolg,
            "kosten": (int(e["input_tokens"]) * pi + int(e["output_tokens"]) * po) / 1000 if erfolg else 0.0,
            "nach_austritt": bool(u and u["left_date"] and tag > date.fromisoformat(u["left_date"])),
            "hat_uc": e["use_case_id"] != "",
        })

    w: dict = {}
    kosten_ges = sum(f["kosten"] for f in fct)
    erf = [f for f in fct if f["erfolg"]]
    w["anfragen_geliefert"] = de(len(roh), 0)
    w["anfragen_ohne_duplikate"] = de(len(fct), 0)
    w["anfragen_erfolgreich"] = de(len(erf), 0)
    w["kosten_gesamt_eur"] = de(kosten_ges)

    # ---- Frage 1: Kosten je Abteilung ----
    je_abt: dict[str, float] = defaultdict(float)
    je_monat: dict[tuple, float] = defaultdict(float)
    for f in fct:
        je_abt[f["dept"]] += f["kosten"]
        je_monat[f["monat"]] += f["kosten"]
    bekannt = {k: v for k, v in je_abt.items() if k != "Unbekannt"}
    top = max(bekannt, key=bekannt.get)
    w["kosten_teuerste_abteilung"] = top
    w["kosten_teuerste_abteilung_eur"] = de(bekannt[top])
    w["kosten_unbekannt_eur"] = de(je_abt.get("Unbekannt", 0.0))
    je_abt_monat: dict[tuple, float] = defaultdict(float)
    for f in fct:
        je_abt_monat[(f["dept"], f["monat"])] += f["kosten"]
    w["kosten_summe_gerundet_eur"] = de(sum(round(v, 2) for v in je_abt_monat.values()))
    w["kosten_januar_eur"] = de(je_monat[(2025, 1)])
    w["kosten_dezember_eur"] = de(je_monat[(2025, 12)])

    # ---- Frage 2: aktive Nutzer (Dezember) ----
    aktiv_dez = {f["user"] for f in fct if f["erfolg"] and not f["nach_austritt"] and f["monat"] == (2025, 12)}
    aktiv_jan = {f["user"] for f in fct if f["erfolg"] and not f["nach_austritt"] and f["monat"] == (2025, 1)}
    w["aktive_nutzer_dezember"] = de(len(aktiv_dez), 0)
    w["aktive_nutzer_januar"] = de(len(aktiv_jan), 0)
    w["nutzer_gesamt"] = de(len(users), 0)

    # ---- Frage 3: Konformität ----
    for klasse in ["minimal", "begrenzt", "hoch"]:
        fs = [c for c in cases.values() if c["risk_class"] == klasse and c["status"] != "eingestellt"]
        ok = [c for c in fs if c["status"] == "freigegeben" and c["documentation_complete"] == "true"]
        w[f"konform_{klasse}_anzahl"] = f"{len(ok)} von {len(fs)}"
        w[f"konform_{klasse}_prozent"] = de(len(ok) / len(fs) * 100, 1) if fs else "0,0"

    # ---- Frage 4: Kosten je erfolgreicher Anfrage je Anwendungsfall ----
    je_uc: dict[str, dict] = defaultdict(lambda: {"n": 0, "n_erf": 0, "k": 0.0})
    for f in fct:
        if f["uc"] in cases:
            x = je_uc[f["uc"]]
            x["n"] += 1
            x["n_erf"] += 1 if f["erfolg"] else 0
            x["k"] += f["kosten"]
    rang = sorted(((cases[i]["use_case_name"], cases[i]["risk_class"], x["k"] / x["n_erf"])
                   for i, x in je_uc.items() if x["n"] >= 100 and x["n_erf"]), key=lambda t: -t[2])
    w["teuerster_anwendungsfall"] = rang[0][0]
    w["teuerster_anwendungsfall_risiko"] = rang[0][1]
    w["teuerster_anwendungsfall_je_anfrage_eur"] = de(rang[0][2], 4)
    w["guenstigster_anwendungsfall"] = rang[-1][0]
    w["guenstigster_anwendungsfall_je_anfrage_eur"] = de(rang[-1][2], 4)

    # ---- Frage 5: Datenqualität ----
    w["dq_doppelte"] = de(len(roh) - len(fct), 0)
    w["dq_ohne_anwendungsfall"] = de(sum(1 for f in fct if not f["hat_uc"]), 0)
    w["dq_nach_austritt"] = de(sum(1 for f in fct if f["nach_austritt"]), 0)
    w["dq_unbekannte_abteilung"] = de(sum(1 for u in users.values() if u["department_id"] not in abt), 0)

    # ---- Budget gegen Ist ----
    budgets = lese(d / "budgets.csv")
    plan: dict[tuple, float] = defaultdict(float)
    for b in budgets:
        m = date.fromisoformat(b["budget_month"])
        plan[(b["department_id"], (m.year, m.month))] += float(b["budget_eur"])
    name_zu_id = {v: k for k, v in abt.items()}
    ist: dict[tuple, float] = defaultdict(float)
    for f in fct:
        if f["dept"] in name_zu_id:
            ist[(name_zu_id[f["dept"]], f["monat"])] += f["kosten"]
    deps_mit_budget = sorted({k[0] for k in plan})
    bud_ges = sum(plan.values())
    ist_mit_budget = sum(v for key, v in ist.items() if key in plan)  # nur Monate mit Budget
    ueber = [(dep, mon) for (dep, mon), p in plan.items() if ist.get((dep, mon), 0.0) > p]
    ueber_nach_dep: dict[str, int] = defaultdict(int)
    for dep, _ in ueber:
        ueber_nach_dep[dep] += 1
    erste_ueber = min((mon for _, mon in ueber), default=None)
    ohne_budget = [(dep, m) for dep in abt for m in range(1, 13) if (dep, (2025, m)) not in plan]
    w["budget_gesamt_eur"] = de(bud_ges)
    w["budget_ist_eur"] = de(ist_mit_budget)
    w["budget_abweichung_eur"] = de(ist_mit_budget - bud_ges)
    w["budget_monate_ueber_anzahl"] = de(len(ueber), 0)
    w["budget_monate_geplant"] = de(len(plan), 0)
    monatsnamen = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September",
                   "Oktober", "November", "Dezember"]
    w["budget_erster_monat_ueber"] = f"{monatsnamen[erste_ueber[1] - 1]} {erste_ueber[0]}" if erste_ueber else "keiner"
    w["budget_abteilungen_mit_luecke"] = ", ".join(sorted({abt[dep] for dep, _ in ohne_budget}))
    w["budget_luecke_monate"] = de(len(ohne_budget), 0)
    luecke_kosten = sum(v for (dep, mon), v in ist.items() if (dep, mon) not in plan)
    w["budget_ist_ohne_budget_eur"] = de(luecke_kosten)
    ab_ueber = max(ueber_nach_dep, key=ueber_nach_dep.get) if ueber_nach_dep else None
    w["budget_abteilung_meiste_ueberschreitungen"] = abt[ab_ueber] if ab_ueber else "keine"
    w["budget_abteilung_meiste_ueberschreitungen_monate"] = de(ueber_nach_dep.get(ab_ueber, 0), 0)

    # ---- Lizenzen ----
    lic = lese(d / "licenses.csv")
    inaktiv = []
    for l in lic:
        login = date.fromisoformat(l["last_login_date"]) if l["last_login_date"] else None
        if login is None or (STICHTAG - login).days > LIZENZ_INAKTIV_TAGE:
            inaktiv.append(l)
    preis = float(lic[0]["monthly_price_eur"])
    nutzer_mit_lizenz = {l["user_id"] for l in lic}
    doppelt = [u for u in nutzer_mit_lizenz if sum(1 for l in lic if l["user_id"] == u) > 1]
    ausgetreten = [l for l in lic if users[l["user_id"]]["left_date"]]
    nie = [l for l in lic if not l["last_login_date"]]
    w["lizenzen_gesamt"] = de(len(lic), 0)
    w["lizenzen_ungenutzt"] = de(len(inaktiv), 0)
    w["lizenzen_ungenutzt_prozent"] = de(len(inaktiv) / len(lic) * 100, 1)
    w["lizenzen_ungenutzt_kosten_monat_eur"] = de(len(inaktiv) * preis)
    w["lizenzen_kosten_monat_eur"] = de(len(lic) * preis)
    w["lizenzen_preis_eur"] = de(preis)
    w["lizenzen_nie_genutzt"] = de(len(nie), 0)
    w["lizenzen_ausgetretene"] = de(len(ausgetreten), 0)
    w["lizenzen_nutzer_doppelt"] = de(len(doppelt), 0)

    # ---- Schulungen ----
    kurse = {k["course_id"]: k for k in lese(d / "training_courses.csv")}
    ab = lese(d / "training_completions.csv")
    bekannte_ab, unbekannt_ab, erfasst = [], 0, set()
    doppelt_ab = 0
    for a in ab:
        if a["user_id"] not in users:
            unbekannt_ab += 1
            continue
        key = (a["user_id"], a["course_id"], a["completed_date"])
        if key in erfasst:
            doppelt_ab += 1
            continue
        erfasst.add(key)
        bekannte_ab.append(a)

    def gueltig(user_id: str, kurs: str) -> bool:
        k = kurse[kurs]
        for a in bekannte_ab:
            if a["user_id"] == user_id and a["course_id"] == kurs:
                if monate_zurueck(STICHTAG, date.fromisoformat(a["completed_date"])) < int(k["valid_months"]):
                    return True
        return False

    im_haus = [u for u in users.values() if not u["left_date"]]
    mit_c1 = [u for u in im_haus if gueltig(u["user_id"], "C1")]
    mit_c2 = [u for u in im_haus if gueltig(u["user_id"], "C2")]
    beide = [u for u in im_haus if gueltig(u["user_id"], "C1") and gueltig(u["user_id"], "C2")]
    w["schulung_nutzer_im_haus"] = de(len(im_haus), 0)
    w["schulung_c1_prozent"] = de(len(mit_c1) / len(im_haus) * 100, 1)
    w["schulung_c2_prozent"] = de(len(mit_c2) / len(im_haus) * 100, 1)
    w["schulung_beide_anzahl"] = de(len(beide), 0)
    w["schulung_beide_prozent"] = de(len(beide) / len(im_haus) * 100, 1)
    w["schulung_unbekannte_nutzer"] = de(unbekannt_ab, 0)
    w["schulung_doppelt_erfasst"] = de(doppelt_ab, 0)
    hoch = {i for i, c in cases.items() if c["risk_class"] == "hoch"}
    hoch_nutzer = {f["user"] for f in fct if f["erfolg"] and f["monat"] == (2025, 12) and f["uc"] in hoch
                   and f["user"] in users and not users[f["user"]]["left_date"]}
    ohne_c1 = [u for u in hoch_nutzer if not gueltig(u, "C1")]
    w["hochrisiko_nutzer_dezember"] = de(len(hoch_nutzer), 0)
    w["hochrisiko_ohne_grundlagen"] = de(len(ohne_c1), 0)
    w["hochrisiko_ohne_grundlagen_prozent"] = de(len(ohne_c1) / len(hoch_nutzer) * 100, 1) if hoch_nutzer else "0,0"

    # ---- Anbieter und Datenstandort ----
    prov = {p["provider_id"]: p for p in lese(d / "ai_providers.csv")}
    mp = {r["model_id"]: r["provider_id"] for r in lese(d / "model_providers.csv")}
    n_pro: dict[str, int] = defaultdict(int)
    k_pro: dict[str, float] = defaultdict(float)
    n_hoch_ges, n_hoch_ohne_avv = 0, 0
    for f in erf:
        p = mp[f["model"]]
        n_pro[p] += 1
        k_pro[p] += f["kosten"]
        if f["uc"] in hoch:
            n_hoch_ges += 1
            if prov[p]["dpa_signed"] != "true":
                n_hoch_ohne_avv += 1
    ohne_avv = [p for p in prov if prov[p]["dpa_signed"] != "true"]
    n_ohne = sum(n_pro[p] for p in ohne_avv)
    k_ohne = sum(k_pro[p] for p in ohne_avv)
    w["anbieter_anzahl"] = de(len(prov), 0)
    w["anbieter_ohne_avv"] = ", ".join(prov[p]["provider_name"] for p in ohne_avv)
    w["anbieter_ohne_avv_standort"] = ", ".join(prov[p]["data_location"] for p in ohne_avv)
    w["anbieter_ohne_avv_vertragsende"] = ", ".join(
        date.fromisoformat(prov[p]["contract_end_date"]).strftime("%d.%m.%Y") for p in ohne_avv)
    w["anfragen_ohne_avv_prozent"] = de(n_ohne / len(erf) * 100, 1)
    w["kosten_ohne_avv_prozent"] = de(k_ohne / kosten_ges * 100, 1)
    w["hochrisiko_ohne_avv_prozent"] = de(n_hoch_ohne_avv / n_hoch_ges * 100, 1) if n_hoch_ges else "0,0"
    for p in sorted(prov):
        w[f"anfragen_{p}_prozent"] = de(n_pro[p] / len(erf) * 100, 1)
    return w


if __name__ == "__main__":
    wurzel = Path(__file__).resolve().parent.parent
    werte = berechne(wurzel / "data" / "raw")
    ziel = wurzel / "katalog" / "kennzahlen.json"
    ziel.parent.mkdir(exist_ok=True)
    ziel.write_text(json.dumps(werte, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(werte, ensure_ascii=False, indent=2, sort_keys=True))
