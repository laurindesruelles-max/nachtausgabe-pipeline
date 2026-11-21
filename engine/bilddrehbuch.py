#!/usr/bin/env python3
"""Bild-Drehbuch-Prüfung (Laurin, 21.11.2026) – gleiche Datei in allen fünf Kanal-Repos.

Prüft VOR dem Einsprechen, ob jede Stelle des Skripts so gezeigt wird, dass Neugier und
Spannung über die ganze Länge halten (Ziel: >= 60 % Wiedergabe). Regeln: HANDWERK.md,
Abschnitt „Bild-Drehbuch“; erlaubte Animationen: EFFEKTE.md + ANIMATION.md des Kanals.

Aufruf:  python3 engine/bilddrehbuch.py videos/NNN-slug/bilddrehbuch.json [--kanal goldsmith]
Exit 1 bei Fehlern (dann Drehbuch/Skript überarbeiten), Warnungen nur melden.
Zahlen, Jahre und Uhrzeiten im Feld „satz“ als Ziffern schreiben. Mehrere Ereignisse in einem Bild = mehrere Einträge mit „sek“.

bilddrehbuch.json = Liste von Einstellungen in Videoreihenfolge:
  {
    "satz": "Am 14. März 1961, um 23:47 Uhr, klingelt in Mailand ein Telefon.",
    "sek": 4.2,                      # optional, sonst aus Wortzahl geschätzt (2,4 Wörter/s)
    "zeigt": "Schreibmaschine tippt MAILAND 1961, Telefon auf dem Schreibtisch klingelt",
    "animation": "Ort und Datum tippen",   # exakter Name aus EFFEKTE.md/ANIMATION.md
    "inhalt": ["zeit", "ort", "geschehen"],# zeit|ort|geschehen|zahl|person|gefuehl|erklaerung|vergleich
    "genauigkeit": "exakt",                # exakt | schema | stimmung
    "neugier": "frage:anrufer",            # frage:<id> | antwort:<id> | teaser:<id> | ""
    "kapitel": 1                            # optional
  }
"""
import json, re, sys, pathlib, argparse

WPS = 2.4  # deutsche/englische Sprechgeschwindigkeit der Kanalstimmen, Wörter pro Sekunde

# Kanal-Regeln: welche Animationen Zeit/Zahl EXAKT tragen können (zusätzlich zur Pflicht „exakt“)
KANAL = {
    "goldsmith":   {"min_events": 12, "max_sek": 5.5},
    "meisterwerk": {"min_events": 12, "max_sek": 6.0},
    "unterbau":    {"min_events": 15, "max_sek": 4.5},
    "denkmuster":  {"min_events": 12, "max_sek": 6.0},
    "nachtausgabe": {"min_events": 13, "max_sek": 5.0},
}

JAHR = re.compile(r"\b(1[0-9]{3}|20[0-9]{2})\b")
UHR = re.compile(r"\b\d{1,2}[:.]\d{2}\s*(Uhr)?\b|\b\d{1,2}\s*Uhr\b|\b(a\.?m\.?|p\.?m\.?)\b", re.I)
ZAHL = re.compile(r"\b\d[\d.,]*\s*(%|Prozent|percent|Millionen|Milliarden|million|billion|Tonnen|tons|km|Meter|meters|Euro|€|\$|Dollar|Grad|Mikrometer|Jahre|years|Tage|days|Stunden|hours|Minuten|minutes)\b", re.I)


def katalog(repo: pathlib.Path):
    """Animationsnamen = erste Spalte aller Tabellen in EFFEKTE.md und ANIMATION.md."""
    namen = set()
    for f in ("EFFEKTE.md", "ANIMATION.md"):
        p = repo / f
        if not p.exists():
            continue
        im_katalog = False
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                im_katalog = "katalog" in line.lower()
                continue
            if im_katalog and line.startswith("|") and not line.startswith("| ---"):
                zelle = line.strip("|").split("|")[0].strip().strip("*`")
                if zelle and zelle.lower() not in ("effekt", "animation", "", "kanal"):
                    namen.add(zelle)
    return namen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("datei")
    ap.add_argument("--kanal", default=None)
    a = ap.parse_args()
    datei = pathlib.Path(a.datei)
    repo = pathlib.Path(__file__).resolve().parent.parent
    kanal = (a.kanal or repo.name.split("-")[0]).lower()
    regel = KANAL.get(kanal, {"min_events": 12, "max_sek": 5.5})
    erlaubt = katalog(repo)
    shots = json.loads(datei.read_text(encoding="utf-8"))

    fehler, warn = [], []
    t = 0.0
    zeiten = []
    offene = {}
    beantwortet = set()
    for i, s in enumerate(shots, 1):
        satz = s.get("satz", "")
        sek = float(s.get("sek") or max(1.5, len(satz.split()) / WPS))
        anim = s.get("animation", "").strip()
        inhalt = set(s.get("inhalt", []))
        gen = s.get("genauigkeit", "")
        zeigt = s.get("zeigt", "").strip()
        ort = f"#{i} ({t:5.1f}s)"
        zeiten.append((t, sek, anim))

        if erlaubt and anim not in erlaubt:
            fehler.append(f"{ort} Animation „{anim}“ steht nicht in EFFEKTE.md/ANIMATION.md")
        if len(zeigt.split()) < 4:
            fehler.append(f"{ort} „zeigt“ zu vage – konkret beschreiben, was im Bild passiert")
        if sek > regel["max_sek"] + 1.0:
            fehler.append(f"{ort} {sek:.1f}s ohne neues Bild-Ereignis (max {regel['max_sek']}s) – Satz teilen oder zweites Ereignis")
        elif sek > regel["max_sek"]:
            warn.append(f"{ort} {sek:.1f}s lang – Eigenbewegung im Bild sicherstellen")
        if (JAHR.search(satz) or UHR.search(satz)) and gen != "exakt":
            fehler.append(f"{ort} Satz nennt Jahr/Uhrzeit → Zeit muss EXAKT im Bild stehen (genauigkeit: exakt)")
        if UHR.search(satz) and "zeit" not in inhalt:
            fehler.append(f"{ort} Uhrzeit im Satz, aber inhalt ohne „zeit“")
        if ZAHL.search(satz) and gen != "exakt":
            fehler.append(f"{ort} harte Zahl → als Zahl im Bild zeigen (genauigkeit: exakt)")
        if "geschehen" in inhalt and gen == "stimmung":
            fehler.append(f"{ort} Geschehen nur als Stimmung – zeigen, WAS passiert (Moment der Veränderung)")
        if "erklaerung" in inhalt and gen == "stimmung":
            warn.append(f"{ort} Erklärung nur als Stimmung – Schema/Ablauf zeigen")
        n = s.get("neugier", "") or ""
        if n.startswith("frage:"):
            offene[n[6:]] = t
        elif n.startswith("antwort:"):
            k = n[8:]
            if k not in offene:
                warn.append(f"{ort} Antwort „{k}“ ohne vorher gestellte Frage")
            else:
                if t - offene[k] < 20:
                    warn.append(f"{ort} Frage „{k}“ nach {t - offene[k]:.0f}s schon aufgelöst – Spannung länger halten")
                offene.pop(k)
                beantwortet.add(k)
        t += sek

    dauer = t
    # 1) Hook: in den ersten 30 s muss eine Frage offen sein
    if not any((s.get("neugier", "") or "").startswith("frage:")
               for s, (z, _, _) in zip(shots, zeiten) if z < 30):
        fehler.append("Hook: in den ersten 30 s wird keine Frage geöffnet")
    # 2) Spannungsbogen: bis 60 s vor Schluss immer mindestens eine offene Frage
    offen_jetzt = {}
    luecken = []
    for s, (z, sek, _) in zip(shots, zeiten):
        n = s.get("neugier", "") or ""
        if n.startswith("frage:"):
            offen_jetzt[n[6:]] = z
        elif n.startswith("antwort:"):
            offen_jetzt.pop(n[8:], None)
        if 30 < z < dauer - 60 and not offen_jetzt:
            luecken.append(z)
    if luecken:
        fehler.append(f"Spannungsloch: keine offene Frage ab {luecken[0]:.0f}s ({len(luecken)} Einstellungen) – neue Frage/Teaser setzen")
    if offene:
        warn.append(f"Nie aufgelöst: {', '.join(offene)}")
    # 3) Musterbruch: in jedem 30-s-Fenster mindestens 3 verschiedene Animationen
    for start in range(0, max(1, int(dauer) - 30), 15):
        im = {an for z, sk, an in zeiten if start <= z < start + 30}
        if len(im) < 3:
            fehler.append(f"Monotonie {start}–{start+30}s: nur {len(im)} Animationsarten – Musterbruch einbauen")
    # 4) Gleiche Animation nicht mehr als 2x hintereinander
    for i in range(2, len(zeiten)):
        if zeiten[i][2] == zeiten[i-1][2] == zeiten[i-2][2]:
            warn.append(f"#{i+1} „{zeiten[i][2]}“ dreimal hintereinander")
    # 5) Bild-Ereignisse pro Minute
    pro_min = len(shots) / (dauer / 60) if dauer else 0
    if pro_min < regel["min_events"]:
        fehler.append(f"Nur {pro_min:.1f} Bild-Ereignisse/Min (Ziel ≥ {regel['min_events']})")
    # 6) Länge > 8 Min
    if dauer < 8 * 60:
        warn.append(f"Geschätzte Länge {dauer/60:.1f} Min – unter 8 Minuten")

    print(f"Bild-Drehbuch {datei} – Kanal {kanal}: {len(shots)} Einstellungen, ~{dauer/60:.1f} Min, {pro_min:.1f} Ereignisse/Min")
    for f in fehler:
        print("FEHLER ", f)
    for w in warn:
        print("WARNUNG", w)
    print("OK ✅" if not fehler else f"{len(fehler)} Fehler ❌")
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
