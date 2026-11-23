#!/bin/sh
# Einrichtung für einen Nachtausgabe-Lauf
set -e
pip install --break-system-packages -q faster-whisper opencv-python-headless pillow numpy 2>/dev/null || true
export HF_HUB_DISABLE_XET=1
python3 -c "import faster_whisper, cv2, PIL, numpy; print('Setup ok')"
mkdir -p "${WORK:-/home/claude/na-work}/img" "${WORK:-/home/claude/na-work}/vo" "${WORK:-/home/claude/na-work}/stills"
# Ton-Werkzeug audiokit (18.11.2026): Sounds aufräumen, Musik nach Spannungskurve, Endkontrolle.
# Gemeinsam sind nur die Regeln – Sounds und Musik bleiben kanal-eigen. Repo: laurindesruelles-max/sound-mediathek
AK="${AUDIOKIT:-/home/claude/audiokit}"
if [ ! -f "$AK/adapter.py" ] || [ -n "$AK_UPDATE" ]; then
  AKT=$(mktemp -d); git clone -q --depth 1 --filter=blob:none --sparse https://github.com/laurindesruelles-max/sound-mediathek "$AKT/r" && git -C "$AKT/r" sparse-checkout set audiokit && mkdir -p "$AK" && cp "$AKT"/r/audiokit/*.py "$AKT"/r/audiokit/*.json "$AK"/ && echo "audiokit bereit: $AK"; rm -rf "$AKT"
fi
# Laurins Sound-Bibliothek (19.11.2026): eigene Effekte dieses Kanals + gemeinsame Geräusche -> /home/claude/sfx-bibliothek/bibliothek
python3 -c "import sys; sys.path.insert(0, '$AK'); import bibliothek; print('Sound-Bibliothek bereit:', bibliothek.ensure('nachtausgabe'))" || echo "WARNUNG: Sound-Bibliothek nicht geladen"
echo "Arbeitsordner: ${WORK:-/home/claude/na-work}"

# 2D-Motion-Graphics (Remotion): Node-Pakete einmal installieren
[ -d "$(dirname "$0")/engine/motion/node_modules" ] || (cd "$(dirname "$0")/engine/motion" && npm install --silent >/dev/null 2>&1 && echo "motion bereit")
