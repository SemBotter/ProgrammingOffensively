from PIL import Image, ImageGrab
from time import strftime

class screencapture(object):
    def __init__(self):
        self.out_name = ""
        self.take()

    def take(self):
        img = ImageGrab.grab(bbox = None)
        self.out_name = ".\\ScreenShots\\SSHOT-{}.png".format(strftime("%H-%M-%S %d-%m-%Y"))
        img.save(self.out_name)
