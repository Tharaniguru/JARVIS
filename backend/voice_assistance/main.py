import os
import queue
import sounddevice as sd
import vosk
import json
import pyttsx3
import time
import datetime
import subprocess
# Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Global flag to control mic input
is_speaking = False

def speak(text):
    global is_speaking
    is_speaking = True  # pause mic
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.2)  # short buffer
    is_speaking = False  # resume mic

# Load Vosk model
model_path = os.path.join("..", "models", "vosk-model-small-en-us-0.15")
if not os.path.exists(model_path):
    print("Please download the model from https://alphacephei.com/vosk/models and place it in the 'model' folder.")
    exit(1)

model = vosk.Model(model_path)
q = queue.Queue()

# Called automatically when mic captures audio
def callback(indata, frames, time_info, status):
    if status:
        print(status)
    if not is_speaking:  # Only queue audio when not speaking
        q.put(bytes(indata))

# Start speech recognition
def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        speak("Hello! I am JARVIS. How can I help you?")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
                if text:
                    print(f"You: {text}")
                
                if "stop" in text or "exit" in text:
                    speak("Goodbye!")
                    break

                elif "your name" in text:
                    speak("I am JARVIS, your offline assistant.")

                elif "time" in text:
                    current_time = datetime.datetime.now().strftime("%I:%M %p")
                    speak(f"The time is {current_time}.")

                elif "date" in text:
                    today = datetime.date.today().strftime("%B %d, %Y")
                    speak(f"Today is {today}.")

                elif "open notepad" in text:
                    subprocess.Popen(["notepad.exe"])
                    speak("Opening Notepad.")

                else:
                    speak("Sorry, I didn't understand that yet.")

if __name__ == "__main__":
    listen()
