import sys, subprocess, re
# Aufruf: get.py <ordner> <prefix> idx=url idx=url ...
d, pre = sys.argv[1], sys.argv[2]
for a in sys.argv[3:]:
    i, u = a.split("=", 1)
    ext = u.rsplit(".", 1)[1]
    subprocess.run(["curl", "-sS", "-o", f"{d}/{pre}{int(i):02d}.{ext}", u], check=True)
print("ok", len(sys.argv) - 3)
