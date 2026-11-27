# Laurins Regeln für Nachtausgabe (verbindlich)

> **Seit 20.11.2026 zuerst lesen:** `HANDWERK.md` (Regeln für alle Kanäle) und `EFFEKTE.md` (Handschrift und erlaubte Effekte dieses Kanals, von Laurin abgenommen). Bei Widerspruch gelten diese beiden Dateien.


## Kanal
- Deutsch, Kriminalfälle **aus aller Welt** – Mord, Mafia/organisierte Kriminalität, Coups, Betrug, Ungelöstes.
- Darf Goldsmith (englisch, dunkle 2,5D-Ermittlungsakte, Pinnwand, Polaroids, Miniatur-Dioramen) **optisch nicht ähneln**.
- Look: **Comic-Noir** (Graphic Novel), nur Schwarz/Papierweiß/Bernstein. Laurin: „sieht richtig krass aus“.

## Stimme
- **Immer ElevenLabs v4** (`elevenlabs_v4`), Stimme **Sterling** (`dc382508-c8bd-443c-8cb2-46e57b8d2e6f`), stability 0.5.
- Jahreszahlen/Daten/Zahlen **ausschreiben** – sonst falsche Aussprache (Laurin hat das bemängelt).
- Wörter, die Sterling falsch spricht (gefunden per Spracherkennung): „Razzia“, „Also“ am Satzanfang (klingt englisch), „Wärter“, „Prozesstag“, „Rivale“, „Polizeiuniformen“ → umformulieren („Kontrolle der Polizei“, „Deshalb“, „das Personal“, „Tag des Prozesses“, „Gegner“, „Uniformen der Polizei“).
- Jede Zeile mit `engine/asr.py` prüfen.

## Musik (Laurin 18.11.2026)
- **Noir-Jazz** (gedämpfte Trompete, Kontrabass, Besen) – gewählt aus drei Proben. Feste Bibliothek in `assets/music`, **keine neue Musik erzeugen**.
- Musik muss **gut hörbar** sein und **durchgehend Spannung halten**: **keine Musikpausen/Stopps**, Kapitel werden überblendet.
- Vor Enthüllungen (Stempel, Kapitelkarten) schwillt die Musik an; unter der Stimme leicht leiser (Ducking), in Pausen voller. Leise Stellen der Stücke werden automatisch angehoben. Das macht `render.py` – Regler nicht absenken.
- Kapitelkarten-Schlag **leise** (CH_BOOM 0.18).

## Geräusche
- Nur zu dem, was im Bild passiert; kein Dauer-Rauschteppich (Regen nur, wo es im Panel regnet).
- Nie selbst synthetisieren, nicht mit Higgsfield erzeugen. Quelle: Hugging Face `flreey/sfxmint-cc0-sound-effects` (Ordner `sample/`, CC0) → in `assets/sfx` ablegen und in `SOUNDS.md` eintragen.

## Video
- **Immer über 8 Minuten** (Ziel 8:15–9:30). Kapitel mit Kapitelkarten, Einstieg mit Titeltafel.
- Ein Satz = ein Panel, nie ein Bild doppelt. Sichtbare Bewegung in jedem Panel (Effekte), 6–10 Datengrafiken, Stempel bei Enthüllungen, Atempausen vor Enthüllungen.
- Ende: konkrete Kommentar-Frage + „Abonniere den Kanal und aktiviere die Glocke. Bis zur nächsten Nacht.“
- Thumbnail: **ein** großes Motiv + **2 Zeilen** Text, dunkel/dramatisch, Thema als Text, nie Logos. Titel neugierig statt beschreibend.

## Fakten & Recht
- Primärquellen, Quellenliste in die Beschreibung, Links vorher aufrufen und prüfen.
- Schätzungen als Schätzung kennzeichnen. Unbestätigtes weglassen.
- Keine Gewaltdarstellung, keine echten Fotos von Personen, keine Logos/Marken. Lebende Personen und laufende Verfahren: Unschuldsvermutung, nur Belegtes (Äußerungsrecht).
- In der Beschreibung KI-Hinweis; in YouTube „Veränderte oder synthetische Inhalte: Ja“.

## Upload
- Nachtausgabe ist **nicht mit vidIQ verbunden** (vidIQ-Plan-Limit, Stand 18.11.2026). Laurin lädt selbst hoch.
- Er braucht jedes Mal: **Video, Thumbnail, Titel, Beschreibung** (+ Tags, Einstellungen) – Texte als Kopier-Kästen im Chat.
- Falls Nachtausgabe später in `vidiq_social_account_list` mit canPublish true auftaucht: Upload wie bei Goldsmith (Higgsfield media_upload → vidiq_video_upload/upload_image → draft_create → erst nach Laurins „ja“ publish).

## Kosten
- Pro Video ca. 40–50 Higgsfield-Credits (65 Panels × 0,25 + ~70 Sprachzeilen + 2 Thumbnail-Motive). Keine KI-Videoclips, keine neue Musik.

## Video-Log
| Nr | Datum | Titel | Länge | Credits |
|---|---|---|---|---|
| 001 | 18.11.2026 | Der mächtigste Gangster Amerikas – gestürzt von einem Buchhalter | 8:10 | ~110 (inkl. einmalig Musikbibliothek) |
| 002 | 21.11.2026 | Der perfekte Raub, der zur tödlichen Falle wurde (Lufthansa-Raub 1978) | 8:56 | ~100 (Bilder 0,75 statt 0,25!) |
| 003 | 27.11.2026 | Vier Minuten, 113 Millionen: Der Coup im Grünen Gewölbe (Upload So 29.11., 20:00) | 9:58 | ~100 (64 Bilder à 0,75 + 76 Sprachzeilen) |

## Ton & Musik mit audiokit (Laurin 18.11.2026)
Problem: Soundeffekte oft unpassend/billig, Musik zu gleichförmig – Laurin schaut die eigenen Videos nicht zu Ende. vidIQ-Auswertung 18.11.: größter Absprung in den ersten ~30 s; Musik läuft 1,5–3 Min. gleich durch, kein Spannungsaufbau vor Enthüllungen; Passagen von 25–60 s ohne neuen Reiz.
- `setup.sh` lädt audiokit (Repo sound-mediathek) nach /home/claude/audiokit. Die Engine nutzt es automatisch und schreibt `ton_bericht.txt` – Bericht in qa.md übernehmen.
- Sounds werden vor dem Mischen aufgeräumt: gleiche Lautheit, Einblendungs-Sounds nicht im Dauerfeuer, max. 2 Sounds gleichzeitig, keine Endlos-Schleifen, defekte Dateien fliegen raus. Geräusche zu sichtbarer Bewegung bleiben.
- Musik nach Spannungskurve: Wechsel der Stelle/des Tracks spätestens alle ~60–80 s, Anschwellen vor Enthüllungen/Zahlen, Bogen pro Kapitel, Pegel automatisch unter der Stimme. Weiterhin nur die eigene Musik-Bibliothek, keine neuen Tracks.
- Im Skript Enthüllungen klar formulieren (Zahl, „aber“, „doch“, Frage → Antwort): daraus baut die Spannungskurve.
- Bericht meldet Lücken > 22 s ohne neuen Reiz → dort Bild/Effekt/Schnitt ergänzen, bevor gerendert wird.

## Hook-Regeln (Laurin 19.11.2026 – gilt ab dem nächsten Video)
Grundlage: Auswertung erfolgreicher Ausreißer-Videos in allen 5 Nischen (vidIQ), Hook-Studie mit über 4.000 Hooks aus Videos mit über 1 Mio. Aufrufen, Aprilynne Alters Intro-Formel. Es gibt keinen einzelnen besten Hook-Typ – aber alle erfolgreichen Hooks haben diesen Aufbau:
1. **Thema in 0–5 s gesagt UND gezeigt** – genau das, was Titel und Thumbnail versprechen; das Thumbnail-Motiv ist im ersten Bild zu sehen. Kein Datum, kein Logo, keine Vorrede als erster Satz.
2. **Offene Frage / Rätsel spätestens bei 10–15 s.** Die Antwort kommt frühestens im letzten Drittel.
3. **Konkretes Versprechen vor Hook-Ende** (was man am Ende weiß, wie viele Punkte, wer dahintersteckt).
4. **Bestes Material zuerst:** die stärkste Animation / das stärkste Bild gehört in den Hook.
5. **Kurz:** Hook-Länge siehe Kanal-Regel unten. Kontext erst danach, nicht vorne stapeln.
6. **Rehook:** Jedes Kapitel endet mit einer neuen offenen Frage.

**Prüfung vor dem Rendern** (in qa.md eintragen): Sekunde, ab der das Thema klar ist (≤ 5), Sekunde der offenen Frage (≤ 15), Versprechen ja/nein, Hook-Länge (Wörter ÷ 2,4 = Sekunden).
**Nach 48 h:** Retention bei 30 s per vidIQ (audience_retention) ins Video-Log. Ziel ≥ 70 %. Unter 50 % → beim nächsten Video den Alternativ-Typ unten nehmen.
**Nachtausgabe-Hook:** **Szene mitten im Geschehen** bleibt (Capone-Einstieg passt). Ergänzung: Name/Fall aus dem Titel in den ersten 5 s im Bild, mindestens zwei offene Fragen („Wer war es wirklich?“), ein Versprechen („Die Wahrheit ist schlimmer, als Chicago glaubte.“). True Crime verträgt etwas mehr: **bis „… das ist die Geschichte der heutigen Nachtausgabe.“ höchstens 60–75 s.**

## Sound-Bibliothek aus Laurins Sammlung (19.11.2026)
- setup.sh lädt `bibliothek/nachtausgabe/` (NUR die Effekte dieses Kanals) + `bibliothek/gemeinsam/` (Foley, Atmos, Waffen) nach /home/claude/sfx-bibliothek/bibliothek. Liste: `bibliothek/nachtausgabe/LISTE.md` im Repo sound-mediathek.
- **Reihenfolge bei der Sound-Wahl:** 1. eigene assets/sfx (abgenommen) → 2. Bibliothek (`import bibliothek as BIB; BIB.pick("nachtausgabe", "whoosh", seed=<video-ordner>)`, `BIB.suche("auto")`) → 3. Hugging Face/SFXMint nur, wenn nichts passt.
- `seed` = Video-Ordner: so wechseln die Sounds von Video zu Video, ohne dass es zufällig klingt. Alle Bibliotheks-Sounds sind geprüft (audit.py), Memes/geschützte/kommerzielle Sounds sind aussortiert.
- Nie Effekte aus fremden Kanal-Ordnern nehmen; `reserve/` nur nach Rückfrage bei Laurin.

## Erkenntnisse aus 002 (21.11.2026)
- Neue Effekte (Extrablatt, Schlagzeile, Fahndungsplakat, Taschenlampe, Panel zerbricht, Zeitsprung-Uhr, Seite umblättern) sind jetzt fest in `engine/engine.py` + `render.py` (Kurzschreibweisen HL, WA, CL, TL, SH). Extrablatt ersetzt die Kapitelkarte automatisch (`CH_PAUSE = 3.0`).
- Fahndungsplakat nur mit passender Überschrift (z. B. „VERMISST“, „DER TIPPGEBER“) – „GESUCHT“ nur, wenn die Person wirklich gesucht wurde.
- Sterling spricht „Burke“ am Satzanfang falsch → „Jimmy Burke …“.
- Hook wird schnell zu lang: 15 Zeilen = 95 s. Mit 10 Zeilen ~74 s. Frage früher stellen (≤ 15 s).
- Higgsfield: max. 8 gleichzeitige Jobs – Stimm-Batches nacheinander abschicken und abwarten.
- Upload-Kopie: `-maxrate 4M -bufsize 8M` (5M ergibt bei 9 Min. über 299 MB). Höhen-EQ vor AAC erhöht True Peak nach dem Kodieren um ~1,5 dB → Limiter auf −3,5 dB.
- **Kosten (21.11.2026):** GPT Image 2.6 kostet jetzt 0,75 Credits pro Bild (README sagt 0,25), Eleven v4 0,23–1,15 pro Zeile. 71 Panels + 2 Heros + 80 Sprachzeilen ≈ 100 Credits – über der 45er-Grenze aus HANDWERK.md. Laurin entscheiden lassen: billigeres Bildmodell oder weniger Panels.

## Erzähl-Bausteine nach Wissenswert-Vorbild (Laurin 22.11.2026, gilt ab dem nächsten Video)
Referenz: Wissenswert „Wie eine Spionin den größten CEO der Welt ruinierte“ (Spionage-/Affären-Fall, 372 Tsd. Aufrufe in 2 Tagen). Nur die Erzählweise übernehmen – **keine echten Clips** (würden den Comic-Noir-Look brechen).
- **Kaltstart als Szene mit Datum + Ort** als Schlagzeile/Panel („6. JUNI 2024 – TAIPEH“), ein konkreter Moment (Foto, Begegnung, Nachricht) als Anker.
- **Eskalationstreppe im Hook:** 3–4 Stufen, jede größer; danach 3-teiliges Versprechen („wie …, wie …, warum …“). Frage spätestens bei 15 s.
- **Doppelleben/zwei Welten:** wo der Fall es hergibt, Split-Panel „öffentlich vs. heimlich“.
- **Anker-Panel als Rahmen:** Das Panel vom Anfang kommt am Ende verändert zurück.
- **Belegte Fun-Facts** alle 2–3 Min. als Zeitungsausschnitt-Panel.
- **Schluss:** offene Frage/3 Deutungen des Falls + Kommentar-Frage.

- **2D-Motion-Graphics (23.11.2026):** Laurin will das Handwerk der ANOM-Stilprobe (viel 2D-Animation, Bildwechsel alle 2–4 s) in jedem Kanal – als Erweiterung im eigenen Stil, nichts überschreiben; Unterschied nicht nur in Farben, sondern auch in Symbolen und Formen. Bisheriges (echte Fakten mit Quelle, Effekt-Katalog, Sounds) bleibt.

## Erkenntnisse aus 003 (27.11.2026)
- **2D-Motion-Clips sind jetzt in `render.py` eingebaut:** `MOTION = {zeile: (baustein, props)}` in episode.py. Diese Zeilen brauchen kein KI-Panel (spart Credits), im Seitenstreifen steht das Schlussbild des Clips, der Clip blendet über das Panel. Am Kapitelstart beginnt der Clip erst nach dem Extrablatt. 10 Clips rendern ≈ 20 Min. (Remotion) – vorher Schriften installieren: `cp assets/fonts/*.ttf ~/.fonts && fc-cache -f`, sonst Serifen-Ersatzschrift.
- **Schlagzeilen-Sound neu:** `newspaper-slap-01` (Freesound 67034, CC0) im Gemini-Casting PREMIUM, `impact-slam-35` CHEAP. Steht als `HEADLINE_SFX` in episode.py. Auch PREMIUM: `book-drop-08` (Freesound 484904, CC0).
- **Gemini bei Motion-Sounds:** Zähler-Tick (`clock_tick`) und Karten-Pin-Klopfen (`door-knock-01`) klangen nach „Arcade/Plopp“ → render.py lässt sie bei Motion-Clips weg.
- **Whoosh nur noch bei echtem Bildwechsel** (Laurin 24.11.): render.py setzt keinen Whoosh mehr bei jeder Panel-Fahrt (nur mit `PANEL_WHOOSH=1`), mindestens 6 s Abstand.
- **Musik unter Sprache ≥ 16 dB:** `DUCK = 0.68` → 16,9 dB.
- **Master:** dynamisches Einmal-loudnorm drückte „loudest 3 s“ auf 2,8 LU (earshot major). Neu: `MASTER_LINEAR=1` (Messung + linear) und `TITLE_GAIN` (Titeltafel als Höhepunkt). Limiter `MASTER_LIM=0.58`, sonst Clipping nach AAC (flache Limiter-Spitzen → +4 dB True Peak beim Dekodieren). Ergebnis launch-grade, 0 major.
- **Faktencheck vor dem Einsprechen hat sich gelohnt:** 4:56 (nur Wikipedia) → 4:57 laut Anklage; Fluchtauto-Marke „Mercedes“ unbelegt; die Degenklinge ist ein Schaden, kein fehlendes Stück.
- Higgsfield markierte „surveillance camera“-Prompts zweimal als NSFW → umschreiben („tiny amber indicator light“). Deutsche Gerichte: keine Hämmer, keine Flaggen im Prompt (Panel kam mit US-Flagge).
- Sterling spricht „kurz“ am Satzanfang wie „Kürbs/Kürzt“ → „Wenige Minuten vor …“, „Wenig später …“.
- Video wurde 9:58 lang (Ziel 9:30): 72 Zeilen mit ~1.050 Wörtern sind die Obergrenze; Hook 83 s statt ≤ 75 s – beim nächsten Mal 8 statt 10 Hook-Zeilen.
- **Kosten bleiben ~100 Credits** (Bilder 0,75). Für 40–50 Credits müsste Laurin entscheiden: weniger Panels (mehr Motion-Clips statt Bildern) oder ein billigeres Bildmodell.
