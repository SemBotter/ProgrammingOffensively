import sys
import winreg as reg

helpMSGADD = """
Syntax:
persist.py add -program <PROGRAM> -path <PATH> [-background]
Examples:
Make explorer.exe run on startup as a foreground program:
persist.py -program explorer.exe -path C:\\Windows\\explorer.exe
Make Taskmgr.exe run on startup as a background program:
persist.py -program TaskManager -path C:\\Windows\\System32\\Taskmgr.exe -background

Explanation of the parameters:
-program    <PROGRAM>   Name of the program to be persisted, this will not impact the working, but can be used to cloak the program under an alias
-path       <PATH>      Complete path of the program to be persisted, this must include the program's file. 
-background (OPT)       Should the program start as a background program or not? Default is as a foreground program
-bg         (OPT)       Alias for -background

(OPT) parameters are optional and do not need to be specified

"""

helpMSGREM = """


Syntax:
persist.py remove <PROGRAMNAME>

Example:
Remove program named TaskManager from running on startup:
persist.py remove TaskManager

Explanation of the Parameters:
<PROGRAMNAME>   Name of the program to be removed from running on startup
"""

def add_to_startup_registry(program_name, program_path, background):
    try:
        key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
        match background:
            case True:
                reg_key_value = f"\"{program_path}\" /background"
            case False:
                reg_key_value = program_path
        reg.SetValueEx(registry_key, program_name, 0, reg.REG_SZ, reg_key_value)
        print(f"{program_name} is set for persistence")
        reg.CloseKey(registry_key)
    except Exception as e:
        print(f"Error persisting {program_name}: {e}")

def remove_from_startup_registry(program_name):
    try:
        key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_ALL_ACCESS)
        reg.DeleteValue(registry_key, program_name)
        print(f"Removed {program_name} from the startup programs")
        reg.CloseKey(registry_key)
    except Exception as e:
        print(f"Error removing {program_name} from startup programs: {e}")
#programma = "NotePad++"
#programma_pad = "C:\\Program Files\\Notepad++\\notepad++.exe"

programma = ""
programma_pad = ""
bg = False

operation = sys.argv[1]
if operation == "add":


    try:
        for i in range(len(sys.argv[2:])):
            match sys.argv[i]:
                case "-program":
                    programma = sys.argv[i+1]
                    continue
                case "-path":
                    programma_pad = sys.argv[i+1]
                    continue
                case "-background":
                    bg = True
                    continue
        if programma != "" and programma_pad != "":
            add_to_startup_registry(programma, programma_pad, bg)
        else:
            print(helpMSGADD)
    except IndexError as e:
        print(helpMSGADD)
        print(e)
        print("Did you specify all values?")
    except NameError as e:
        print(e)
        print("Something ain't right, you sure all was right?")

elif operation == "remove":
    try:
      
        programma = sys.argv[2]
        if programma != "":
            remove_from_startup_registry(programma)
        else:
            print(sys.argv)
            print(programma, sep="\n")
            print(helpMSGREM + "1")
    except IndexError as e:
        print(helpMSGREM)
        print(e)
        print("Did you specify all values?")
    except NameError as e:
        print(e)
        print("Something went wrong, try again!")