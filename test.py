import hear, newthink2
# import keyboard 
import time 
import pyttsx3

HISTORY = "InMoov: I am a helpful assistant named InMoov. I am also a open source, 3D printable robot, made by Gael Langevin. How can I help you?"

def ask():
  print("Name?")
  username = input()
  return username

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 130)

while True: 
  s = time.time()
  hear.listen(True)
  text = newthink2.transcribe('output.wav')
  response = newthink2.response(HISTORY, text)
  engine.say(response)
  engine.runAndWait()
  e = time.time()
  print("\n elapsed time:" + str(e-s))