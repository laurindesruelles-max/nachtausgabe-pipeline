# Nachtausgabe – Handschrift und Effekte (von Laurin abgenommen am 20.11.2026)

Gemeinsame Regeln: `HANDWERK.md`. Hier steht nur, was Nachtausgabe von den anderen Kanälen unterscheidet.

## Erkennungsmerkmale
| | Nachtausgabe |
| --- | --- |
| Sprache | Deutsch |
| Welt | Comicseite. Das ganze Video spielt auf den Seiten |
| Technik | 2D-Panels mit Parallax-Ebenen und Partikeln (`engine/engine.py`) |
| Farben | Schwarz, Papierweiß, Bernstein |
| Kamera | **bleibt auf der Comicseite** wie im Pilot: Rahmen und Nachbar-Panels sind zu sehen, die Kamera springt von Panel zu Panel. Bildfüllend nur Extrablatt und Seitenwechsel (Laurin, 20.11.: „die Mitte“ aus Pilot und Stilprobe) |
| Panel-Inhalt | **Jedes Panel zeigt die ganze Szene** (Straße, Raum, Personen) wie im Pilot, keine Gesichter in Großaufnahme als Normalfall (Laurin, 20.11.) |
| Tempo | ein Satz = ein Panel |
| Schrift | Comic-Kästen (Comic Neue), Sprechblasen, Bangers |
| Übergang | Seite umblättern (gehört nur Nachtausgabe) |
| Zahlen und Karten | Zeitungsgrafik im Comic-Stil, Comic-Stadtplan |
| Musik | Noir-Jazz, durchgehend, ohne Pausen, schwillt vor Enthüllungen an |
| Stimme | Sterling |

## Effekt-Katalog (nur diese verwenden)
| Effekt | Was passiert | Wann | Status |
| --- | --- | --- | --- |
| Panel-Fahrt | Die Kamera springt von Panel zu Panel, jedes Panel hat Tiefe | durchgehend | steht |
| Regen, Schnee, Rauch | Wetter und Rauch bewegen sich im Panel | nur wo die Szene es verlangt, Regen ist kein Standard (Laurin 20.11.2026) | steht |
| Flackernde Lampe | Laterne oder Neonschild flackert | Nacht, Spannung | steht |
| Blitzlicht | Ein Kamerablitz der Polizei friert das Panel ein | Tatort, Verhaftung | steht |
| Extrablatt | Titelseite rotiert aus der Druckerpresse, die Schlagzeile ist der Kapiteltitel | Kapitelstart | neu, ersetzt die Kapitelkarte, Stilprobe 20.11. |
| Schlagzeile knallt | Ein fetter Zeitungsbalken schlägt ins Bild, die Kamera ruckt | Enthüllung | neu, **ersetzt den Stempel** (Stempel gehört Goldsmith) |
| Fahndungsplakat | Die Person erscheint als „GESUCHT“-Plakat mit Namen und Jahr | neue Person | neu, Stilprobe 20.11. |
| Taschenlampe | Ein Lichtkegel tastet das dunkle Panel ab und findet das Detail | Spur, Geheimnis | neu, Stilprobe 20.11. |
| Panel zerbricht | Der Rahmen reißt, das nächste Bild bricht durch | Wendung | neu, Stilprobe 20.11. |
| Zeitsprung-Uhr | Eine Uhr dreht sich vor oder zurück, das Jahr zählt mit | Rückblende | neu, Stilprobe 20.11. |
| Sprechblase | Echte Zitate als Sprechblase | belegtes Zitat | steht |
| Erzählkästchen | Comic-Kastentexte mit Ort und Datum | Ort, Zeit | steht |
| Comic-Stadtplan | Route in Bernstein auf einem gezeichneten Stadtplan | Fluchtweg, Tatorte | steht |
| Zeitungsgrafik | Zahl und Balken im Stil einer alten Zeitung | harte Zahl | steht, Stil anpassen |
| Seite umblättern | Die Comicseite schlägt um | großer Übergang | neu, Stilprobe 20.11. |

**Raus:** der Stempel bei Enthüllungen (ab jetzt Schlagzeile).

Stilproben: `stilprobe_nachtausgabe.mp4` (bildfüllend) und `stilprobe_nachtausgabe_mitte.mp4` (gewählte Richtung), beide vom 20.11.2026. Sounds folgen nach dem Casting (`doku-ohren`).

## Sound je Effekt (Stand 20.11.2026, von Laurin abgenommen („war gut“, 20.11.2026))
Geplant nach dem Grundsatz aus `HANDWERK.md`: erst festlegen, wo überhaupt ein Sound hingehört, dann je Stelle genau einen. Skripte: `engine/stilproben/ton_*.py`.

| Effekt | Sound |
| --- | --- |
| Extrablatt | Druckmaschine (machine_engine, Bibliothek) leise + Whoosh + Umblättern + leiser cinematic-boom |
| Fahndungsplakat | paper-fabric-card-flip-06 + reveal-impact-01 |
| Taschenlampe | lighter-flick-01, Fund: scroll-unroll-01 |
| Panel zerbricht | glass-clink-01 (Riss) + glass_shatter_01 (Bibliothek), danach Regen nur im Regen-Panel |
| Zeitsprung-Uhr | clock_tick |
| Schlagzeile knallt | impact-slam-35 + reveal-impact-01 + cinematic-boom-01, Musik schwillt davor an |
| Seite umblättern | paper-fabric-card-flip-06 |
| Panel-Fahrt | short-video-whoosh-01 sehr leise |
| Musik | noir_3_jagd ab 0:30 (Anfang zu leise), durchgehend, Anschwellen vor Enthüllungen |
