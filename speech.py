import speech_recognition as sr

recognizer = sr.Recognizer()



def get_text():
        with sr.Microphone() as source:
            print("🎙️ Speak something...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                print("📝 You said:", text)
                return text
            except sr.UnknownValueError:
                print("😕 Sorry, I couldn't understand.")
            except sr.RequestError:
                print("🚫 Service is down or unreachable.")

#------Speak with gTTS without saving file permanently------
# This code uses gTTS to convert text to speech and plays it using pydub.

from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import os
from pydub.utils import which

# Add ffmpeg to PATH (replace the path below with your actual path to ffmpeg\bin)
os.environ["PATH"] += os.pathsep + r"C:\Users\Dulhara\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin"
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

def speak_text(text):
    tts = gTTS(text)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    audio = AudioSegment.from_file(fp, format="mp3")
    play(audio)


# speak_text("Hello, this is a text-to-speech conversion using gTTS. remember that, you are great and great. everyday you achieve your goals like a master. keep going Dulhara! you will win for sure.")  # Example text to convert to speech