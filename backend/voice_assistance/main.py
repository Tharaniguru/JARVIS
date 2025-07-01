import os
import queue
import sounddevice as sd
import vosk
import json
import pyttsx3
import time
import datetime
import subprocess
import threading
import sys

# Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Global flags
is_speaking = False
is_listening = False
q = queue.Queue()

def speak(text):
    global is_speaking
    is_speaking = True
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.2)
    is_speaking = False

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "..", "models", "vosk-model-small-en-us-0.15")

if not os.path.exists(model_path):
    print("Please download the model from https://alphacephei.com/vosk/models and place it in the 'model' folder.")
    exit(1)

model = vosk.Model(model_path)

def callback(indata, frames, time_info, status):
    if status:
        print(status)
    if is_listening and not is_speaking:
        q.put(bytes(indata))

def listen_loop():
    global is_listening
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)

        while True:
            data = q.get()
            if not is_listening:
                continue

            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
                if text:
                    print(f"You: {text}")

                if "your name" in text:
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

def control_loop():
    global is_listening
    for line in sys.stdin:
        command = line.strip().lower()
        if command == "start":
            is_listening = True
            print("[INFO] Listening started.")
        elif command == "stop":
            is_listening = False
            print("[INFO] Listening stopped.")

if __name__ == "__main__":
    speak("Hello! I am JARVIS. How can I help you?")
    threading.Thread(target=control_loop, daemon=True).start()
    listen_loop()
