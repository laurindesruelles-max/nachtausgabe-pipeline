# Nachtausgabe – Pipeline

Deutscher Faceless-True-Crime-Kanal **Nachtausgabe** (youtube.com/@Nachtausgabe).
Kriminalfälle aus aller Welt (Mord, Mafia, Coups, Betrug, Ungelöstes), erzählt als **Comic-Noir**:
Graphic-Novel-Panels in Schwarz, Papierweiß und Bernstein; die Kamera fährt über Comicseiten von Panel zu Panel.

Pilot: `videos/001-al-capone` (8:10, „Der mächtigste Gangster Amerikas – gestürzt von einem Buchhalter“).

**Vor jedem Lauf `LESSONS.md` lesen** – dort stehen Laurins feste Regeln.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `engine/engine.py` | Seitenlayout, Effekte (Schnee, Regen, Rauch, Lampen, Blitzlicht, Atmen), Overlays (Caption, Stempel, Sprechblase, Zähler, Karte, Balken, Kapitelkarte), Kurzschreibweisen `C S L SM BR PU RAIN SNOW FL` |
| `engine/render.py` | rendert eine Episode komplett (Bild + Ton + Kapitelmarken) |
| `engine/asr.py` | Aussprache-Kontrolle per Spracherkennung |
| `engine/thumbnail.py` | Hero-Thumbnail (Motiv + 2 Zeilen) |
| `engine/qa.py` | technische Endkontrolle → `qa.md` |
| `engine/get.py` | lädt Higgsfield-Ergebnisse: `python3 engine/get.py ORDNER PREFIX 1=url 2=url …` |
| `assets/music/` | feste Noir-Jazz-Bibliothek (siehe `MUSIK.md`) – **keine neue Musik erzeugen** |
| `assets/sfx/` | Geräusche, CC0 (siehe `SOUNDS.md`) |
| `assets/fonts/` | Bangers (Titel/Stempel), Comic Neue Bold (Kästen) – SIL OFL |
| `videos/NNN-slug/` | `lines.py` (Sprechertext), `episode.py` (Effekte/Overlays/Kapitel), `beschreibung.txt`, Thumbnails, `qa.md` |

## Ein neues Video bauen

```sh
export WORK=/home/claude/na-work && sh setup.sh
```

1. **Recherche** mit Primärquellen (Gerichtsakten, Behörden, Archive, seriöse Presse). Mindestens 6 Quellen.
2. **Skript** `videos/NNN-slug/lines.py`: `LINES = {1: "...", ...}` – ein Satz/Gedanke = ein Panel (Ziel 60–70 Zeilen).
   Aufbau: Einstieg ~15–18 Zeilen, max. 60–75 s (Hook mit dem dramatischsten Moment, Fall/Name in den ersten 5 s im Bild, offene Fragen + Versprechen – siehe LESSONS.md „Hook-Regeln“, Wendung, Satz „… das ist die Geschichte der heutigen Nachtausgabe.“), dann 4 Kapitel, Ende mit Kommentar-Frage + „Abonniere den Kanal und aktiviere die Glocke. Bis zur nächsten Nacht.“
   **Zahlen immer ausschreiben** („neunzehnhundertneunundzwanzig“), keine Abkürzungen, englische Namen sparsam.
3. **Panels** mit Higgsfield `generate_image_batch` (Modell `gpt_image_2_6`, `aspect_ratio 16:9`, 0,25 Credits/Bild), höchstens 6 pro Aufruf (sonst Rate-Limit). Jeder Prompt beginnt mit:
   > Comic book panel, graphic novel noir style, bold black ink linework, heavy shadows, halftone dot shading, limited palette of black, off-white paper and a single warm amber-yellow accent color.

   und endet mit „No readable text, no logos.“ Keine Gewaltdarstellung (kein Blut, keine Leichen, keine Waffen im Anschlag). Echte Personen nur als gezeichnete, nicht fotorealistische Figur. Speichern als `$WORK/img/p01.png …`.
4. **Stimme**: Sterling über **ElevenLabs v4** – `generate_audio_batch`, `model elevenlabs_v4`, `stability 0.5`,
   `dialogue: [{text, voice_type: "preset", voice_id: "dc382508-c8bd-443c-8cb2-46e57b8d2e6f"}]`, eine Datei pro Zeile → `$WORK/vo/s01.mp3 …`. Höchstens 6 pro Aufruf.
5. **Aussprache prüfen**: `python3 engine/asr.py $WORK/vo/s*.mp3` und mit `lines.py` vergleichen. Auffällige Zeilen umformulieren (nicht nur neu würfeln) und neu einsprechen.
6. **episode.py** schreiben (Vorlage `videos/001-al-capone/episode.py`): pro Panel `fx`, `ov`, `sfx`, `drift`, ggf. `rain=True`; `CHAPTERS = {erste_zeile: ("KAPITEL 1", "TITEL", musik_nr)}`; `PRE` (Atempausen vor Enthüllungen); `TITLE_AFTER`, `TITLE_LINES`, `TWIST`, `N_PANELS`, `FIRST_CHAPTER_LABEL`.
   Ziel: 6–10 Datengrafiken (Zähler, Karte, Balken), Stempel bei Enthüllungen, Bewegung in jedem Panel.
7. **Standbilder prüfen**: `EPISODE=videos/NNN-slug python3 engine/render.py stills 30 120 250 …` → `$WORK/stills/`.
8. **Rendern** (ca. 12 Min. für 8 Min. Video, im Hintergrund): `python3 engine/render.py $WORK/final_raw.mp4 videos/NNN-slug`
   Danach Upload-Kopie: `ffmpeg -i final_raw.mp4 -c:v libx264 -preset veryfast -crf 26 -maxrate 5M -bufsize 10M -c:a copy final.mp4` (< 299 MB).
   Länge steht in der Ausgabe – **unter 8:00 nicht abgeben**, sondern Zeilen ergänzen.
9. **Thumbnail**: Hero-Motiv mit Higgsfield (linke 40 % dunkel/leer), dann `python3 engine/thumbnail.py hero.png "ZEILE 1" "ZEILE 2" thumbnail_A.jpg`. 2 Varianten.
10. **Endkontrolle**: `python3 engine/qa.py final.mp4 thumbnail_A.jpg videos/NNN-slug`, Spracherkennung am fertigen Ton (Stichproben), unabhängiger Faktencheck, Rechts-Check (siehe LESSONS).
11. **Übergabe an Laurin** (Nachtausgabe ist nicht mit vidIQ verbunden – Plan-Limit): Video + Thumbnail per SendUserFile, Titel/Beschreibung/Tags in Kopier-Kästen per SendUserMessage. Laurin lädt selbst in YouTube Studio hoch.

## Nur den Ton neu mischen
`AUDIO_ONLY=1 python3 engine/render.py neu.mp4 videos/NNN-slug` (nutzt `$WORK/full_v.mp4`). Regler: `MUSIC_GAIN` (Standard 1.15), `CH_BOOM` (Kapitel-Schlag, Standard 0.18).
