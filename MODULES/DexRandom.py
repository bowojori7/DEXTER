import re
from Mouth import Mouth
from Ears import Ears
import random


dexSay = Mouth()
dexHear = Ears()

moduleID = '12'

randRegexes = [
    r'(.*)',
]


def getID():
    return moduleID

def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''
    if dexActive == False:
        return False
    if dexActive == True:
        for regex in randRegexes:
            if re.search(regex, data, re.I):
                return True

        return False

def handle(data, dexActive):
    '''
    1. Figure out what control function is needed
    2. Call the function
    '''

    for regex in randRegexes:
        if re.search(regex, data, re.I):
            dexReply(data)
            return 'task complete'


def dexReply(data):
    '''Open Start Menu and search for query'''

    query = data
    if query == "How are you":
        reply = ["I'm okay", "I'm good", "Dunno", "I'm doing great", "I'm okay, you ?", "I'm good, how you doing ?", "Dunno, what's up with you ?", "I'm doing great, how about you?",]
        rep = random.choice(reply)
        if "you" in rep:
            dexSay.speak(rep, 'm', True)
            #listen and reply
        else:
            dexSay.speak(rep, 'm', True)