import os
import sys
class getnames():
    def __init__(self):
        self.__users = []
        self.__mod_files = os.listdir(path="users")
        for i in self.__mod_files:
            if ".py" in i:
                next
            else:
                self.__users.append(i)
        sys.path.insert(0, './users/')
    def get_all(self):
        return self.__users