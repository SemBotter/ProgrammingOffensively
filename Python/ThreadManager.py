import threading
import sys
import subprocess

class ThreadManager(threading.Thread):
    def __init__(self, name, target, args: None | tuple = None):
        threading.Thread.__init__(self)
        self.name = name
        self.target = target
        self.daemon = True
        if args != None:
            self.args = args
        else:
            self.args = None

    def run(self):
        if self.args:
            self.target(self.args)
        else:
            self.target()

