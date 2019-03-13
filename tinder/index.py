# import sense hat
from sense_hat import SenseHat
sense = SenseHat()
# import sleep
from time import sleep
# Import the request library
import requests
# Import the json library
import json

sense.low_light = True

# rotate the led matrix of the pi
sense.rotation = 180

# function to load data from 
def loadDataFromFile():
  with open('data.json') as myJsonDataFromFile:
    data = json.load(myJsonDataFromFile)
    return data

# function to load all saved data
def loadSavedUsers(choice):
    data = loadDataFromFile()
    i = 0
    if(choice == 'liked'):
        print ('all liked persons')
        for p in data['liked']:
            print(data['liked'][i])
            sense.show_message(data['liked'][i])
            i += 1
            sleep (1)
        start()
    if(choice == 'disliked'):
        print ('all disliked persons')
        for p in data['disliked']:
            print(data['disliked'][i])
            sense.show_message(data['disliked'][i])
            i += 1
            sleep (1)
        start()


# function to save data to json file
def saveDataToFile(name, data, choice):
    if(choice == 'liked'):
        data['liked'].append(
            name
        )
    else:
        data['disliked'].append(
            name
        )
    with open('data.json', 'w') as dataFile:  
        json.dump(data, dataFile)

def getUserData():
    # Make a get request to get a random name
    response = requests.get("https://randomuser.me/api/").json()
    data = response['results'][0]
    name = data['name']['first'] + " " + data['name']['last'];
    return name

def mainFunction():
    # calls the function getUserData
    name = getUserData()
    #calls the function loadDataFromFile
    data = loadDataFromFile()
    print (name)
    # shows the name of the current person
    while 1:
        sense.show_message(name)
        for event in sense.stick.get_events():
            if event.direction == "right":
                sense.clear(0, 255, 0)
                print ('liked')
                saveDataToFile(name, data, 'liked')
                mainFunction()
            if event.direction == "left":
                sense.clear(255, 0, 0)
                print ('disliked')
                saveDataToFile(name, data, 'disliked')
                mainFunction()
            if event.direction == "middle":
                sense.show_message('gestopt')
                sense.clear()
                start()
        sleep(1)

def start():
    print('werkt')
    while 1:
        sense.show_message('press joystick to start, up to show all liked, down to show all disliked')
        try:
            for event in sense.stick.get_events():
                if event.direction == "up":
                    sense.clear(0, 255, 0)
                    loadSavedUsers('liked')
                if event.direction == "down":
                    sense.clear(255, 0, 0)
                    loadSavedUsers('disliked')
                if event.direction == "middle":
                    sense.show_message('start')
                    mainFunction()
        except KeyboardInterrupt:
            sense.show_message('STOP!')
            print('Please run again')
            start()
            sense.clear()

start()