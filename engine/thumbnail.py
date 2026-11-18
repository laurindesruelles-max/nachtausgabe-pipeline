"""Hero-Thumbnail im Nachtausgabe-Stil (ein großes Motiv + 2 Zeilen Text, links dunkel).
Aufruf: python3 engine/thumbnail.py HERO.png "ZEILE 1" "ZEILE 2" AUSGABE.jpg [left|right]
Zeile 1 hell (Papierweiß), Zeile 2 groß in Bernstein. Kurz halten: max. 3 Wörter pro Zeile."""
import sys, os
from PIL import Image, ImageDraw, ImageFont
F = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fonts") + "/"
AMBER = (245, 180, 30); INK = (10, 9, 8); PAPER = (240, 230, 208)

def fit(d, txt, maxw, start):
    s = start
    while s > 40:
        f = ImageFont.truetype(F + "Bangers-Regular.ttf", s)
        if d.textlength(txt, font=f) <= maxw: return f, s
        s -= 4
    return ImageFont.truetype(F + "Bangers-Regular.ttf", s), s

def thumb(src, l1, l2, out, side="left"):
    im = Image.open(src).convert("RGB").resize((1280, 720), Image.LANCZOS)
    g = Image.new("L", (1280, 720), 0); d = ImageDraw.Draw(g)
    for x in range(700): d.line([(x, 0), (x, 720)], fill=int(200 * (1 - x / 700) ** 1.2))
    if side == "right": g = g.transpose(Image.FLIP_LEFT_RIGHT)
    im = Image.composite(Image.new("RGB", (1280, 720), INK), im, g)
    d = ImageDraw.Draw(im)
    y = 200
    for txt, start, col in [(l1, 130, PAPER), (l2, 190, AMBER)]:
        f, s = fit(d, txt, 720, start)
        x = 50 if side == "left" else 1230 - d.textlength(txt, font=f)
        d.text((x + 8, y + 8), txt, font=f, fill=(0, 0, 0))
        d.text((x, y), txt, font=f, fill=col, stroke_width=8, stroke_fill=INK)
        y += s + 10
    im.save(out, quality=92)

if __name__ == "__main__":
    thumb(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "left")
