# Endkontrolle 003 – Der Juwelenraub im Grünen Gewölbe (27.11.2026)

| Prüfung | Wert | OK |
|---|---|---|
| Länge über 8:00 | 9:58 | ✅ (etwas über Ziel 9:30) |
| Auflösung 1920x1080 | 1920x1080 | ✅ |
| Lautheit | −15,3 LUFS, True Peak −2,2 dBTP (nach AAC) | ✅ |
| Musik unter Stimme | 16,9 dB (Regel ≥ 16 dB) | ✅ |
| Datei (Upload-Kopie) | 232 MB | ✅ |
| Thumbnails A/B | 1280x720, 0,35 / 0,33 MB | ✅ |
| 2D-Motion-Clips | 10 (Zeilen 6, 13, 24, 42, 47, 49, 53, 62, 65, 68) | ✅ |
| Bild-Drehbuch | `engine/bilddrehbuch.py` → OK, 18,6 Ereignisse/Min (2 Warnungen: offene Fragen am Ende, gewollt) | ✅ |
| earshot critique (doku_profil) | **launch-grade, 0 major**, 20/23 (3 minor: wenig Sub-Bass, wenig „Luft“, Mitten leicht zurück) | ✅ |
| sk.py check | Exit 0, Sync 69 % der Schnitte mit Onset ±100 ms, Bildbogen `qa_sound/sheet.png` angesehen | ✅ |
| Spracherkennung (alle 72 Zeilen) | 4 Zeilen umformuliert + neu eingesprochen (7, 14, 28, 40: „kurz“, „Juwelen“, „Säulenfüße“) | ✅ |
| Spracherkennung fertiger Ton (3 Stichproben 1:00, 4:10, 8:40) | Stimme über Musik verständlich | ✅ |
| Gemini hört Vorschau (gemini-3-flash-preview) | 1. Durchlauf: Zähler-„Pling“, Karten-„Plopp“, Whoosh zu laut → entfernt/leiser; 2. Durchlauf 8/10; Titeltafel-Höhepunkt „stimmig, eher laut“ | ✅ |
| Sound-Casting Schlagzeile | newspaper-slap-01 (Freesound 67034, CC0) PREMIUM; book-drop-08 (Freesound 484904, CC0) PREMIUM; impact-slam-35 CHEAP | ✅ |
| Unabhängiger Faktencheck (Agent) | 3 MUSS (4:56→4:57, Fluchtauto „Mercedes“ unbelegt → „zweites Auto, als Taxi getarnt“, fehlende Stücke: Kollier-Teil statt Degenklinge) + 1 SOLL (Spitze abgetrennt) + Präzisierungen – alle eingearbeitet vor dem Einsprechen | ✅ |
| Quellen-Links | 8 Links vom Faktencheck-Agenten aufgerufen (HTTP 200) | ✅ |
| Rechts-Check | keine Logos (Panel 58 mit US-Flagge neu erzeugt), keine echten Fotos, keine Gewalt (Axt nur auf Vitrine), keine Vornamen, Freispruch neutral, Urteil rechtskräftig (BGH 5 StR 125/24), „Anwaltskanzlei“ als Medienbericht, Insider als Vermutung, KI-Hinweis in Beschreibung | ✅ |

## Hook-Prüfung
- Thema klar: Sekunde 1–5 (Satz „Das Grüne Gewölbe in Dresden…“ + Erzählkästchen Ort/Datum) ✅
- Offene Frage: „Doch wer waren die Männer? Und wo ist die Beute geblieben?“ ≈ 0:50 (Laurins Ziel ≤ 15 s verfehlt – Eskalationstreppe davor 3 Stufen) ⚠️
- Versprechen: ja („wie der Coup ablief, wie die Täter gefasst wurden und welcher Diamant bis heute fehlt“)
- Hook-Länge bis „… heutigen Nachtausgabe“: ≈ 83 s (Ziel 60–75 s) ⚠️

## Master (neu in render.py, 27.11.2026)
`MASTER_LINEAR=1 MASTER_I=15 MASTER_LIM=0.58 DUCK=0.68 SWELL=1.6 TITLE_GAIN=6 TITLE_BOOM=0.6`: Messung + linearer loudnorm statt dynamischem Einmal-loudnorm, Titeltafel als lautester Moment (earshot „loudest 3 s“ 3,0 LU), Limiter so tief, dass nach AAC kein Clipping.
