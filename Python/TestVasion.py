import asyncio
import subprocess
from typing import Any

class Installer(asyncio.SubprocessProtocol):
    def __init__(self):
        super(Installer, self).__init__()
        self.powershellpaths = [r"C:\Windows\System32\powershell.exe", r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"]

    async def bootemUp(self):        
        try:
            self.cmd = subprocess.Popen("pip install cryptography fernet requests", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable=self.powershellpaths[0])
        except FileNotFoundError:
            self.cmd = subprocess.Popen("pip install cryptography fernet requests", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable=self.powershellpaths[1])

    async def cancel(self, msg: Any | None = None) -> bool:
        super(Installer, self).cancel(msg)
        self.cmd.send_signal(subprocess.SIGTERM)

async def importio() -> bool:
    import os
    import sys

    os.chdir("C:\\")
    print(os.getcwd())
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

# dictionary syntax:
# {
# "1": "import pyfiglet"
# 
# }

def encryptCodeBlock(inp: dict) -> dict:
    pass

import pyfiglet




if __name__ == "__main__":

    asyncio.run(togetherYAY())


    try:
        from fernet import Fernet
        import requests
    except:
        sys.exit()

    a = Fernet.generate_key()
    print(a)
    a_inst = Fernet(a)
    token = a_inst.encrypt(b"Coole Tekst hier lmao") 
    print(token)

    b = a_inst.decrypt(token)
    print(b)