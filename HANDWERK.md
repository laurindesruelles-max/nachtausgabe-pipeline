# Handwerk – gilt für alle Kanäle (Laurin, 20.11.2026)

Alle fünf Kanäle (Goldsmith, Meisterwerk, Unterbau, Denkmuster, Nachtausgabe) folgen denselben Qualitätsregeln. Wie jeder Kanal aussieht und klingt, steht in seiner eigenen `EFFEKTE.md`. Eine Einheits-Engine gibt es nicht.
Messlatte: fern, Simplicissimus, große Netflix-Dokus. **Ziel: mindestens 60 % durchschnittliche Wiedergabedauer.**
Quelle: Claude-Doc „Kanal-Handschriften“ https://claude.ai/artifact/UGsg2WZKdDs1vB93mWaGTZ

## Skript
- **Du-Bezug, wo er trägt:** Der Zuschauer soll merken, was das Thema mit ihm zu tun hat. Ein Video muss aber nicht beim Zuschauer starten (Laurin, 20.11.2026).
- **Spannungslinie ab Minute 1:** eine offene Frage oder ein Countdown. Die Auflösung kommt erst spät.
- **Höchstens eine harte Zahl alle ~20 s.** Ein Beispiel wird ausführlich als Szene erzählt, statt vieles aufzuzählen.
- **2–3 echte Wendungen** pro Video, der Satzrhythmus wechselt.
- **Hook: für alle Kanäle dieselbe Messlatte, nämlich der stärkste Hook.** Die Hook-Art muss sich je Kanal nicht unterscheiden. Die Kanäle unterscheiden sich durch Nische und Darstellung. Gemeinsam ist das Ziel: jedes Video klingt sehr gut, bleibt über die ganze Länge spannend und wird gern geschaut (Laurin, 20.11.2026). Bewährte Hook-Mittel: Kaltstart mitten in der stärksten Szene, offene Frage oder Neugier-Lücke, Konflikt oder Verlust, Geheimnis oder Insiderwissen, und das Versprechen, was der Zuschauer am Ende weiß. Ein Hook muss in den ersten 5 Sekunden klar sein, Bild, Satz und Ton sagen dasselbe. Die Ausreißer-Erkenntnisse in `LESSONS.md` bleiben als Ideen erhalten.
- **Unabhängiger Faktencheck** (Agent) vor dem Einsprechen.

## Bild
- **Durchgehend animiert:** Von der ersten bis zur letzten Sekunde bleibt der Zuschauer in der animierten Welt des Kanals. Fotos, Clips und Grafiken erscheinen nur innerhalb dieser Welt, nie als nacktes Standbild mit Zoom.
- **Jeder Absatz hat ein Bild-Ereignis.** Kein Bild steht länger als ~5 s ohne Eigenbewegung, geschnitten wird alle 3–5 s. Das sind mindestens 12 Bild-Ereignisse pro Minute, und das wird gemessen.
- **Nur Effekte aus `EFFEKTE.md` und `ANIMATION.md` des Kanals.** `ANIMATION.md` enthält alle für die Nische freigegebenen Animationsarten (Laurin, 21.11.2026: alles außer Higgsfield-Videoclips). Weitere Effekte erst nach Laurins Freigabe.
- **Wetter nicht als Standard** (Laurin, 20.11.2026): Regen, Schnee oder Nebel nur, wenn Geschichte oder Ort es verlangen, nicht in jedem Video und nicht als Dauer-Atmosphäre. Bewegung im Bild kommt aus Handlung, Licht, Fahrzeugen und Menschen.
- **Kein Bild kommt zweimal vor.** Günstige Bewegung: Blender, eigene Motion-Grafik, Pixabay. KI-Videoclips nur mit Laurins Freigabe.

## Bild-Drehbuch: Darstellung von Zeit und Geschehen (Laurin, 21.11.2026)
Jedes Skript bekommt **vor dem Einsprechen** ein Bild-Drehbuch (`videos/NNN-slug/bilddrehbuch.json`), das Satz für Satz festlegt, was im Bild passiert. Prüfung: `python3 engine/bilddrehbuch.py videos/NNN-slug/bilddrehbuch.json` – erst bei 0 Fehlern wird eingesprochen. Im Bild-Drehbuch stehen Jahre, Uhrzeiten und Zahlen als Ziffern (auch wenn das Sprech-Skript sie ausschreibt), damit die Prüfung sie erkennt. Ein Satz darf mehrere Einträge haben, wenn im selben Bild mehrere Ereignisse passieren. Welche Animationen der Kanal dafür hat, steht in seiner `ANIMATION.md` (alles außer Higgsfield-Videoclips ist erlaubt, Laurin 21.11.2026).

**Wie genau muss das Bild sein?** Je Satz eine Stufe wählen:
- **exakt** – das Bild zeigt genau das Gesagte: das Jahr, die Uhrzeit, den Ort, die Zahl, den einen Moment der Handlung. Pflicht bei jeder Jahreszahl, Uhrzeit, harten Zahl und bei jedem Wendepunkt. Ungenauigkeit an diesen Stellen kostet Vertrauen und damit Zuschauer.
- **schema** – das Bild zeigt den Ablauf vereinfacht (Kette, Diagramm, Explosionsansicht, Querschnitt). Pflicht bei Erklärungen: Wer nur Atmosphäre sieht, während etwas erklärt wird, steigt aus.
- **stimmung** – Atmosphäre ohne Informationsauftrag. Nur für Übergänge und Atempausen, höchstens jede fünfte Einstellung.

**Regeln, die Neugier und Spannung halten:**
1. **Zeigen, nicht nennen:** Das Bild zeigt den *Moment der Veränderung* (die Tür geht auf, das Licht erlischt, der Stahl reißt), nicht den Zustand danach.
2. **Zeit sichtbar machen:** Jeder Zeitsprung hat ein Bild-Signal (Uhr, Datum, Kalender, Tag/Nacht, Zeitraffer). Der Zuschauer weiß immer, *wann* er ist.
3. **Ort sichtbar machen:** Jeder Ortswechsel hat ein Bild-Signal (Karte, Flug, Ortsmarke). Der Zuschauer weiß immer, *wo* er ist.
4. **Neugier-Lücke im Bild:** Vor einer Auflösung wird das Entscheidende angedeutet, aber verdeckt gezeigt (abgedeckt, im Dunkeln, unscharf, halb gezeichnet). Aufgelöst wird frühestens 20 s später.
5. **Immer eine offene Frage:** Ab Sekunde 30 bis eine Minute vor Schluss ist immer mindestens eine Frage offen. Wird eine beantwortet, öffnet sich im selben Moment die nächste.
6. **Musterbruch:** In jedem 30-s-Fenster mindestens 3 verschiedene Animationsarten. Dieselbe Animation nie dreimal hintereinander.
7. **Maßstab wechseln:** Zwischen Totale und Detail springen (Welt → Gebäude → Hand → Mikrometer). Gleiche Bildgröße länger als 15 s wirkt wie Stillstand.
8. **Steigerung:** Die stärksten Animationen sitzen an den Wendepunkten und vor der Auflösung, nicht alle im Intro.
9. **Rückkehr zum Hook:** Am Ende jedes Kapitels kommt das Hook-Bild kurz verändert zurück und zeigt, wie nah wir der Antwort sind.

Nach der Veröffentlichung: Fällt die Retention-Kurve an einer Stelle ab, im Bild-Drehbuch nachsehen, welche Regel dort verletzt war, und das in `LESSONS.md` festhalten.

## Ton
- **Skill `doku-ohren` ist Pflicht:** Casting jedes Sounds, Effektspur, Endmix „launch-grade“ mit 0 major, Gemini hört die Vorschau.
- **Effekte nur aus dem abgenommenen Sound-Kit des Kanals** (`SOUNDS.md`). Geräusche nur passend zum Bild, kein Rauschen als Füller.
- **Musik:** 5–7 eigene Tracks je Kanal, erzeugt mit ElevenLabs Music über Higgsfield (keine anderen Higgsfield-Musikmodelle). Keine epische Musik. Die Musik baut gezielt Spannung auf, wie genau, legt der Kanal fest.
- **Sound-Plan vor dem Mischen** (Laurin, 20.11.2026): Erst festlegen, wo überhaupt ein Sound hingehört und wie viele es sind. Jeder Sound sitzt auf einem echten Bild-Ereignis, im Zweifel weniger. Vor großen Momenten setzt die Musik kurz aus (außer bei Nachtausgabe), die Enthüllung bekommt einen trockenen tiefen Treffer statt Funkel- oder Zaubertönen.
- **Musik atmet wie bei fern** (Laurin, 20.11.2026): Sie läuft nicht gleich laut durch.
  - Unter der Stimme ~9 dB leiser (Ducking), in Sprechpausen voller.
  - Vor Enthüllungen und Wendepunkten schwillt sie an (+4–6 dB über ~2,5 s).
  - Vor großen Sätzen kurz weg (0,5–1,5 s Stille), dann setzt sie mit dem Treffer wieder ein. Ausnahme Nachtausgabe: keine Pausen, nur Anschwellen.
  - Ein Track pro Kapitel, 2 s Überblendung, kein Track-Hopping.
  - Prüfung mit earshot: Musik in mindestens 60 % der 5-s-Fenster, die lautesten 3 s mindestens 3,5 LU über dem Durchschnitt.
  - Umsetzung je Engine: Unterbau `unterbau.py` (duck_db, swell, rests), Goldsmith `mix_full.py` (sidechain, beats), Nachtausgabe `render.py`, Denkmuster `kit.py`, Meisterwerk audiokit (`ak_music`). Stilproben: `engine/stilproben/mixer.py`.
- **Master:** −14 LUFS, True Peak −2 dB.

## Stimme
- **Nur ElevenLabs** (v4 oder v4 Turbo). Danach ASR-Abgleich mit dem Skript, Ziel > 94 %.

## Format und Recht
- **Länge über 8 Minuten.** Am Ende kommen eine Kommentar-Frage und der Glocken-Hinweis.
- **Quellen** stehen in der Beschreibung. Bilder, Musik und Clips nur mit Lizenz, die Monetarisierung erlaubt.
- **Hero-Thumbnail:** ein großes Motiv, das Thema steht im Bild, kein Leuchten hinter der Schrift. Neugierige Titel.

## Lernschleife und Freigabe
- **Nach 48 h** die Retention-Kurve über vidIQ prüfen: Wo fallen Zuschauer ab, und warum? Das Ergebnis kommt in die `LESSONS.md`.
- **Veröffentlicht wird nur nach Laurins „ja“.**
- **Kosten:** 35–45 Credits je Video, nie mehr als 45. Rhythmus: alle 4 Tage ein Video je Kanal.
