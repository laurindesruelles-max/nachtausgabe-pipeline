"""Episode 001 – Al Capone. Panel-Effekte, Overlays, Geräusche, Kapitel.
Zeiten in Overlays/SFX sind Sekunden relativ zum Sprechbeginn des Panels."""
from engine import *

TITLE_AFTER = 17                       # nach welchem Panel die Titeltafel kommt (Ende des Einstiegs)
TITLE_LINES = ["WIE EIN KASSENBUCH", "AL CAPONE STÜRZTE"]
TWIST = 13                             # Wendepunkt im Einstieg (Musik kurz leiser, dann stärker)
N_PANELS = 65
FIRST_CHAPTER_LABEL = "Valentinstag 1929"   # Kapitelmarke 0:00

P = {
 1: dict(fx=[SNOW()], ov=[C("CHICAGO · 14. FEBRUAR 1929", size=78, big=True)], sfx=[("footsteps-concrete-03", 0.4, 0.35)], drift=(-0.3, 0)),
 2: dict(fx=[SNOW(0.55)], ov=[C("10:30 Uhr · North Clark Street")], sfx=[("car-door-opening-and-closing-01", 4.4, 0.6)], drift=(0.3, 0)),
 3: dict(fx=[L((0.5, 0.06), 0.12, 0.3, 1)], ov=[C("Sieben Männer an der Wand")], sfx=[], drift=(0, -0.3)),
 4: dict(fx=[SNOW(0.6)], ov=[], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.35), ("door-close-01", -0.25, 0.7)], drift=(0.3, 0)),
 5: dict(fx=[SNOW(0.5)], ov=[], sfx=[("paper-fabric-crumple-36", 0.2, 0.4)], drift=(-0.3, 0)),
 6: dict(fx=[SM((0.24, 0.5), 0.9, 0.32)], ov=[S("AL CAPONE", 0.05, center=(1340, 840), scale=0.8)], sfx=[("impact-slam-35", 0.05, 0.8)], drift=(0, 0)),
 7: dict(fx=[PU((0.88, 0.17), 0.1, 0.25, 1.2)], ov=[("map", 0.3, None, dict(center=(1530, 560)))], sfx=[], drift=(-0.3, 0)),
 8: dict(fx=[SM((0.58, 0.8), 0.6, 0.25)], ov=[S("ALIBI", 0.35, center=(1000, 860), scale=0.9, rot=8)], sfx=[("glass-clink-01", 0.0, 0.5), ("impact-slam-35", 0.35, 0.7)], drift=(0.3, 0)),
 9: dict(fx=[L((0.43, 0.08), 0.1, 0.28, 3)], ov=[("counter", 0.3, None, dict(value=100000000, prefix="$ ", label="pro Jahr · Schätzung", center=(W / 2, 620), dur=2.6))],
         sfx=[("empty-banknote-counter-01", 0.3, 0.7), ("coin-dropped-on-wooden-table-01", 5.6, 0.5)], drift=(0, 0)),
 10: dict(fx=[RAIN()], ov=[C("Auf der Gehaltsliste: Polizei · Justiz · Politik")], sfx=[("paper-fabric-crumple-36", 1.0, 0.3)], drift=(0.3, 0), rain=True),
 11: dict(fx=[BR(0.04, 2.2)], ov=[("bubble", 1.6, None, dict(lines=["Ich … erinnere mich", "an nichts."], pos=(820, 60)))], sfx=[], drift=(0, -0.3)),
 12: dict(fx=[FL([(0.2, (0.13, 0.42)), (0.7, (0.33, 0.40)), (1.3, (0.28, 0.62)), (1.9, (0.08, 0.30)), (2.4, (0.36, 0.55))])],
          ov=[S("UNANTASTBAR", 1.4, center=(W / 2, 880), scale=0.75, rot=-5)],
          sfx=[("office-camera-08", 0.2, 0.5), ("office-camera-08", 0.7, 0.45), ("office-camera-08", 1.3, 0.5), ("office-camera-08", 1.9, 0.45), ("impact-slam-35", 1.4, 0.8)], drift=(-0.3, 0)),
 13: dict(fx=[RAIN(0.45), L((0.25, 0.17), 0.08, 0.3, 5)], ov=[], sfx=[], drift=(0.3, 0), rain=True),
 14: dict(fx=[L((0.82, 0.3), 0.12, 0.22, 2)], ov=[], sfx=[("paper-fabric-card-flip-06", 0.6, 0.5)], drift=(0, -0.3)),
 15: dict(fx=[L((0.18, 0.08), 0.1, 0.25, 4)], ov=[C("Frank J. Wilson · Steuerfahndung")], sfx=[("footsteps-stone-01", 0.0, 0.45)], drift=(0.3, 0)),
 16: dict(fx=[L((0.38, 0.06), 0.12, 0.3, 6)], ov=[], sfx=[("scroll-unroll-01", 0.0, 0.5)], drift=(0.2, 0.2)),
 17: dict(fx=[BR(0.06, 1.2)], ov=[], sfx=[], drift=(0, 0)),
 # Kapitel 1
 18: dict(fx=[BR(0.03)], ov=[], sfx=[("footsteps-concrete-03", 0.3, 0.25)], drift=(-0.3, 0)),
 19: dict(fx=[L((0.66, 0.7), 0.1, 0.3, 7)], ov=[C("Brooklyn, New York · 1899")], sfx=[], drift=(0.3, 0)),
 20: dict(fx=[BR(0.05, 2.5)], ov=[], sfx=[("impact-crate-break-08", 3.3, 0.35)], drift=(0, -0.3)),
 21: dict(fx=[L((0.14, 0.1), 0.1, 0.3, 8)], ov=[S("SCARFACE", 3.2, center=(1350, 860), scale=0.8, rot=-6)], sfx=[("impact-slam-35", 3.2, 0.7)], drift=(0.3, 0)),
 22: dict(fx=[SM((0.25, 0.75), 1.2, 0.3)], ov=[("map", 0.3, None, dict(center=(1530, 560), a_label="NEW YORK", b_label="CHICAGO", a=(450, 260), b=(170, 520), dist="ca. 1.150 km"))],
          sfx=[("air-hiss-01", 0.0, 0.4)], drift=(-0.3, 0)),
 23: dict(fx=[BR(0.04)], ov=[C("Prohibition · 1920 bis 1933")], sfx=[("impact-crate-break-08", 0.3, 0.45), ("water-pour-10", 1.0, 0.45)], drift=(0.3, 0)),
 24: dict(fx=[SM((0.55, 0.3), 1.0, 0.22)], ov=[], sfx=[("door-knock-01", 0.0, 0.5), ("glass-clink-01", 2.5, 0.4)], drift=(0, -0.3)),
 25: dict(fx=[RAIN(0.3), L((0.08, 0.2), 0.08, 0.25, 9)], ov=[C("1925")], sfx=[], drift=(0.3, 0), rain=True),
 26: dict(fx=[SM((0.2, 0.45), 0.9, 0.25)], ov=[("counter", 0.2, None, dict(value=26, suffix=" JAHRE", label="Capones Alter bei der Übernahme", center=(W / 2, 560), dur=1.6))],
          sfx=[("coin-dropped-on-wooden-table-01", 3.0, 0.4)], drift=(-0.3, 0)),
 27: dict(fx=[BR(0.03)], ov=[], sfx=[("car-door-opening-and-closing-01", 3.0, 0.45)], drift=(0.3, 0)),
 28: dict(fx=[PU((0.55, 0.5), 0.15, 0.25, 2.0)], ov=[S("ALLES IN BAR", 4.2, center=(560, 860), scale=0.75, rot=6)], sfx=[("empty-banknote-counter-01", 0.5, 0.5), ("impact-slam-35", 4.2, 0.6)], drift=(0, 0)),
 29: dict(fx=[L((0.72, 0.25), 0.1, 0.25, 10)], ov=[S("KEINE", 1.2, center=(1250, 820), scale=0.8, rot=-8)], sfx=[("impact-slam-35", 1.2, 0.7)], drift=(0.2, 0)),
 # Kapitel 2
 30: dict(fx=[RAIN(0.55)], ov=[], sfx=[], drift=(0, -0.3), rain=True),
 31: dict(fx=[L((0.8, 0.85), 0.1, 0.22, 11)], ov=[C("Herbert Hoover · US-Präsident ab 1929")], sfx=[("impact-slam-35", 0.2, 0.45)], drift=(0.3, 0)),
 32: dict(fx=[L((0.6, 0.08), 0.12, 0.3, 12)], ov=[S("KEINE BEWEISE", 0.6, center=(W / 2, 860), scale=0.7, rot=-5)], sfx=[("impact-slam-35", 0.6, 0.6)], drift=(0, -0.3)),
 33: dict(fx=[PU((0.5, 0.25), 0.2, 0.2, 1.0)], ov=[C("Oberstes Gericht der USA · 1927")], sfx=[("hammer-01", 0.1, 0.6)], drift=(-0.3, 0)),
 34: dict(fx=[SM((0.3, 0.35), 0.9, 0.22)], ov=[], sfx=[], drift=(0.3, 0)),
 35: dict(fx=[BR(0.04, 3.0)], ov=[("map", 0.4, None, dict(center=(1530, 560), a_label="WASHINGTON", b_label="CHICAGO", a=(430, 520), b=(170, 220), dist="Mai 1930"))], sfx=[], drift=(-0.3, 0)),
 36: dict(fx=[L((0.08, 0.12), 0.1, 0.25, 13)], ov=[C("Frank J. Wilson · Steuerfahnder")], sfx=[], drift=(0, 0)),
 37: dict(fx=[L((0.82, 0.35), 0.1, 0.25, 14)], ov=[C("Monatelange Kleinarbeit")], sfx=[("paper-fabric-card-flip-06", 1.0, 0.4), ("paper-fabric-card-flip-06", 4.0, 0.35)], drift=(0.3, 0)),
 38: dict(fx=[PU((0.6, 0.3), 0.1, 0.25, 2.5)], ov=[], sfx=[("door-knock-01", 2.6, 0.4)], drift=(-0.3, 0)),
 39: dict(fx=[L((0.6, 0.1), 0.12, 0.3, 15)], ov=[], sfx=[("cardboard-box-close-01", 0.4, 0.45)], drift=(0, -0.3)),
 40: dict(fx=[L((0.08, 0.15), 0.12, 0.28, 16)], ov=[], sfx=[("paper-fabric-card-flip-06", 0.4, 0.45)], drift=(0.2, 0.2)),
 41: dict(fx=[RAIN(0.4)], ov=[S("WER?", 0.3, center=(560, 820), scale=0.9, rot=7)], sfx=[("impact-slam-35", 0.3, 0.5)], drift=(0.3, 0), rain=True),
 42: dict(fx=[L((0.45, 0.08), 0.12, 0.3, 17)], ov=[C("Leslie Shumway · Buchhalter", a=4.0)], sfx=[("reveal-impact-01", 4.0, 0.5)], drift=(0, 0)),
 43: dict(fx=[PU((0.8, 0.1), 0.12, 0.25, 3.0)], ov=[C("Miami, Florida")], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.35)], drift=(-0.3, 0)),
 44: dict(fx=[RAIN(0.45)], ov=[], sfx=[], drift=(0.3, 0), rain=True),
 45: dict(fx=[L((0.2, 0.25), 0.1, 0.25, 18)], ov=[C("Fred Ries · Kassierer")], sfx=[("door-lock-01", 4.5, 0.5)], drift=(0, -0.3)),
 46: dict(fx=[FL([(0.3, (0.1, 0.4)), (0.9, (0.3, 0.35)), (1.6, (0.7, 0.4))])], ov=[S("ANGEKLAGT", 3.0, center=(W / 2, 860), scale=0.8, rot=-6)],
          sfx=[("office-camera-08", 0.3, 0.45), ("office-camera-08", 0.9, 0.45), ("office-camera-08", 1.6, 0.45), ("impact-slam-35", 3.0, 0.7)], drift=(0.3, 0)),
 # Kapitel 3
 47: dict(fx=[SM((0.72, 0.3), 0.8, 0.25)], ov=[C("Angebotener Deal: 2,5 Jahre Haft", a=3.0)], sfx=[("match-strike-01", 0.2, 0.4)], drift=(-0.3, 0)),
 48: dict(fx=[BR(0.04)], ov=[C("Richter James H. Wilkerson"), S("ABGELEHNT", 2.9, center=(1350, 860), scale=0.75, rot=-6)], sfx=[("impact-slam-35", 2.9, 0.7)], drift=(0, -0.3)),
 49: dict(fx=[L((0.55, 0.08), 0.1, 0.28, 19)], ov=[C("Geschworene: bestochen und bedroht", a=3.0)], sfx=[("door-knock-01", 0.0, 0.5)], drift=(0.3, 0)),
 50: dict(fx=[L((0.1, 0.25), 0.1, 0.25, 20)], ov=[], sfx=[("paper-fabric-card-flip-06", 0.5, 0.4)], drift=(-0.3, 0)),
 51: dict(fx=[BR(0.04)], ov=[C("Oktober 1931 · erster Prozesstag")], sfx=[("daily-20260923-hushed-crowd-walla-short", 2.0, 0.35)], drift=(0.3, 0)),
 52: dict(fx=[BR(0.07, 3.0)], ov=[], sfx=[], drift=(0, 0)),
 53: dict(fx=[BR(0.04)], ov=[], sfx=[("paper-fabric-card-flip-06", 0.2, 0.45)], drift=(-0.3, 0)),
 54: dict(fx=[PU((0.5, 0.2), 0.2, 0.2, 1.2)], ov=[S("SCHULDIG", 2.0, center=(W / 2, 860), scale=0.9, rot=-5)], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.3), ("impact-slam-35", 2.0, 0.8)], drift=(0, -0.3)),
 55: dict(fx=[PU((0.5, 0.6), 0.25, 0.3, 4.0)], ov=[("bars", 0.2, None, dict(title="DEAL GEGEN URTEIL", items=[("Angebotener Deal", 2.5, "2,5 Jahre"), ("Urteil", 11, "11 Jahre")], center=(1300, 520)))],
          sfx=[("hammer-01", 0.0, 0.8)], drift=(-0.3, 0)),
 56: dict(fx=[FL([(0.2, (0.1, 0.45)), (0.8, (0.85, 0.4)), (1.5, (0.15, 0.6)), (2.3, (0.9, 0.55))])], ov=[],
          sfx=[("office-camera-08", 0.2, 0.45), ("office-camera-08", 0.8, 0.45), ("office-camera-08", 1.5, 0.45), ("office-camera-08", 2.3, 0.45)], drift=(0.3, 0)),
 # Kapitel 4
 57: dict(fx=[L((0.5, 0.1), 0.1, 0.25, 21)], ov=[C("Atlanta · 1932")], sfx=[("keys-jingling-01", 0.3, 0.45)], drift=(-0.3, 0)),
 58: dict(fx=[RAIN(0.3), PU((0.62, 0.25), 0.1, 0.3, 2.0)], ov=[C("Alcatraz · 1934")], sfx=[("iron-gate-01", 4.5, 0.45)], drift=(0.3, 0), rain=True),
 59: dict(fx=[BR(0.03, 1.0)], ov=[C("Entlassen · 1939")], sfx=[], drift=(0, -0.3)),
 60: dict(fx=[PU((0.82, 0.25), 0.12, 0.25, 1.0)], ov=[C("† 25. Januar 1947 · Miami")], sfx=[], drift=(-0.3, 0)),
 61: dict(fx=[BR(0.03)], ov=[C("Frank J. Wilson · Chef des Secret Service")], sfx=[], drift=(0.3, 0)),
 62: dict(fx=[L((0.5, 0.05), 0.12, 0.25, 22)], ov=[C("„Folge dem Geld“")], sfx=[], drift=(0, -0.3)),
 63: dict(fx=[L((0.4, 0.08), 0.12, 0.3, 23), SM((0.3, 0.75), 0.6, 0.18)], ov=[], sfx=[], drift=(0.2, 0.2)),
 64: dict(fx=[RAIN(0.45), L((0.08, 0.12), 0.08, 0.3, 24)], ov=[("bubble", 0.4, None, dict(lines=["Was meinst du?", "Schreib es in die Kommentare!"], pos=(900, 60)))], sfx=[], drift=(0, 0), rain=True),
 65: dict(fx=[SM((0.25, 0.1), 1.0, 0.2), BR(0.03, 4.0)], ov=[C("Abonnieren · Glocke aktivieren", a=1.5, size=64)], sfx=[("factory-machinery-ambience-01", 0.0, 0.25)], drift=(0.3, 0)),
}
CHAPTERS = {18: ("KAPITEL 1", "DER AUFSTIEG", 2), 30: ("KAPITEL 2", "DIE JAGD", 3), 47: ("KAPITEL 3", "DER PROZESS", 4), 57: ("KAPITEL 4", "DAS ENDE", 5)}
PRE = {6: 0.5, 13: 1.0, 17: 0.4, 54: 0.5, 56: 0.4, 63: 0.5}
CH_PAUSE = 2.2
