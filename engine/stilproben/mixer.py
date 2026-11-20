"""Einfacher Ton-Mixer fuer die Stilproben: Effekte zu Zeitpunkten + Musikbett, Master auf -14 LUFS / True Peak -2 dB.
mix(video_in, video_out, events=[(t, pfad, gain)], music=(pfad, gain, start, fade_in, fade_out, swells=[(t, db, dauer)]), dur)"""
import subprocess, json, numpy as np, os, re
SR = 48000
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
_C = {}
def clip(p):
    if p not in _C: _C[p] = load(p)
    return _C[p]
def place(buf, a, t, g):
    i = int(t * SR)
    if i >= len(buf): return
    a = a[:len(buf) - i]; buf[i:i + len(a)] += a * g

def lufs(path):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(o[o.rindex("{"):o.rindex("}") + 1]); return float(j["input_i"]), float(j["input_tp"])

def mix(vin, vout, events, dur, music=None, master_lufs=-14.0):
    buf = np.zeros((int(dur * SR), 2), np.float32)
    musics = music if isinstance(music, list) else ([music] if music else [])
    for mu in musics:   # (pfad, gain, start, fade_in, fade_out, swells, offset, ende)
        p, g, start, fi, fo = mu[:5]; swells = mu[5] if len(mu) > 5 else []; off = mu[6] if len(mu) > 6 else 0
        end = mu[7] if len(mu) > 7 else dur
        m = clip(p)[int(off * SR): int(off * SR) + int((end - start) * SR)].copy()
        n = len(m); env = np.ones(n, np.float32) * g
        k = min(n, int(fi * SR)); env[:k] *= np.linspace(0, 1, k)
        k = min(n, int(fo * SR)); env[n - k:] *= np.linspace(1, 0, k)
        tt = np.arange(n) / SR + start
        for ts, db, d in swells:      # Swell/Dip: +-db als Dreieck ueber +-d Sekunden
            sh = np.clip(1 - np.abs(tt - ts) / d, 0, 1); env *= 10 ** (db * sh / 20)
        place(buf, m * env[:, None], start, 1.0)
    for t, p, g in events:
        place(buf, clip(p), t, g)
    tmp = vout + ".wav"
    pk = np.abs(buf).max() + 1e-9; buf = buf / pk * 0.5
    import wave
    with wave.open(tmp, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(buf, -1, 1) * 32767).astype("<i2").tobytes())
    i, tp = lufs(tmp); gain = master_lufs - i + 1.5
    for _ in range(3):
        af = f"highpass=f=35,equalizer=f=6000:width_type=o:width=1:g=-4,equalizer=f=500:width_type=o:width=1.2:g=2,volume={gain:.2f}dB,alimiter=limit={10 ** (-3.5 / 20):.3f}:level=false"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", vin, "-i", tmp, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", af,
                        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", str(dur), vout], check=True)
        got, _ = lufs(vout)
        if abs(got - master_lufs) < 0.6: break
        gain += (master_lufs - got)
    os.remove(tmp)
    return lufs(vout)
