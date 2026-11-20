"""Stilprobe Nachtausgabe (20.11.2026): neue Effekte, ohne Ton.
Extrablatt, Fahndungsplakat, Taschenlampe, Panel zerbricht, Zeitsprung-Uhr, Schlagzeile knallt, Seite umblaettern.
Panels sind Ausschnitte aus den Al-Capone-Thumbnails (Platzhalter, 0 Credits)."""
import sys, math, subprocess
sys.path.insert(0, "/home/claude/repos/nachtausgabe-pipeline/engine")
from engine import *

SRC = "/home/claude/repos/nachtausgabe-pipeline/videos/001-al-capone/"
A = Image.open(SRC + "thumbnail_A.jpg").convert("RGB"); B = Image.open(SRC + "thumbnail_B.jpg").convert("RGB")
def crop(im, box): return np.array(im.crop(box).resize((PW, PH), Image.LANCZOS))
P = [crop(A, (800, 0, 1280, 270)),      # 0 Gesicht
     crop(A, (0, 450, 480, 720)),       # 1 Buch
     crop(B, (800, 110, 1280, 380)),    # 2 Gitter
     crop(B, (850, 0, 1250, 225)),      # 3 Lampe
     crop(A, (700, 450, 1180, 720)),    # 4 Anzug
     crop(B, (800, 450, 1280, 720))]    # 5 Haende
D = 23.0
fT = lambda s: ImageFont.truetype(FONT_TITLE, s)
fC = lambda s: ImageFont.truetype(FONT_CAP, s)
eo = lambda u: 1 - (1 - min(max(u, 0), 1)) ** 3

def show_panel(img, t, t0, dur, drift=(0.3, 0.0), fx=(), name="p"):
    """Panel bildfuellend mit langsamer Kamerafahrt."""
    u = (t - t0) / dur; z = 1.06 + 0.06 * u
    big = cv2.resize(img, (int(W * z), int(H * z)), interpolation=cv2.INTER_LINEAR)
    ox = int((big.shape[1] - W) / 2 + drift[0] * (u - 0.5) * (big.shape[1] - W))
    oy = int((big.shape[0] - H) / 2 + drift[1] * (u - 0.5) * (big.shape[0] - H))
    fr = np.ascontiguousarray(big[oy:oy + H, ox:ox + W])
    return apply_fx(name, fr, t, list(fx))

# ---------- neue Effekte ----------
def extrablatt_img(head, sub):
    im = Image.new("RGBA", (1500, 1000), PAPER + (255,)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 1499, 999], outline=INK, width=10)
    d.text((750, 70), "NACHTAUSGABE", font=fT(150), fill=INK, anchor="mt")
    d.line([(60, 245), (1440, 245)], fill=INK, width=8); d.line([(60, 262), (1440, 262)], fill=INK, width=3)
    d.text((750, 290), "EXTRABLATT  ·  CHICAGO  ·  1931", font=fC(46), fill=INK, anchor="mt")
    d.text((750, 380), head, font=fT(190), fill=INK, anchor="mt")
    d.rectangle([60, 620, 1440, 640], fill=AMBER)
    d.text((750, 680), sub, font=fC(58), fill=INK, anchor="mt")
    for i in range(4):  # Spalten-Andeutung
        for j in range(3):
            d.rectangle([80 + i * 345, 790 + j * 60, 380 + i * 345, 815 + j * 60], fill=(150, 140, 120))
    return np.array(im)
EXTRA = extrablatt_img("DER BUCHHALTER", "Kapitel 3")

def wanted_img(face, name, year):
    im = Image.new("RGBA", (620, 820), (226, 212, 176, 255)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 619, 819], outline=INK, width=8)
    d.text((310, 30), "GESUCHT", font=fT(140), fill=INK, anchor="mt")
    ph = Image.fromarray(face).resize((500, 280)).convert("L").convert("RGB")
    im.paste(ph, (60, 200)); d.rectangle([60, 200, 560, 480], outline=INK, width=6)
    d.text((310, 520), name, font=fT(96), fill=INK, anchor="mt")
    d.text((310, 650), year, font=fC(60), fill=INK, anchor="mt")
    return np.array(im.rotate(-4, expand=True, resample=Image.BICUBIC))
WANTED = wanted_img(P[0], "AL CAPONE", "Chicago, 1929")

def headline_img(text):
    f = fT(210); w = int(f.getlength(text))
    im = Image.new("RGBA", (w + 160, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([14, 14, im.width - 1, im.height - 1], fill=(0, 0, 0, 255))
    d.rectangle([0, 0, im.width - 15, im.height - 15], fill=PAPER + (255,), outline=INK + (255,), width=8)
    d.text((80, 30), text, font=f, fill=INK)
    d.rectangle([0, 0, 40, im.height - 15], fill=AMBER + (255,))
    return np.array(im)
HEAD = headline_img("STEUERBETRUG!")

def clock_img(ang):
    im = Image.new("RGBA", (420, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([10, 10, 410, 410], fill=PAPER + (255,), outline=INK + (255,), width=12)
    for k in range(12):
        a = k * math.pi / 6; d.line([(210 + 160 * math.sin(a), 210 - 160 * math.cos(a)), (210 + 185 * math.sin(a), 210 - 185 * math.cos(a))], fill=INK, width=8)
    d.line([(210, 210), (210 + 150 * math.sin(ang), 210 - 150 * math.cos(ang))], fill=INK, width=12)
    d.line([(210, 210), (210 + 100 * math.sin(ang / 12), 210 - 100 * math.cos(ang / 12))], fill=AMBER, width=16)
    d.ellipse([195, 195, 225, 225], fill=INK)
    return np.array(im)

def flashlight(fr, t, t0, path):
    u = eo((t - t0) / 3.0)
    k = min(int(u * (len(path) - 1)), len(path) - 2); r = u * (len(path) - 1) - k
    cx = path[k][0] + (path[k + 1][0] - path[k][0]) * r; cy = path[k][1] + (path[k + 1][1] - path[k][1]) * r
    rad = 340 + 160 * u
    yy, xx = np.ogrid[:H, :W]
    m = np.clip(1.25 - np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / rad, 0, 1)[..., None] ** 1.4
    return np.clip(fr * (0.12 + 1.15 * m), 0, 255).astype(np.uint8)

SHARDS = None
def shatter(fr_a, fr_b, u):
    """Panel bricht: Scherben von fr_a fliegen auseinander, dahinter fr_b."""
    global SHARDS
    if SHARDS is None:
        r = np.random.default_rng(3); cx, cy = W * 0.55, H * 0.45
        angs = np.sort(r.uniform(0, 2 * math.pi, 9)); SHARDS = []
        far = 2400
        for a0, a1 in zip(angs, np.roll(angs, -1)):
            if a1 < a0: a1 += 2 * math.pi
            poly = np.array([(cx, cy), (cx + far * math.cos(a0), cy + far * math.sin(a0)), (cx + far * math.cos((a0 + a1) / 2), cy + far * math.sin((a0 + a1) / 2)),
                             (cx + far * math.cos(a1), cy + far * math.sin(a1))], np.int32)
            m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [poly], 255)
            SHARDS.append((m, (a0 + a1) / 2, r.uniform(-0.6, 0.6)))
    out = fr_b.copy()
    if u <= 0.0:
        out = fr_a.copy()
    for m, a, rot in SHARDS:
        if u <= 0: break
        dist = 900 * u ** 1.6
        M = cv2.getRotationMatrix2D((W * 0.55, H * 0.45), rot * 40 * u, 1 - 0.25 * u)
        M[0, 2] += dist * math.cos(a); M[1, 2] += dist * math.sin(a) + 300 * u * u
        piece = cv2.warpAffine(fr_a, M, (W, H)); mm = cv2.warpAffine(m, M, (W, H))
        a_ = (mm[..., None] / 255.0) * (1 - u * 0.3)
        out = (out * (1 - a_) + piece * a_).astype(np.uint8)
        e = cv2.Canny(mm, 50, 150); out[e > 0] = INK
    return out

def cracks(fr, u):
    if u <= 0: return fr
    r = np.random.default_rng(5); cx, cy = int(W * 0.55), int(H * 0.45)
    for k in range(9):
        a = k * 0.7 + 0.3; L = 1400 * u; x, y = cx, cy; pts = [(x, y)]
        for s in range(8):
            a += r.uniform(-0.35, 0.35); x += L / 8 * math.cos(a); y += L / 8 * math.sin(a); pts.append((int(x), int(y)))
        cv2.polylines(fr, [np.array(pts, np.int32)], False, (250, 240, 215), 3, cv2.LINE_AA)
    return fr

strip, rects = build_strip(P + [np.ascontiguousarray(p[:, ::-1]) for p in P])
def page_frame(p):
    cx, cy, s = page_view(p)
    M = np.array([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]], np.float32)
    return cv2.warpAffine(strip, M, (W, H), borderValue=(24, 22, 20))

# ---------- Zeitplan ----------
def frame(t):
    if t < 3.2:   # Extrablatt aus der Druckerpresse
        fr = np.full((H, W, 3), (18, 16, 14), np.uint8)
        u = eo(t / 1.3)
        rot = (1 - u) * 720; sc = 0.15 + 0.85 * u
        im = Image.fromarray(EXTRA).rotate(rot, expand=True, resample=Image.BICUBIC)
        fr = blit(fr, np.array(im), W / 2, H / 2, sc * 0.95, 1.0)
        if t > 2.6: fr = (fr * (1 - (t - 2.6) / 0.6)).astype(np.uint8)
        return fr
    if t < 6.6:   # Panel + Fahndungsplakat
        fr = show_panel(P[0], t, 3.2, 3.4, (0.4, 0), [SM((0.25, 0.55), 0.9, 0.3)], "p0")
        if t > 4.0:
            u = eo((t - 4.0) / 0.35)
            fr = blit(fr, WANTED, 470, 560, 1.6 - 0.8 * u, min(1, (t - 4.0) / 0.12))
        return fr
    if t < 10.0:  # Taschenlampe tastet das dunkle Panel ab
        fr = show_panel(P[1], t, 6.6, 3.4, (0.2, 0.2), [], "p1")
        return flashlight(fr, t, 6.6, [(1700, 200), (1300, 700), (600, 350), (520, 820)])
    if t < 13.4:  # Panel zerbricht
        a = show_panel(P[3], t, 10.0, 3.4, (0, 0.3), [L((0.5, 0.25), 0.12, 0.35, 2)], "p3")
        b = show_panel(P[2], t, 10.0, 3.4, (0.3, 0), [RAIN(0.45)], "p2")
        if t < 11.4: return cracks(a, eo((t - 10.6) / 0.5)) if t > 10.6 else a
        return shatter(cracks(a, 1.0), b, (t - 11.4) / 1.4)
    if t < 16.8:  # Zeitsprung-Uhr
        fr = show_panel(P[4], t, 13.4, 3.4, (-0.3, 0), [BR(0.05, 2.0)], "p4")
        fr = (fr * 0.55).astype(np.uint8)
        ang = -eo((t - 13.6) / 2.4) * 2 * math.pi * 30
        fr = blit(fr, clock_img(ang), W / 2, H / 2 - 40, 1.0, min(1, (t - 13.4) / 0.25))
        yr = 1931 - int(32 * eo((t - 13.6) / 2.4))
        fr = blit(fr, caption_img(str(yr), 110, big=True), W / 2, H / 2 + 300, 1.0, 1.0)
        return fr
    if t < 20.0:  # Schlagzeile knallt
        fr = show_panel(P[2], t, 16.8, 3.2, (0.2, 0), [RAIN(0.5), L((0.32, 0.05), 0.1, 0.3, 4)], "p2b")
        if t > 17.5:
            u = min((t - 17.5) / 0.14, 1)
            sh = (1 - min((t - 17.5) / 0.3, 1)) * 18
            fr = np.roll(fr, int(sh * math.sin(t * 90)), axis=0)
            fr = blit(fr, HEAD, W / 2, 860, 1.9 - 0.9 * u ** 2, 1.0)
        return fr
    # Seite umblaettern: Seite 1 klappt nach links weg, Seite 2 darunter
    pa, pb = page_frame(0), page_frame(1)
    u = eo((t - 20.6) / 1.4) if t > 20.6 else 0
    if u <= 0: return pa
    out = pb.copy()
    w = int(W * (1 - u))
    if w > 2:
        sq = cv2.resize(pa, (w, H))
        shade = np.linspace(1.0, 0.55 + 0.45 * (1 - u), w)[None, :, None]
        out[:, :w] = (sq * shade).astype(np.uint8)
        out[:, w:min(W, w + 40)] = (out[:, w:min(W, w + 40)] * np.linspace(0.4, 1, min(40, W - w))[None, :, None]).astype(np.uint8)
    return out

if __name__ == "__main__":
    out = "/home/claude/stilproben/stilprobe_nachtausgabe.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", out], stdin=subprocess.PIPE)
    for i in range(int(D * FPS)):
        p.stdin.write(np.ascontiguousarray(frame(i / FPS)).tobytes())
    p.stdin.close(); p.wait(); print("ok")
