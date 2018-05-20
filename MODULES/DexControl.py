import re
from Mouth import Mouth
from Ears import Ears
import time
import os
import logging

dexSay = Mouth()
dexHear = Ears()

curfilePath = os.path.abspath(__file__)
curDir = os.path.abspath(os.path.join(curfilePath,os.pardir))
parentDir = os.path.abspath(os.path.join(curDir,os.pardir))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

moduleID = '0'

activeControlRegexes = [
    r'(\w*)*( Dexter)?( )*(close|terminate|die|quit) Dexter',
    r'(\w*)*( Dexter)?( )*(Thank you|Thanks|Bye( Bye)*|Buy( Buy)*|shut up|go away|goodbye|later) Dexter',
    r'(\w*)*( Dexter)?( )*(change|set|switch) mode(.*)'
]

quitRegex = r'(\w*)*( Dexter)?( )*(close|terminate|die|quit) Dexter'
passiveRegex = r'(\w*)*( Dexter)?( )*(Thank you|Thanks|Bye( Bye)*|Buy( Buy)*|shut up|go away|goodbye|later) Dexter'
setModeRegex = r'(\w*)*( Dexter)?( )*(change|set) mode(.*)'

def getID():
    return moduleID

def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''

    if dexActive == False:
        return False
    if dexActive == True:
        for regex in activeControlRegexes:
            if re.search(regex, data, re.I):
                return True

        return False

def handle(data, dexActive):
    '''
    1. Figure out what control function is needed
    2. Call the function
    '''

    if re.search(quitRegex, data, re.I):
        dexQuit()
    if re.search(passiveRegex, data, re.I):
        dexPassive(data,dexActive)
        return 'task complete'
    if re.search(setModeRegex, data, re.I):
        setMode(data)
        return 'task complete'

def dexQuit():
    '''Close dexter and random quit messages'''
    dexSay.speak("Okay. Shutting down now.", 'm', True)
    time.sleep(1)
    dexSay.speak("Dexter Terminated", 'f', True)
    quit()

def dexPassive(data,dexActive):
    '''Change dexter to passive mode'''
    data = data.lower()

    if 'thank' in data:
        dexSay.speak("You're welcome", "m", dexActive)
        dexSay.speak("You're welcome", "m", dexActive)
    elif 'buy' in data:
        dexSay.speak("Bye", "m", dexActive)
    elif 'shut up' in data:
        dexSay.speak("Oh! Sorry", "m", dexActive)
    elif 'go away' in data:
        dexSay.speak("I'll leave you alone", "m", dexActive)
    elif 'later' in data:
        dexSay.speak("later", "m", dexActive)
    else:
        dexSay.speak("Okay", "m", dexActive)

    dexActive = False
    return dexActive


def setMode(data):
    mode = data

    if data == None:
        dexSay.speak('What mode do you want dexter to use', 'f', True)
        dexSay.speak('say 1 for always listen.', 'f', True)
        dexSay.speak('say 2 for push to talk.', 'f', True)

        try:
            mode = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        logger.info(mode)

        if mode == 'RequestError' or mode == None:
            dexSay.speak('Something went wrong.', 'm', True)
            return
    else:
        if 'push' in mode:
            mode = 2
        elif 'always' in mode:
            mode = 1
        elif mode == 'set mode':
            dexSay.speak('What mode do you want dexter to use', 'f', True)
            dexSay.speak('say 1 for always listen.', 'f', True)
            dexSay.speak('say 2 for push to talk.', 'f', True)

            try:
                mode = dexHear.listen(True)
            except OSError as e:
                if 'Invalid input device' in str(e):
                    dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                                 True)
                if 'Unanticipated host error' in str(e):
                    dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                                 True)
                if 'Stream closed' in str(e):
                    dexSay.speak('Changing microphone.', 'f', True)

            logger.info(mode)

            if mode == 'RequestError' or mode == None:
                dexSay.speak('Something went wrong.', 'm', True)
                return


    if mode in [1, '1', 'one']:
        modeFile = open(parentDir+'\DexMode.txt', 'w')
        modeFile.write('1')
        modeFile.close()
        dexSay.speak("Ok, call me if you need my help.", 'm', True)
    elif mode in [2, '2', 'two']:
        modeFile = open(parentDir + '\DexMode.txt', 'w')
        modeFile.write('2')
        modeFile.close()
        dexSay.speak("Ok, push to talk mode activated", 'm', True)
    if mode not in [1, 2, '1', '2', 'one', 'two']:
        dexSay.speak('Sorry, that\'s an invalid answer. Setting mode to always listen', 'f', True)
        modeFile = open(parentDir + '\DexMode.txt', 'w')
        modeFile.write('1')
        modeFile.close()
