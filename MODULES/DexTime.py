import re
from Mouth import Mouth
from Ears import Ears
import time
import datetime

dexSay = Mouth()
dexHear = Ears()

moduleID = '2'

activeTimeRegexes = [
    r'(.*)(time|date)(.*)',
]

daySuffixes = {
    1: 'st',
    2: 'nd',
    3: 'rd',
    21: 'st',
    22: 'nd',
    23: 'rd',
    31: 'st'
}

def custom_strftime(format, t):
    return time.strftime(format, t).replace('{TH}', str(t[2]) + daySuffixes.get(t[2], 'th'))

def getID():
    return moduleID

def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''
    if dexActive == False:
        return False
    if dexActive == True:
        for regex in activeTimeRegexes:
            if re.search(regex, data, re.I):
                if re.search('times',data, re.I):
                    return False
                return True

        return False

def handle(data, dexActive):
    '''
    1. Figure out what control function is needed
    2. Call the function
    '''

    for regex in activeTimeRegexes:
        if re.search(regex, data, re.I):
            dexTime(data)
            return 'task complete'


def dexTime(data):
    '''Open Start Menu and search for query'''

    query = data.strip()
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    weekday = datetime.date.today().strftime("%A")

    if re.search(r'time', query):
        if hour > 12:
            dexSay.speak("The time is " + str(hour-12) + " " + str(minute) + " pm", 'm', True)
        else:
            dexSay.speak("The time is " + str(hour) + " " + str(minute) + " am", 'm', True)

    if re.search(r'date', query):
        dexSay.speak("Today is " + str(weekday) + " the " + custom_strftime('{TH} of %B, %Y', time.localtime()) , 'm', True)
