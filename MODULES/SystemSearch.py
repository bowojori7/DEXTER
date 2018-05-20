import re
from Mouth import Mouth
from Ears import Ears
import time
import os
import keyboard
import inspect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
utilityDIR = DIR + '\\UTILITIES'

dexSay = Mouth()
dexHear = Ears()

moduleID = '5'

activeSystemSearchRegexes = [
    r'(.*)(Dexter)?(.*)(search|look|find)+(.*)(on|in)*(.*)(my|the)*( )*(offline|computer|system|pc|laptop|desktop)(.*)',
    r'(.*)(Dexter)?(.*)(offline|computer|system|pc|laptop|desktop)( )*(search)+( )*(for|on|about)(.*)'
]

searchWithQueryRegexes = [r'(.*)(Dexter)?(.*)(search|look|find)+(.*)(on|in)*(.*)(my|the)*( )*(offline|computer|system|pc|laptop|desktop)(.*)',
                          r'(.*)(Dexter)?(.*)(offline|computer|system|pc|laptop|desktop)( )*(search)+( )*(for|on|about)(.*)'
]
searchWithoutQueryRegexes =  [r'(.*)(Dexter)?(.*)(offline|computer|system|pc|laptop|desktop)( )*(search)( )*(for|on|about)$',
                              r'(.*)(Dexter)?(.*)(search)( )*(the)*( )*(offline|computer|system|pc|laptop|desktop)( )*(for|on|about)$'
]

def getID():
    return moduleID

def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''
    if dexActive == False:
        return False
    if dexActive == True:
        for regex in activeSystemSearchRegexes:
            if re.search(regex, data, re.I):
                return True

        return False

def handle(data, dexActive):
    '''
    1. Figure out what control function is needed
    2. Call the function
    '''
    logger.info(data)

    for regex in searchWithoutQueryRegexes:
        if re.search(regex, data, re.I):
            dexSystemNoQuery()
            return 'task complete'

    for regex in searchWithQueryRegexes:
        if re.search(regex, data, re.I):
            dexSystemQuery(data)
            return 'task complete'


def dexSystemQuery(data):
    '''Open Start Menu and search for query'''

    query = data

    if re.search(r'(.*)(Dexter)?(.*)(search|look|find)+(.*)(on|in)*(.*)(my|the)*( )*(offline|computer|system|pc|laptop|desktop)(.*)',data, re.I):

        query = re.sub(r'(.*)(Dexter)?(.*)(search|look|find)+', '', data, 1, re.I)
        query = re.sub(r'( for | about | on )', '', query, 1, re.I)
        query = re.sub(r'( on | in )*( )*( my | the )*( )*(offline|computer|system|pc|laptop|desktop)', '', query, 1, re.I)

    if re.search(r'(.*)(Dexter)?(.*)(offline|computer|system|pc|laptop|desktop)(search)+( )*(for|on|about)(.*)', data, re.I):
        query = re.sub(r'(.*)(Dexter)?(.*)(offline|computer|system|pc|laptop|desktop)(search)+( )*(for|on|about)', '', data, 1, re.I)


    query = query.strip()

    dexSay.speak("Searching your computer for " + str(query), 'm', True)
    time.sleep(1)

    try:
        os.system('"' + utilityDIR + '\start.vbs' + '"')
    except:
        logger.info("An error has occurred")
    else:
        time.sleep(1)
        keyboard.write(query)

def dexSystemNoQuery():
    '''Ask user for query'''
    query = None
    dexSay.speak("Okay? what do you want me to search for? ", 'm', True)

    try:
        query = dexHear.listen(True)
    except OSError as e:
        if 'Invalid input device' in str(e):
            dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                         True)
        if 'Unanticipated host error' in str(e):
            dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                         True)
        if 'Stream closed' in str(e):
            dexSay.speak('Changing microphone.', 'f', True)

    if query == 'RequestError' or query == None:
        time.sleep(0.5)
        dexSay.speak('Something went wrong. Please type what you want to search for. ', 'm', True)
        query = input('>> ')

    dexSystemQuery(query)

#hey dexter please look for abc on my computer
#hey dexter please search for abc on my computer
#hey dexter please search for abc def in the computer
#hey dexter find abc on my laptop
#hey dexter please could you look for def abc on my pc
#hey dexter can you find abc on my laptop
