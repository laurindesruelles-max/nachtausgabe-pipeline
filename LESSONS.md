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
