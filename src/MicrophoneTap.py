import pyaudio
import wave
from os import chdir, getcwd, listdir, mkdir
from time import strftime, time

class simpleExcept(Exception):
    def __init__(self):
        super(simpleExcept, self).__init__()

class MicrophoneTap(pyaudio.PyAudio):
    def __init__(self, giventime):
        super(MicrophoneTap, self).__init__()
        self.giventime = float(giventime)
        self.starttime = time()
        self.endtime = self.giventime + self.starttime

    def start(self):
        return self.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    def activate(self) -> str:
        stream = self.start()
        self.framelist = []
        try:
            
            while True:
                self.data = stream.read(1024)
                self.framelist.append(self.data)
                if time() > self.endtime:
                    raise simpleExcept
        except KeyboardInterrupt:
            print("Received stop signal from user, stopping recording...")
        except simpleExcept:
            print(f"Finished recording, stopping now...")
        except Exception as e:
            print(f"The following exception has occurred: {e}")
            return "" 
        finally:
            stream.stop_stream()
            stream.close()
            self.terminate()
            self.filename = self.save()
            return f"\\AudioCaptures\\{self.filename}"
    def save(self) -> str:
        sample_width = self.get_sample_size(pyaudio.paInt16)
        letsSave = saveAudio(sample_width, self.framelist)
        return letsSave.filename
        
  


class saveAudio():
    def __init__(self, audioSampleSize: int, frames: list):
        super(saveAudio, self).__init__()
        filename = "{}.wav".format(strftime("%S-%M-%H %d-%m-%Y"))
        self.filename = filename
        self.chdir()
        output = wave.open(filename, "wb")
        output.setnchannels(1)
        output.setsampwidth(audioSampleSize)
        output.setframerate(44100)
        output.writeframes(b''.join(frames))
        output.close()
        chdir("..\\")
        return
    def chdir(self):
        cwd = listdir()
        
        if "AudioCaptures" not in cwd:
            mkdir(getcwd() + "\\AudioCaptures")
        chdir(getcwd() + "\\AudioCaptures")
        


if __name__ == "__main__":
    micTap = MicrophoneTap()
    listenOn = micTap.activate()
    print("Audio saved into file: {}".format(listenOn))

