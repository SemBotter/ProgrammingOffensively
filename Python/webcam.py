import cv2
import time
import asyncio
import os

class webcam(object):
    def __init__(self):
        self.out_name = ""

    async def activate(self) -> tuple:
        activated = cv2.VideoCapture(0)
        
        if not activated.isOpened():
            return ("Could not open the webcam", "WebcamNotOpenedError")
        await asyncio.sleep(1)  # Simulate async operation
        return (activated, "0")

    async def capture(self, camera):
        readright, frame = camera.read()

        if not readright:
            return "NoImageCapturedError"

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow("frame", gray)
        await asyncio.sleep(1)  # Simulate async operation
        return "0"
    
    async def save(self, camera):
        readright, frame = camera.read()
        if not readright:
            return "NoImageSavedError"

        self.out_name = "webcamcapture({}).png".format(time.strftime("%H-%M-%S_%Y-%m-%d"))
        os.chdir(".\\WebcamCaptures")
        try:
            writeimg = cv2.imwrite(self.out_name, frame)
            os.chdir("..\\")
            if writeimg:
                self.out_name=".\\WebcamCaptures\\{}".format(self.out_name)
                await asyncio.sleep(1)  # Simulate async operation
                return "{} written!".format(self.out_name)
            else:
                return "Failed to write image"
        except Exception as e:
            return f"Error saving image: {e}"

    async def release(self, camera):
        camera.release()
        cv2.destroyAllWindows()
        await asyncio.sleep(1)  # Simulate async operation