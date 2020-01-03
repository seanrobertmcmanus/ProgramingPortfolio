#webbroswing
import requests
import webbrowser

#webscraping
from bs4 import BeautifulSoup as bs
import urllib
import json

def google_search(text, type_of):
    if type_of == "1" or type_of == 2:
        term = ""
        x = 0 
        for i in text.splt(" "):
            if i == "top":
                x = 1
                term += i
            if x == 1:
                term += i
    if type_of == "3":
        term = text


            
    url = 'https://www.google.co.uk/search?hl=en&q={0}&source=lnms'.format(term)
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    return soup
    



def movie_music(useless, text, interactions):
    soup = google_search(text, "1")
    name = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
    artist = soup.find_all('div', class_='BNeawe tAd8D AP7Wnd')
    print('Top 20 current: ')
    for i in range(20):
        string1 = "name {}".format(name[i].text)
        string2 = "artist {}".format(artist[i].text)
        interactions.speak(string1)
        interactions.speak(string2)
    


def area(useless, text, interactions):
    soup = google_search(text, "2")
    name = soup.find_all('div', class_='BNeawe deIvCb AP7Wnd')
    print('Top 3 in your area: ')
    for i in range(4):
        string = "location one {}".format(name[i].text)
        interactions.speak(string)


    

def define(useless, text, interactions):
    soup = google_search(text, "3")
    definition = soup.find_all('div', 'BNeawe s3v9rd AP7Wnd' )
    interactions.speak("Here's what I found")
    for i in range(1,2):
        string = definition[i].text 
        interactions.speak(string)
        

    
