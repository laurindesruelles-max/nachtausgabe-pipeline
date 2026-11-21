# Nachtausgabe – Animations-Möglichkeiten (Laurin, 21.11.2026)

Ergänzt `EFFEKTE.md` (abgenommener Kern-Katalog) um alles, was zur Nische passt: True-Crime-Fälle aus aller Welt, Mafia und organisierte Kriminalität. Alles spielt weiter **auf der Comicseite** (Schwarz, Papierweiß, Bernstein), die Kamera bleibt auf der Seite, jedes Panel zeigt die ganze Szene. Exklusiv-Regeln bleiben: kein Stempel (Goldsmith – hier Schlagzeile), Seite umblättern gehört nur Nachtausgabe. Werbefreundlich: keine Gewalt im Detail, keine Opfer-Fotos. Für jedes Skript gilt das Bild-Drehbuch aus `HANDWERK.md`.

## Zeit und Geschehen in dieser Nische
- **Zeit:** True Crime lebt von der **minutengenauen Chronologie**. Jede belegte Uhrzeit steht im Erzählkästchen („14. Februar 1929, 10:30 Uhr“). Rückblenden immer mit Zeitsprung-Uhr, damit niemand die Reihenfolge verliert.
- **Ort:** Jeder Ortswechsel mit Comic-Stadtplan oder Erzählkästchen.
- **Geschehen:** Der Tathergang wird **exakt nach den Quellen** gezeigt, Panel für Panel in der richtigen Reihenfolge – Gewalt nur angedeutet (Schatten, Geräusch-Schrift, Schnitt auf Reaktion).
- **Unsicheres:** Was nicht belegt ist, wird als Vermutung erkennbar gezeichnet (gestrichelter Panelrahmen, „vermutlich“ im Kästchen).
- **Neugier-Lücke:** Täter als Silhouette, Beweisstück im Dunkeln (Taschenlampe), Panel mit Fragezeichen, das erst später gefüllt wird.

## Animations-Katalog (zusätzlich zu EFFEKTE.md)
| Animation | Was passiert | Wann | Genauigkeit | Werkzeug | Status |
| --- | --- | --- | --- | --- | --- |
| Tatzeit-Leiste | Am Seitenrand läuft eine Uhrzeit-Leiste mit, bei jedem Panel springt die Minute | Tathergang, Nacht der Tat | exakt | engine.py | bauen |
| Beweisstück | Ein Objekt liegt im Beweisbeutel mit Nummernschild, Kamera tastet es ab, Lupenkreis zeigt das Detail | Spur, Indiz | exakt | engine.py | bauen |
| Schatten an der Wand | Eine Silhouette wandert über die Panelwand, Person bleibt unerkannt | Täter unbekannt, Bedrohung | stimmung | engine.py (Parallax-Ebene) | bauen |
| Verfolgungsjagd | Auto/Person rast über mehrere Panels, Speedlines, Panelrahmen biegen sich | Flucht, Verfolgung | exakt (Route) | engine.py | bauen |
| Zwei Aussagen | Zwei Panels nebeneinander zeigen dieselbe Szene unterschiedlich, Sprechblasen widersprechen sich | widersprüchliche Zeugen | exakt (belegt) | engine.py | bauen |
| Mafia-Stammbaum | Comic-Porträts in Rahmen, Linien für Familie und Rang, Pfeil wer wen ersetzt | Clan, Hierarchie | exakt | engine.py (Layout per Manim) | bauen |
| Rasterpunkt-Zoom | Zoom in ein Panel bis die Comic-Rasterpunkte sichtbar werden, darin ein neues Detail | Detail entdecken | exakt | engine.py | bauen |
| Mikrofilm-Archiv | Ein Mikrofilm-Lesegerät scrollt durch alte Zeitungsseiten, stoppt bei der Meldung | Quelle aus der Zeit | exakt | engine.py + Quelle | bauen |
| Abgehörtes Telefonat | Telefon im Panel, eine Schallwelle läuft, das Zitat erscheint Wort für Wort in der Blase | Abhörprotokoll, Anruf | exakt (Zitat belegt) | engine.py | bauen |
| Geräusch-Schrift | Sparsame Comic-Lautmalerei (KNARR, KLICK, RING) springt ins Panel | Geräusch im Moment | exakt | engine.py | bauen (keine Schuss-/Gewaltlaute) |
| Gerichtsszene | Panel im Gerichtssaal, Urteil erscheint als Schlagzeile, Jahre zählen hoch | Urteil, Strafe | exakt | engine.py | bauen |
| Vermutungs-Panel | Gestrichelter Rahmen, entsättigtes Bernstein: so könnte es gewesen sein | nicht belegte Theorie | schema | engine.py | bauen |
| Leeres Panel | Ein Panel bleibt schwarz mit einem „?“, wird erst bei der Auflösung gefüllt | offene Frage über Kapitel | – | engine.py | bauen |
| Weltkarte im Comic | Comic-Globus dreht sich zum Land des Falls | neuer Fall, Land | exakt | engine.py | bauen (ergänzt Comic-Stadtplan) |

## Werkzeuge (alle ohne Credits, getestet 21.11.2026)
| Werkzeug | Wofür | Einrichten |
| --- | --- | --- |
| Blender (`bpy`) | echtes 3D, Physik (Rigid Body, Flüssigkeit, Stoff, Partikel), Geometry Nodes für Wachstum/Aufbau, Grease Pencil für gezeichnete Linien im Raum, Rigging für Figuren | `pip install bpy` (setup.sh) |
| 2,5D-Tiefe (`depth25d.py`, Depth Anything) | jedes Standbild in Ebenen zerlegen, Kamera fährt mit Tiefe hindurch, Ebenen bewegen sich einzeln | im Goldsmith-/Unterbau-Repo vorhanden |
| PIL + numpy + ffmpeg | eigene Motion-Grafik, Partikel, Licht, Übergänge, Compositing | vorhanden |
| Manim | exakte, animierte Diagramme, Netzwerke, Abläufe, Formeln, Zählwerke – danach im Kanal-Look eingefärbt | `apt-get install -y libpango1.0-dev libcairo2-dev && pip install manim` |
| rlottie | Lottie-Vektoranimationen (Icons, kleine Abläufe) als Vorlage, immer im Kanal-Stil nachgezeichnet | `pip install rlottie-python` |
| Pixabay, Wikimedia, Archive | echte Clips und Fotos, nur innerhalb der Kanal-Welt eingebaut (siehe HANDWERK.md) | `stock.py`, `sources.py` |
| Higgsfield | nur KI-**Bilder** (0,25 Credits), Freistellen, 3D-Modell aus Bild. **Keine KI-Videoclips** (Laurin 21.11.2026) | – |

Status in den Tabellen: **steht** = in der Engine vorhanden · **bauen** = freigegeben (Laurin 21.11.2026), beim ersten Einsatz als Baustein in die Engine aufnehmen und kurz Stilprobe an Laurin.
