import os
import sys
class getnames():
    def __init__(self):
        self.__mods = []
        self.__mod_files = os.listdir(path="mods")
        for i in self.__mod_files:
            if ".py" in i:
                next
            else:
                self.__mods.append(i)
        sys.path.insert(0, './mods/')
    def get_all(self):
        return self.__mods