"""Ton fuer die Nachtausgabe-Stilprobe (Variante Mitte): Nachtausgabe-Geraeusche + Noir-Jazz durchgehend, Anschwellen vor Enthuellungen, keine Pausen."""
import sys; sys.path.insert(0, "/home/claude/stilproben")
from mixer import mix
N = "/home/claude/repos/nachtausgabe-pipeline/assets/sfx/"; X = "/home/claude/na_sfx/"; M = "/home/claude/repos/nachtausgabe-pipeline/assets/music/"
f = lambda n: N + n + ".mp3"
ev = [(0.0, X + "machine_engine.wav", 0.22), (0.15, f("short-video-whoosh-01"), 0.45), (1.25, f("paper-fabric-card-flip-06"), 0.7),
      (1.3, f("cinematic-boom-01"), 0.3),
      (3.2, f("short-video-whoosh-01"), 0.3), (3.45, f("match-strike-01"), 0.35),
      (4.2, f("paper-fabric-card-flip-06"), 0.55), (4.25, f("reveal-impact-01"), 0.45),
      (6.6, f("short-video-whoosh-01"), 0.25), (7.0, f("lighter-flick-01"), 0.4), (9.4, f("scroll-unroll-01"), 0.4),
      (10.4, f("short-video-whoosh-01"), 0.25), (11.25, f("glass-clink-01"), 0.25), (11.9, X + "glass_shatter_01.wav", 0.75),
      (12.0, f("ambience-rain-03"), 0.12),
      (13.6, f("short-video-whoosh-01"), 0.25), (14.4, "/home/claude/gs_sfx/clock_tick.wav", 0.35),
      (17.0, f("short-video-whoosh-01"), 0.25), (18.2, f("impact-slam-35"), 1.4), (18.22, f("reveal-impact-01"), 0.9), (18.2, f("cinematic-boom-01"), 0.6),
      (20.0, f("short-video-whoosh-01"), 0.2), (20.75, f("paper-fabric-card-flip-06"), 0.8), (21.6, f("cinematic-boom-01"), 0.15)]
music = (M + "noir_3_jagd.mp3", 0.22, 0.0, 0.8, 0.3, [(4.1, 4, 1.2), (11.8, 4, 1.2), (18.6, 9, 1.6), (21.5, 2, 1.5)], 30.0)
print(mix("/home/claude/stilproben/stilprobe_nachtausgabe_mitte.mp4", "/home/claude/stilproben/ton_nachtausgabe.mp4", ev, 23.0, music))
