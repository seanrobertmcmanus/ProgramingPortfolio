import threading
import datetime
import time
import pickle
import importlib



def program_setup():
    thread1 = threadCheck()
    thread1.start()
    thread1.join()
    return


class ALARM:
    def __init__(self, name, time, uid, location):
        self.name = name
        self.time = time
        self.uid = uid
        self.location = location
    

class threadCheck(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.threadId = 2
        self.name = "Alarm - Checker"
    
    def run(self):
        print ("Starting: " + self.name + "\n")
        alarm_checker()
    



def get_current_time():
   now = datetime.datetime.now()
   now = str(now)
   z = now.split(" ")
   current_time = z[1].split(":")
   current_time = "{}:{}".format(current_time[0], current_time[1])
   return current_time 

def alarm_start(settings,location):
    location = "mods/spotify/body.py"
    spec = importlib.util.spec_from_file_location("spotify", location)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    foo.start_playback(location, settings)

def alarm_checker():
    next_alarm = []
    count = 0
    while True:
        time.sleep(1)
        try:
            current_time = get_current_time()
            if current_time == next_alarm[0]:
                alarm_start(alarm[2],alarm[3])
            count += 1
        except:
            print ("No alarms.")
        if count == 10:
            alarms = []
            try:
                with open("mods/alarms/alarms.DAT",'rb') as fh:
                    while True:
                        try:
                            alarm_handle = pickle.load(fh)
                            alarms.append([alarm_handle.name, alarm_handle.time, alarm_handle.uid, alarm_handle.location])
                        except:
                            print ("EOF")
                            break
                current_time = get_current_time()
                try:
                    next_time = 0
                    for i in range(len(alarms)):
                        timer = alarms[i][1]
                        timer = time.split(":")
                        current_time = current_time.split(":")
                        if int(timer[0]) > int(current_time[0]):
                            temp = alarms[next_time][0].split(":")
                            if int(temp[0]) > int(timer[0]):
                                next_time = i
                            elif int(temp[0]) == int(timer[0]):
                                if int(temp[1]) > int(timer[1]):
                                    next_time = i
                            else:
                                next
                    next_alarm = [alarms[i][0], alarms[i][1], alarms[i][2]]
                except:
                    print ("Something went wrong?")
                    next_alarm = [alarms[i][0], alarms[i][1], alarms[i][2]]
            except:
                print ("Nothing in file reverting")


#Requires a call
def set_alarm(location, text, interactions):
    interactions.speak("hello, what would you like me to call the alarm?")
    print ("Setting alarm name")
    while True:
        name = interactions.listen()
        if len(name) > 1:
            interactions.speak("Great, what time would you like the alarm to go off, use o'clock for better input")
            count = 0 
            while True:
                try:
                    if count == 2:
                        time = str(input("Input time through text: "))
                        actual_time = time_find(time)
                    else:
                        time = interactions.listen()
                        actual_time = format_time(time)
                    while True:
                        interactions.speak("Ok, what album would you like for the alarm")
                        try:
                            album = interactions.listen()
                            location = "mods/spotify/body.py"
                            spec = importlib.util.spec_from_file_location("spotify", location)
                            foo = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(foo)
                            albums = foo.get_album(location, album)
                            interactions.speak("Which album would you like say the number")
                            for i in range(5):
                                album_name = albums[i][1]
                                string = "1 {}".format(album_name)
                                interactions.speak(string)
                            while True:
                                text = interactions.listen()
                                if "1" in text or "one" in text:
                                    uri = albums[0][2]
                                    break
                                if "2" in text or "two" in text:
                                    uri = albums[1][2]
                                    break
                                if "3" in text or "three" in text:
                                    uri = albums[2][2]
                                    break
                                if "4" in text or "four" in text:
                                    uri = albums[3][2]
                                    break
                                else:
                                    interactions.speak("Nothing was picked, input again")
                            temp_alarm = ALARM(name, actual_time, uri, location)
                            with open ('mods/alarms/alarms.DAT','ab') as fh:
                                pickle.dump(temp_alarm, fh)

                        except:
                            interactions.speak("I didnt quite get that")
                except:
                    interactions.speak("That did not input correctly")

def format_time(r):
    while True:
        minutes_tens = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fiveteen", "sixteen", "seventeen", "eightteen", "nineteen","twentyone", "twenty two", "twenty three", "twenty four", "twenty five", "twenty six", "twenty seven", "twenty eight", "twenty nine", "thirty one", "thirty two", "thirty three", "thirty four", "thirty five", "thirty six", "thirty seven", "thirty eight", "thirty nine", "fourty one", "fourty two", "fourty three", "fourty four", "fourty five", "fourty six", "fourty seven", "fourty eight", "fourty nine", "fifty one", "fifty two", "fifty three", "fifty four", "fifty five", "fifty six", "fifty seven", "fifty eight", "fifty nine" ]
        hours = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven","twelve"]
        slang = ["to", "past", "half", "quarter", "am", "pm"]
        r = r.lower()
        r = r.split(" ")
        
        h = "h"
        m = "m"
        s = "s"
        
        piv1 = "msh"
        piv2 = "ssh"
        piv3 = "hms"
        piv4 = "hmh"

        
        for i in range(len(r)):
            try:
                if r[i] in hours:
                    layout += h
                elif r[i] in minutes_tens:
                    layout += m
                elif r[i] in slang:
                    layout += s
                if r[i+1] in hours:
                        layout += h
                elif r[i+1] in minutes_tens:
                    layout += m
                elif r[i+1] in slang:
                    layout += s
                if r[i+2] in hours:
                        layout += h
                elif r[i+2] in minutes_tens:
                    layout += m
                elif r[i+2] in slang:
                    layout += s
                if len(layout) == 2:
                    if layout == piv1:
                        lay = 0
                        break
                    elif layout == piv2:
                        lay = 1
                        break
                    elif layout == piv3:
                        lay = 2
                        break
                    elif layout == piv4:
                        lay = 0
                        break 
                    else:
                        layout = ""
                        next
            except:
                print ("Something went wrong")

        hour = 0
        minutes = 0
        slang = ""               
        
        if lay == 0:
            for z in minutes_tens:
                if r[i] == z:
                    minutes = z.index + 1
            for z in slang:
                if r[i+1] == z:
                    slang = z
            for z in hours:
                if r[i+2] == z:
                    hours = z.index + 1
            
            if slang == "to":
                minutes = 60 - minutes
                hour = hour - 1
            elif slang == "past":
                continue
        
        if lay == 1:
            for z in slang:
                if r[i] == z:
                    slang1 = z
                if r[i+1] == z:
                    slang2 = z
            for z  in hours:
                if r[i+2] == z:
                    hour = z.index + 1
            
            if slang1 == "quarter":
                minutes = 15
            if slang1 == "half":
                minutes = 30
            if slang2 == "past":
                continue
            if slang2 == "to":
                minutes = 60-minutes
                hour = hour - 1
            
        if lay == 2:
            for z in hours:
                if r[i] == z:
                    hour = z.index + 1
            for z in minutes_tens:
                if r[i+1] == z:
                    minutes = z.index + 1
            for z in slang:
                if r[i+2] == z:
                    if z == "am":
                        continue
                    elif z == "pm":
                        hour += 12
        
        time = "{}:{}".format(hour, minutes)
        return time




        
        