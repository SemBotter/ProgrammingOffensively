import os
import sys
import subprocess
import threading
import queue
import time
import asyncio

class Installer(asyncio.SubprocessProtocol):
    def __init__(self):
        super(Installer, self).__init__()
        self.powershellpaths = [r"C:\Windows\System32\powershell.exe", r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"]

    async def bootemUp(self):        
        try:
            self.cmd = subprocess.Popen("pip install cryptography fernet requests", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable=self.powershellpaths[0])
        except FileNotFoundError:
            self.cmd = subprocess.Popen("pip install cryptography fernet requests", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable=self.powershellpaths[1])


async def installers() -> subprocess.Popen[bytes]:

    

    cmd = subprocess.Popen("pip install cryptography fernet requests", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)



    return cmd

    



    """
    os.system("pip install cryptography")
    os.system("pip install fernet")
    os.system("pip install requests")
    """

async def importio() -> bool:
    import os
    import sys

    os.chdir("C:\\")
    print(sys.exc_info())

    await asyncio.sleep(5)
    return True
#readwrite = os.pipe()

async def printout(classThingy: Installer):
    try:
        print(classThingy.cmd)
    except:
        print("HOW DARE THEE")

async def togetherYAY():
    installerObj = Installer()
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(installerObj.bootemUp())
        task2 = tg.create_task(importio())
    print("Import Complete")
    stdout, stderr = installerObj.cmd.communicate()
    output = stdout.decode(encoding="UTF-8")#.replace("\r","").replace("\n","")
    errors = stderr.decode(encoding="UTF-8")#.replace("\r","").replace("\n","")
    print(output, errors, sep="\n"*3)

if __name__ == "__main__":

    asyncio.run(togetherYAY())
"""
tmp1 = True

while tmp1:
    with os.read(readwrite[0]) as fifo:
        print(fifo)
        if "EOF" in fifo.decode(encoding="UTF-8"): tmp1=False; break

try:
    from fernet import Fernet
    import requests
except:
    sys.exit()

print(Fernet.generate_key())
"""