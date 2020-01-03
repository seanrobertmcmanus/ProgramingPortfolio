#The modules used from pythons library in this script. 
import speech_recognition as sr 
import playsound
from gtts import gTTS
import os
import pyaudio


class counter:
    #Counter used by speak to reduce risk of error. 
    count = 0

def speak(text):
    #This is a function called speak
    #It will return the mp3 of any file we test we send to it. 
    counter.count += 1
    #Counter for next mp3 file incase of an overlap which will casue a sys error
    tts = gTTS(text=text, lang='en')
    print ("Text Uploading  to google cloud...")
    fn = 'bot_output{}.mp3'.format(counter.count)
    print("mp3 downloaded...")
    tts.save(fn)
    print ("mp3 saved...")
    #Saves the downloaded MP3
    playsound.playsound(fn)
    print ("mp3 file playing")
    #Play the MP3 file 
    os.remove(fn)
    print ("mp3 file removed")
    #Removes the Mp3 file (to save storage and returns to main program)
    print ("returning to main function...")


def listen():
    r = sr.Recognizer()
    #Sets up the function Speech recognition with computers local sound/mic resources
    r.energy_threshold = 4000
    print ("Checking Sound threshold")
    with sr.Microphone() as source:
        print ("recording sound")
        audio = r.listen(source)
        #This records sound to be recorded locally, if conditions met it will upload sample, else it will delete the sample
        said = ""
        print ("Analyising sound...")

        try:
            #'iyea4J_odgncTymkPrZReg==','vdsEtwN3XU1RYwx8w-3likrXDApSU7S26g43WQBOt41bJoJbAIMpYPeUobqSa7KO7sQ85yiW4MorRfFt90eXcA=='
            said = r.recognize_google(audio)
            #File is uploaded to (selected method's cloud)
            print ("Converting to text..")
            print ("User: "+ said)
            #Text has been returned and is returned to hte main function. 

        except Exception as e:
            print("Exception: " + str(e))

    print ("returning to main function...")
    return said