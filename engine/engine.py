"""Nachtausgabe-Engine (Comic-Noir): Comic-Noir-Video aus Panels, Sprecherzeilen, Effekten und Overlays."""
import subprocess, math, json, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
import os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.environ.get("WORK", "/home/claude/na-work")   # Arbeitsordner mit img/ und vo/
FONTS = os.path.join(REPO, "assets", "fonts")
FONT_TITLE = f"{FONTS}/Bangers-Regular.ttf"
FONT_CAP = f"{FONTS}/ComicNeue-Bold.ttf"
AMBER = (240, 176, 30)
INK = (14, 12, 10)
PAPER = (236, 226, 204)
SR = 48000
rng = np.random.default_rng(11)

# ======================= Seitenlayout =======================
PW, PH = 1344, 752
M, G, BORDER, PGAP = 90, 56, 12, 420
PAGE_W = 2 * M + 3 * PW + 2 * G
PAGE_H = 2 * M + 2 * PH + G

def build_strip(panel_imgs):
    """panel_imgs: Liste von RGB-Arrays (PH x PW). 6 pro Seite."""
    n_pages = (len(panel_imgs) + 5) // 6
    SW = n_pages * PAGE_W + (n_pages - 1) * PGAP
    strip = np.full((PAGE_H, SW, 3), (24, 22, 20), np.uint8)
    rects = []
    for p in range(n_pages):
        ox = p * (PAGE_W + PGAP)
        pg = np.full((PAGE_H, PAGE_W, 3), PAPER, np.float32) + rng.normal(0, 6, (PAGE_H, PAGE_W, 1))
        strip[:, ox:ox + PAGE_W] = np.clip(pg, 0, 255).astype(np.uint8)
    for i, im in enumerate(panel_imgs):
        p, k = divmod(i, 6)
        c, r = k % 3, k // 3
        x = p * (PAGE_W + PGAP) + M + c * (PW + G); y = M + r * (PH + G)
        strip[y - BORDER:y + PH + BORDER, x - BORDER:x + PW + BORDER] = INK
        strip[y:y + PH, x:x + PW] = im
        rects.append((x, y, PW, PH))
    return strip, rects

def page_view(p):
    cx = p * (PAGE_W + PGAP) + PAGE_W / 2
    return (cx, PAGE_H / 2, min(W / (PAGE_W * 1.04), H / (PAGE_H * 1.04)))

# ======================= Effekte =======================
class Particles:
    def __init__(s, n, kind, seed):
        r = np.random.default_rng(seed)
        s.kind = kind
        s.x = r.uniform(-0.1, 1.1, n); s.y = r.uniform(0, 1, n)
        s.v = r.uniform(0.05, 0.12, n) if kind == "snow" else r.uniform(1.6, 2.6, n)
        s.sz = r.uniform(1.5, 4.5, n); s.ph = r.uniform(0, 6.28, n); s.l = r.uniform(0.03, 0.07, n)
    def draw(s, img, t, alpha):
        ov = np.zeros_like(img); h, w = img.shape[:2]
        if s.kind == "snow":
            y = (s.y + s.v * t) % 1.05
            x = s.x + 0.015 * np.sin(t * 1.3 + s.ph)
            for xi, yi, si in zip(x, y, s.sz):
                cv2.circle(ov, (int(xi * w), int(yi * h)), int(si), (245, 240, 230), -1, cv2.LINE_AA)
            ov = cv2.GaussianBlur(ov, (0, 0), 0.8)
        else:
            ang = 0.15
            y = (s.y + s.v * t) % 1.15 - 0.1
            x = (s.x + ang * s.v * t) % 1.3 - 0.2
            for xi, yi, li in zip(x, y, s.l):
                cv2.line(ov, (int(xi * w), int(yi * h)), (int((xi - ang * li) * w), int((yi - li) * h)), (225, 215, 190), 2, cv2.LINE_AA)
        return cv2.addWeighted(img, 1.0, ov, alpha, 0)

def smoke_sprite(size=260, seed=0):
    r = np.random.default_rng(seed)
    n = cv2.resize(r.random((size // 8, size // 8)).astype(np.float32), (size, size), interpolation=cv2.INTER_CUBIC)
    yy, xx = np.mgrid[0:size, 0:size]
    mask = np.exp(-(((xx - size / 2) / (size * 0.3)) ** 2 + ((yy - size / 2) / (size * 0.42)) ** 2))
    a = cv2.GaussianBlur(n * mask, (0, 0), 9); return a / a.max()
SPR = [smoke_sprite(seed=i) for i in range(4)]

def smoke(img, t, src, scale=1.0, strength=0.3, col=(235, 220, 190)):
    h, w = img.shape[:2]; out = img.astype(np.float32)
    for i in range(6):
        ph = (t * 0.22 + i / 6) % 1.0
        cx = src[0] * w + math.sin(ph * 5 + i) * 30 * scale; cy = src[1] * h - ph * 330 * scale
        sz = int((90 + 260 * ph) * scale); spr = cv2.resize(SPR[i % 4], (sz, sz))
        a = spr * strength * math.sin(ph * math.pi)
        x0, y0 = int(cx - sz / 2), int(cy - sz / 2)
        xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + sz, w), min(y0 + sz, h)
        if xb <= xa or yb <= ya: continue
        aa = a[ya - y0:yb - y0, xa - x0:xb - x0][..., None]
        out[ya:yb, xa:xb] = out[ya:yb, xa:xb] * (1 - aa) + np.array(col, np.float32) * aa
    return np.clip(out, 0, 255).astype(np.uint8)

GLOWS = {}
def glow(img, key, c, radius, amount, col=(255, 190, 80)):
    h, w = img.shape[:2]
    if key not in GLOWS:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        g = np.exp(-(((xx - c[0] * w) ** 2 + (yy - c[1] * h) ** 2) / (2 * (radius * w) ** 2)))
        GLOWS[key] = g[..., None] * np.array(col, np.float32)
    return np.clip(img.astype(np.float32) + GLOWS[key] * amount, 0, 255).astype(np.uint8)

def flicker(t, seed=0):
    # unruhiges Lampenflackern
    v = 1.0 + 0.05 * math.sin(t * 9 + seed) + 0.03 * math.sin(t * 23 + seed * 2)
    if int(t * 14 + seed) % 31 in (5, 6): v -= 0.35
    return v

PART = {}
def apply_fx(name, img, t, fx):
    for e in fx:
        k = e["type"]
        if k in ("snow", "rain"):
            key = (name, k)
            if key not in PART: PART[key] = Particles(e.get("n", 320 if k == "snow" else 380), k, hash(key) % 1000)
            img = PART[key].draw(img, t, e.get("alpha", 0.7 if k == "snow" else 0.5))
        elif k == "smoke":
            img = smoke(img, t, e["at"], e.get("scale", 1.0), e.get("strength", 0.3))
        elif k == "lamp":
            f = flicker(t, e.get("seed", 0))
            img = glow(img, (name, "lamp"), e["at"], e.get("r", 0.1), e.get("amount", 0.25) * f)
        elif k == "pulse":
            a = e.get("amount", 0.2) * (0.6 + 0.4 * math.sin(t * e.get("speed", 2.0)))
            img = glow(img, (name, "pulse"), e["at"], e.get("r", 0.12), a)
        elif k == "flashes":
            for j, (tt, pos) in enumerate(e["events"]):
                d = t - tt
                if 0 <= d < 0.35:
                    a = (1 - d / 0.35) ** 2 * 1.4
                    img = glow(img, (name, "flash", j), pos, 0.07, a, (255, 250, 235))
        elif k == "breathe":
            v = 1 + e.get("amount", 0.05) * math.sin(t * e.get("speed", 1.5))
            img = np.clip(img.astype(np.float32) * v, 0, 255).astype(np.uint8)
    return img

# ======================= Overlays =======================
fcap = ImageFont.truetype(FONT_CAP, 48)
def caption_img(text, size=56, big=False):
    f = ImageFont.truetype(FONT_TITLE if big else FONT_CAP, size)
    pad = (34, 10) if big else (28, 16)
    w = int(f.getlength(text)); asc, desc = f.getmetrics()
    im = Image.new("RGBA", (w + 2 * pad[0] + 10, asc + desc + 2 * pad[1] + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([8, 8, im.width - 1, im.height - 1], fill=(0, 0, 0, 255))
    d.rectangle([0, 0, im.width - 10, im.height - 10], fill=AMBER + (255,), outline=INK + (255,), width=5)
    d.text((pad[0], pad[1] - 2), text, font=f, fill=INK)
    return np.array(im)

def stamp_img(text, size=170, rot=-7):
    f = ImageFont.truetype(FONT_TITLE, size)
    w = int(f.getlength(text)); asc, desc = f.getmetrics()
    im = Image.new("RGBA", (w + 120, asc + desc + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([10, 10, im.width - 10, im.height - 10], outline=AMBER + (255,), width=14)
    d.text((60, 30), text, font=f, fill=AMBER, stroke_width=6, stroke_fill=INK)
    im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    return np.array(im)

def bubble_img(lines, size=46):
    f = ImageFont.truetype(FONT_CAP, size)
    lw = max(int(f.getlength(l)) for l in lines); asc, desc = f.getmetrics(); lh = asc + desc + 6
    bw, bh = lw + 120, lh * len(lines) + 90
    im = Image.new("RGBA", (bw, bh + 90), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(bw * 0.30, bh - 20), (bw * 0.18, bh + 80), (bw * 0.40, bh - 25)], fill=(250, 246, 236, 255), outline=INK, width=5)
    d.ellipse([0, 0, bw - 1, bh - 1], fill=(250, 246, 236, 255), outline=INK, width=6)
    d.polygon([(bw * 0.31, bh - 30), (bw * 0.19, bh + 70), (bw * 0.39, bh - 32)], fill=(250, 246, 236, 255))
    for i, l in enumerate(lines):
        d.text(((bw - f.getlength(l)) / 2, 45 + i * lh), l, font=f, fill=INK)
    return np.array(im)

def blit(frame, rgba, cx, cy, scale, alpha):
    if alpha <= 0.01: return frame
    im = cv2.resize(rgba, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR) if abs(scale - 1) > 1e-3 else rgba
    h, w = im.shape[:2]; x, y = int(cx - w / 2), int(cy - h / 2)
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0: return frame
    sub = im[y0 - y:y1 - y, x0 - x:x1 - x]
    a = sub[..., 3:4].astype(np.float32) / 255 * alpha
    frame[y0:y1, x0:x1] = (frame[y0:y1, x0:x1] * (1 - a) + sub[..., :3] * a).astype(np.uint8)
    return frame

class Overlay:
    """kind: caption | stamp | bubble | counter | map"""
    def __init__(s, kind, t0, t1, **kw):
        s.kind, s.t0, s.t1, s.kw = kind, t0, t1, kw
        if kind == "caption":
            s.img = caption_img(kw["text"], kw.get("size", 56), kw.get("big", False))
        elif kind == "stamp":
            s.img = stamp_img(kw["text"], kw.get("size", 170), kw.get("rot", -7))
        elif kind == "bubble":
            s.img = bubble_img(kw["lines"])
    def draw(s, fr, t):
        if not (s.t0 <= t <= s.t1): return fr
        u_in = min((t - s.t0) / 0.22, 1); u_out = min((s.t1 - t) / 0.25, 1); al = max(min(u_in, u_out), 0)
        if s.kind in ("caption", "bubble"):
            sc = 0.75 + 0.25 * (1 - (1 - u_in) ** 3) + 0.05 * math.sin(u_in * math.pi)
            h, w = s.img.shape[:2]
            px, py = s.kw.get("pos", (110, 90))
            return blit(fr, s.img, px + w / 2, py + h / 2, sc, al)
        if s.kind == "stamp":
            u = min((t - s.t0) / 0.16, 1)
            sc = 1.8 - 0.8 * (u ** 2)
            cx, cy = s.kw.get("center", (W / 2, H / 2))
            return blit(fr, s.img, cx, cy, sc * s.kw.get("scale", 1.0), al)
        if s.kind == "counter":
            u = min(max((t - s.t0) / s.kw.get("dur", 2.4), 0), 1); u = 1 - (1 - u) ** 3
            val = int(s.kw["value"] * u)
            txt = s.kw.get("prefix", "") + f"{val:,}".replace(",", ".") + s.kw.get("suffix", "")
            img = Image.new("RGBA", (1500, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
            f = ImageFont.truetype(FONT_TITLE, 190); w = d.textlength(txt, font=f)
            d.text(((1500 - w) / 2 + 10, 30 + 10), txt, font=f, fill=(0, 0, 0, 200))
            d.text(((1500 - w) / 2, 30), txt, font=f, fill=AMBER, stroke_width=7, stroke_fill=INK)
            sub = s.kw.get("label", "")
            if sub:
                f2 = ImageFont.truetype(FONT_CAP, 52); w2 = d.textlength(sub, font=f2)
                d.rectangle([(1500 - w2) / 2 - 24, 255, (1500 + w2) / 2 + 24, 335], fill=PAPER + (255,), outline=INK + (255,), width=5)
                d.text(((1500 - w2) / 2, 263), sub, font=f2, fill=INK)
            cx, cy = s.kw.get("center", (W / 2, H / 2))
            return blit(fr, np.array(img), cx, cy, 1.0, al)
        if s.kind == "map":
            u = min(max((t - s.t0 - 0.3) / 1.6, 0), 1); u = 1 - (1 - u) ** 2
            img = Image.new("RGBA", (620, 760), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
            d.rectangle([12, 12, 619, 759], fill=(0, 0, 0, 255))
            d.rectangle([0, 0, 606, 746], fill=PAPER + (255,), outline=INK + (255,), width=6)
            f = ImageFont.truetype(FONT_TITLE, 64); f2 = ImageFont.truetype(FONT_CAP, 44)
            a, b = s.kw.get("a", (190, 150)), s.kw.get("b", (430, 600))
            n = 26
            for i in range(n):
                if i / n > u: break
                if i % 2 == 0:
                    p0 = (a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n - 60 * math.sin(math.pi * i / n))
                    p1 = (a[0] + (b[0] - a[0]) * (i + 1) / n, a[1] + (b[1] - a[1]) * (i + 1) / n - 60 * math.sin(math.pi * (i + 1) / n))
                    d.line([p0, p1], fill=INK, width=8)
            for (px, py), lab, dy in [(a, s.kw.get("a_label", "CHICAGO"), -95), (b, s.kw.get("b_label", "MIAMI"), 40)]:
                d.ellipse([px - 20, py - 20, px + 20, py + 20], fill=AMBER, outline=INK, width=5)
                w = d.textlength(lab, font=f); d.text((px - w / 2, py + dy), lab, font=f, fill=INK)
            if u > 0.95:
                txt = s.kw.get("dist", "ca. 2.000 km"); w = d.textlength(txt, font=f2)
                d.rectangle([303 - w / 2 - 20, 360, 303 + w / 2 + 20, 430], fill=AMBER, outline=INK, width=4)
                d.text((303 - w / 2, 368), txt, font=f2, fill=INK)
            cx, cy = s.kw.get("center", (1500, 540))
            sc = 0.85 + 0.15 * min((t - s.t0) / 0.25, 1)
            return blit(fr, np.array(img), cx, cy, sc, al)
        if s.kind == "bars":
            items = s.kw["items"]; vmax = max(v for _, v, _ in items)
            img = Image.new("RGBA", (1100, 140 + 150 * len(items)), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
            d.rectangle([12, 12, img.width - 1, img.height - 1], fill=(0, 0, 0, 255))
            d.rectangle([0, 0, img.width - 13, img.height - 13], fill=PAPER + (255,), outline=INK + (255,), width=6)
            f = ImageFont.truetype(FONT_CAP, 46); fb = ImageFont.truetype(FONT_TITLE, 64)
            d.text((40, 26), s.kw.get("title", ""), font=fb, fill=INK)
            for i, (lab, v, txt) in enumerate(items):
                u = min(max((t - s.t0 - 0.3 - i * 0.6) / 1.0, 0), 1); u = 1 - (1 - u) ** 3
                y = 120 + i * 150
                d.text((40, y), lab, font=f, fill=INK)
                bw = int(700 * v / vmax * u)
                d.rectangle([40, y + 58, 40 + max(bw, 4), y + 118], fill=AMBER if i == len(items) - 1 else (150, 140, 120), outline=INK, width=4)
                if u > 0.9: d.text((60 + bw, y + 60), txt, font=fb, fill=INK)
            cx, cy = s.kw.get("center", (W / 2, H / 2))
            return blit(fr, np.array(img), cx, cy, 0.9 + 0.1 * min((t - s.t0) / 0.25, 1), al)
        if s.kind == "chapter":
            img = Image.new("RGBA", (1500, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
            f1 = ImageFont.truetype(FONT_CAP, 60); f2 = ImageFont.truetype(FONT_TITLE, 170)
            d.rectangle([0, 0, 1499, 419], fill=(10, 9, 8, 225))
            t1 = s.kw["num"]; t2 = s.kw["title"]
            d.text(((1500 - d.textlength(t1, font=f1)) / 2, 40), t1, font=f1, fill=PAPER)
            d.text(((1500 - d.textlength(t2, font=f2)) / 2, 140), t2, font=f2, fill=AMBER, stroke_width=6, stroke_fill=INK)
            u = min((t - s.t0) / 0.35, 1); sc = 1.15 - 0.15 * (1 - (1 - u) ** 3)
            return blit(fr, np.array(img), W / 2, H / 2, sc, al)
        return fr

# ======================= Kamera / Zeitplan =======================
def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)
def lerp_view(a, b, u):
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * u))

def panel_view(rect, z=0.0, drift=(0, 0)):
    x, y, w, h = rect
    s = W / (w * 1.08) * (1 + z)
    return (x + w / 2 + drift[0] * w * z, y + h / 2 + drift[1] * h * z, s)

# ======================= Audio =======================
def load_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def mix_into(buf, clip, t, gain=1.0, fade_in=0.0, fade_out=0.0, max_len=None):
    c = clip if max_len is None else clip[:int(max_len * SR)]
    c = c.copy()
    if fade_in > 0: n = min(int(fade_in * SR), len(c)); c[:n] *= np.linspace(0, 1, n)[:, None]
    if fade_out > 0: n = min(int(fade_out * SR), len(c)); c[-n:] *= np.linspace(1, 0, n)[:, None]
    i = int(t * SR); j = min(i + len(c), len(buf))
    if j > i: buf[i:j] += c[:j - i] * gain


# ======================= Kurzschreibweisen für Episoden =======================
C = lambda text, a=0.15, **k: ("caption", a, None, dict(text=text, **k))
S = lambda text, a=0.1, **k: ("stamp", a, None, dict(text=text, **k))
L = lambda at, r=0.1, amt=0.25, seed=0: {"type": "lamp", "at": at, "r": r, "amount": amt, "seed": seed}
SM = lambda at, sc=0.8, st=0.28: {"type": "smoke", "at": at, "scale": sc, "strength": st}
BR = lambda amt=0.04, sp=1.5: {"type": "breathe", "amount": amt, "speed": sp}
PU = lambda at, r=0.12, amt=0.22, sp=1.5: {"type": "pulse", "at": at, "r": r, "amount": amt, "speed": sp}
RAIN = lambda a=0.5: {"type": "rain", "alpha": a}
SNOW = lambda a=0.65: {"type": "snow", "alpha": a}
FL = lambda ev: {"type": "flashes", "events": ev}

