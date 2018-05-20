import re
from Mouth import Mouth
from Ears import Ears
import time
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import winsound
import threading
import json
import logging
import os
import inspect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dexSay = Mouth()
dexHear = Ears()

moduleID = '10'

activeAlarmRegexes = [
    r'(.*)(set)(.*)(alarm)(.*)',
]

Alarms = []


def getID():
    return moduleID


def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''
    if dexActive == False:
        return False
    if dexActive == True:
        for regex in activeAlarmRegexes:
            if re.search(regex, data, re.I):
                return True

        return False


def handle(data, dexActive):
    '''
    1. Figure out what control function is needed
    2. Call the function
    '''

    for regex in activeAlarmRegexes:
        if re.search(regex, data, re.I):
            success = dexAlarm(data)
            if success == 'Failed':
                return None

            return 'task complete'


# checkAlarm() runs in a thread and checks for each alarm in the dictionary if now.time = alarm.time
# if True then playAlarm()
# if alarm.temporary = True then after playing the alarm delete it from the dictionary
def checkAlarm():

    global Alarms

    while (True):
        readAlarms()
        now = time.localtime()

        if len(Alarms) == 0:
            continue

        i = 0

        for alarm in Alarms:
            thiselem = Alarms[i]
            i = (i + 1) % len(Alarms)
            nextelem = Alarms[i]

            hour = alarm[0]
            minutes = alarm[1]
            days = alarm[2]
            temporary = alarm[3]
            dayInYear = alarm[4]
            period = alarm[5]



            if hour == now.tm_hour and minutes == now.tm_min and dayInYear == now.tm_yday:
                if temporary == 'True':
                    Alarms.remove(alarm)
                playAlarm()
            elif hour == now.tm_hour and minutes == now.tm_min and dayInYear == 0:
                if len(days) == 0:
                    if temporary == 'True':
                        Alarms.remove(alarm)
                    playAlarm()
                else:
                    for day in days:
                        if any(['monday', 'mondays']) == day:
                            if now.tm_wday == 0:
                                if temporary == 'True':
                                    Alarms.remove(alarm)
                                playAlarm()
                        if any(['tuesday', 'tuesdays']) == day:
                            if now.tm_wday == 1:
                                if temporary == 'True':
                                    Alarms.remove(alarm)
                                playAlarm()
                        if any(['wednesday', 'wednesdays']) == day:
                            if now.tm_wday == 2:
                                if temporary == 'True':
                                    Alarms.remove(alarm)
                                playAlarm()
                        if any(['thursday', 'thursdays']) == day:
                            if now.tm_wday == 3:
                                if temporary == 'True':
                                    Alarms.remove(alarm)
                                playAlarm()
                        if any(['friday', 'fridays']) == day:
                            if now.tm_wday == 4:
                                if temporary == 'True':
                                    Alarms.remove(alarm)
                                playAlarm()
                        if any(['saturday', 'saturdays']) == day:
                            if now.tm_wday == 5:
                                if temporary == 'True':
                                    Alarms.remove(alarm)
                                playAlarm()
                        if any(['sunday', 'sundays']) == day:
                            if now.tm_wday == 6:
                                if temporary == 'True':
                                    Alarms.remove(alarm)
                                playAlarm()
                        if any(['everyday', 'week']) == day:
                            if temporary == 'True':
                                Alarms.remove(alarm)
                            playAlarm()
        saveAlarms(Alarms)
        time.sleep(1)


        # def playAlarm(). To sound alarm. Show snooze and stop button.
        # snooze is a constant variable it's always 10minutes - 600 seconds.
        # snooze = 10; make button for snooze and stop
        # if snooze is pressed then make dexter say "Okay, i'll wake you up again in 10 minutes"
        # then sleep play alarm for 10 minutes and call play alarm again
        # if stop is pressed then break out of the loop playing the sound


alarmThread = threading.Thread(target=checkAlarm)
def dexAlarm(data):
    alarm = getAlarm(data)

    if alarm == None:
        return 'Failed'
    setAlarm(alarm)

    if alarmThread.isAlive():
        pass
    else:
        alarmThread.start()

    return 'succeeded'


def triggerCheckAlarm():
    if alarmThread.isAlive():
        pass
    else:
        alarmThread.start()


def saveAlarms(Alarms):
    DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    with open(DIR+'\Alarms.txt', 'w') as Alarmfile:
        json.dump(Alarms, Alarmfile)



def readAlarms():
    global Alarms
    DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    try:
        with open(DIR+'\Alarms.txt') as Alarmfile:
            Alarms = json.load(Alarmfile)
    except ValueError:
        Alarms = []
    except:
        saveAlarms(Alarms)
        readAlarms()



#def getAlarm(data)
        #extracts alarm time and day from user input
        #if day is not in input then save only current day in days and temporary = true.
        #if tomorrow is in input then temporary = true
        #if day/days from now in input then temporary = true


def getAlarm(data):
    query = data
    hour = 0
    minutes = 0
    days = []
    temporary = 'True'
    daysFromNow = 0
    period = None

    keywords = ['a.m.', 'p.m.', 'every','am','pm','monday','mondays','tuesday','tuesdays','wednesday','wednesdays','thursday','thursdays', 'friday','fridays','saturday','saturdays','sunday','sundays','week','everyday','tomorrow','day','days','minute','minutes']

    realQuery = []

    query = query.split()
    i = 0

    for word in query:
        for keyword in keywords:
            if ':' in word:
                HM = word.split(':')
                HM.append(':')
                temp = HM[1]
                HM[1] = HM[2]
                HM[2] = temp
                realQuery.append(HM[0])
                realQuery.append(HM[1])
                realQuery.append(HM[2])
                realQuery.append('minutes')
                break
            if word.isdigit():
                realQuery.append(word)
                break
            if word == keyword:
                realQuery.append(word)

    if 'am' in realQuery or 'a.m.' in realQuery:
        period = 'am'
    elif 'pm' in realQuery or 'p.m.' in realQuery:
        period = 'pm'
    else:
        dexSay.speak('a.m. or p.m. ?', 'm', True)

        try:
            period = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        logger.info(period)

        if period == 'RequestError' or period == None:
            dexSay.speak('Something went wrong.', 'm', True)
            return

        if period not in ['am', 'pm', 'p.m.', 'pma', 'a.m.', 'iain', 'pain', 'ian', 'em']:
            dexSay.speak('That\'s an invalid answer. Terminating alarm creation', 'm', True)
            return

        if period in ['am', 'em', 'a.m.', 'ian', 'iain']:
            period = 'am'
        else:
            period = 'pm'

    for word in realQuery:
        thiselem = realQuery[i]
        i = (i + 1) % len(realQuery)
        nextelem = realQuery[i]

        if (word.isdigit() and nextelem in ['minutes', 'minute']) or (thiselem == ':' and nextelem.isdigit()):
            if word.isdigit():
                minutes = word
            else:
                minutes = nextelem
        if word.isdigit() and (nextelem in ['am', 'pm', 'o', 'oh', '0']):
            hour = word
        if word.isdigit() and nextelem == ':':
            hour = word
        if word.isdigit() and nextelem.isdigit():
            hour = word
        if word.isdigit() and nextelem in ['day', 'days']:
            daysFromNow = word
        if word in ['monday', 'friday', 'tuesday', 'saturday', 'wednesday', 'sunday', 'thursday']:
            days.append(word)
        if word in ['mondays', 'fridays', 'tuesdays', 'saturdays', 'wednesdays', 'sundays', 'thursdays']:
            days.append(word)
            temporary = 'False'
        if word in ['everyday', 'week']:
            days.append(word)
            temporary = 'False'
        if 'every' == word:
            temporary = 'False'



    alarm = [hour, minutes, days, temporary, daysFromNow, period]
    return alarm


#def setAlarm(hour, minutes, days)
        #gets parameters from getAlarm
        #setAlarm() saves alarm in dictionary.
def setAlarm(alarm):
    global Alarms
    readAlarms()

    now = time.localtime()

    hour = alarm[0]
    minutes = alarm[1]
    days = alarm[2]
    temporary = alarm[3]
    if int(alarm[4]) == 0:
        dayInYear = 0
    else:
        dayInYear = int(alarm[4])+now.tm_yday

    if dayInYear > 356:
        dayInYear = dayInYear-356
    period = alarm[5]

    if period == 'am':
        if int(hour) == 12:
            hour = 0

    if period == 'pm':
        if int(hour) < 12:
            hour = int(hour) + 12

    hour = int(hour)
    minutes =  int(minutes)

    alarm[0] = hour
    alarm[1] = minutes
    alarm[4] = dayInYear

    Alarms.append(alarm)
    saveAlarms(Alarms)

    dexSay.speak('I set your alarm for ' + str(hour-12 if hour>12 else hour) + ":" + str(format(minutes, '02d')) + ' ' + ('p.m.' if period == 'pm' else 'a.m.'), 'm', True)




play = 1
snooze = 0

def playAlarm():
    global play
    global snooze

    snoozeTime = 600

    GUIThread = threading.Thread(target=alarmWindow)
    GUIThread.start()


    while play == 1:
        winsound.Beep(440, 250)
        time.sleep(0.25)

        if snooze == 1:
            dexSay.speak("Okay, I'll remind you again in 10 minutes", 'm', True)
            time.sleep(snoozeTime)
            snooze = 0
            playAlarm()

    play = 1
    return


class DexAlarmGUI(QMainWindow):

    def __init__(self):
        super(DexAlarmGUI, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(Qt.StrongFocus)
        self.activateWindow()
        self.initUI()


    def setbackColor(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.black)
        self.setPalette(palette)

    def setforeColor(self, object):
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.white)
        object.setPalette(palette)



    def initUI(self):
        now = time.localtime()

        MainFrame = QFrame(self)
        self.setCentralWidget(MainFrame)
        MainFrameLayout = QVBoxLayout(MainFrame)

        self.setbackColor()

        font = QFont()
        font.setFamily('Helvetica')
        font.setBold(True)


        font.setPixelSize(20)
        label = QLabel('DEXTER')
        label.setAlignment(Qt.AlignCenter)
        label.setFont(font)
        self.setforeColor(label)
        MainFrameLayout.addWidget(label)


        font.setPixelSize(15)
        label2 = QLabel(str(now.tm_hour if now.tm_hour <= 12 else now.tm_hour - 12) +
                        ' : ' + str(format(now.tm_min, '02d')))
        label2.setAlignment(Qt.AlignCenter)
        label2.setFont(font)
        self.setforeColor(label2)
        MainFrameLayout.addWidget(label2)


        font.setPixelSize(13)
        label2 = QLabel('PRESS SPACE TO SNOOZE, ESC TO EXIT')
        label2.setAlignment(Qt.AlignCenter)
        label2.setFont(font)
        self.setforeColor(label2)
        MainFrameLayout.addWidget(label2)


        self.setGeometry(0, 0, 300, 100)

        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                        (resolution.height() / 2) - (self.frameSize().height() / 2))

        self.show()

    def keyPressEvent(self, event):
        global snooze
        global play

        if event.key() == Qt.Key_Escape:
            play = 0
            self.close()
        if event.key() == Qt.Key_Space:
            snooze = 1
            self.close()


    def closeEvent(self, event):
        pass


class GUIThread(QThread):

    def __init__(self):
        QThread.__init__(self)


    def run(self):
        if play == 1:
            app = QApplication(sys.argv)
            mainWindow = DexAlarmGUI()

            sys.exit(app.exec_())


def alarmWindow():
    if play == 1:
        alarmGUI = GUIThread()
        alarmGUI.run()
    return
