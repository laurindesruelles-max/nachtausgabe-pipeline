# Endkontrolle

| Prüfung | Wert | OK |
|---|---|---|
| Länge über 8:00 | 8:56 | ✅ |
| Auflösung 1920x1080 | 1920x1080 | ✅ |
| Lautheit -15 bis -13 LUFS | -14.3 | ✅ |
| Datei unter 299 MB (Upload) | 225 MB | ✅ |
| Thumbnail 1280x720, unter 2 MB | 1280x720, 0.36 MB | ✅ |

Weitere Pflichtpunkte (von Hand eintragen): Spracherkennung aller Zeilen, unabhängiger Faktencheck, Rechts-Check.

## Hook-Prüfung
| Punkt | Wert |
|---|---|
| Thema klar (Name im Bild + gesagt) | 0–5 s ✅ („Der Lufthansa-Raub“, Erzählkasten) |
| Erste offene Frage | ~25 s („Wohin ist dieses Geld verschwunden?“) – Ziel ≤ 15 s knapp verfehlt |
| Versprechen | ja („Am Ende dieser Nacht weißt du, warum …“) |
| Hook-Länge bis „… heutigen Nachtausgabe“ | 74 s ✅ (≤ 75 s) |

## Spracherkennung
- Alle 71 Zeilen per faster-whisper geprüft: Ø 97 % Übereinstimmung (Zahlen als Ziffern nicht gezählt).
- „Burke“ am Satzanfang wurde als „Virg/Burg“ erkannt → umformuliert zu „Jimmy Burke …“ und neu eingesprochen (Zeilen 21, 53).
- Stichproben im fertigen Ton (0:20, 4:20, 7:50): Stimme über Musik einwandfrei verständlich.

## Faktencheck (unabhängiger Agent)
- Kein harter Fehler. Alle 5 SOLLTE-Punkte eingearbeitet: „laut Hill“ bei Burke/DeSimone, gestohlene (nicht falsche) Nummernschilder, College-Basketball-Manipulation, „der allergrößte Teil wurde nie gefunden“ statt „nichts“, Gruenewald als Mitwisser.
- Quellen-Links: 6 von 7 vom Prüf-Agenten geladen (HTTP 200); Wikipedia „Vincent Asaro“ vom Recherche-Agenten geladen.

## Rechts-Check
- Keine Logos, keine echten Fotos (alle Personen gezeichnet), keine Gewaltdarstellung (keine Leichen, kein Blut; ein Panel mit Waffe im Hintergrund wurde ersetzt).
- Kein Täter für die Morde wird benannt; Asaro mit Freispruch genannt (verstorben 2023); Werner rechtskräftig verurteilt.
- KI-Hinweis in der Beschreibung.

## Ton (doku-ohren)
- earshot critique (Profil fern/Simplicissimus/Netflix): **launch-grade, 20/23, 0 critical, 0 major**. Erster Mix hatte 1 major (lauteste 3 s nur 2,9 LU über Schnitt) → zwei Enthüllungen (REKORD-RAUB, FINGERABDRÜCKE) +2–2,6 dB, leichte Bass-/Höhenanhebung, Limiter −3,5 dB. Rest: 3 minor (wenig Sub-Bass, wenig Luft – liegt an den Musikstücken).
- sk.py check: −14,2 LUFS, True Peak −2,2 dBTP, Exit 0. sheet.png angesehen.
- Gemini-Hörprobe NICHT gemacht: kein Gemini-Schlüssel im unbeaufsichtigten Lauf (Schlüssel nur von Laurin zur Laufzeit).
- Sounds nur aus dem abgenommenen Kit (EFFEKTE.md „Sound je Effekt“) + Bibliothek: machine_engine, glass_shatter_01, clock_tick neu nach assets/sfx übernommen (CC0).
