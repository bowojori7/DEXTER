import re
from Mouth import Mouth
from Ears import Ears
from MODULES import SystemSearch
from MODULES import OnlineSearch
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dexSay = Mouth()
dexHear = Ears()

moduleID = '9'

activeSearchRegexes = [
    r'(.*)(Dexter)?(.*)(search|look|find)+(.*)',
    r'(.*)(what |who |where |when |how |is |are |do |does |can |will |if |would |could| did)+(.*)'
]

def getID():
    return moduleID

def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''
    if dexActive == False:
        return False

    if dexActive == True:
        for regex in activeSearchRegexes:
            if re.search(regex, data, re.I):
                return True

        return False

def handle(data, dexActive):
    '''
    1. Figure out what control function is needed
    2. Call the function
    '''
    logger.info(data)

    for regex in activeSearchRegexes:
        if re.search(regex, data, re.I):
            dexSearch(data)
            return 'task complete'


def dexSearch(data):
    '''Open Start Menu and search for query'''

    query = data

    if re.search(r'(.*)(what |who |where |when |how |is |are |do |does |can |will |if |would |could |did )+(.*)', data, re.I):
        query = re.findall(r'(.*)(Dexter)?(.*)(what |who |where |when |how |is |are |do |does |can |will |if |would |could |did )(.*)', query, re.I)
        query1Split = query[0][0].split()
        if query1Split != '' and len(query1Split) !=0:
            query1Split = query1Split[-1]
        else:
            query1Split = ''
        query = query1Split + ' ' + query[0][3] + query[0][4]
        OnlineSearch.handle('search google for ' + query, True)

    elif re.search(r'(.*)(Dexter)?(.*)(search|look|find)+(.*)', data, re.I):
        query = re.sub(r'(.*)(Dexter)?(.*)(search|look|find)+', '', data, 1, re.I)
        query = re.sub(r'( for | about | on )', '', query, 1, re.I)

        query = query.strip()

        dexSay.speak("Should I search the internet or your computer? ", 'm', True)
        try:
            option = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        if option == 'RequestError' or option == None:
            dexSay.speak('Something went wrong. Please type where you want me to search. ', 'm', True)
            option = input('>> ')

        if re.search(r'(offline|computer|system|pc|laptop|desktop)', option, re.I):
            SystemSearch.handle('search my computer for ' + query, True)
        elif re.search(r'(google|internet|online|web)', option, re.I):
            OnlineSearch.handle('search google for ' + query, True)
        elif re.search(r'(wikipedia|wiki)', option, re.I):
            OnlineSearch.handle('search wikipedia for ' + query, True)
        else:
            dexSay.speak('Sorry, couldn\'t get that', 'm', True)

