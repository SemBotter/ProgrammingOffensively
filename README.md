# IMPORTANT READ ME IF YOU INTEND TO USE THIS
This creates a Python virtual environment in the directory `venv`. It is important the directory is called specifically `venv`, otherwise this script will not work.

2. Execute PyInstaller on the `ProgrammingOffensively.spec` file:
### Required to build:
python 3.13
pyinstaller		(run `python.exe -m pip install pyinstaller`)

### To compile into an executable format:

1. Initiate a virtual environment in the same directory as the `ProgrammingOffensively.py` file:
  ```BatchFile cmd or powershell
  C:\ProgrammingOffensively>python.exe -m venv venv
  ```

  This creates a python virtual environment in the directory `venv`, it is important the directory is called specifically `venv`, otherwise this script will not work.
2. Execute PyInstaller on the `ProgrammingOffensively.spec` file
  ```BatchFile cmd or powershell
  C:\ProgrammingOffensively>pyinstaller -y ProgrammingOffensively.spec
  ```
3. Copy the executable file, saved into the `dist` folder, onto a Windows 10 or higher computer and execute it.