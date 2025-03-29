import random
import time
import sys
import os
try:
	import KNC
except ImportError:
	os.system('pip3.11 install KNC -qq && pip3.9 install KNC -qq')
colors = ['\033[2;31m', '\033[2;32m', '\033[1;33m']
for i in range(3):
    h = colors[i % len(colors)]
    time.sleep(0.2)
    print(h + 'DeCode BY - Ibn-Suleiman | 𝗩𝟭𝟮')
time.sleep(1)
os.system('clear')
print('\n\033[0mDeCode BY - Ibn-Suleiman | 𝗩𝟭𝟮')
repr = lambda *args: f"{args}"
stdout = type("Stdout", (), {"write": lambda self, text: sys.stdout.write(text), "flush": lambda self: sys.stdout.flush()})()