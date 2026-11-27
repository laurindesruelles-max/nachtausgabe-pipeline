"""Erzeugt bilddrehbuch.json aus lines.py + episode.py (Zahlen im Satz als Ziffern für die Prüfung)."""
import json, os, sys, importlib.util
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "..", "engine"))
def load(n):
    sp = importlib.util.spec_from_file_location(n, os.path.join(H, n + ".py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
L = load("lines").LINES; E = load("episode")
NUM = [("neunzehnhundertfünfundvierzig", "1945"), ("neunzehnhundertachtundfünfzig", "1958"), ("siebzehnhundertdreiundzwanzig", "1723"), ("siebzehnhundertdreißig", "1730"),
       ("zweitausendneunzehn", "2019"), ("zweitausendsechs", "2006"), ("Zweitausendsechs", "2006"), ("zweitausendsiebzehn", "2017"), ("zweitausendzwanzig", "2020"),
       ("zweitausendzweiundzwanzig", "2022"), ("zweitausenddreiundzwanzig", "2023"), ("zweitausendvierundzwanzig", "2024"), ("Fünfundzwanzigster", "25."), ("fünfundzwanzigsten", "25."),
       ("siebzehnten", "17."), ("sechzehnten", "16."), ("vier Uhr siebenundfünfzig", "4:57 Uhr"), ("vier Uhr neunundfünfzig", "4:59 Uhr"), ("kurz vor fünf Uhr", "kurz vor 5 Uhr"),
       ("viertausenddreihundert Diamanten", "4300 Diamanten"), ("hundertdreizehn Millionen Euro", "113 Millionen Euro"), ("hundertachtundzwanzig Millionen Euro", "128 Millionen Euro"),
       ("Hundert Kilogramm", "100 Kilogramm"), ("sechzehnhundert Polizisten", "1600 Polizisten"), ("achtzehn Orte", "18 Orte"), ("einunddreißig Einzelteile", "31 Einzelteile"),
       ("vier Jahren und vier Monaten und sechs Jahren und drei Monaten", "4 Jahren 4 Monaten und 6 Jahren 3 Monaten"), ("dreihundert Jahre", "300 Jahre")]
AN = {"lamp": "Flackernde Lampe", "smoke": "Regen, Schnee, Rauch", "snow": "Regen, Schnee, Rauch", "breathe": "Panel-Fahrt", "pulse": "Flackernde Lampe", "flashes": "Blitzlicht",
      "flashlight": "Taschenlampe", "shatter": "Panel zerbricht"}
OV = {"caption": "Erzählkästchen", "headline": "Schlagzeile knallt", "wanted": "Fahndungsplakat", "clock": "Zeitsprung-Uhr", "bubble": "Sprechblase"}
MO = {"counter": "Beute-Zahl (`motion` counter)", "map": "Panel-Grafik Karte (`motion` map)", "flow": "Der Plan (`motion` flow)", "flip": "Fahndungsplakat dreht sich (`motion` flip)",
      "stack": "Akten-Stapel (`motion` stack)", "bars": "Zeitungsgrafik"}
NEU = {1: "frage:wer", 7: "frage:juwelen0", 10: "frage:diamant", 23: "frage:schwachstelle", 29: "antwort:schwachstelle", 47: "antwort:wer", 49: "antwort:juwelen0", 51: "frage:wieder", 54: "antwort:wieder",
       55: "frage:juwelen", 60: "antwort:juwelen", 62: "frage:rest", 63: "antwort:diamant", 69: "frage:insider", 70: "teaser:weisser"}
out = []
for k in sorted(L):
    s = L[k]
    for a, b in NUM: s = s.replace(a, b)
    p = E.P[k]; evs = []
    if k in E.CHAPTERS: evs.append(("Extrablatt", "Extrablatt aus der Druckerpresse: " + E.CHAPTERS[k][1]))
    if k in E.MOTION: evs.append((MO[E.MOTION[k][0]], f"2D-Grafik im Panel: {E.MOTION[k][1].get('label', '')} {E.MOTION[k][1].get('caption', '')}".strip()))
    for o in p["ov"]: evs.append((OV.get(o[0], "Erzählkästchen"), f"{OV.get(o[0])}: {o[3].get('text') or o[3].get('name') or o[3].get('lines') or o[3].get('y1', '')}"))
    for f in p["fx"]: evs.append((AN[f["type"]], f"{AN[f['type']]} im Panel (Szene: Zeile {k})"))
    evs.append(("Panel-Fahrt", "Kamera fährt im Panel weiter, dann Sprung zum nächsten Panel"))
    seen, ev2 = set(), []
    for a, z in evs:
        if a not in seen: seen.add(a); ev2.append((a, z))
    dur = len(L[k].split()) / 2.4 + 1.0 + (E.CH_PAUSE if k in E.CHAPTERS else 0)
    n = int(dur // 4.2) + 1
    pad = [("Panel-Fahrt", "Kamera driftet weiter durchs Panel"), ("Flackernde Lampe", "Licht im Panel flackert")]
    while len(ev2) < n: ev2.append(pad[len(ev2) % 2])
    n = min(n, len(ev2)) if dur > 4.2 * len(ev2) else n
    ev2 = ev2[:max(1, n)]; n = len(ev2)
    has_t = any(c.isdigit() for c in s)
    import re
    inh = ["geschehen"] + (["zeit"] if __import__("bilddrehbuch").UHR.search(s) or __import__("bilddrehbuch").JAHR.search(s) or re.search(r"\b\d{1,2}[:.]\d{2}\s*(Uhr)?\b|\b\d{1,2}\s*Uhr\b|\b(1[0-9]{3}|20[0-9]{2})\b", s) else []) + (["zahl"] if has_t else [])
    for i, (a, z) in enumerate(ev2):
        out.append({"satz": s if i == 0 else "", "sek": round(dur / n, 1), "zeigt": z + f" – Zeile {k}: {L[k][:60]}", "animation": a, "inhalt": inh,
                    "genauigkeit": "exakt" if (has_t or k in E.MOTION or i == 0) else "schema", "neugier": NEU.get(k, "") if i == 0 else "",
                    "kapitel": max([0] + [c for c in E.CHAPTERS if c <= k])})
json.dump(out, open(os.path.join(H, "bilddrehbuch.json"), "w"), ensure_ascii=False, indent=1)
print(len(out), "Einträge")
