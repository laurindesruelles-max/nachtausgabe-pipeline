"""Episode 003 – Der Juwelenraub im Grünen Gewölbe. Panel-Effekte, Overlays, Geräusche, Kapitel, 2D-Motion-Clips.
Zeiten in Overlays/SFX sind Sekunden relativ zum Sprechbeginn des Panels.
MOTION (Pflicht seit 25.11.2026, mind. 8): Zeilen ohne KI-Panel, der Clip zeigt die Grafik in einem Panel auf der Comicseite.
Schlagzeilen-Sound newspaper-slap-01 (Gemini-Casting 27.11.2026: PREMIUM, impact-slam-35: CHEAP)."""
from engine import *

TITLE_AFTER = 10
TITLE_LINES = ["DAS GRÜNE GEWÖLBE", "DRESDEN 2019"]
TWIST = 7
N_PANELS = 72
FIRST_CHAPTER_LABEL = "Der Coup im Grünen Gewölbe"
EXTRA_LINE = "EXTRABLATT  ·  DRESDEN  ·  2019"
CH_PAUSE = 3.0
FLIP_GAP = 1.25
HEADLINE_SFX = "newspaper-slap-01"
DUCK = 0.62          # Musik unter Sprache >= 16 dB unter der Stimme (Laurin 24.11.2026)

MOTION = {
 6: ("counter", dict(label="DIE BEUTE", value=113.8, dec=1, suffix=" MIO. €", caption="WERT LAUT ANKLAGE")),
 13: ("map", dict(label="1723 – 1730", view="europe", pins=[dict(lonlat=[13.74, 51.05], label="DRESDEN · SCHLOSS")], threads="none")),
 24: ("flow", dict(label="DER PLAN", nodes=[dict(icon="eye", label="Fenster wählen"), dict(icon="lock", label="Gitter schneiden"),
                                             dict(icon="car", label="Zwei Autos"), dict(icon="clock", label="Strom aus"), dict(icon="money", label="Juwelen")])),
 42: ("map", dict(label="DIE FLUCHT", view=[13.55, 51.75, 9000], pins=[dict(lonlat=[13.74, 51.05], label="DRESDEN"), dict(lonlat=[13.40, 52.52], label="BERLIN")],
                  threads="chain", counter=dict(value=190, suffix=" KM", label="STRASSE, CA."))),
 47: ("flip", dict(teaser="DNA im zweiten Fluchtauto ...", front=dict(icon="eye", title="DIE SPUR"), back=dict(title="NEUKÖLLN", sub="Berlin · Großfamilie Remmo"), at=2.2)),
 49: ("counter", dict(label="BERLIN · MÄRZ 2017", value=100, suffix=" KG", caption="GOLDMÜNZE AUS DEM BODE-MUSEUM")),
 53: ("counter", dict(label="17. NOVEMBER 2020", value=1638, caption="POLIZISTEN · 18 ORTE IN BERLIN")),
 62: ("stack", dict(label="WAS FEHLT", cards=[["EPAULETTE", "mit dem Sächsischen Weißen"], ["BRUSTSCHLEIFE", "Königin Amalie Auguste"], ["KOLLIER", "abgerissenes Teil"]], symbol="?", question="Wo sind sie?")),
 65: ("bars", dict(label="DAS URTEIL · 16.05.2023", title="HAFTSTRAFEN", unit=" MON.", bars=[["6 J. 3 M.", 75, True], ["6 J. 2 M.", 74, False], ["6 J.", 72, False], ["5 J. 10 M.", 70, False], ["4 J. 4 M.", 52, False]])),
 68: ("bars", dict(label="DER WERT", title="MIO. € · KULTURMINISTERIUM", bars=[["VOR DEM EINBRUCH", 128.6, False], ["HEUTE", 76.1, True]])),
}
_M = dict(fx=[], ov=[], sfx=[], drift=(0, 0))

P = {
 1: dict(fx=[L((0.42, 0.42), 0.06, 0.35, 1), L((0.89, 0.6), 0.05, 0.3, 2), BR(0.03, 1.2)], ov=[C("DRESDEN · 25. NOVEMBER 2019 · KURZ VOR 5 UHR", size=60, big=True)], sfx=[], drift=(-0.3, 0)),
 2: dict(fx=[SM((0.25, 0.25), 0.8, 0.35), L((0.28, 0.6), 0.08, 0.45, 3), L((0.55, 0.35), 0.05, 0.3, 4)], ov=[C("Augustusbrücke · Stromverteiler")], sfx=[("match-strike-01", 0.3, 0.3)], drift=(0.3, 0)),
 3: dict(fx=[L((0.56, 0.12), 0.06, 0.3, 5), TL([(0.9, 0.3), (0.75, 0.45), (0.85, 0.55)], 0.3, 3.0)], ov=[], sfx=[("footsteps-stone-01", 0.4, 0.3)], drift=(0, -0.3)),
 4: dict(fx=[PU((0.48, 0.25), 0.12, 0.3, 2.2), L((0.13, 0.25), 0.08, 0.3, 6)], ov=[], sfx=[], drift=(0.3, 0)),
 5: dict(fx=[SM((0.55, 0.5), 1.0, 0.3), L((0.75, 0.4), 0.1, 0.3, 7)], ov=[], sfx=[("glass-clink-01", 0.2, 0.3)], drift=(-0.3, 0)),
 6: _M,
 7: dict(fx=[TL([(0.2, 0.3), (0.7, 0.3), (0.5, 0.7), (0.42, 0.72)], 0.0, 3.0)], ov=[], sfx=[], drift=(0, 0)),
 8: dict(fx=[L((0.45, 0.6), 0.08, 0.3, 8), L((0.8, 0.3), 0.06, 0.3, 9)], ov=[C("Berlin")], sfx=[("car-door-opening-and-closing-01", 3.0, 0.35)], drift=(0.3, 0)),
 9: dict(fx=[L((0.73, 0.35), 0.1, 0.4, 10), PU((0.55, 0.6), 0.1, 0.3, 1.5)], ov=[], sfx=[("cardboard-box-close-01", 0.5, 0.3)], drift=(-0.3, 0)),
 10: dict(fx=[PU((0.85, 0.65), 0.12, 0.35, 1.2), BR(0.03)], ov=[], sfx=[], drift=(0.3, 0)),
 # Kapitel 1 – Die Schatzkammer
 11: dict(fx=[BR(0.04, 1.0)], ov=[CL(0.0, 3.2, dir=-1, y0=2019, y1=1723, center=(560, 470))], sfx=[], drift=(-0.3, 0)),
 12: dict(fx=[L((0.55, 0.2), 0.1, 0.25, 11)], ov=[WA("AUGUST DER STARKE", "DER KURFÜRST", "1670 – 1733", (0.2, 0.06, 0.46, 0.6), 0.8, center=(1450, 560))], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.25)], drift=(0.3, 0)),
 13: _M,
 14: dict(fx=[L((0.48, 0.18), 0.1, 0.3, 12), PU((0.5, 0.45), 0.12, 0.25, 1.5)], ov=[C("Sockel und Kapitelle · malachitgrün")], sfx=[], drift=(0, -0.3)),
 15: dict(fx=[L((0.5, 0.1), 0.08, 0.3, 13), BR(0.03)], ov=[C("eines der ältesten Museen Europas")], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.25)], drift=(0.3, 0)),
 16: dict(fx=[L((0.52, 0.12), 0.1, 0.35, 14), PU((0.6, 0.6), 0.1, 0.3, 2.0)], ov=[C("Das Juwelenzimmer")], sfx=[], drift=(-0.3, 0)),
 17: dict(fx=[PU((0.72, 0.4), 0.1, 0.4, 1.4), PU((0.3, 0.45), 0.08, 0.3, 1.8)], ov=[], sfx=[("coin-dropped-on-wooden-table-01", 1.5, 0.3)], drift=(0.3, 0)),
 18: dict(fx=[PU((0.62, 0.55), 0.12, 0.4, 1.3), L((0.52, 0.12), 0.08, 0.3, 15)], ov=[C("Epaulette · fast 50 Karat in der Mitte")], sfx=[], drift=(0, -0.3)),
 19: dict(fx=[PU((0.3, 0.25), 0.15, 0.5, 1.0), L((0.28, 0.48), 0.06, 0.35, 16)], ov=[HL("DER SÄCHSISCHE WEISSE", 0.6, center=(W / 2, 880), scale=0.7)], sfx=[], drift=(0.3, 0)),
 20: dict(fx=[SM((0.85, 0.35), 0.9, 0.3), BR(0.03)], ov=[CL(0.0, 2.8, dir=1, y0=1730, y1=1945, center=(1450, 470))], sfx=[("cardboard-box-close-01", 3.6, 0.3)], drift=(-0.3, 0)),
 21: dict(fx=[SM((0.2, 0.1), 1.0, 0.35), SNOW(0.4)], ov=[C("Moskau · bis 1958")], sfx=[("air-hiss-01", 0.2, 0.3)], drift=(0.3, 0)),
 22: dict(fx=[L((0.5, 0.45), 0.08, 0.3, 17), FL([(0.6, (0.3, 0.6)), (1.4, (0.7, 0.6))])], ov=[CL(0.0, 2.4, dir=1, y0=1958, y1=2006, center=(1450, 470))], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.3), ("office-camera-08", 0.6, 0.3)], drift=(0, -0.3)),
 23: dict(fx=[FL([(1.0, (0.12, 0.45))]), L((0.33, 0.45), 0.06, 0.3, 18)], ov=[HL("DIE SCHWACHSTELLE", 4.0, center=(W / 2, 880), scale=0.75)], sfx=[("office-camera-08", 1.0, 0.4)], drift=(0.3, 0)),
 # Kapitel 2 – Die Nacht
 24: _M,
 25: dict(fx=[L((0.65, 0.35), 0.06, 0.3, 19), TL([(0.3, 0.3), (0.6, 0.5), (0.7, 0.45)], 0.2, 2.6)], ov=[C("ab 18. November 2019 · mehrere Fahrten nach Dresden")], sfx=[], drift=(-0.3, 0)),
 26: dict(fx=[L((0.55, 0.12), 0.1, 0.4, 20)], ov=[C("gekauft unter falschen Namen")], sfx=[("car-door-opening-and-closing-01", 0.5, 0.35)], drift=(0.3, 0)),
 27: dict(fx=[BR(0.03), L((0.52, 0.75), 0.06, 0.3, 21)], ov=[CL(0.0, 2.2, dir=1, text="25.11.2019", center=(1450, 470))], sfx=[], drift=(0, -0.3)),
 28: dict(fx=[SM((0.62, 0.45), 0.7, 0.35), L((0.6, 0.6), 0.08, 0.5, 22)], ov=[C("Augustusbrücke · kurz vor 5 Uhr")], sfx=[("match-strike-01", 0.6, 0.35)], drift=(-0.3, 0)),
 29: dict(fx=[L((0.55, 0.2), 0.08, 0.3, 23)], ov=[C("Der Strom fällt aus")], sfx=[], drift=(0.3, 0)),
 30: dict(fx=[PU((0.5, 0.2), 0.04, 0.6, 2.5)], ov=[], sfx=[], drift=(0, -0.3)),
 31: dict(fx=[L((0.65, 0.1), 0.06, 0.3, 24)], ov=[], sfx=[("footsteps-stone-01", 0.3, 0.35)], drift=(-0.3, 0)),
 32: dict(fx=[PU((0.68, 0.45), 0.1, 0.35, 1.2)], ov=[], sfx=[("footsteps-stone-01", 0.0, 0.35)], drift=(0.3, 0)),
 33: dict(fx=[L((0.4, 0.12), 0.08, 0.3, 25), PU((0.6, 0.55), 0.08, 0.3, 2.0)], ov=[C("4:57 Uhr")], sfx=[("clock_tick", 0.0, 0.2)], drift=(0, -0.3)),
 34: dict(fx=[SH(-0.25), L((0.6, 0.12), 0.08, 0.3, 26)], ov=[], sfx=[], drift=(0.3, 0)),
 35: dict(fx=[PU((0.95, 0.12), 0.05, 0.6, 3.0), L((0.4, 0.1), 0.06, 0.3, 27)], ov=[C("4:59 Uhr · Notruf")], sfx=[], drift=(-0.3, 0)),
 36: dict(fx=[TL([(0.15, 0.6), (0.4, 0.4), (0.7, 0.35), (0.75, 0.45)], 0.0, 3.0)], ov=[], sfx=[("glass-clink-01", 0.5, 0.25)], drift=(0, -0.3)),
 37: dict(fx=[SM((0.4, 0.4), 1.2, 0.45), SM((0.6, 0.55), 1.0, 0.35)], ov=[], sfx=[("air-hiss-01", 0.2, 0.45)], drift=(0.3, 0)),
 38: dict(fx=[L((0.88, 0.1), 0.06, 0.3, 28), PU((0.9, 0.65), 0.05, 0.3, 2.0)], ov=[C("wenige Minuten · laut Anklage 4:57 bis 5:01 Uhr")], sfx=[("footsteps-concrete-03", 0.3, 0.35), ("car-door-opening-and-closing-01", 3.0, 0.35)], drift=(-0.3, 0)),
 39: dict(fx=[FL([(0.3, (0.2, 0.6)), (0.7, (0.4, 0.62)), (1.2, (0.3, 0.6))])], ov=[], sfx=[("car-door-opening-and-closing-01", 0.4, 0.4)], drift=(0.3, 0)),
 40: dict(fx=[SM((0.65, 0.4), 1.2, 0.4), L((0.62, 0.72), 0.08, 0.45, 29)], ov=[C("Dresden-Pieschen · Tiefgarage")], sfx=[], drift=(0, -0.3)),
 41: dict(fx=[SM((0.3, 0.3), 1.1, 0.45), L((0.25, 0.55), 0.1, 0.5, 30)], ov=[], sfx=[], drift=(-0.3, 0)),
 42: _M,
 # Kapitel 3 – Die Spur nach Berlin
 43: dict(fx=[PU((0.75, 0.2), 0.12, 0.3, 1.5)], ov=[C("Morgen des 25. November")], sfx=[("factory-machinery-ambience-01", 0.0, 0.2)], drift=(0.3, 0)),
 44: dict(fx=[L((0.65, 0.5), 0.08, 0.35, 31)], ov=[C("Soko „Epaulette“")], sfx=[("paper-fabric-card-flip-06", 1.0, 0.3)], drift=(0, -0.3)),
 45: dict(fx=[FL([(0.4, (0.15, 0.55)), (1.6, (0.45, 0.5))])], ov=[], sfx=[("office-camera-08", 0.4, 0.35), ("office-camera-08", 1.6, 0.35)], drift=(-0.3, 0)),
 46: dict(fx=[PU((0.85, 0.3), 0.15, 0.4, 1.2), L((0.62, 0.12), 0.08, 0.35, 32)], ov=[HL("DNA-TREFFER", 0.9, center=(W / 2, 880), scale=0.85)], sfx=[], drift=(0.3, 0)),
 47: _M,
 48: dict(fx=[L((0.88, 0.1), 0.08, 0.3, 33), PU((0.2, 0.75), 0.1, 0.25, 2.0)], ov=[C("Bode-Museum · Berlin")], sfx=[], drift=(-0.3, 0)),
 49: _M,
 50: dict(fx=[L((0.6, 0.12), 0.1, 0.4, 34), PU((0.4, 0.6), 0.12, 0.3, 1.6)], ov=[C("vermutlich zerteilt und verkauft")], sfx=[("coin-dropped-on-wooden-table-01", 0.4, 0.35)], drift=(0, -0.3)),
 51: dict(fx=[L((0.25, 0.2), 0.08, 0.3, 35), BR(0.03)], ov=[C("Urteil zur Goldmünze")], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.25)], drift=(0.3, 0)),
 52: dict(fx=[FL([(0.5, (0.25, 0.6)), (1.0, (0.15, 0.62)), (1.8, (0.35, 0.6))])], ov=[], sfx=[("car-door-opening-and-closing-01", 2.0, 0.35), ("footsteps-concrete-03", 3.0, 0.35)], drift=(-0.3, 0)),
 53: _M,
 54: dict(fx=[FL([(0.3, (0.75, 0.5)), (1.0, (0.5, 0.45))])], ov=[], sfx=[("car-door-opening-and-closing-01", 2.2, 0.4)], drift=(0.3, 0)),
 55: dict(fx=[TL([(0.85, 0.2), (0.5, 0.4), (0.65, 0.6), (0.66, 0.55)], 0.0, 2.6)], ov=[], sfx=[], drift=(0, 0)),
 # Kapitel 4 – Der Deal
 56: dict(fx=[L((0.5, 0.1), 0.08, 0.3, 36), BR(0.03)], ov=[C("Landgericht Dresden · Januar 2022")], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.3)], drift=(-0.3, 0)),
 57: dict(fx=[L((0.3, 0.4), 0.08, 0.3, 37)], ov=[], sfx=[("scroll-unroll-01", 0.3, 0.3)], drift=(0.3, 0)),
 58: dict(fx=[SNOW(0.35), L((0.5, 0.15), 0.06, 0.3, 38)], ov=[C("Dezember 2022")], sfx=[], drift=(0, -0.3)),
 59: dict(fx=[SH(-0.25), L((0.42, 0.12), 0.1, 0.4, 39)], ov=[], sfx=[("paper-fabric-card-flip-06", 1.5, 0.3)], drift=(-0.3, 0)),
 60: dict(fx=[PU((0.5, 0.55), 0.12, 0.45, 1.2), L((0.62, 0.18), 0.08, 0.35, 40)], ov=[C("Nacht zum 17. Dezember 2022"), HL("BEUTE TAUCHT AUF", 3.4, center=(W / 2, 880), scale=0.75)], sfx=[("cardboard-box-close-01", 0.6, 0.3)], drift=(0.3, 0)),
 61: dict(fx=[L((0.48, 0.1), 0.1, 0.4, 41), PU((0.52, 0.5), 0.1, 0.35, 1.4)], ov=[C("31 Einzelteile · teils schwer beschädigt")], sfx=[("glass-clink-01", 0.3, 0.2)], drift=(0, -0.3)),
 62: _M,
 63: dict(fx=[TL([(0.1, 0.4), (0.4, 0.3), (0.62, 0.5), (0.6, 0.48)], 0.0, 2.8)], ov=[], sfx=[], drift=(0, 0)),
 64: dict(fx=[FL([(0.3, (0.3, 0.7)), (0.9, (0.7, 0.7))]), L((0.5, 0.05), 0.06, 0.3, 42)], ov=[C("16. Mai 2023"), HL("VERURTEILT", 3.0, center=(W / 2, 880), scale=0.85)], sfx=[("daily-20260923-hushed-crowd-walla-short", 0.0, 0.3), ("office-camera-08", 0.3, 0.35)], drift=(-0.3, 0)),
 65: _M,
 66: dict(fx=[BR(0.03), L((0.75, 0.4), 0.08, 0.3, 43)], ov=[C("Bundesgerichtshof · April 2024")], sfx=[("footsteps-stone-01", 0.3, 0.3)], drift=(0.3, 0)),
 67: dict(fx=[L((0.55, 0.3), 0.12, 0.4, 44), PU((0.5, 0.55), 0.1, 0.3, 1.6)], ov=[C("seit August 2024 · unrestauriert")], sfx=[("footsteps-stone-01", 0.2, 0.25)], drift=(-0.3, 0)),
 68: _M,
 69: dict(fx=[L((0.75, 0.4), 0.1, 0.3, 45), BR(0.03)], ov=[C("Vermutung · nicht bewiesen")], sfx=[], drift=(0.3, 0)),
 70: dict(fx=[PU((0.48, 0.65), 0.15, 0.5, 1.0)], ov=[HL("VERSCHWUNDEN", 2.2, center=(W / 2, 880), scale=0.85)], sfx=[], drift=(0, -0.3)),
 71: dict(fx=[L((0.82, 0.18), 0.08, 0.4, 46)], ov=[("bubble", 0.4, None, dict(lines=["Taucht er je wieder auf?", "Schreib es in die Kommentare!"], pos=(900, 60)))], sfx=[], drift=(-0.3, 0)),
 72: dict(fx=[L((0.82, 0.12), 0.08, 0.4, 47), BR(0.03, 4.0)], ov=[C("Abonnieren · Glocke aktivieren", a=1.0, size=64)], sfx=[("paper-fabric-crumple-36", 0.5, 0.25)], drift=(0.3, 0)),
}
CHAPTERS = {11: ("KAPITEL 1", "DIE SCHATZKAMMER", 2), 24: ("KAPITEL 2", "DIE NACHT", 3), 43: ("KAPITEL 3", "DIE SPUR NACH BERLIN", 4), 56: ("KAPITEL 4", "DER DEAL", 5)}
PRE = {7: 0.7, 19: 0.6, 34: 0.4, 46: 0.6, 60: 0.5, 63: 0.6, 64: 0.5, 70: 0.6, 47: 0.3}
