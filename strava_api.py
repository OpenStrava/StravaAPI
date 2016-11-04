#!/usr/bin/env python3
import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

class Food:
    def __init__(self, name, info, alergens, selectable, selected):
        self.name = name
        self.info = info
        self.alergens = alergens
        self.selectable = selectable
        self.selected = selected

class Launch:
    def __init__(self, date, foods):
        self.date = date
        self.foods = foods

def init():
    global __BROWSER__
    global __LOGGEDIN__
    __BROWSER__ = webdriver.Firefox()
    __LOGGEDIN__ = False

def logout():
    global __LOGGEDIN__
    if __LOGGEDIN__ == False:
        return False

    __BROWSER__.get("https://www.strava.cz/Strava/Stravnik/Odhlaseni")

    time.sleep(2)

    # Check success
    if __BROWSER__.current_url == "https://www.strava.cz/Strava/Stravnik/prihlaseni":
        __LOGGEDIN__ = False
        return True
    else:
        return False

def login(room, id, password):
    global __LOGGEDIN__
    if __LOGGEDIN__ == True:
        logout()
        time.sleep(2)

    __BROWSER__.get("https://www.strava.cz/Strava/Stravnik/prihlaseni")
    __BROWSER__.implicitly_wait(2)

    # Get elements
    room_element = __BROWSER__.find_element_by_id("prihlaseni_jidelna")
    id_element = __BROWSER__.find_element_by_id("prihlaseni_uzivatel")
    password_element = __BROWSER__.find_element_by_id("prihlaseni_heslo")
    submit = __BROWSER__.find_element_by_class_name("prihlaseni-prihlasit")

    # Fill elements
    room_element.send_keys(room);
    id_element.send_keys(id);
    password_element.send_keys(password);

    # Submit form
    submit.click()

    time.sleep(2);

    # Check success
    if __BROWSER__.current_url == "https://www.strava.cz/Strava/Stravnik/prihlaseni":
        return False
    else:
        __LOGGEDIN__ = True
        return True

def getInfo():
    global __LOGGEDIN__
    if __LOGGEDIN__ == False:
        return false

    __BROWSER__.get("https://www.strava.cz/Strava/Stravnik/Objednavky")
    __BROWSER__.implicitly_wait(2000)

    buffer = []

    # Get elements
    food_cover_element = __BROWSER__.find_element_by_id("seznam_objednavek_obalka")
    day_elements = food_cover_element.find_elements_by_class_name("objednavka-obalka-jednotne")

    # Iterate over all days
    for day_element in day_elements:
        # Get elements
        date = day_element.find_element_by_class_name("objednavka-den-datum").text
        options_cover_element = day_element.find_element_by_class_name("objednavka-jidla-obalka")
        option_elements = options_cover_element.find_elements_by_class_name("objednavka-jidlo-obalka")

        foods = []

        for option_element in option_elements:
            name_element = option_element.find_element_by_class_name("objednavka-jidlo-popis")
            info_element = option_element.find_element_by_class_name("objednavka-jidlo-nazev")
            food = Food(name_element.text, info_element.text, "", False, False)
            foods.append(food)
        launch = Launch(date, foods)
        
        buffer.append(launch)
    return buffer