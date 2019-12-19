import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint

browser = webdriver.Firefox()
browser.get("https://www.freerice.com")

#d = {}

#Function to find synonym of word
def synonym_finder(word):
    #Searching for word in theasaurus.com
    URL = "https://www.thesaurus.com/browse/" + word + "?s=t"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    #Collecting synonyms
    synonyms = []
    answers = soup.find('ul', attrs = {'class':'css-1lc0dpe et6tpn80'})
    for row in answers.findAll('a', attrs = {'class':'css-q7ic04 etbu2a31'}):
        synonyms.append(row.text)
    for row in answers.findAll('a', attrs = {'class':'css-zu4egz etbu2a31'}):
        synonyms.append(row.text)
    for row in answers.findAll('a', attrs = {'class':'css-gkae64 etbu2a31'}):
        synonyms.append(row.text)
    
    return synonyms


#Getting rid of the cookie warning by website
cookieButn = browser.find_element_by_class_name("as-oil__btn-optin")
cookieButn.send_keys(Keys.RETURN)
time.sleep(2)

#Logging into the account
browser.get("https://www.freerice.com/profile-login")
username = "hahaeyewin"
password = "Test23"
time.sleep(2)

userTextbox = browser.find_element_by_id("login-username")
passTextbox = browser.find_element_by_id("login-password")

userTextbox.send_keys(username)
passTextbox.send_keys(password)
browser.find_element_by_class_name("box-button").click()
time.sleep(5)

browser.get("https://www.freerice.com")

#Play time :)
while True:
    time.sleep(5)
    #Getting question word and corresponding synonyms
    qCard = browser.find_element_by_class_name("card-title")
    word = qCard.text.split()[0]
    synonyms = synonym_finder(word)

    #if word not in d:
    #    d[word] = synonyms

    #collecting given options
    options = browser.find_elements_by_class_name('card-button')
    wordsInOptions = [i.text for i in options]

    #Answer finding begins...
    
    flag = False
    #check if options are in synonyms of word,
    for i in range(0, 4):
        if flag:
            break
        x = wordsInOptions[i]
        #print(', '.join(d[word]))
        for j in synonyms:
            if j in x or x in j:
                flag = True
                options[i].click()
                break
    #check if word is present in synonyms of options
    for i in range(0, 4):
        if flag:
            break
        x_syn = synonym_finder(wordsInOptions[i])
        #print(x_syn)
        for j in x_syn:
            if word in j or j in word:
                flag = True
                options[i].click()
                break
    

    #Clicking random option if nothing matches
    if not flag:
        print("Sorry, couldn't do that one..")
        guess = randint(0,3)
        options[guess].click()
        
    else:
        print("Success")

    #input("Next?")
