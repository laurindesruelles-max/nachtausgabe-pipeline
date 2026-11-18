"""Endkontrolle: python3 engine/qa.py VIDEO.mp4 THUMBNAIL.jpg videos/NNN-slug  -> schreibt qa.md in den Episodenordner."""
import sys, subprocess, json, os, re
vid, thumb, ep = sys.argv[1:4]
def probe(f):
    return json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=width,height,codec_type", "-of", "json", f], capture_output=True, text=True).stdout)
p = probe(vid); dur = float(p["format"]["duration"]); size = int(p["format"]["size"]) / 1e6
v = [s for s in p["streams"] if s["codec_type"] == "video"][0]
lo = subprocess.run(["ffmpeg", "-i", vid, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", lo)[-1])
from PIL import Image
t = Image.open(thumb); tsize = os.path.getsize(thumb) / 1e6
rows = [
 ("Länge über 8:00", f"{int(dur//60)}:{int(dur%60):02d}", dur >= 480),
 ("Auflösung 1920x1080", f"{v['width']}x{v['height']}", (v["width"], v["height"]) == (1920, 1080)),
 ("Lautheit -15 bis -13 LUFS", f"{I:.1f}", -15.5 <= I <= -12.5),
 ("Datei unter 299 MB (Upload)", f"{size:.0f} MB", size < 299),
 ("Thumbnail 1280x720, unter 2 MB", f"{t.size[0]}x{t.size[1]}, {tsize:.2f} MB", t.size == (1280, 720) and tsize < 2),
]
ok = all(r[2] for r in rows)
md = "# Endkontrolle\n\n| Prüfung | Wert | OK |\n|---|---|---|\n" + "\n".join(f"| {a} | {b} | {'✅' if c else '❌'} |" for a, b, c in rows)
md += "\n\nWeitere Pflichtpunkte (von Hand eintragen): Spracherkennung aller Zeilen, unabhängiger Faktencheck, Rechts-Check.\n"
open(os.path.join(ep, "qa.md"), "w").write(md); print(md); sys.exit(0 if ok else 1)
