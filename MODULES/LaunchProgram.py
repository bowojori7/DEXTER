import regex as re
from Mouth import Mouth
from Ears import Ears
import time
import os
import winshell
from MODULES import SystemSearch
import logging
import threading
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

curfilePath = os.path.abspath(__file__)
curDir = os.path.abspath(os.path.join(curfilePath,os.pardir))
parentDir = os.path.abspath(os.path.join(curDir,os.pardir))
GUIdir = parentDir + '\GUIS'


dexSay = Mouth()
dexHear = Ears()

moduleID = '7'

def getID():
    return moduleID


def validate(data, dexActive):

    '''Return true if the module can be used to handle the input'''
    if dexActive == False:
        return False

    if dexActive == True:
        for regex in activeProgramLaunchRegexes:

            if re.search(r'(.*)(Dexter)?(.*)(open|launch|start)+( )*', data, re.I):
                reg = re.sub(r'(.*)(Dexter)?(.*)(open|launch|start)+( )*', '', data, 1, re.I)
                for item in programNameList:
                    if reg.lower() in item.lower():
                        return True

        return False


def handle(data, dexActive):
    for regex in activeProgramLaunchRegexes:
        if re.search(r'(.*)(Dexter)?(.*)(open|launch|start)+( )*', data, re.I):
            dexLaunchProgram(data)
            return 'task complete'


def populateProgramList():
    shortcuts = {}
    programpaths = {}

    user_programs = winshell.programs()
    for dirpath, dirnames, filenames in os.walk(user_programs):
        relpath = dirpath[1 + len(user_programs):]
        shortcuts.setdefault(
            relpath, []
        ).extend(
            [winshell.shortcut(os.path.join(dirpath, f)) for f in filenames]
        )

    all_programs = winshell.programs(common=1)
    for dirpath, dirnames, filenames in os.walk(all_programs):
        relpath = dirpath[1 + len(all_programs):]
        shortcuts.setdefault(
            relpath, []
        ).extend(
            [winshell.shortcut(os.path.join(dirpath, f)) for f in filenames]
        )

    for relpath, lnks in sorted(shortcuts.items()):
        level = relpath.count("\\")
        if level == 0:
            print("")
        #print("%s+ %s" % ("    " * level, relpath))

        for lnk in lnks:
            name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
            #print("%s* %s -> %s" % ("    " * (level + 1), name, lnk.path))
            programpaths[name] = lnk.lnk_filepath

    programpaths = sorted(programpaths.items())

    '''
    for program, path in programpaths:
        if '.exe' in path:
            print(program)
            print(path)
    '''
    return programpaths


def dexLaunchProgram(data):
    '''
    1. search the 'programs' part of the programpaths dictionary for the user query with regexes
    2. save the resulting program and its path in another ordered dictionary
    3. show the user if there is more than one result
    4. Number the results and ask the user to pick a number
    5. If the number is chosen run whatever is in the path of the dict object of that number
    '''
    i = 1
    query = data
    query = re.sub(r'(.*)(Dexter)?(.*)(open|launch|start)+( )*', '', data, 1, re.I)
    foundProgramList = []
    pathsfound = []
    global globalFoundProgramList
    logger.info(query)


    for name in programNameList:
        query = query.lower()
        name = name.lower()
        querySplit = query.split()
        programNameSplit = name.split()

        if set(querySplit).intersection(set(programNameSplit)) != set():
            foundProgramList.append(name)


    if len(foundProgramList) == 0:
        dexSay.speak('Sorry, I couldn\'t find that program', 'm', True)
        time.sleep(1)
        dexSay.speak('Let me search for it', 'm', True)
        SystemSearch.handle('search my computer for ' + query, True)
        return

    if len(foundProgramList) == 1:
        for program, path in programDictionary:
            if program.lower() == foundProgramList[0].lower():
                dexSay.speak('Opening ' + program, 'm', True)
                programThread = threading.Thread(target=launchProgram, args=(path, ))
                programThread.isDaemon = True
                programThread.start()
                return

    if len(foundProgramList) > 1:
        for program, path in programDictionary:
            for name in foundProgramList:
                if program.lower() == name.lower():

                    pathsfound.append(path)
                    i = i+1

        process = subprocess.Popen(['python', GUIdir + "\programsGUI.py"] + foundProgramList)

        dexSay.speak('Which one should I open?', 'm', True)

        try:
            number = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        if number == 'RequestError' or number == None:
            time.sleep(0.5)
            dexSay.speak('Something went wrong.', 'm', True)

            process.kill()
            return

        if number.isalpha():
            number = text2int(number)
        elif not number.isdigit():
            number = text2int(number)

        if number == 0:
            dexSay.speak('Sorry, thats an invalid option', 'm', True)

            process.kill()
            return

        number = int(number) - 1
        for program, path in programDictionary:
            try:
                if path == pathsfound[number]:

                    process.kill()

                    dexSay.speak('Opening ' + program, 'm', True)

                    programThread = threading.Thread(target=launchProgram, args=(path,))
                    programThread.isDaemon = True
                    programThread.start()


                    return
            except:
                dexSay.speak("You didn't pick a valid option", 'm', True)
                process.kill()
                return



def launchProgram(path):
    os.startfile(path)
    return

def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            print(textnum)
            textnum = re.sub(word+' ', '', textnum)
            print(textnum)
            continue

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current




programDictionary = populateProgramList()
programNameList = []

for program, path in programDictionary:
    if '.lnk' in path:
        programNameList.append(program)

activeProgramLaunchRegexes = [
    r'(.*)(Dexter)?(.*)(open|launch|start)+( )*'+r"(?=(" + '|'.join(programNameList) + r"))"
]


