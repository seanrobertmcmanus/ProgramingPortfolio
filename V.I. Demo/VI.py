#Python modules used for V.I. to run.
import pickle 
import json
import importlib
import importlib.util
import os 
import threading
import datetime
import time 
import random


def __main__():
    print ("Program Starting... setting up...")
    try:
        #Checks if the user was previously logged in, if so will give them the option to coninue session or start a new session
        with open('bin/prev_session.DAT', 'rb') as fh:
            while True:
                command = str(input("1 - Continue with last session \n2- New Session \nSelection: "))
                if command == '1':
                    print ("Continueing session")
                    VI_handle = pickle.load(fh)
                    VI_handle.startup()
                    break
                elif command == '2':
                    print ("Restarting...")
                    os.remove('bin/pre_session.DAT')
                    raise("New session slected")
                else:
                    print ("Please select appropriate selection")
    except:
        print ("error loading previous session, new sessions started")
        VI_handle = VI()
        print("Object assigned, startup initiating...")
        VI_handle.startup()
        print ("Startup finished...")
        print ("Initiating Voice setup")
        VI_handle.voice_in_out_setup()
        print ("Interactions setup complete")
        print ("Starting login...")
        while True: 
            command = str(input("1 - Text Login \n 2 - Vocal Login \n Selection: "))
            if command == "1":
                VI_handle.text_user_login()
                break
            elif command == "2":
                VI_handle.voice_user_login()
                break
        print ("login success")
        print ("Starting threading...")
        thread1 = voiceThread(VI_handle)
        thread2 = textThread(VI_handle)

        thread1.start()
        print ("Thread 1 [Voice] Started: ", datetime.datetime.now())
        thread2.start()
        print ("Thread 2 [Text] Started: ", datetime.datetime.now())
        print ("Threading Successfully started...")
        thread1.join()
        thread2.join()
        print ("Threading Successful")
        print ("Error, this should not be printed")
        

class user:
    def __init__(self, username, uid, refname):
        self.__username = username
        self.__uid = uid
        self.__refname = refname
    
    def get_username(self):
        print ("returning username")
        return self.__username

    def get_uid(self):
        print ("returing user id")
        return self.__uid
    
    def get_refname(self):
        print ("returning user ref_name")
        return self.__refname


class voiceThread(threading.Thread):
    def __init__(self, handle):
        threading.Thread.__init__(self)
        self.threadId = 1
        self.name = "V.I.-Voice"
        self.voice_handle = handle
    
    def run(self):
        print ("Starting: " + self.name + "\n")
        voice(self.voice_handle)
        print ("Exiting: " + self.name + "\n")

class textThread(threading.Thread):
    def __init__(self, handle):
        threading.Thread.__init__(self)
        self.threadId = 2
        self.name = "V.I.-Text"
        self.text_handle = handle

    def run(self):
        print ("Startin: " + self.name + "\n")
        text(self.text_handle)
        print("exiting thread 2")


def voice(voice_handle):
    while True:
        wake = "activate"
        end = "end"
        print ("Thread Voice,Time Stamp = [" +  str(datetime.datetime.now()) + "]")
        r = voice_handle.voice_check()
        if (r.lower()).count(wake) > 0:
            voice_handle.voice_command()
        if (r.lower()).count(end) > 0:
            with open("bin/prev_session.DAT",'wb') as fh:
                pickle.dump(voice_handle, fh)
                VI.end_program("end")

def text(text_handle):
    while True:
        print ("Thread Text, Time Stamp = [" +  str(datetime.datetime.now()) + "]")
        command = str(input("Input Command: "))
        if command == "end":
            with open("bin/prev_session.DAT",'wb') as fh:
                pickle.dump(text_handle, fh)
                VI.end_program("end")

        text_handle.text_command(command)     


    
#Class V.I. acts as the gateway for transfers to occur, almost like a port, and will feed certain content to certain scripts as well as activate them. 
class VI:
    #Constructor method (Which sets up the object)
    def __init__(self):
        #Self.__ makes the method private, meaning unless the data is called in script, nothing can access it outside of the program. 
        self.__interactions = ""
        #The control unit for the interactions we will use to communicate with (the input and output functions)
        self.__current_mods = []
        #The list of currently installed and useable mods, as well as their functions and which words they are called by
        self.__user = []
        #The currently signed in users details.
    
    def startup(self):
        self.__interactions = ""
        self.__current_mods = []
        #This will load in all currently installed mods and update the current mods variable.
        from mods import get_list
        print ("startup function initiated, importing mods list from current mods folder...")
        mods = get_list.getnames().get_all()
        names = []
        #name of mods array to prevent any duplicates
        mids = []
        #mod id array, for later inputting and file saving. 
        print ("Mods list imported, beggining import of individual mods")
        for name in mods:
            if (name not in names) and (name != '__pycache__'):
                print ("Module ", name, " found adding... ")
                mod_name, user_ref_words, mtype = VI.save_current_mods(name)
                names.append(name)
                while True:
                    if mtype == "VAVR":
                        #If the mod loading in contains this, the program will then make it the base interactions file
                        mid = random.randint(100,999)
                        mid = str(mid)
                        mid = "VAVR{}".format(mid)
                    else:
                        #give the program mods their id's for saving data to
                        mid = random.randint(1000000,9999999)
                        mid = str(mid)
                    if mid not in mids:
                        #ensures ID's are unique.
                        self.__current_mods.append([mod_name, mid, user_ref_words, name])
                        mids.append(mid)
                        break  
    
    def voice_in_out_setup(self):
        location = ''
        print ("Setting up Interactions Variable for Voice Recog and Output")
        for mod in self.__current_mods:
            if "VAVR" in mod[1]:
                location = "mods/{}/body.py".format(mod[3])
                print ("Voice settings found in module, attampting to connect...")
        if location == '':
            print ("Using base interactions...")
            location = "bin/interactions_base.py"
        spec = importlib.util.spec_from_file_location("interactions", location)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        self.__interactions = foo

    def text_user_login(self):
        selection = str(input("1 - Login \n2 - Register \nSelection: "))
        if selection == "1":
            self.__interactions.speak("Please input username below")
            while True:
                try:
                    username = str(input("Username: "))
                    if len(username) < 1:
                        raise("Not a valid username, input again")
                    if VI.validate_user(username) == True:
                        print ("not a vlaid username")
                    else:
                        uid = VI.convert(username)
                        path = 'users/{}/user.DAT'.format(uid)
                        print ("User found")
                        with open(path,'rb') as fh:
                            handle = pickle.load(fh)
                            username = handle.get_username()
                            uid = handle.get_uid()
                            ref_name = handle.get_refname
                            self.__user = [username, uid, ref_name]
                            return
                except Exception as e:
                    print (e)
        if selection == "2":
            print ("Register selected ")
            self.__interactions.speak("Registering, what would you like me to call you")
            while True:
                try:
                    userref = str(input("Ref name: "))
                    if len(userref) < 1:
                        raise ("Not valid")
                    self.__interactions.speak("Input your username")
                    while True:
                        try:
                            username = str(input("Input Username: "))
                            if VI.validate_user(username) == True:
                                raise("Not a vlaid name")
                            else:
                                uid = VI.convert(username)
                                mainpath = ('users/{}').format(uid)
                                if not os.path.exists(mainpath):
                                    os.makedirs(mainpath)
                                newpath = ('users/{}/Mod_saves').format(uid)
                                if not os.path.exists(newpath):
                                    os.makedirs(newpath)
                                mainpath = "{}/user.DAT".format(mainpath)
                                with open(mainpath, 'wb') as fh:
                                    user_save = user(username, uid, userref)
                                    pickle.dump(user_save, fh)
                                    self.__user = [username, uid, userref]
                                return
                        except Exception as e:
                            print (e)
                except Exception as e:
                    print (e)

    def voice_user_login(self):
        while True: 
            self.__interactions.speak("Please say Login or Register")
            selection = self.__interactions.listen()
            if selection == "1" or selection.lower() == "login":
                self.__interactions.speak("Please input username below")
                while True:
                    try:
                        username = self.__interactions.listen()
                        if len(username) < 1:
                            raise("Not a valid username, input again")
                        if VI.validate_user(username) == True:
                            print ("not a vlaid username")
                        else:
                            uid = VI.convert(username)
                            path = 'users/{}/user.DAT'.format(uid)
                            print ("User found")
                            with open(path,'rb') as fh:
                                handle = pickle.load(fh)
                                username = handle.get_username()
                                uid = handle.get_uid()
                                ref_name = handle.get_refname
                                self.__user = [username, uid, ref_name]
                                return
                    except Exception as e:
                        print (e)
            if selection == "2" or selection.lower() == "register":
                print ("Register selected ")
                self.__interactions.speak("Registering, what would you like me to call you")
                while True:
                    try:
                        userref = self.__interactions.listen()
                        if len(userref) < 1:
                            raise ("Not valid")
                        self.__interactions.speak("Input your username")
                        while True:
                            try:
                                username = self.__interactions.listen()
                                if VI.validate_user(username) == True:
                                    raise("Not a vlaid name")
                                else:
                                    uid = VI.convert(username)
                                    mainpath = ('users/{}').format(uid)
                                    if not os.path.exists(mainpath):
                                        os.makedirs(mainpath)
                                    newpath = ('users/{}/Mod_saves').format(uid)
                                    if not os.path.exists(newpath):
                                        os.makedirs(newpath)
                                    mainpath = "{}/user.DAT".format(mainpath)
                                    with open(mainpath, 'wb') as fh:
                                        user_save = user(username, uid, userref)
                                        pickle.dump(user_save, fh)
                                        self.__user = [username, uid, userref]
                                    return
                            except Exception as e:
                                print (e)
                    except Exception as e:
                        print (e)
    
    def voice_command(self):
        self.__interactions.speak("Listening")
        try:
            print ("Voice Called, attempting translation")
            text = self.__interactions.listen()
            for mods in self.__current_mods:
                for activation_words in mods[2]:
                    if text in activation_words[1]:
                        location = "mods/{}/body.py".format(mods[0])
                        spec = importlib.util.spec_from_file_location(activation_words[0], location)
                        foo = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(foo)
                        methods_to_call = getattr(foo, activation_words[0])
                        if activation_words[2] == 0:
                            if activation_words[3] == 0:
                                methods_to_call()
                            if activation_words[3] == 1:
                                location = "users/{}".format(self.__user[1])
                                methods_to_call(location, text)

                        if activation_words[2] == 1:
                            location = "users/{}".format(self.__user[1])
                            if activation_words[3] == 0:
                                return1 = methods_to_call()
                            if activation_words[3] == 1:
                                return1 = methods_to_call(location, text)
                            with open(location, 'rb') as fh:
                                pickle.dump(return1, fh)                                                      
                        return
        except Exception as e:
            print (e)
            return
    
    def text_command(self, text):
        try:
            for mods in self.__current_mods:
                for activation_words in mods[2]:
                    if text in activation_words[1]:
                        location = "mods/{}/body.py".format(mods[0])
                        spec = importlib.util.spec_from_file_location(activation_words[0], location)
                        foo = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(foo)
                        methods_to_call = getattr(foo, activation_words[0])
                        if activation_words[2] == 0:
                            if activation_words[3] == 0:
                                methods_to_call()
                            if activation_words[3] == 1:
                                location = "users/{}".format(self.__user[1])
                                methods_to_call(location, text)

                        if activation_words[2] == 1:
                            location = "users/{}".format(self.__user[1])
                            if activation_words[3] == 0:
                                return1 = methods_to_call()
                            if activation_words[3] == 1:
                                return1 = methods_to_call(location, text)
                            with open(location, 'rb') as fh:
                                pickle.dump(return1, fh)                                                      
                        return
        except Exception as e:
            print (e)

    def voice_check(self):
        text = self.__interactions.listen()
        return text

    @staticmethod
    def validate_user(username):
        username = VI.convert(username)
        from users import get_user_list
        names = get_user_list.getnames().get_all()
        for name in names:
            if name == username:
                return False
        return True

    @staticmethod
    def convert(username):
        temp2 = username.split(" ")
        temp = ""
        for i in temp2:
            temp += i
        temp = [ord(c) for c in temp]
        text = ''
        for i in range(len(temp)):
            text += str(temp[i])
        text = hex(int(text))
        return text
    
    @staticmethod
    def save_current_mods(name):
        location = 'mods/{}/setup.json'.format(name)
        #open's that mod's location
        try:
            with open(location, 'r') as fh:
                print ("mod data uploading for user...")
                info = json.load(fh)
                mod_name = info['name']
                mtype = info['type']
                json_ref_words = info['user_ref_words']
                user_ref_words = []
                for i in range(len(json_ref_words)):
                    user_ref_words.append([info['user_ref_words'][i]['function'], info['user_ref_words'][i]['call_words'], info['user_ref_words'][i]['returns'], info['user_ref_words'][i]['needs']])
            print ("adding ", name, " successful")
            #This adds the mod's data (in the json file) so the program can now referance what is needs 
            return mod_name, user_ref_words, mtype
        except:
            error = "Mod style incorrect, terminating" + name
            VI.end_program(error)
    
    @staticmethod
    def end_program(error):
        print (error)
        exit()

if __name__ == "__main__":
    __main__()