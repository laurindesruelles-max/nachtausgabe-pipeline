"""Stilprobe Nachtausgabe, Variante „Mitte“: Kamera bleibt auf der Comicseite wie im Pilot (Seite, Rahmen, Nachbar-Panels sichtbar),
die neuen Effekte passieren IM Panel. Nur Extrablatt und Seitenwechsel sind bildfuellend."""
from nachtausgabe import *

ZM = -0.16                     # etwas weiter weg als im Pilot -> Seite und Nachbarn sichtbar
SLOT = list(P)                 # aktueller Inhalt je Panel-Platz
PAGE = strip[:, :PAGE_W].copy()
R = rects[:6]
_x, _y, _w, _h = R[3]; strip[_y:_y + _h, _x:_x + _w] = P[2]   # nach dem Zerbrechen zeigt Panel 3 das Gitter

def panel_fx(k, t):
    """Inhalt von Panel k zur Zeit t, inkl. Effekte im Panel."""
    img = SLOT[k]
    if k == 0: return apply_fx("m0", img.copy(), t, [SM((0.25, 0.55), 0.9, 0.3)])
    if k == 1 and 6.6 <= t < 10.6:
        big = cv2.resize(img, (W, H)); big = flashlight(big, t, 7.0, [(1700, 200), (1300, 700), (600, 350), (520, 820)])
        return cv2.resize(big, (PW, PH))
    if k == 3 and 11.0 <= t:
        a = cv2.resize(apply_fx("m3", P[3].copy(), t, [L((0.5, 0.25), 0.12, 0.35, 2)]), (W, H))
        b = cv2.resize(apply_fx("m2", P[2].copy(), t, [RAIN(0.45)]), (W, H))
        if t < 11.9: fr = cracks(a, eo((t - 11.2) / 0.5)) if t > 11.2 else a
        else: fr = shatter(cracks(a, 1.0), b, (t - 11.9) / 1.3)
        return cv2.resize(fr, (PW, PH))
    if k == 3: return apply_fx("m3", img.copy(), t, [L((0.5, 0.25), 0.12, 0.35, 2)])
    if k == 4: return apply_fx("m4", img.copy(), t, [BR(0.05, 2.0)])
    if k == 5: return apply_fx("m5", img.copy(), t, [RAIN(0.4)])
    return img

def page_at(t):
    pg = PAGE.copy()
    for k, (x, y, w, h) in enumerate(R):
        pg[y:y + h, x:x + w] = panel_fx(k, t)
    return pg

def view_of(k): return panel_view(R[k], ZM)
WHOLE = page_view(0)
CAMK = [(3.2, view_of(0)), (6.6, view_of(0)), (7.2, view_of(1)), (10.4, view_of(1)), (11.0, view_of(3)), (13.6, view_of(3)),
        (14.2, view_of(4)), (17.0, view_of(4)), (17.6, view_of(5)), (20.0, view_of(5)), (20.7, WHOLE), (D, WHOLE)]
def camv(t):
    for (ta, a), (tb, b) in zip(CAMK, CAMK[1:]):
        if ta <= t <= tb:
            u = ease((t - ta) / (tb - ta)) if a != b else 0
            return lerp_view(a, b, u)
    return CAMK[-1][1]

def render_page(t, sx=0, sy=0):
    cx, cy, s = camv(t)
    M = np.array([[s, 0, W / 2 - cx * s + sx], [0, s, H / 2 - cy * s + sy]], np.float32)
    return cv2.warpAffine(page_at(t), M, (W, H), borderValue=(24, 22, 20))

def frame2(t):
    if t < 3.2: return frame(t)                    # Extrablatt (bildfuellend)
    if t < 3.6:                                     # Ueberblendung in die Seite
        a = (t - 3.2) / 0.4; return (frame(3.19) * (1 - a) + render_page(t) * a).astype(np.uint8)
    if t < 20.9:
        sx = sy = 0
        if 18.2 <= t < 18.5: k = (1 - (t - 18.2) / 0.3) ** 2; sy = 18 * k * math.sin(t * 90)
        fr = render_page(t, sx, sy)
        if 4.2 < t < 6.9:                           # Fahndungsplakat
            u = eo((t - 4.2) / 0.35); fr = blit(fr, WANTED, 430, 560, 1.4 - 0.75 * u, min(1, (t - 4.2) / 0.12, (6.9 - t) / 0.25))
        if 14.2 < t < 17.3:                         # Zeitsprung-Uhr
            ang = -eo((t - 14.4) / 2.4) * 2 * math.pi * 30; al = min(1, (t - 14.2) / 0.25, (17.3 - t) / 0.25)
            fr = blit(fr, clock_img(ang), W / 2 + 420, H / 2 - 60, 0.9, al)
            yr = 1931 - int(32 * eo((t - 14.4) / 2.4))
            fr = blit(fr, caption_img(str(yr), 100, big=True), W / 2 + 420, H / 2 + 230, 1.0, al)
        if 18.2 <= t < 20.4:                        # Schlagzeile knallt
            u = min((t - 18.2) / 0.14, 1); fr = blit(fr, HEAD, W / 2, 860, 1.9 - 0.9 * u ** 2, min(1, (20.4 - t) / 0.25))
        return fr
    return frame(t)                                 # Seite umblaettern

if __name__ == "__main__":
    out = "/home/claude/stilproben/stilprobe_nachtausgabe_mitte.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", out], stdin=subprocess.PIPE)
    for i in range(int(D * FPS)):
        p.stdin.write(np.ascontiguousarray(frame2(i / FPS)).tobytes())
    p.stdin.close(); p.wait(); print("ok")
