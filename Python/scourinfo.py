import os
import socket

class scourinfo(object):
    """description of class"""
    def __init__(self):
        self.complete_info = {}
        self.sysname = {"System hostname information": socket.gethostbyaddr(socket.gethostname())}
        self.username = {"User running the bot file": os.getlogin()}
        self.processID = {"Process ID of the bot file": os.getpid()}
        self.parentProcessID = {"Process ID of the parent-process of the bot file": os.getppid()}
        self.currentDirectory = {"Directory in which the process is running": os.getcwd()}
        inbetweenlist = [self.sysname, self.username, self.processID, self.parentProcessID, self.currentDirectory]
        #self.complete_info.update(self.sysname).update(self.username).update(self.processID).update(self.parentProcessID).update(self.currentDirectory)
        #print(dict(map(self.complete_info.update, inbetweenlist)))
        list((map(self.complete_info.update, inbetweenlist[:])))
        print("\n\n\n\n5555")
        print(self.complete_info)


    def environment(self) -> str:
        return os.environ

