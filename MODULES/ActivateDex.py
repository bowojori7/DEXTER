import re
from Mouth import Mouth


dexSay = Mouth()

moduleID = '1'

activateRegexes = [r'^(hey|hi|hello|what\'s up|yo|how far|alpha|how are you|how you they|how you day)*( )*(Dexter)+$',
                   r'^(could you|can you|please)* help( me )*( )*Dexter$',
                   r'^Dexter( )*(help)*(.*)$',
                   r'^Dexter$',]

dexActive = False

def getID():
    return moduleID

def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''
    data = data.strip()
    valid = False
    for regex in activateRegexes:
        if re.search(regex, data, re.I):
            valid = True

    if valid == True:
        return valid

    return valid

def handle(data, dexActive):
    data = data.strip()
    data = data.lower()
    dexActive = False

    for regex in activateRegexes:
        if re.search(regex, data, re.I):
            if 'alpha' in data:
                dexSay.speak('I day', 'm', True)
            if 'far' in data:
                dexSay.speak('I day', 'm', True)
            elif 'hey' in data:
                dexSay.speak('Hey', 'm', True)
            elif 'hi' in data:
                dexSay.speak('Hi', 'm', True)
            elif 'how are you' in data:
                dexSay.speak("I'm doing fine, thank you", 'm', True)
            elif 'they' in data:
                dexSay.speak('I day fine.', 'm', True)
            elif 'day' in data:
                dexSay.speak('I day fine.', 'm', True)
            elif data == 'yo dexter':
                dexSay.speak('what\'s up?', 'm', True)
            elif 'up' in data:
                dexSay.speak('what\'s up?', 'm', True)
            else:
                dexSay.speak('Hello', 'm', True)

            dexActive = True

    if dexActive == True:
        return dexActive

    return dexActive