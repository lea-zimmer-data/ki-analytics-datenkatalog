"""Baut die Webseite des Katalogs. Alles wird aus den Markdown-Dateien erzeugt.

Grundsatz: Die Seite zeigt nur, was stimmt. Es gibt keine erfundenen Bewertungen, Punkte
oder Beliebtheitslisten. "Zuletzt angesehen" und die Rollenauswahl bleiben im Browser der
Besucherin (localStorage) und werden nirgends gespeichert.
"""

from __future__ import annotations

import html
import json
import re
from urllib.parse import quote

import markdown

from server import katalog

REPO = "https://github.com/lea-zimmer-data/ki-analytics-datenkatalog"
E = html.escape

CSS = """
:root{--bg:#f7f6f2;--card:#fff;--ink:#1d2433;--muted:#5b6475;--line:#e3e0d8;--accent:#1c5d7a;--accent-soft:#e3f0f6;
--ok:#1f6b45;--ok-bg:#e4f3ea;--warn:#7a4f00;--warn-bg:#fff1cf;--bau:#8a3200;--bau-bg:#ffe5d3;--radius:14px}
@media (prefers-color-scheme:dark){:root{--bg:#14171d;--card:#1d222b;--ink:#eceff5;--muted:#a3adbf;--line:#2c3340;
--accent:#7cc3e2;--accent-soft:#1b2d38;--ok:#7fd3a3;--ok-bg:#16301f;--warn:#f2c76b;--warn-bg:#3a2c0d;--bau:#ffb58a;--bau-bg:#3b2214}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent)}a:hover{text-decoration-thickness:2px}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
header.top{border-bottom:1px solid var(--line);background:var(--card)}
header.top .wrap{display:flex;gap:24px;align-items:center;padding-top:14px;padding-bottom:14px;flex-wrap:wrap}
header.top .logo{font-weight:700;font-size:18px;color:var(--ink);text-decoration:none}
header.top nav{display:flex;gap:18px;margin-left:auto}header.top nav a{color:var(--muted);text-decoration:none}
header.top nav a:hover{color:var(--ink)}
.hero{padding:44px 0 20px}.hero h1{font-size:clamp(28px,5vw,42px);line-height:1.15;margin:0 0 10px}
.hero p{color:var(--muted);max-width:640px;margin:0 0 20px;font-size:18px}
.suche{display:flex;gap:8px;max-width:640px}
.suche input{flex:1;padding:14px 16px;border:1px solid var(--line);border-radius:12px;font:inherit;background:var(--card);color:var(--ink)}
button,.knopf{padding:12px 18px;border-radius:12px;border:0;background:var(--accent);color:#fff;font:inherit;font-weight:600;cursor:pointer;text-decoration:none;display:inline-block}
@media (prefers-color-scheme:dark){button,.knopf{color:#0e1318}}
button.leise,.knopf.leise{background:var(--accent-soft);color:var(--accent)}
.rollen{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0;align-items:center}
.rollen span.l{color:var(--muted);margin-right:4px}
.rollen button{padding:8px 14px;background:var(--card);color:var(--ink);border:1px solid var(--line);font-weight:500}
.rollen button[aria-pressed=true]{background:var(--accent);color:#fff;border-color:var(--accent)}
@media (prefers-color-scheme:dark){.rollen button[aria-pressed=true]{color:#0e1318}}
section.reihe{margin:34px 0}section.reihe h2{font-size:20px;margin:0 0 4px}section.reihe .unter{color:var(--muted);margin:0 0 12px}
.zeile{display:flex;gap:14px;overflow-x:auto;padding:4px 2px 14px;scroll-snap-type:x proximity}
.zeile .kachel{flex:0 0 min(300px,82vw);scroll-snap-align:start}
.raster{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.kachel{display:flex;flex-direction:column;gap:8px;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:16px;text-decoration:none;color:var(--ink);transition:transform .12s,box-shadow .12s}
.kachel:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.08)}
.kachel h3{margin:0;font-size:17px;line-height:1.3}.kachel p{margin:0;color:var(--muted);font-size:14.5px}
.kachel .fuss{margin-top:auto;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.chip{display:inline-block;padding:2px 10px;border-radius:999px;font-size:13px;font-weight:600}
.chip.verlaessig{background:var(--ok-bg);color:var(--ok)}.chip.mit-vorsicht{background:var(--warn-bg);color:var(--warn)}
.chip.baustelle{background:var(--bau-bg);color:var(--bau)}.tag{font-size:12.5px;color:var(--muted)}
.leer{color:var(--muted)}
.krumen{margin:22px 0 4px;color:var(--muted);font-size:14px}.krumen a{color:var(--muted)}
.karte h1{font-size:clamp(26px,4vw,36px);line-height:1.2;margin:6px 0 10px}
.antwort{font-size:19px;background:var(--accent-soft);border-radius:var(--radius);padding:16px 18px;margin:12px 0}
.status{border-radius:var(--radius);padding:12px 16px;margin:12px 0;border:1px solid var(--line)}
.status.verlaessig{background:var(--ok-bg);color:var(--ok)}.status.mit-vorsicht{background:var(--warn-bg);color:var(--warn)}
.status.baustelle{background:var(--bau-bg);color:var(--bau)}.status b{display:block;font-size:15px}
.abzeichen{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 0;padding:0;list-style:none}
.abzeichen li{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:3px 12px;font-size:13.5px}
.abzeichen li::before{content:"\\2713\\00a0";color:var(--ok);font-weight:700}
.abschnitt{margin:28px 0}.abschnitt h2{font-size:21px;margin:0 0 8px}
.abschnitt table{border-collapse:collapse;width:100%;font-size:15px}
.abschnitt th,.abschnitt td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left}
.linie{list-style:none;padding:0;margin:14px 0;display:flex;gap:0;counter-reset:s}
.linie li{flex:1;position:relative;padding:34px 12px 0 0;min-width:0}
.linie li::before{content:"";position:absolute;top:11px;left:0;right:0;height:4px;background:var(--accent)}
.linie li::after{content:counter(s);counter-increment:s;position:absolute;top:0;left:0;width:26px;height:26px;border-radius:50%;
background:var(--card);border:4px solid var(--accent);font-size:12px;font-weight:700;display:grid;place-items:center;color:var(--ink)}
.linie li:last-child::before{right:calc(100% - 26px)}
.linie b{display:block;font-size:15px;line-height:1.3}.linie span{display:block;color:var(--muted);font-size:14px;margin-top:2px}
@media (max-width:760px){.linie{flex-direction:column}.linie li{padding:0 0 22px 44px}
.linie li::before{top:0;bottom:0;left:11px;right:auto;width:4px;height:auto}
.linie li:last-child::before{right:auto;bottom:calc(100% - 26px)}}
.chat{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:6px 16px}
.chat li{margin:10px 0;display:flex;gap:10px;align-items:center;justify-content:space-between;list-style:none}
.chat ul{padding:0;margin:8px 0}.chat button{padding:6px 12px;font-size:14px}
details.it{margin:22px 0;color:var(--muted)}details.it summary{cursor:pointer}
footer{margin:60px 0 40px;color:var(--muted);font-size:14px;border-top:1px solid var(--line);padding-top:18px}
.glossar dt{font-weight:700;margin-top:18px;font-size:18px}.glossar dd{margin:4px 0 0}.glossar .nv{color:var(--muted);font-size:15px}
.glossar .syn{color:var(--muted);font-size:14px}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
"""

JS = """
(function(){
  function get(k){try{return JSON.parse(localStorage.getItem(k)||'null')}catch(e){return null}}
  function set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
  var kacheln={};document.querySelectorAll('a.kachel[data-karte]').forEach(function(el){kacheln[el.dataset.karte]=el});
  function kopie(el){var c=el.cloneNode(true);c.removeAttribute('hidden');return c}
  // Rollen
  var rolle=get('rolle');var knoepfe=document.querySelectorAll('[data-rolle]');
  function zeigeRolle(){
    knoepfe.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.rolle===rolle?'true':'false')});
    var box=document.getElementById('fuer-dich');if(!box)return;
    var ziel=box.querySelector('.zeile');ziel.innerHTML='';
    if(!rolle){box.hidden=true;return}
    var n=0;Object.keys(kacheln).forEach(function(id){var el=kacheln[id];
      if((el.dataset.fuer||'').split('|').indexOf(rolle)>-1){ziel.appendChild(kopie(el));n++}});
    box.hidden=n===0;box.querySelector('h2').textContent='Für dich: '+rolle;
  }
  knoepfe.forEach(function(b){b.addEventListener('click',function(){rolle=(rolle===b.dataset.rolle)?null:b.dataset.rolle;set('rolle',rolle);zeigeRolle()})});
  // Zuletzt angesehen
  var seite=document.body.dataset.karte;
  if(seite){var l=(get('zuletzt')||[]).filter(function(x){return x!==seite});l.unshift(seite);set('zuletzt',l.slice(0,6))}
  var box2=document.getElementById('zuletzt');
  if(box2){var l2=get('zuletzt')||[];var z2=box2.querySelector('.zeile');
    l2.forEach(function(id){if(kacheln[id])z2.appendChild(kopie(kacheln[id]))});box2.hidden=!z2.children.length}
  zeigeRolle();
  // Kopieren
  document.querySelectorAll('[data-kopieren]').forEach(function(b){b.addEventListener('click',function(){
    var t=b.dataset.kopieren;var fertig=function(){var o=b.textContent;b.textContent='Kopiert';setTimeout(function(){b.textContent=o},1400)};
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(fertig,function(){})}})});
  // Glossar-Filter
  var f=document.getElementById('glossar-filter');
  if(f){f.addEventListener('input',function(){var q=f.value.toLowerCase();
    document.querySelectorAll('.glossar .eintrag').forEach(function(e){e.hidden=q&&e.textContent.toLowerCase().indexOf(q)<0})})}
})();
"""


def md(text: str) -> str:
    return markdown.markdown(text, extensions=["tables"])


def seitenrahmen(titel: str, inhalt: str, karte_id: str | None = None) -> str:
    daten = f' data-karte="{E(karte_id)}"' if karte_id else ""
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(titel)} · KI-Datenkatalog</title><meta name="description" content="Wo kommt die Zahl her? Der KI-Datenkatalog erklärt KI-Nutzung und KI-Kosten für Fachbereiche.">
<style>{CSS}</style></head>
<body{daten}>
<header class="top"><div class="wrap"><a class="logo" href="/">KI-Datenkatalog</a>
<nav aria-label="Hauptmenü"><a href="/">Start</a><a href="/glossar">Glossar</a><a href="/ueber">Über diesen Katalog</a></nav></div></header>
<main class="wrap">{inhalt}</main>
<div class="wrap"><footer>Alle Zahlen sind frei erfundene Beispieldaten für 2025. Rollen, Verträge und Kanäle sind erfunden.
<a href="{REPO}">Quellcode und Tests auf GitHub</a></footer></div>
<script>{JS}</script></body></html>"""


def chip(status: str) -> str:
    name = katalog.STATUS[status][0]
    kopf = "🚧 " if status == "baustelle" else ""
    return f'<span class="chip {E(status)}">{kopf}{E(name)}</span>'


def kachel(k: katalog.Karte) -> str:
    m = k.meta
    fuer = "|".join(m.get("fuer", []))
    tags = " · ".join(E(x) for x in m.get("fuer", []))
    return (f'<a class="kachel" href="/karte/{E(k.id)}" data-karte="{E(k.id)}" data-fuer="{E(fuer)}">'
            f'<h3>{E(k.titel)}</h3><p>{E(m["kurzantwort"])}</p>'
            f'<div class="fuss">{chip(k.status)}<span class="tag">{tags}</span></div></a>')


def reihe(titel: str, unter: str, karten: list[katalog.Karte], id_: str = "", versteckt: bool = False) -> str:
    attr = (f' id="{id_}"' if id_ else "") + (" hidden" if versteckt else "")
    inhalt = "".join(kachel(k) for k in karten)
    return (f'<section class="reihe"{attr}><h2>{E(titel)}</h2><p class="unter">{E(unter)}</p>'
            f'<div class="zeile">{inhalt}</div></section>')


def startseite() -> str:
    karten = list(katalog.karten().values())
    neu_datum = max(k.meta["seit"] for k in karten)
    neu = [k for k in karten if k.meta["seit"] == neu_datum]
    genau = [k for k in karten if k.status in ("mit-vorsicht", "baustelle") and k not in neu]
    rollen = "".join(f'<button type="button" data-rolle="{E(r)}" aria-pressed="false">{E(r)}</button>' for r in katalog.ROLLEN)
    verborgen = "".join(kachel(k).replace("<a ", '<a hidden ', 1) for k in karten)  # Vorlagen für die Zeilen "Für dich" und "Zuletzt angesehen"
    inhalt = f"""
<section class="hero"><h1>Woher kommt diese Zahl?</h1>
<p>Hier steht, was die Zahlen zu KI-Nutzung und KI-Kosten bedeuten, wie sie entstehen, wie verlässlich sie sind und wer helfen kann.</p>
<form class="suche" action="/suche" method="get" role="search"><label class="sr" for="q" style="position:absolute;left:-9999px">Frage oder Begriff</label>
<input id="q" name="q" placeholder="Zum Beispiel: Was kostet KI pro Abteilung?" autocomplete="off"><button type="submit">Suchen</button></form>
<div class="rollen" role="group" aria-label="Rolle wählen"><span class="l">Ich arbeite in:</span>{rollen}</div></section>
{reihe("Für dich", "Karten für deine Rolle. Deine Auswahl bleibt nur in deinem Browser.", [], "fuer-dich", True)}
{reihe("Zuletzt angesehen", "Nur in deinem Browser gemerkt.", [], "zuletzt", True)}
{reihe("Neu im Katalog", f"Seit {neu_datum:%d.%m.%Y}", neu)}
{reihe("Hier bitte genau lesen", "Diese älteren Karten haben eine bekannte Lücke. Der Status steht auf jeder Karte.", genau) if genau else ""}
<section class="reihe"><h2>Alle Auswertungen</h2><div class="raster">{"".join(kachel(k) for k in karten)}</div></section>
<div hidden id="vorlagen">{verborgen}</div>"""
    return seitenrahmen("Start", inhalt)


def kartenseite(karte_id: str) -> str | None:
    k = katalog.karten().get(karte_id)
    if not k:
        return None
    m = k.meta
    name, bedeutung = katalog.STATUS[k.status]
    kopf = "🚧 " if k.status == "baustelle" else ""
    hinweis = f" {m['status_hinweis']}" if m.get("status_hinweis") else ""
    abz = "".join(f'<li title="{E(t)}">{E(n)}</li>' for n, t in k.abzeichen())
    stationen = "".join(f'<li><b>{E(s["station"])}</b><span>{E(s["text"])}</span></li>' for s in m["herkunft"])
    fragen = "".join(
        f'<li><span>{E(f)}</span><button type="button" class="leise" data-kopieren="{E(f)}">Kopieren</button></li>'
        for f in m.get("beispielfragen", []))
    nv = "".join(f"<li>{E(x)}</li>" for x in m.get("nicht_verwechseln", []))
    abschnitte = "".join(
        f'<section class="abschnitt"><h2>{E(a)}</h2>{md(k.abschnitte[a])}</section>'
        for a in katalog.ABSCHNITTE[:3])
    issue = f"{REPO}/issues/new?title=" + quote(f"Karte {k.id}: Verbesserungsvorschlag")
    inhalt = f"""
<div class="krumen"><a href="/">Start</a> › Auswertungen</div>
<article class="karte"><h1>{E(k.titel)}</h1>
<div class="antwort">{E(m["kurzantwort"])}</div>
<div class="status {E(k.status)}"><b>{kopf}Status: {E(name)}</b>{E(bedeutung)}{E(hinweis)}</div>
<ul class="abzeichen" aria-label="Geprüfte Eigenschaften">{abz}</ul>
{abschnitte}
<section class="abschnitt"><h2>Woher kommt die Zahl?</h2><ol class="linie">{stationen}</ol></section>
<section class="abschnitt"><h2>Nicht zu verwechseln mit</h2><ul>{nv}</ul></section>
<section class="abschnitt"><h2>Frag den Chat</h2><p>Diese Fragen beantwortet der Chat aus dieser Karte. Mehr dazu unter <a href="/ueber">Über diesen Katalog</a>.</p>
<div class="chat"><ul>{fragen}</ul></div></section>
<section class="abschnitt"><h2>Wer hilft?</h2>{md(k.abschnitte["Wer hilft?"])}
<p><a class="knopf leise" href="{issue}">Verbesserung vorschlagen</a></p></section>
<section class="abschnitt"><h2>Was hat sich geändert?</h2>{md(k.abschnitte["Was hat sich geändert?"])}</section>
<details class="it"><summary>Für die IT</summary><p>Technischer Name: {E(m["technischer_name"])}<br>Quelle im Katalog: <code>katalog/auswertungen/{E(k.id)}.md</code></p></details>
</article>
<div hidden id="vorlagen">{"".join(kachel(x).replace("<a ", "<a hidden ", 1) for x in katalog.karten().values())}</div>"""
    return seitenrahmen(k.titel, inhalt, karte_id=k.id)


def glossarseite() -> str:
    eintraege = ""
    for e in sorted(katalog.glossar(), key=lambda x: x.name.lower()):
        siehe = ", ".join(f'<a href="/karte/{E(i)}">{E(katalog.karten()[i].titel)}</a>' for i in e.siehe if i in katalog.karten())
        eintraege += (f'<div class="eintrag"><dt id="{E(re.sub(r"[^a-z0-9]+", "-", e.name.lower()))}">{E(e.name)}</dt>'
                      f'<dd>{E(e.text)}'
                      + (f'<div class="syn">Auch genannt: {E(", ".join(e.synonyme))}</div>' if e.synonyme else "")
                      + (f'<div class="nv">Nicht zu verwechseln mit: {E(e.abgrenzung)}</div>' if e.abgrenzung else "")
                      + (f'<div class="nv">Mehr dazu: {siehe}</div>' if siehe else "") + "</dd></div>")
    inhalt = f"""<section class="hero"><h1>Glossar</h1>
<p>So sind die Begriffe in diesem Katalog gemeint.</p>
<div class="suche"><label for="glossar-filter" style="position:absolute;left:-9999px">Begriff filtern</label>
<input id="glossar-filter" placeholder="Begriff filtern, zum Beispiel Lizenz" autocomplete="off"></div></section>
<dl class="glossar">{eintraege}</dl>"""
    return seitenrahmen("Glossar", inhalt)


def suchseite(q: str) -> str:
    q = q.strip()[:200]
    karten = katalog.karten()
    treffer = katalog.suche(q) if q else []
    begriff = katalog.finde_begriff(q) if q else None
    teile = ""
    if treffer:
        teile += '<section class="reihe"><h2>Passende Karten</h2><div class="raster">' + "".join(kachel(karten[t["id"]]) for t in treffer) + "</div></section>"
    if begriff:
        teile += (f'<section class="reihe"><h2>Begriff: {E(begriff.name)}</h2><p>{E(begriff.text)}</p>'
                  + (f'<p class="leer">Nicht zu verwechseln mit: {E(begriff.abgrenzung)}</p>' if begriff.abgrenzung else "")
                  + '<p><a href="/glossar">Zum Glossar</a></p></section>')
    if q and not teile:
        teile = ('<section class="reihe"><h2>Das steht nicht im Katalog.</h2><p class="unter">Zu dieser Frage gibt es keine Karte. '
                 'Der Katalog sagt das lieber ehrlich, als zu raten.</p>'
                 + "".join(f'<p><a href="/karte/{E(k.id)}">{E(k.titel)}</a></p>' for k in karten.values()) + "</section>")
    inhalt = f"""<section class="hero"><h1>Suche</h1>
<form class="suche" action="/suche" method="get" role="search"><label for="q" style="position:absolute;left:-9999px">Frage oder Begriff</label>
<input id="q" name="q" value="{E(q)}" autocomplete="off"><button type="submit">Suchen</button></form></section>{teile}"""
    return seitenrahmen("Suche", inhalt)


def ueberseite() -> str:
    inhalt = f"""<section class="hero"><h1>Über diesen Katalog</h1></section>
<div class="abschnitt"><h2>Was das hier ist</h2>
<p>Ein Beispielkatalog für Fachbereiche. Er erklärt Zahlen zu KI-Nutzung und KI-Kosten: was sie bedeuten, wie sie berechnet werden,
woher sie kommen, wie verlässlich sie sind und wer helfen kann. Er zeigt keine Live-Daten.</p></div>
<div class="abschnitt"><h2>Was echt ist und was erfunden</h2>
<ul><li><b>Erfunden:</b> alle Daten, Anbieter, Verträge, Rollen und Kanäle. Es gibt keinen Bezug zu realen Unternehmen oder Personen.</li>
<li><b>Echt:</b> Jede Zahl auf den Karten wird von einem Test aus den Beispieldaten nachgerechnet. Die Abzeichen auf den Karten werden nur vergeben, wenn die Bedingung erfüllt ist.</li>
<li><b>Bewusst nicht vorhanden:</b> Sterne, Punkte und Beliebtheitslisten. Ohne echte Nutzung dahinter wären sie erfunden. "Für dich" und "Zuletzt angesehen" bleiben im eigenen Browser.</li></ul></div>
<div class="abschnitt"><h2>So fragt man den Chat</h2>
<p>Dieser Katalog hat einen MCP-Server. Das ist eine Schnittstelle, über die ein Chat-Programm wie Claude den Katalog lesen kann.
In Claude fügst du in den Einstellungen unter Konnektoren einen benutzerdefinierten Konnektor hinzu (je nach Tarif) und trägst die Adresse deines
Servers ein, die auf <code>/mcp</code> endet. Danach kannst du Fragen wie <i>"Was kostet uns KI pro Abteilung?"</i> stellen.</p>
<p>Der Chat soll nur aus dem Katalog antworten, die Karte als Quelle nennen und bei Lücken <i>"Das steht nicht im Katalog."</i> sagen.
Das haben wir mit Testfragen geprüft, darunter zwei Fallen. Die Testfragen stehen im Repository.</p></div>
<div class="abschnitt"><h2>Was in der Praxis die Arbeit ist</h2>
<p>Die Technik dahinter ist klein. Aufwendig ist, dass die Fachbereiche die Texte pflegen: Was bedeutet die Zahl, wer ist zuständig, wo ist eine Lücke.
Der Katalog hilft nur, solange diese Texte aktuell bleiben.</p>
<p><a href="{REPO}">Zum Repository</a></p></div>"""
    return seitenrahmen("Über diesen Katalog", inhalt)


def nicht_gefunden() -> str:
    return seitenrahmen("Nicht gefunden", '<section class="hero"><h1>Diese Karte gibt es nicht.</h1><p><a href="/">Zurück zum Start</a></p></section>')
