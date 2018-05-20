import regex as re
from Mouth import Mouth
from Ears import Ears
import time
import os
import winshell
from winreg import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


dexSay = Mouth()
dexHear = Ears()

moduleID = '8'

activeSystemLocationRegexes = [
    r'(.*)(Dexter)?(.*)(open)+(.*)',
]

def getID():
    return moduleID

def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''
    if dexActive == False:
        return False
    if dexActive == True:
        for regex in activeSystemLocationRegexes:
            if re.search(regex, data, re.I):
                return True

        return False


def handle(data, dexActive):
    '''
    1. Figure out what control function is needed
    2. Call the function
    '''
    logger.info(data)
    for regex in activeSystemLocationRegexes:
        if re.search(regex, data, re.I):
            dexSystemLocation(data)
            return 'task complete'



def dexSystemLocation(data):
    query = data
    query = re.sub(r'(.*)(Dexter)?(.*)(open)+( )*', '', data, 1)

    if 'music' in query.lower():
        dexSay.speak('Opening Music Folder', 'm', True)
        time.sleep(2)
        os.startfile(winshell.folder('mymusic'))

    if 'picture' in query.lower():
        dexSay.speak('Opening Pictures Folder', 'm', True)
        time.sleep(2)
        os.startfile(winshell.folder('mypictures'))

    if 'video' in query.lower():
        dexSay.speak('Opening Video Folder', 'm', True)
        time.sleep(2)
        os.startfile(winshell.folder('myvideo'))

    if 'documents' in query.lower():
        dexSay.speak('Opening Documents Folder', 'm', True)
        time.sleep(2)
        os.startfile(winshell.folder('personal'))

    if re.search(r'program file', query, re.I):
        dexSay.speak('Opening Program Files', 'm', True)
        time.sleep(2)
        os.startfile(winshell.folder('program_files'))

    if re.search(r'(86|eighty six)', query, re.I):
        dexSay.speak('Opening Program Files x 86', 'm', True)
        time.sleep(2)
        os.startfile(winshell.folder('program_filesx86'))

    if re.search(r'control panel', query, re.I):
        dexSay.speak('Opening Control panel', 'm', True)
        time.sleep(2)
        os.system('{0}\\System32\\control.exe'.format(os.environ['WINDIR']))

    if re.search(r'my computer', query, re.I):
        dexSay.speak('Opening My Computer', 'm', True)
        time.sleep(2)
        os.system('%WinDir%\explorer.exe /e,::{20d04fe0-3aea-1069-a2d8-08002b30309d}')

    if re.search(r'drive', query, re.I):
        query = re.sub('( )*drive( )*', '', query)
        dexSay.speak('Opening your ' + query.lower() + ' drive', 'm', True)
        time.sleep(2)
        try:
            os.startfile(query.upper() + ':')
        except:
            dexSay.speak('Sorry, Can\'t find the drive on your computer', 'm', True)
    if re.search('document', query):
        dexSay.speak('Opening Documents Folder', 'm', True)
        time.sleep(2)
        os.startfile(winshell.folder('personal'))

    if re.search('download', query, re.I):
        dexSay.speak('Opening Downloads folder', 'm', True)
        time.sleep(2)
        with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
            Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]

        os.startfile(Downloads)

