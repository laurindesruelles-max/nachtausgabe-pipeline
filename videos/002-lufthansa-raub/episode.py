"""Episode 002 – Der Lufthansa-Raub. Panel-Effekte, Overlays, Geräusche, Kapitel.
Zeiten in Overlays/SFX sind Sekunden relativ zum Sprechbeginn des Panels.
Neue Effekte (EFFEKTE.md, 20.11.2026): HL Schlagzeile, WA Fahndungsplakat, CL Zeitsprung-Uhr, TL Taschenlampe, SH Panel zerbricht,
Extrablatt am Kapitelstart und Seite umblättern macht render.py automatisch."""
from engine import *

TITLE_AFTER = 10
TITLE_LINES = ["DER LUFTHANSA-RAUB", "NEW YORK 1978"]
TWIST = 7
N_PANELS = 71
FIRST_CHAPTER_LABEL = "Der Coup am Kennedy-Flughafen"
EXTRA_LINE = "EXTRABLATT  ·  NEW YORK  ·  1978"
CH_PAUSE = 3.0
FLIP_GAP = 1.25

M_ = lambda value, label, **k: ("counter", 0.3, None, dict(value=value, label=label, **k))

P = {
 1: dict(fx=[L((0.16, 0.05), 0.1, 0.3, 1), PU((0.5, 0.35), 0.15, 0.18, 1.2)], ov=[C("DER LUFTHANSA-RAUB · 11.12.1978 · 3:00 UHR", size=66, big=True)], sfx=[("car-door-opening-and-closing-01", 4.0, 0.45)], drift=(-0.3, 0)),
 2: dict(fx=[PU((0.3, 0.55), 0.1, 0.3, 2.5), L((0.82, 0.1), 0.08, 0.3, 2)], ov=[C("Kennedy-Flughafen · Frachtgelände")], sfx=[("iron-gate-01", 0.6, 0.3)], drift=(0.3, 0)),
 3: dict(fx=[L((0.58, 0.12), 0.12, 0.3, 3)], ov=[M_(5875000, "Bargeld und Schmuck", prefix="$ ", center=(W / 2, 600), dur=2.4)], sfx=[("empty-banknote-counter-01", 3.0, 0.5)], drift=(0.3, 0)),
 4: dict(fx=[BR(0.04, 1.5)], ov=[HL("REKORD-RAUB", 1.0, center=(W / 2, 880), scale=0.85)], sfx=[("paper-fabric-crumple-36", 0.0, 0.35)], drift=(-0.3, 0)),
 5: dict(fx=[SH(-0.3), L((0.7, 0.1), 0.08, 0.3, 5)], ov=[C("18. Dezember 1978")], sfx=[("footsteps-stone-01", 0.4, 0.35)], drift=(0, -0.3)),
 6: dict(fx=[L((0.35, 0.05), 0.12, 0.28, 6)], ov=[], sfx=[], drift=(0.3, 0)),
 7: dict(fx=[PU((0.65, 0.5), 0.2, 0.2, 1.0), L((0.2, 0.6), 0.08, 0.25, 7)], ov=[C("Wer? Und wo ist das Geld?", a=0.4)], sfx=[], drift=(-0.3, 0)),
 8: dict(fx=[SM((0.5, 0.35), 0.9, 0.3), L((0.55, 0.05), 0.1, 0.3, 8)], ov=[WA("JIMMY BURKE", "DER GENTLEMAN", "Queens, 1978", (0.42, 0.3, 0.66, 0.72), 0.6, center=(1500, 560))], sfx=[], drift=(0.3, 0)),
 9: dict(fx=[L((0.15, 0.25), 0.1, 0.3, 9)], ov=[WA("LOUIS WERNER", "DER TIPPGEBER", "Lufthansa-Fracht", (0.5, 0.08, 0.82, 0.62), 0.3, center=(430, 560))], sfx=[], drift=(0, -0.3)),
 10: dict(fx=[L((0.65, 0.12), 0.1, 0.28, 10), BR(0.04, 1.0)], ov=[], sfx=[], drift=(0.2, 0)),
 # Kapitel 1 – Der Tipp
 11: dict(fx=[L((0.45, 0.62), 0.1, 0.3, 11)], ov=[CL(0.0, None, dir=-1, text="EIN PAAR MONATE ZUVOR", center=(1350, 470))], sfx=[], drift=(-0.3, 0)),
 12: dict(fx=[BR(0.03)], ov=[C("Louis Werner · Frachtabteilung")], sfx=[("cardboard-box-close-01", 1.0, 0.3)], drift=(0.3, 0)),
 13: dict(fx=[PU((0.3, 0.2), 0.12, 0.2, 1.5)], ov=[("map", 0.3, None, dict(center=(1530, 560), a_label="DEUTSCHLAND", b_label="NEW YORK", a=(440, 230), b=(170, 560), dist="ca. 6.200 km"))], sfx=[], drift=(-0.3, 0)),
 14: dict(fx=[BR(0.03)], ov=[C("Westdeutschland · 1970er-Jahre")], sfx=[("coin-dropped-on-wooden-table-01", 2.0, 0.35)], drift=(0.3, 0)),
 15: dict(fx=[TL([(0.2, 0.2), (0.5, 0.6), (0.8, 0.5), (0.9, 0.25)], 0.0, 3.0)], ov=[], sfx=[], drift=(0, -0.3)),
 16: dict(fx=[SM((0.25, 0.3), 0.9, 0.3), L((0.5, 0.05), 0.1, 0.25, 12)], ov=[], sfx=[("paper-fabric-crumple-36", 2.4, 0.4)], drift=(0.3, 0)),
 17: dict(fx=[L((0.3, 0.12), 0.1, 0.3, 13)], ov=[M_(20000, "Spielschulden", prefix="$ ", center=(W / 2, 640), dur=1.8)], sfx=[("empty-banknote-counter-01", 0.3, 0.4)], drift=(-0.3, 0)),
 18: dict(fx=[L((0.5, 0.08), 0.12, 0.3, 14)], ov=[HL("DER TIPP", 2.6, center=(W / 2, 880), scale=0.85)], sfx=[("car-door-opening-and-closing-01", 0.0, 0.3)], drift=(0, -0.3)),
 19: dict(fx=[L((0.6, 0.08), 0.1, 0.3, 15)], ov=[WA("HENRY HILL", "DER VERMITTLER", "Queens, 1978", (0.12, 0.08, 0.46, 0.68), 1.6, center=(1500, 560))], sfx=[("glass-clink-01", 0.2, 0.25)], drift=(0.3, 0)),
 20: dict(fx=[FL([(0.3, (0.88, 0.25))]), L((0.86, 0.3), 0.08, 0.3, 16)], ov=[C("James „Jimmy“ Burke")], sfx=[("footsteps-concrete-03", 0.2, 0.35), ("door-close-01", 4.0, 0.3)], drift=(-0.3, 0)),
 21: dict(fx=[PU((0.48, 0.65), 0.08, 0.35, 2.0)], ov=[C("Queens, New York")], sfx=[], drift=(0.2, 0.2)),
 22: dict(fx=[L((0.5, 0.15), 0.14, 0.3, 17), SM((0.7, 0.4), 0.7, 0.2)], ov=[C("6 Männer · 1 Lieferwagen · 1 Begleitauto", a=1.4)], sfx=[("paper-fabric-card-flip-06", 0.3, 0.35)], drift=(0, -0.3)),
 23: dict(fx=[SM((0.62, 0.7), 0.7, 0.25)], ov=[M_(2000000, "Burkes Erwartung", prefix="$ ", center=(W / 2, 620), dur=2.0)], sfx=[], drift=(0.3, 0)),
 # Kapitel 2 – Die Nacht
 24: dict(fx=[PU((0.35, 0.6), 0.08, 0.35, 3.0)], ov=[C("Montag, 11. Dezember 1978 · kurz vor 3 Uhr")], sfx=[("car-door-opening-and-closing-01", 4.5, 0.4)], drift=(-0.3, 0)),
 25: dict(fx=[L((0.86, 0.06), 0.1, 0.3, 2)], ov=[], sfx=[("footsteps-concrete-03", 0.2, 0.4)], drift=(0, -0.3)),
 26: dict(fx=[L((0.55, 0.1), 0.1, 0.3, 18)], ov=[], sfx=[("footsteps-concrete-03", 0.0, 0.4)], drift=(0.3, 0)),
 27: dict(fx=[L((0.3, 0.05), 0.12, 0.3, 19)], ov=[C("Der Pausenraum")], sfx=[("door-close-01", 0.1, 0.5)], drift=(0, -0.3)),
 28: dict(fx=[BR(0.05, 2.5)], ov=[], sfx=[], drift=(0.3, 0)),
 29: dict(fx=[L((0.25, 0.1), 0.1, 0.3, 20)], ov=[], sfx=[("footsteps-concrete-03", 0.3, 0.35)], drift=(-0.3, 0)),
 30: dict(fx=[TL([(0.85, 0.2), (0.6, 0.7), (0.3, 0.4), (0.56, 0.5)], 0.0, 2.8)], ov=[C("Zwei Türen · eine Alarmanlage", a=2.8)], sfx=[], drift=(0.2, 0)),
 31: dict(fx=[L((0.48, 0.08), 0.12, 0.3, 21)], ov=[], sfx=[("keys-jingling-01", 0.3, 0.45), ("door-lock-01", 3.0, 0.5)], drift=(0.3, 0)),
 32: dict(fx=[TL([(0.15, 0.3), (0.45, 0.7), (0.7, 0.4), (0.55, 0.5)], 0.0, 2.6)], ov=[], sfx=[], drift=(0, -0.3)),
 33: dict(fx=[PU((0.45, 0.25), 0.15, 0.25, 1.5)], ov=[C("Dazu Schmuck · fast 1 Mio. $")], sfx=[("coin-dropped-on-wooden-table-01", 0.5, 0.35)], drift=(0, 0)),
 34: dict(fx=[L((0.07, 0.08), 0.1, 0.3, 22)], ov=[], sfx=[("cardboard-box-close-01", 0.4, 0.4), ("cardboard-box-close-01", 2.0, 0.35)], drift=(0.3, 0)),
 35: dict(fx=[PU((0.38, 0.75), 0.06, 0.3, 3.0)], ov=[C("4:21 Uhr")], sfx=[("car-door-opening-and-closing-01", 0.2, 0.4)], drift=(-0.3, 0)),
 36: dict(fx=[PU((0.5, 0.5), 0.2, 0.25, 2.0)], ov=[("bars", 0.3, None, dict(title="ERWARTET GEGEN ERBEUTET", items=[("Burkes Erwartung", 2.0, "2 Mio. $"), ("Erbeutet", 5.875, "5,875 Mio. $")], center=(1250, 520)))],
         sfx=[("empty-banknote-counter-01", 1.2, 0.5)], drift=(0, 0)),
 37: dict(fx=[PU((0.52, 0.2), 0.2, 0.15, 1.0)], ov=[M_(29000000, "heutiger Wert · Schätzung", prefix="$ ", center=(W / 2, 600), dur=2.2)], sfx=[], drift=(0.3, 0)),
 38: dict(fx=[FL([(0.4, (0.3, 0.55)), (1.1, (0.7, 0.5))])], ov=[C("Das FBI übernimmt")], sfx=[("office-camera-08", 0.4, 0.35), ("office-camera-08", 1.1, 0.35), ("car-door-opening-and-closing-01", 2.5, 0.35)], drift=(-0.3, 0)),
 39: dict(fx=[TL([(0.8, 0.2), (0.3, 0.5), (0.45, 0.8), (0.5, 0.82)], 0.0, 2.8)], ov=[], sfx=[], drift=(0.2, 0.2)),
 # Kapitel 3 – Der Lieferwagen
 40: dict(fx=[L((0.24, 0.12), 0.1, 0.3, 23)], ov=[WA("PARNELL EDWARDS", "DER FAHRER", "genannt „Stacks“", (0.36, 0.05, 0.6, 0.48), 0.5, center=(1500, 560))], sfx=[], drift=(-0.3, 0)),
 41: dict(fx=[PU((0.73, 0.45), 0.12, 0.25, 1.5)], ov=[C("Plan: die Schrottpresse")], sfx=[("factory-machinery-ambience-01", 0.0, 0.25)], drift=(0.3, 0)),
 42: dict(fx=[SH(-0.3), L((0.38, 0.12), 0.1, 0.3, 24)], ov=[("map", 0.6, None, dict(center=(1530, 560), a_label="FLUGHAFEN", b_label="BROOKLYN", a=(430, 520), b=(180, 220), dist="Hydrant statt Presse"))], sfx=[], drift=(-0.3, 0)),
 43: dict(fx=[FL([(0.3, (0.6, 0.4)), (0.9, (0.75, 0.5)), (2.6, (0.85, 0.45))])], ov=[HL("FINGERABDRÜCKE", 4.6, center=(W / 2, 880), scale=0.8)], sfx=[("office-camera-08", 0.3, 0.4), ("office-camera-08", 0.9, 0.4), ("office-camera-08", 2.6, 0.35)], drift=(0.3, 0)),
 44: dict(fx=[SM((0.12, 0.3), 0.8, 0.25), L((0.55, 0.45), 0.06, 0.3, 25)], ov=[], sfx=[("lighter-flick-01", 0.0, 0.3)], drift=(0, -0.3)),
 45: dict(fx=[L((0.52, 0.08), 0.1, 0.35, 26), PU((0.75, 0.55), 0.1, 0.3, 1.5)], ov=[C("18. Dezember 1978")], sfx=[("door-close-01", 4.2, 0.5)], drift=(-0.3, 0)),
 46: dict(fx=[L((0.48, 0.12), 0.1, 0.4, 27)], ov=[], sfx=[("footsteps-stone-01", 0.2, 0.3)], drift=(0.3, 0)),
 47: dict(fx=[L((0.53, 0.08), 0.12, 0.3, 28)], ov=[WA("MARTIN KRUGMAN", "VERMISST", "seit Januar 1979", (0.33, 0.15, 0.73, 0.75), 2.8, center=(430, 560))], sfx=[], drift=(0, -0.3)),
 48: dict(fx=[L((0.95, 0.5), 0.08, 0.3, 29)], ov=[WA("TOMMY DESIMONE", "VERMISST", "seit Januar 1979", (0.48, 0.05, 0.76, 0.55), 0.4, center=(430, 560))], sfx=[("car-door-opening-and-closing-01", 6.0, 0.35)], drift=(0.3, 0)),
 49: dict(fx=[L((0.55, 0.45), 0.08, 0.3, 30)], ov=[C("März 1979")], sfx=[], drift=(-0.3, 0)),
 50: dict(fx=[FL([(0.5, (0.45, 0.6)), (1.2, (0.7, 0.62))]), PU((0.15, 0.7), 0.1, 0.3, 4.0)], ov=[C("Mai und Juni 1979")], sfx=[("office-camera-08", 0.5, 0.35), ("office-camera-08", 1.2, 0.35)], drift=(0.3, 0)),
 51: dict(fx=[L((0.5, 0.08), 0.14, 0.35, 31)], ov=[M_(7, "tot oder verschwunden · in 6 Monaten", prefix="", center=(W / 2, 600), dur=2.0)], sfx=[("glass-clink-01", 0.2, 0.3)], drift=(0, 0)),
 52: dict(fx=[SM((0.62, 0.35), 0.8, 0.3)], ov=[HL("JEMAND RÄUMT AUF", 1.5, center=(W / 2, 880), scale=0.75)], sfx=[], drift=(-0.3, 0)),
 53: dict(fx=[L((0.3, 0.45), 0.1, 0.3, 32), BR(0.05, 2.0)], ov=[], sfx=[], drift=(0.3, 0)),
 # Kapitel 4 – Das Schweigen bricht
 54: dict(fx=[BR(0.03)], ov=[C("Louis Werner · 1979")], sfx=[("footsteps-concrete-03", 0.0, 0.4)], drift=(-0.3, 0)),
 55: dict(fx=[L((0.46, 0.1), 0.08, 0.3, 33)], ov=[C("Ein früherer Kollege sagt aus")], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.3)], drift=(0.3, 0)),
 56: dict(fx=[FL([(0.2, (0.15, 0.5)), (0.7, (0.4, 0.55)), (1.3, (0.85, 0.5))])], ov=[M_(15, "Jahre Haft für Werner", prefix="", suffix=" JAHRE", center=(W / 2, 600), dur=1.6), HL("VERURTEILT", 5.4, center=(W / 2, 900), scale=0.8)],
          sfx=[("office-camera-08", 0.2, 0.4), ("office-camera-08", 0.7, 0.4), ("office-camera-08", 1.3, 0.4), ("hammer-01", 5.3, 0.5)], drift=(0, -0.3)),
 57: dict(fx=[SM((0.25, 0.4), 0.9, 0.3)], ov=[], sfx=[], drift=(0.3, 0)),
 58: dict(fx=[PU((0.1, 0.8), 0.1, 0.3, 4.0)], ov=[C("April 1980 · Long Island")], sfx=[("car-door-opening-and-closing-01", 0.4, 0.4)], drift=(-0.3, 0)),
 59: dict(fx=[L((0.35, 0.05), 0.12, 0.35, 34)], ov=[], sfx=[("iron-gate-01", 0.0, 0.3)], drift=(0.3, 0)),
 60: dict(fx=[SH(-0.3), L((0.45, 0.05), 0.12, 0.3, 35)], ov=[HL("ER REDET", 3.6, center=(W / 2, 880), scale=0.9)], sfx=[], drift=(0, -0.3)),
 61: dict(fx=[PU((0.55, 0.65), 0.2, 0.2, 1.0)], ov=[C("Zeugenschutzprogramm")], sfx=[("car-door-opening-and-closing-01", 0.0, 0.35)], drift=(0.3, 0)),
 62: dict(fx=[L((0.88, 0.08), 0.08, 0.3, 36)], ov=[], sfx=[("iron-gate-01", 0.4, 0.4)], drift=(-0.3, 0)),
 63: dict(fx=[FL([(0.6, (0.2, 0.5)), (1.4, (0.8, 0.55)), (2.6, (0.5, 0.45))])], ov=[C("College-Basketball · Spiele manipuliert")], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.35)], drift=(0.3, 0)),
 64: dict(fx=[PU((0.6, 0.25), 0.15, 0.3, 0.8)], ov=[C("† 1996 · in Haft")], sfx=[("keys-jingling-01", 0.3, 0.35)], drift=(0, -0.3)),
 65: dict(fx=[BR(0.03)], ov=[CL(0.0, 3.0, dir=1, y0=1996, y1=2014, center=(480, 470))], sfx=[], drift=(-0.3, 0)),
 66: dict(fx=[PU((0.5, 0.5), 0.2, 0.15, 1.2)], ov=[C("Vincent Asaro · Anklage 2014"), HL("FREIGESPROCHEN", 2.0, center=(W / 2, 880), scale=0.8)], sfx=[("hammer-01", 1.9, 0.6)], drift=(0.3, 0)),
 67: dict(fx=[TL([(0.1, 0.3), (0.5, 0.75), (0.68, 0.5), (0.68, 0.55)], 0.0, 3.0)], ov=[], sfx=[], drift=(0, -0.3)),
 68: dict(fx=[L((0.52, 0.12), 0.15, 0.3, 37), PU((0.9, 0.45), 0.08, 0.3, 3.0)], ov=[C("1990 · im Kino")], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.3)], drift=(-0.3, 0)),
 69: dict(fx=[BR(0.04, 1.0)], ov=[], sfx=[], drift=(0.3, 0)),
 70: dict(fx=[L((0.2, 0.05), 0.08, 0.3, 38)], ov=[("bubble", 0.4, None, dict(lines=["Wo ist das Geld?", "Schreib es in die Kommentare!"], pos=(900, 60)))], sfx=[], drift=(0, 0)),
 71: dict(fx=[SM((0.62, 0.15), 1.0, 0.2), BR(0.03, 4.0)], ov=[C("Abonnieren · Glocke aktivieren", a=1.5, size=64)], sfx=[("factory-machinery-ambience-01", 0.0, 0.25)], drift=(0.3, 0)),
}
CHAPTERS = {11: ("KAPITEL 1", "DER TIPP", 2), 24: ("KAPITEL 2", "DIE NACHT", 3), 40: ("KAPITEL 3", "DER LIEFERWAGEN", 4), 54: ("KAPITEL 4", "DAS SCHWEIGEN BRICHT", 5)}
PRE = {7: 0.8, 6: 0.5, 36: 0.6, 45: 0.5, 46: 0.4, 51: 0.5, 60: 0.6, 66: 0.5, 67: 0.5, 3: 0.4}
