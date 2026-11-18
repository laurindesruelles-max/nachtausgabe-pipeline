#!/bin/sh
# Einrichtung für einen Nachtausgabe-Lauf
set -e
pip install --break-system-packages -q faster-whisper opencv-python-headless pillow numpy 2>/dev/null || true
export HF_HUB_DISABLE_XET=1
python3 -c "import faster_whisper, cv2, PIL, numpy; print('Setup ok')"
mkdir -p "${WORK:-/home/claude/na-work}/img" "${WORK:-/home/claude/na-work}/vo" "${WORK:-/home/claude/na-work}/stills"
echo "Arbeitsordner: ${WORK:-/home/claude/na-work}"
