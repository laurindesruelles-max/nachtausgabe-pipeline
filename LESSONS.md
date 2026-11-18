# Laurins Regeln für Nachtausgabe (verbindlich)

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
