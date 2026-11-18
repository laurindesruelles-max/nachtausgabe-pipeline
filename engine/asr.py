"""Aussprache-Kontrolle: python3 engine/asr.py WORK/vo/s01.mp3 ...  (gibt erkannten Text aus; mit dem Skript vergleichen)"""
import os; os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    raw = subprocess.run(["ffmpeg","-v","error","-i",f,"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
    a = np.frombuffer(raw, np.float32)
    segs, _ = m.transcribe(a, language="de", beam_size=5)
    print(f, "|", " ".join(s.text.strip() for s in segs), flush=True)
