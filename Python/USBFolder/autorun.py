import time
import sys
import os

print("AUTORUN!")

os.chdir("C:\\")

print(os.getcwd())
try:
    while True:
        print(".............",end="\r")
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit()