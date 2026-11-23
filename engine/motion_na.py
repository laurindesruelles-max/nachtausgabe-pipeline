"""2D-Motion-Graphics fuer Nachtausgabe (Remotion, engine/motion/) – Erweiterung aus der ANOM-Stilprobe (Laurin 23.11.2026:
"Genau so sollte ein Video aussehen" – vor allem die vielen 2D-Animationen). Ersetzt nichts aus EFFEKTE.md/ANIMATION.md
(Comicseite, Panel-Fahrt, Extrablatt, Schlagzeile, Fahndungsplakat, Comic-Stadtplan ... bleiben), sondern ergänzt sie.

Look (engine/motion/src/theme.tsx): Grafik steht IN einem Comic-Panel auf der Seite (Nachbar-Panels am Rand sichtbar –
Kamera bleibt auf der Comicseite), Papierweiß + Tusche + Bernstein, Rasterpunkte, Bangers/Comic Neue, Erzählkästchen,
Tusche-Silhouetten als Symbole (Hut-Mann, Revolver, Oldtimer, Geldbündel ...), Stationen als kleine Comic-Panels mit
Speedlines, Raster als GESUCHT-Mini-Plakate, Enthüllung als Fahndungsplakat mit Strahlenkranz, Tatorte als Comic-Burst.

Bausteine: map (Länder/Regionen – für Straßen den bestehenden Comic-Stadtplan nehmen), flow (der Plan / Ablauf der Tat),
flip (GESUCHT-Plakat dreht sich -> Täter), counter (Beute), grid (Beteiligte), stack (Akten/Prozesse + Frage), bars, phone.
Icons zusätzlich: gun, knife, car, badge, gavel. Fakten wie immer belegt (Quelle im Skript); Zitate nur echte.

Im Video-Skript:
    import motion_na as MO
    K = MO.clip("flip", {...}, len=4.0); MO.build(WORK)
    frame = MO.frame(K, t - t0)          # PIL-RGBA 1920x1080
    events += MO.sounds(K, t0)           # [(t, name, gain, dur)] mit Nachtausgabe-Sounds (assets/sfx, .mp3)
Musik bleibt durchgehend Noir-Jazz (keine Pausen – Laurin). Einmalig: `cd engine/motion && npm install`.
"""
import os, json, hashlib, subprocess
import numpy as np, cv2
from PIL import Image

W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
_JOBS = {}
_WK = {"dir": "."}


def clip(comp, props, len=5.0):
    j = json.dumps({"c": comp, "p": props, "l": float(len)}, sort_keys=True, ensure_ascii=False)
    k = hashlib.sha1(j.encode()).hexdigest()[:12]
    _JOBS[k] = {"comp": comp, "props": props, "len": float(len)}
    return k


def path(k): return os.path.join(_WK["dir"], "motion", f"{k}.mp4")


def build(wk="."):
    _WK["dir"] = wk; os.makedirs(os.path.join(wk, "motion"), exist_ok=True)
    todo = [dict(v, out=os.path.abspath(path(k))) for k, v in _JOBS.items() if not os.path.exists(path(k))]
    if not todo: return
    jf = os.path.abspath(os.path.join(wk, "motion", "jobs.json")); json.dump(todo, open(jf, "w"), ensure_ascii=False, indent=1)
    print(f"motion: {len(todo)} Clips rendern ...")
    subprocess.run(["node", os.path.join(HERE, "motion", "render.mjs"), jf], check=True)


_CAP = {}
def frame(k, lt):
    p = path(k); c = _CAP.get(p)
    if c is None:
        cap = cv2.VideoCapture(p); c = _CAP[p] = [cap, -1, None, int(cap.get(cv2.CAP_PROP_FRAME_COUNT))]
    i = max(0, min(int(lt * FPS), c[3] - 1))
    if i != c[1]:
        if i != c[1] + 1: c[0].set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, fr = c[0].read()
        if ok: c[1], c[2] = i, cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(c[2]).convert("RGBA")


WH = "short-video-whoosh-01"; CARD = "paper-fabric-card-flip-06"
def sounds(k, t0=0.0):
    """Ton-Ereignisse ab Clip-Start t0 (Nachtausgabe-Sounds). Zeitpunkte = comps.tsx."""
    j = _JOBS[k]; c, q, L = j["comp"], j["props"], j["len"]
    ev = [(0.0, WH, 0.2, None)]
    if q.get("label"): ev += [(0.05, CARD, 0.25, None)]
    if c == "map":
        ev += [(0.45 + i * 0.55, "door-knock-01", 0.18, 0.25) for i in range(len(q.get("pins", [])))]
        if q.get("counter"): ev += [(1.6, CARD, 0.3, None)]
    elif c == "flow":
        b = q.get("branch")
        if b: bt = 0.6 + 0.75 * (b["after"] + 0.5); ev += [(bt + 0.5, "impact-slam-35", 0.5, None)]
    elif c == "flip":
        at = q.get("at", 2.4); ev += [(at - 0.05, WH, 0.45, None), (at + 0.15, "reveal-impact-01", 0.7, None)]
    elif c == "counter":
        ev += [(0.1, "empty-banknote-counter-01", 0.16, 1.2)] if q.get("items") == "money" else [(0.1, "clock_tick", 0.25, 1.5)]
        ev += [(0.9, CARD, 0.3, None)]
    elif c == "grid":
        ev += [(0.2, CARD, 0.2, None), (1.6, "impact-slam-35", 0.22, None)]
    elif c == "bars":
        ev += [(0.4 + i * 0.35, CARD, 0.25, None) for i in range(len(q.get("bars", [])))]
    elif c == "stack":
        ev += [(0.1 + i * 0.16, CARD, 0.28, None) for i in range(len(q.get("cards", [])))] + [(1.5, "impact-slam-35", 0.55, None)]
    elif c == "phone":
        ev += [(0.15 + i * 0.4, CARD, 0.15, None) for i in range(len(q.get("messages", [])))]
    return [(t0 + t, n, g, d) for t, n, g, d in ev if t < L and g > 0]
