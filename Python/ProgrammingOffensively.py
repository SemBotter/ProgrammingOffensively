import os
import os.path
import subprocess
helpMSG = """
/help   Print this message
/disabledefender    Disables Windows Defender
/addtostartup       Adds a specified program to startup


"""
env = os.environ
userInp = input("What would you like to do today?\n")

match userInp:
    case "/help":
        print(helpMSG)
    case "/disabledefender":
        currPath = os.getcwd()
        print(currPath)
        file = "python " + os.path.join(currPath, "defender.py")
        print(file)
        defdisabler = subprocess.run(file, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, env = env)
        defdisabler.returncode
    case "/discord":
        import discordbot
