"""Nachtausgabe-Renderer.
Aufruf:  WORK=/pfad/arbeitsordner python3 engine/render.py AUSGABE.mp4 videos/NNN-slug
Standbilder: WORK=... EPISODE=videos/NNN-slug python3 engine/render.py stills 30 120 200
Nur Ton neu mischen: AUDIO_ONLY=1 (nutzt WORK/full_v.mp4)
Im WORK-Ordner: img/pNN.png (Panels), vo/sNN.mp3 (Sprecherzeilen)."""
import sys, math, subprocess, json, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *

def vo(i):
    a = load_audio(f"{ROOT}/vo/s{i:02d}.mp3")
    e = np.abs(a).max(axis=1); idx = np.where(e > 0.01)[0]
    a0 = max(idx[0] - int(0.03 * SR), 0) if len(idx) else 0
    a = a[a0:]; idx = idx - a0
    return a, (idx[-1] + 1) / SR if len(idx) else len(a) / SR

# Episode laden
import importlib.util
EP_DIR = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] != "stills" else os.environ["EPISODE"])
_spec = importlib.util.spec_from_file_location("episode", os.path.join(EP_DIR, "episode.py"))
EP = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(EP)
P, CHAPTERS, PRE = EP.P, EP.CHAPTERS, EP.PRE
CH_PAUSE = getattr(EP, "CH_PAUSE", 2.2)



def title_panel():
    im = Image.new("RGB", (PW, PH), INK); d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(FONT_TITLE, 120); f2 = ImageFont.truetype(FONT_CAP, 50)
    for i, t in enumerate(EP.TITLE_LINES):
        w = d.textlength(t, font=f1); d.text(((PW - w) / 2, 200 + i * 140), t, font=f1, fill=AMBER, stroke_width=4, stroke_fill=(0, 0, 0))
    t = "NACHTAUSGABE"; w = d.textlength(t, font=f2)
    d.rectangle([(PW - w) / 2 - 30, 560, (PW + w) / 2 + 30, 640], fill=PAPER); d.text(((PW - w) / 2, 570), t, font=f2, fill=INK)
    return np.array(im)

def _audiokit():
    """Gemeinsames Ton-Werkzeug (Repo sound-mediathek/audiokit, setup.sh lädt es). Fehlt es, läuft der alte Weg weiter."""
    d = os.environ.get("AUDIOKIT", "/home/claude/audiokit")
    if not os.path.exists(f"{d}/adapter.py"): print("WARNUNG: audiokit fehlt – sh setup.sh ausführen"); return None
    sys.path.insert(0, d); import adapter; return adapter

def main(out_mp4, stills=None):
    order = list(range(1, EP.TITLE_AFTER + 1)) + ["T"] + list(range(EP.TITLE_AFTER + 1, EP.N_PANELS + 1))
    imgs = []
    for k in order:
        imgs.append(title_panel() if k == "T" else cv2.resize(np.array(Image.open(f"{ROOT}/img/p{k:02d}.png").convert("RGB")), (PW, PH), interpolation=cv2.INTER_AREA))
    strip, rects = build_strip(imgs)
    slot = {k: i for i, k in enumerate(order)}
    page_of = lambda k: slot[k] // 6

    shots, vos, t = [], {}, 1.4
    music_marks = [(0.0, 1)]
    for k in order:
        if k == "T":
            shots.append(dict(k="T", start=t, v0=t, v1=t + 3.0, end=t + 3.2)); t += 3.2
        else:
            pre = PRE.get(k, 0.0)
            if k in CHAPTERS: pre = CH_PAUSE; music_marks.append((t - 0.3, CHAPTERS[k][2]))
            if k != 1: a, L_ = vo(k)
            else: a, L_ = vo(1)
            vos[k] = a
            start = t; v0 = start + pre + 0.15; v1 = v0 + L_; end = v1 + 0.7
            shots.append(dict(k=k, start=start, v0=v0, v1=v1, end=end, pre=pre))
            t = end
        if len(shots) < len(order):
            nxt = order[len(shots)]
            t += 0.55 if page_of(shots[-1]["k"]) == page_of(nxt) else 0.95
    T_END = t + 4.0
    print("Länge:", round(T_END, 1), "s =", int(T_END // 60), "min", int(T_END % 60), "s")

    overlays = []
    for s in shots:
        if s["k"] == "T": continue
        for kind, a, b, kw in P[s["k"]]["ov"]:
            overlays.append(Overlay(kind, s["v0"] + a, (s["v0"] + b) if b else s["end"] - 0.05, **kw))
        if s["k"] in CHAPTERS:
            n, ti, _ = CHAPTERS[s["k"]]
            overlays.append(Overlay("chapter", s["start"] + 0.1, s["v0"] - 0.1, num=n, title=ti))
    stamps = [o.t0 + 0.14 for o in overlays if o.kind == "stamp"]

    def view_of(s, z=0.0):
        return panel_view(rects[slot[s["k"]]], z, (0, 0) if s["k"] == "T" else P[s["k"]]["drift"])
    def camera(t):
        if t < 1.4: return lerp_view(page_view(0), view_of(shots[0]), ease(t / 1.4))
        for i, s in enumerate(shots):
            dur = s["end"] - s["start"]
            if s["start"] <= t <= s["end"]: return view_of(s, 0.07 * (t - s["start"]) / dur)
            if i + 1 < len(shots) and s["end"] < t < shots[i + 1]["start"]:
                a, b = view_of(s, 0.07), view_of(shots[i + 1])
                u = ease((t - s["end"]) / (shots[i + 1]["start"] - s["end"]))
                if page_of(s["k"]) != page_of(shots[i + 1]["k"]):
                    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, a[2] * 0.5)
                    return lerp_view(a, mid, ease(u * 2)) if u < 0.5 else lerp_view(mid, b, ease(u * 2 - 1))
                return lerp_view(a, b, u)
        last = shots[-1]
        return lerp_view(view_of(last, 0.07), page_view(page_of(last["k"])), ease((t - last["end"]) / 1.5))

    grains = [rng.normal(0, 7, (H, W, 1)).astype(np.float32) for _ in range(6)]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vign = np.clip(1 - 0.35 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.4, 0.55, 1)[..., None]
    fx_of = {slot[k]: P[k]["fx"] for k in P}

    def frame_at(t, fi=0):
        cx, cy, s = camera(t)
        cx += 5 * math.sin(t * 0.7) / s * 2; cy += 4 * math.sin(t * 0.9 + 1) / s * 2
        for st in stamps:
            d = t - st
            if 0 <= d < 0.3:
                k = (1 - d / 0.3) * 14 / s; cx += k * math.sin(d * 90); cy += k * math.cos(d * 77)
        vw, vh = W / s, H / s
        x0 = int(max(cx - vw / 2 - 4, 0)); y0 = int(max(cy - vh / 2 - 4, 0))
        x1 = int(min(cx + vw / 2 + 4, strip.shape[1])); y1 = int(min(cy + vh / 2 + 4, strip.shape[0]))
        crop = strip[y0:y1, x0:x1].copy()
        for j, r in enumerate(rects):
            if j not in fx_of: continue
            x, y, w, h = r
            if x < x1 and x + w > x0 and y < y1 and y + h > y0:
                ani = apply_fx(j, imgs[j].copy(), t, fx_of[j])
                ax0, ay0 = max(x, x0), max(y, y0); ax1, ay1 = min(x + w, x1), min(y + h, y1)
                crop[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0] = ani[ay0 - y:ay1 - y, ax0 - x:ax1 - x]
        Mx = np.array([[s, 0, W / 2 - s * (cx - x0)], [0, s, H / 2 - s * (cy - y0)]], np.float32)
        fr = cv2.warpAffine(crop, Mx, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(24, 22, 20))
        for ov in overlays: fr = ov.draw(fr, t)
        fr = np.clip(fr.astype(np.float32) * vign + grains[fi % 6], 0, 255)
        if t > T_END - 1.0: fr *= max((T_END - t) / 1.0, 0)
        if t < 0.4: fr *= t / 0.4
        return fr.astype(np.uint8)

    if stills:
        for ta in stills: Image.fromarray(frame_at(ta)).save(f"{ROOT}/stills/full_{ta:06.1f}.png")
        return

    import os
    AUDIO_ONLY = os.environ.get("AUDIO_ONLY") == "1"
    n = int(T_END * FPS)
    if AUDIO_ONLY: n = 0
    ff = None if AUDIO_ONLY else subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", f"{ROOT}/full_v.mp4"], stdin=subprocess.PIPE)
    for f in range(n):
        ff.stdin.write(frame_at(f / FPS, f).tobytes())
        if f % 600 == 0: print(f, "/", n, flush=True)
    if ff: ff.stdin.close(); ff.wait()

    # ---------- Ton ----------
    N = int((T_END + 1) * SR)
    voice = np.zeros((N, 2), np.float32); buf = np.zeros((N, 2), np.float32)
    for s in shots:
        if s["k"] != "T": mix_into(voice, vos[s["k"]], s["v0"], 1.0)
    rms = np.sqrt(np.mean(voice[np.abs(voice) > 1e-4] ** 2)); voice *= 0.12 / max(rms, 1e-6)
    buf += voice
    cache = {}
    def sfx(name):
        if name not in cache: cache[name] = load_audio(f"{REPO}/assets/sfx/{name}.mp3")
        return cache[name]
    _ev = []   # Geräusche erst sammeln, dann audiokit aufräumen lassen (Wiederholung, Dichte, defekte Dateien)
    def _add(name, t, g, **kw): _ev.append((t, name, g, kw))
    for i, s in enumerate(shots):
        if s["k"] == "T":
            _add("logo-reveal-01", s["start"] - 0.1, 0.45); _add("cinematic-boom-01", s["start"] + 0.05, 0.45); continue
        for name, at, g in P[s["k"]]["sfx"]:
            _add(name, s["v0"] + at, g * 0.5, fade_out=0.15)
        if P[s["k"]].get("rain"):
            _add("ambience-rain-03", s["start"] - 0.2, 0.2, fade_in=0.4, fade_out=0.5, max_len=min(s["end"] - s["start"] + 0.6, 9.2))
        if s["k"] in CHAPTERS:
            _add("cinematic-boom-01", s["start"] + 0.1, float(os.environ.get("CH_BOOM", "0.18")))
        if i + 1 < len(shots):
            if page_of(s["k"]) != page_of(shots[i + 1]["k"]): _add("paper-fabric-card-flip-06", s["end"] + 0.15, 0.55)
            else: _add("short-video-whoosh-01", s["end"] + 0.05, 0.12)
    AK0 = _audiokit()
    kw_of = {}
    evs = [(t, n, g) for t, n, g, kw in _ev]
    for t, n, g, kw in _ev: kw_of[(round(t, 4), n)] = kw
    if AK0 is not None: evs = AK0.clean_events(evs, "nachtausgabe", f"{REPO}/assets/sfx")
    for t, n, g in evs: mix_into(buf, sfx(n), t, g, **kw_of.get((round(t, 4), n), {}))
    # Musik je Kapitel, mit Pause beim Wechsel und vor dem Wendepunkt
    tracks = json.loads(os.environ["TRACKS"]) if os.environ.get("TRACKS") else {1: "noir_1_einstieg", 2: "noir_2_aufstieg", 3: "noir_3_jagd", 4: "noir_4_prozess", 5: "noir_5_ende"}
    tracks = {int(k): v for k, v in tracks.items()}
    MG = float(os.environ.get("MUSIC_GAIN", "1.15"))
    np.save(f"{ROOT}/stem_voice_sfx.npy", buf[:int(T_END * SR)])
    marks = music_marks + [(T_END, None)]
    music = np.zeros_like(buf)
    AK = _audiokit()
    if AK is not None:
        # audiokit (18.11.2026): innerhalb eines Kapitels wechselt die Musik spätestens alle ~80 s auf eine andere Stelle
        # des Stücks bzw. das Zweitstück – vor Stempeln/Wendepunkt gezielt eine kräftige Stelle. Kein Stopp, keine Pause
        # (Laurin 18.11.). Lautstärke-Kurve, Anschwellen und Ducking bleiben unten genau wie abgenommen.
        from dramaturgie import Dramaturgie
        alt = {1: 3, 2: 3, 3: 2, 4: 3, 5: 4}
        mp = lambda tr: f"{REPO}/assets/music/{tracks[tr]}.mp3"
        stamps = [o.t0 for o in overlays if o.kind == "stamp"]
        tw = [s["v1"] for s in shots if s["k"] == getattr(EP, "TWIST", None)]
        d = Dramaturgie("nachtausgabe", T_END, [(t0, "k" if i else None) for i, (t0, _) in enumerate(marks[:-1])], [],
                        [(t, "stempel", 3) for t in stamps] + [(t, "wendepunkt", 4) for t in tw])
        music = d.music_bed(N, SR, None, [[mp(tr), mp(alt.get(tr, tr))] for _, tr in marks[:-1]], xf=2.5, envelope=False, calibrate=False)
        music *= 0.045 / max(float(np.sqrt(np.mean(music ** 2))), 1e-6)
        AK.LOG.append("MUSIK   " + d.report([s["start"] for s in shots])); print(AK.LOG[-1])
        marks = []   # alter Ein-Stück-pro-Kapitel-Weg wird übersprungen
    for (t0, tr), (t1, _) in zip(marks[:-1], marks[1:]):
        m = load_audio(f"{REPO}/assets/music/{tracks[tr]}.mp3")
        # leise Anfänge/Enden weg (Fenster 0,25 s unter -32 dB)
        w_ = int(0.25 * SR); r_ = np.array([np.sqrt(np.mean(m[i:i + w_] ** 2)) for i in range(0, len(m) - w_, w_)])
        loud = np.where(20 * np.log10(r_ + 1e-9) > -32)[0]
        if len(loud): m = m[loud[0] * w_:(loud[-1] + 1) * w_]
        XF = 2.5
        st = t0 if tr == 1 else t0 - XF / 2
        seg_len = (t1 + (XF / 2 if t1 < T_END else 0)) - st
        need = int(seg_len * SR)
        if len(m) < need:  # weich schleifen
            xf = int(2.0 * SR); out = m.copy()
            while len(out) < need:
                ramp = np.linspace(0, 1, xf)[:, None]
                out[-xf:] = out[-xf:] * (1 - ramp) + m[:xf] * ramp
                out = np.concatenate([out, m[xf:]])
            m = out
        m = m[:need].copy()
        rms = np.sqrt(np.mean(m ** 2)); m *= 0.045 / max(rms, 1e-6)   # jede Spur gleich laut
        fi = int((1.0 if tr == 1 else XF) * SR); fo = int((2.0 if t1 >= T_END else XF) * SR)
        m[:fi] *= np.linspace(0, 1, fi)[:, None]; m[-fo:] *= np.linspace(1, 0, fo)[:, None]
        mix_into(music, m, st, 1.0)
    # Musik-Leveler: leise Stellen in den Stücken anheben, damit nichts abbricht
    w_ = int(0.1 * SR); nb = len(music) // w_
    r_ = np.sqrt(np.mean(music[:nb * w_].reshape(nb, w_, 2) ** 2, axis=(1, 2)))
    k_ = 15; r_s = np.sqrt(np.convolve(r_ ** 2, np.ones(k_) / k_, mode="same"))
    gl = np.clip(0.045 / np.maximum(r_s, 1e-5), 0.6, 5.0)
    gl = np.convolve(gl, np.ones(9) / 9, mode="same")
    glf = np.repeat(gl, w_); glf = np.pad(glf, (0, len(music) - len(glf)), mode="edge")
    music *= glf[:, None]
    g = np.full(N, MG, np.float32)
    def env(t0, t1, f0, f1):
        i0, i1 = max(int(t0 * SR), 0), min(int(t1 * SR), N)
        if i1 > i0: g[i0:i1] *= np.linspace(f0, f1, i1 - i0)
    def hold(t0, t1, f):
        i0, i1 = max(int(t0 * SR), 0), min(int(t1 * SR), N)
        if i1 > i0: g[i0:i1] *= f
    s13 = [s for s in shots if s["k"] == getattr(EP, "TWIST", None)]
    s13 = s13[0] if s13 else None
    if s13:
        env(s13["start"] - 0.6, s13["start"], 1.0, 0.6); hold(s13["start"], s13["v1"] - 1.5, 0.6)
        env(s13["v1"] - 1.5, s13["v1"] + 0.5, 0.6, 1.35); env(s13["v1"] + 0.5, s13["v1"] + 3.0, 1.35, 1.0)
    hits = sorted(set([o.t0 + 0.14 for o in overlays if o.kind == "stamp"] + [s["start"] + 0.1 for s in shots if s["k"] in CHAPTERS]))
    for h in hits:
        env(h - 1.8, h, 1.0, 1.45); env(h, h + 1.6, 1.45, 1.0)
    # Ducking: unter der Stimme etwas leiser, in Sprechpausen voller
    act = (np.abs(voice).max(axis=1) > 0.02).astype(np.float32)
    k = int(0.25 * SR); act = np.convolve(act, np.ones(k, np.float32) / k, mode="same")
    duck = 1.0 - 0.3 * np.clip(act * 3, 0, 1)
    buf += music * (g * duck)[:, None]
    buf = np.tanh(buf * 1.1) * 0.95
    raw = buf[:int(T_END * SR)].astype(np.float32).tobytes()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af", "loudnorm=I=-14:TP=-1.5", f"{ROOT}/full_a.wav"], input=raw)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{ROOT}/full_v.mp4", "-i", f"{ROOT}/full_a.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out_mp4])
    if AK0 is not None:
        import scipy.io.wavfile as _wf
        _wf.write(f"{ROOT}/_v.wav", SR, voice[:int(T_END * SR)].astype(np.float32)); _wf.write(f"{ROOT}/_m.wav", SR, (music * (g * duck)[:, None])[:int(T_END * SR)].astype(np.float32))
        AK0.final_check(f"{ROOT}/full_a.wav", f"{ROOT}/_v.wav", f"{ROOT}/_m.wav"); AK0.write_report(f"{ROOT}/ton_bericht.txt")
    # Kapitelmarken für die Beschreibung
    with open(f"{ROOT}/kapitel.txt", "w") as fh:
        fh.write(f"0:00 {getattr(EP, 'FIRST_CHAPTER_LABEL', 'Einstieg')}\n")
        for s in shots:
            if s["k"] in CHAPTERS:
                m_, s_ = divmod(int(s["start"]), 60); fh.write(f"{m_}:{s_:02d} {CHAPTERS[s['k']][1].title()}\n")

if __name__ == "__main__":
    if sys.argv[1] == "stills": main(None, [float(x) for x in sys.argv[2:]])
    else: main(sys.argv[1])
