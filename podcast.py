import os
import wave
import time
import threading
import tkinter as tk
import datetime
import pyaudio

class Recorder:
    def __init__(self):
        self.ui = tk.Tk()
        self.ui.resizable(False,False)
        self.recordButton = tk.Button(text="🎙️", font=("Lato",60,"normal"), command=self.recordBtnPress)
        self.pawsButton = tk.Button(text="⏸️", font=("Lato",60,"normal"), command=self.paws)
        self.recordButton.pack()
        self.pawsButton.pack()
        self.recording = False
        self.pawsEnabled = False
        self.timeLabel = tk.Label(text="Podcast Length = 00:00:00:00", font=("Lato",30))
        self.timeLabel.pack()
        self.ui.mainloop()
    def recordBtnPress(self):
        if self.recording:
            self.recording = False
            self.recordButton.config(fg="black")
        else:
            self.recording = True
            self.recordButton.config(fg="green")
            threading.Thread(target=self.record).start()
    def paws(self):
        if self.pawsEnabled:
            self.pawsEnabled = False
            self.pawsButton.config(text="⏸️")
        else:
            self.pawsEnabled = True
            self.pawsButton.config(text="▶️")
    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)
        frames = []
        start = time.time()
        while self.recording:
            passed = time.time()-start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            msecs = (secs % 60) - int(secs)
            totalPassed = 0
            if self.pawsEnabled:
                totalPassed += passed
                tsecs = totalPassed % 60
                tmins = totalPassed // 60
                thours = tmins // 60
                tmsecs = (tsecs % 60) - int(tsecs)
                self.timeLabel.config(text=f"Podcast Paused At {int(thours):02d}:{int(tmins):02d}:{int(tsecs):02d}:{int(tmsecs*60):02d}")
                start = time.time()
            else:
                data = stream.read(1024)
                frames.append(data)
                self.timeLabel.config(text=f"Podcast Length = {int(hours):02d}:{int(mins):02d}:{int(secs):02d}:{int(msecs*60):02d}")
        totalPassed += passed
        tsecs = totalPassed % 60
        tmins = totalPassed // 60
        thours = tmins // 60
        tmsecs = (tsecs % 60)-int(tsecs)
        stream.stop_stream()
        stream.close()
        audio.terminate()

        fileExists = True
        i = 0
        while fileExists:
            if i == 0:
                if os.path.exists(f"Podcast Recording At {datetime.datetime.now().year}.{datetime.datetime.now().month}.{datetime.datetime.now().day} ({i}).wav"):
                    i += 1
                else:
                    fileExists = False
            else:
                if os.path.exists(f"Podcast Recording At {datetime.datetime.now().year}.{datetime.datetime.now().month}.{datetime.datetime.now().day}.wav"):
                    i += 1
                else:
                    fileExists = False
        if (i-1) > 1:
            recording = wave.open(f"Podcast Recording At {datetime.datetime.now().year}.{datetime.datetime.now().month}.{datetime.datetime.now().day} ({i}).wav", "wb")
        else:
            recording = wave.open(f"Podcast Recording At {datetime.datetime.now().year}.{datetime.datetime.now().month}.{datetime.datetime.now().day}.wav", "wb")
        recording.setnchannels(2)
        recording.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        recording.setframerate(44100)
        recording.writeframes(b"".join(frames))
        recording.close()

    
if __name__ == "__main__":
    Recorder()
