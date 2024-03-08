import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import ollama
from pygame import mixer
import os
from mutagen.mp3 import MP3
import time

# AudioSegment.converter = r"C:\Users\samyg\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-6.1.1-essentials_build\bin\ffmpeg.exe"

def listen_for_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language="fr_FR")
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

def respond(response_text):
    print(response_text)
    nom = "response.mp3"
    tts = gTTS(text=response_text, lang='fr')
    tts.save(nom)

    AudioSegment.from_mp3(nom)  
    mixer.init()
    mixer.music.load(nom)
    mixer.music.play()
    audio = MP3(nom)
    duration = audio.info.length
    time.sleep(duration+1)
    mixer.music.stop()
    mixer.music.unload()
    os.remove(nom)

tasks = []
listeningToTask = False

def main():
    global tasks
    global listeningToTask
    while True:
        command = listen_for_command()
        AIname="zoé"
        if command and AIname in command:
            toto = ollama.generate(model='stablelm2', prompt=command)["response"]
            print("toto:", toto)
            respond(toto)
        else:
            respond("J'ai compris mais je ne sais pas quoi faire avec ça.")
            print(command)

if __name__ == "__main__":
    respond("Salut mon pote")
    main()
