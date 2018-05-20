import re
from Mouth import Mouth
from Ears import Ears
import time
import os
import inspect
import webbrowser
import wikipedia


DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
utilityDIR = DIR + '\\UTILITIES'

dexSay = Mouth()
dexHear = Ears()

moduleID = '4'
'''
passiveWebSearchRegexes = [
    r'(hey|hi|hello|what\'s up)( )*Dexter(.*)(search|look|find)+(.*)(on|in)*(.*)(my|the)*( )*(google|internet|wikipedia|wiki|online|web|youtube)(.*)',
    r'(hey|hi|hello|what\'s up)( )*Dexter(.*)(google|internet|wikipedia|wiki|online|web|youtube)( )*(search)+( )*(for|on|about)(.*)'
]
'''
activeWebSearchRegexes = [
    r'(.*)(Dexter)?(.*)(search|look|find)+(.*)(on|in)*(.*)(my|the)*( )*(google|internet|wikipedia|wiki|online|web|youtube)(.*)',
    r'(.*)(Dexter)?(.*)(google|internet|wikipedia|wiki|online|web|youtube)( )*(search)?( )*(for|on|about)(.*)'
]

searchWithQueryRegexes = [r'(.*)(Dexter)?(.*)(search|look|find)+(.*)(on|in)*(.*)(my|the)*( )*(google|internet|wikipedia|wiki|online|web|youtube)(.*)',
                          r'(.*)(Dexter)?(.*)(google|internet|wikipedia|wiki|online|web|youtube)( )*(search)?( )*(for|on|about)(.*)'
]
searchWithoutQueryRegexes =  [r'(.*)(Dexter)?(.*)(google|internet|wikipedia|wiki|online|web|youtube)( )*(search)?( )*(for|on|about)$',
                              r'(.*)(Dexter)?(.*)(search)( )*(the)*( )*(google|internet|wikipedia|wiki|online|web|youtube)( )*(for|on|about)$'
]

def getID():
    return moduleID

def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''
    if dexActive == False:
        '''
        for regex in passiveWebSearchRegexes:
            if re.search(regex, data, re.I):
                return True
        '''

        return False
    if dexActive == True:
        for regex in activeWebSearchRegexes:
            if re.search(regex, data, re.I):
                return True

        return False

def handle(data, dexActive):
    '''
    1. Figure out what control function is needed
    2. Call the function
    '''
    print(data)
    for regex in searchWithoutQueryRegexes:
        if re.search(regex, data, re.I):
            dexOnlineNoQuery()
            return 'task complete'

    for regex in searchWithQueryRegexes:
        if re.search(regex, data, re.I):
            dexOnlineQuery(data)
            return 'task complete'


def dexOnlineQuery(data):
    '''Open Start Menu and search for query'''
    query = data

    if re.search(r'(.*)(Dexter)?(.*)(search|look|find)+(.*)(on|in)*(.*)(my|the)*( )*(google|internet|wikipedia|wiki|online|web|youtube)(.*)', data):
        query = re.sub(r'(.*)(Dexter)?(.*)(search|look|find)+', '', data, 1)
        query = re.sub(r'( for | about | on )', '', query, 1)
        query = re.sub(r'( on | in )*( )*( my | the )*( )*(google|internet|wikipedia|wiki|online|web|youtube)', '', query, 1)

    if re.search(r'(.*)(Dexter)?(.*)(google|internet|wikipedia|wiki|online|web|youtube)(search)?( )*(for|on|about)(.*)', data):
        query = re.sub(r'(.*)(Dexter)?(.*)(google|internet|wikipedia|wiki|online|web|youtube)(search)?( )*(for|on|about)', '', data, 1)


    query = query.strip()
    if 'wiki' in data:
        dexSay.speak("Searching wikipedia for " + str(query), 'm', True)
        time.sleep(1)

        wikipedia.set_lang("en")

        url = "https://en.wikipedia.org/wiki/{}".format(query)
        webbrowser.open(url)

        answer = wikipedia.summary(query, sentences=2)
        dexSay.speak(answer, 'm', True)
    elif 'youtube' in data:
        dexSay.speak("Searching youtube for " + str(query), 'm', True)
        time.sleep(1)

        url = "https://www.youtube.com/results?search_query={}".format(query)
        webbrowser.open(url)

    else:
        dexSay.speak("Searching google for " + str(query), 'm', True)
        time.sleep(1)

        url = "https://www.google.com.tr/search?q={}".format(query)
        webbrowser.open(url)



def dexOnlineNoQuery():
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

    dexOnlineQuery(query)

#hey dexter please look for abc on my computer
#hey dexter please search for abc on my computer
#hey dexter please search for abc def in the computer
#hey dexter find abc on my laptop
#hey dexter please could you look for def abc on my pc
#hey dexter can you find abc on my laptop
#hey dexter do an internet search for abc
#hey dexter do an offline search for abc
