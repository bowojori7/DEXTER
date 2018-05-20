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
import os, inspect

dexSay = Mouth()
dexHear = Ears()

moduleID = '6'

activeReminderRegexes = [
    r'(.*)(remind)(.*)'
]

reminders = []


def getID():
    return moduleID


def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''
    if dexActive == False:
        return False
    if dexActive == True:
        for regex in activeReminderRegexes:
            if re.search(regex, data, re.I):
                return True

        return False


def handle(data, dexActive):
    '''
    1. Figure out what control function is needed
    2. Call the function
    '''

    for regex in activeReminderRegexes:
        if re.search(regex, data, re.I):
            success = dexReminder(data)
            if success == 'Failed':
                return None

            return 'task complete'


message = ''

# checkreminder() runs in a thread and checks for each reminder in the list if now.time = reminder.time
# if True then playReminder()
# if reminder.temporary = True then after playing the reminder delete it from the dictionary
def checkReminder():

    global reminders

    while (True):
        readReminders()
        now = time.localtime()

        if len(reminders) == 0:
            continue

        i = 0

        for reminder in reminders:
            global message
            thiselem = reminders[i]
            i = (i + 1) % len(reminders)
            nextelem = reminders[i]

            hour = reminder[1]
            minutes = reminder[2]
            days = reminder[3]
            dayofmonth = reminder[4]
            dayInYear = reminder[5]
            month = reminder[6]
            temporary = reminder[7]
            period = reminder[8]
            message = reminder[0]

            if hour == now.tm_hour and minutes == now.tm_min and dayInYear == now.tm_yday:
                if temporary == 'True':
                    reminders.remove(reminder)
                playReminder()
            elif hour == now.tm_hour and minutes == now.tm_min and dayInYear == 0:
                if dayofmonth == 0:
                    if month == 0:
                        if len(days) == 0:
                            if temporary == 'True':
                                reminders.remove(reminder)
                            playReminder()
                        else:
                            for day in days:
                                if any(['monday', 'mondays']) == day:
                                    if now.tm_wday == 0:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['tuesday', 'tuesdays']) == day:
                                    if now.tm_wday == 1:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['wednesday', 'wednesdays']) == day:
                                    if now.tm_wday == 2:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['thursday', 'thursdays']) == day:
                                    if now.tm_wday == 3:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['friday', 'fridays']) == day:
                                    if now.tm_wday == 4:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['saturday', 'saturdays']) == day:
                                    if now.tm_wday == 5:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['sunday', 'sundays']) == day:
                                    if now.tm_wday == 6:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['everyday', 'week']) == day:
                                    if temporary == 'True':
                                        reminders.remove(reminder)
                                    playReminder()
                    elif month == now.tm_mon:
                        if len(days) == 0:
                            if temporary == 'True':
                                reminders.remove(reminder)
                            playReminder()
                        else:
                            for day in days:
                                if any(['monday', 'mondays']) == day:
                                    if now.tm_wday == 0:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['tuesday', 'tuesdays']) == day:
                                    if now.tm_wday == 1:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['wednesday', 'wednesdays']) == day:
                                    if now.tm_wday == 2:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['thursday', 'thursdays']) == day:
                                    if now.tm_wday == 3:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['friday', 'fridays']) == day:
                                    if now.tm_wday == 4:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['saturday', 'saturdays']) == day:
                                    if now.tm_wday == 5:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['sunday', 'sundays']) == day:
                                    if now.tm_wday == 6:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['everyday', 'week']) == day:
                                    if temporary == 'True':
                                        reminders.remove(reminder)
                                    playReminder()
                elif dayofmonth == now.tm_mday:
                    if month == 0:
                        if len(days) == 0:
                            if temporary == 'True':
                                reminders.remove(reminder)
                            playReminder()
                        else:
                            for day in days:
                                if any(['monday', 'mondays']) == day:
                                    if now.tm_wday == 0:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['tuesday', 'tuesdays']) == day:
                                    if now.tm_wday == 1:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['wednesday', 'wednesdays']) == day:
                                    if now.tm_wday == 2:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['thursday', 'thursdays']) == day:
                                    if now.tm_wday == 3:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['friday', 'fridays']) == day:
                                    if now.tm_wday == 4:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['saturday', 'saturdays']) == day:
                                    if now.tm_wday == 5:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['sunday', 'sundays']) == day:
                                    if now.tm_wday == 6:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['everyday', 'week']) == day:
                                    if temporary == 'True':
                                        reminders.remove(reminder)
                                    playReminder()
                    elif month == now.tm_mon:
                        if len(days) == 0:
                            if temporary == 'True':
                                reminders.remove(reminder)
                            playReminder()
                        else:
                            for day in days:
                                if any(['monday', 'mondays']) == day:
                                    if now.tm_wday == 0:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['tuesday', 'tuesdays']) == day:
                                    if now.tm_wday == 1:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['wednesday', 'wednesdays']) == day:
                                    if now.tm_wday == 2:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['thursday', 'thursdays']) == day:
                                    if now.tm_wday == 3:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['friday', 'fridays']) == day:
                                    if now.tm_wday == 4:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['saturday', 'saturdays']) == day:
                                    if now.tm_wday == 5:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['sunday', 'sundays']) == day:
                                    if now.tm_wday == 6:
                                        if temporary == 'True':
                                            reminders.remove(reminder)
                                        playReminder()
                                if any(['everyday', 'week']) == day:
                                    if temporary == 'True':
                                        reminders.remove(reminder)
                                    playReminder()

        saveReminders(reminders)
        time.sleep(1)


        # def playReminder(). To sound reminder. Show snooze and stop button.
        # snooze is a constant variable it's always 10minutes - 600 seconds.
        # snooze = 10; make button for snooze and stop
        # if snooze is pressed then make dexter say "Okay, i'll wake you up again in 10 minutes"
        # then sleep play reminder for 10 minutes and call play reminder again
        # if stop is pressed then break out of the loop playing the sound


reminderThread = threading.Thread(target=checkReminder)
def dexReminder(data):
    reminder = getReminder(data)

    if reminder == None:
        return 'Failed'
    setReminder(reminder)

    if reminderThread.isAlive():
        pass
    else:
        reminderThread.start()

    return 'succeeded'


def triggerCheckReminder():

    if reminderThread.isAlive():
        pass
    else:
        reminderThread.start()


def saveReminders(reminders):
    DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    with open(DIR+'\\reminders.txt', 'w') as reminderfile:
        json.dump(reminders, reminderfile)


def readReminders():
    DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    global reminders
    try:
        with open(DIR+'\\reminders.txt') as reminderfile:
            reminders = json.load(reminderfile)
    except ValueError:
        reminders = []
    except:
        saveReminders(reminders)
        readReminders()



#def getreminder(data)
        #extracts reminder time and day from user input
        #if day is not in input then save only current day in days and temporary = true.
        #if tomorrow is in input then temporary = true
        #if day/days from now in input then temporary = true


def getReminder(data):
    hour = 0
    minutes = 0
    days = []
    dayofmonth = ''
    daysFromNow = 0
    month = ''
    temporary = 'True'
    period = None
    message = None

    weekdays = ['on monday', 'on tuesday', 'on wednesday', 'on thursday', 'on friday', 'on saturday', 'on sunday']
    specialdays = ['throughout the week', 'all through the week', 'throughout this week', 'all through this week', 'next week', 'tomorrow']

    data = data.lower()

    if ('to' in data or 'about' in data) and 'on' in data and 'at' not in data:
        message = re.findall(r'(to|about) (.*) on', data, re.I)
        message = message[0][1]
        if re.search(r'on(.*)[0-9]', message, re.I):
            message = re.findall(r'^(.*)on(.*)[0-9]', message, re.I)
            message = message[0][0]
        for weekday in weekdays:
            if weekday in message:
                message = re.findall(r'^(.*)('+weekday+')', message, re.I)
                message = message[0][0]



    if ('to' in data or 'about' in data) and 'at' in data:
        message = re.findall(r'(to|about)(.*)at', data, re.I)
        message = message[0][1]
        message = message.strip()
        if re.search(r'on(.*)[0-9]', message, re.I):
            message = re.findall(r'^(.*)on(.*)[0-9]', message, re.I)
            message = message[0][0]
        for weekday in weekdays:
            if weekday in message:
                message = re.findall(r'^(.*)('+weekday+')', message, re.I)
                message = message[0][0]


    # if ('to' in data or 'about' in data) and any(specialday in data for specialday in specialdays) and not any(day in data for day in weekdays):
    #     for specialday in specialdays:
    #         message = re.findall(r'(to|about)(.*)'+specialday, data, re.I)
    #         if len(message) > 0:
    #             break
    #     message = message[0][1]
    #     message = message.strip()


    keywords = ['tomorrow', 'a.m.', 'p.m.', 'every','am','pm','monday','mondays','tuesday','tuesdays','wednesday','wednesdays',
                'thursday','thursdays', 'friday','fridays','saturday','saturdays','sunday','sundays','everyday',
                'day','days','minute','minutes', 'all' ,'through', 'throughout',
                'all through this week', 'next', 'week', 'now',
                'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                'november', 'december']

    realQuery = []


    query = data
    query = query.split()

    splitmsg = message.split()

    for msg in splitmsg:
        for word in query:
            if word == msg:
                query.remove(word)
                break


    i = 0

    for word in query:
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
    for word in query:
        if word.isdigit():
            realQuery.append(word)
            break
    for word in query:
        for keyword in keywords:
            if word == keyword:
                realQuery.append(word)
                break
    for word in query:
        if word.endswith(('st', 'nd', 'rd', 'th')):
            if word != 'remind':
                realQuery.append(word)
            break

    print(realQuery)


    if 'am' in query or 'a.m.' in query:
        period = 'am'
    elif 'pm' in query or 'p.m.' in query:
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


        if period == 'RequestError' or period == None:
            dexSay.speak('Something went wrong.', 'm', True)
            return

        if period not in ['am', 'pm', 'p.m.', 'pma', 'a.m.', 'iain', 'pain', 'ian', 'em']:
            dexSay.speak('That\'s an invalid answer. Terminating reminder creation', 'm', True)
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
        if word.isdigit() and (nextelem in ['am', 'pm', 'a.m.', 'p.m.', 'o', 'oh', '0']):
            hour = word
        if word.isdigit() and nextelem == ':':
            hour = word
        if word.isdigit() and nextelem.isdigit():
            hour = word
        if word.isdigit() and nextelem in ['day', 'days']:
            daysFromNow = word
        if word == 'tomorrow':
            currDay = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            currNo = time.localtime().tm_wday

            if currNo == 6:
                tmrwDay = currDay[0]
            else:
                tmrwDay = currDay[currNo+1]
            days.append(tmrwDay)
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
        if word in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                'november', 'december']:
            month = word
        if word.endswith(('st', 'nd', 'rd', 'th')):
            dayofmonth = word

    message = message.strip()
    reminder = [message, hour, minutes, days, dayofmonth, daysFromNow, month, temporary, period]
    print(reminder)
    return reminder


#def setreminder(hour, minutes, days)
        #gets parameters from getreminder
        #setreminder() saves reminder in dictionary.
def setReminder(reminder):
    global reminders
    readReminders()

    now = time.localtime()

    hour = reminder[1]
    minutes = reminder[2]
    days = reminder[3]
    dayofmonth = reminder[4]
    daysFromNow = reminder[5]
    month = reminder[6]
    temporary = reminder[7]
    period = reminder[8]
    message = reminder[0]

    if int(reminder[5]) == 0:
        dayInYear = 0
    else:
        dayInYear = int(reminder[5])+now.tm_yday

    if dayInYear > 356:
        dayInYear = dayInYear-356

    if period == 'am':
        if int(hour) == 12:
            hour = 0

    if period == 'pm':
        if int(hour) < 12:
            hour = int(hour) + 12

    hour = int(hour)
    minutes = int(minutes)

    if dayofmonth.endswith(('st','nd','rd','th')):
        mday = re.sub(r'(st|nd|rd|th)', '', dayofmonth, re.I)
        mday = int(mday)
    else:
        mday = 0

    if month == 'january':
        month = 1
    elif month == 'february':
        month = 2
    elif month == 'march':
        month = 3
    elif month == 'april':
        month = 4
    elif month == 'may':
        month = 5
    elif month == 'june':
        month = 6
    elif month == 'july':
        month = 7
    elif month == 'august':
        month = 8
    elif month == 'september':
        month = 9
    elif month == 'october':
        month = 10
    elif month == 'november':
        month = 11
    elif month == 'december':
        month = 12
    else:
        month = 0

    reminder[1] = hour
    reminder[2] = minutes
    reminder[5] = dayInYear
    reminder[4] = mday
    reminder[6] = month

    reminders.append(reminder)
    saveReminders(reminders)

    dexSay.speak('Okay, I set a reminder for '+ message, 'm', True)




play = 1
snooze = 0

def playReminder():
    global play
    global snooze

    snoozeTime = 600

    GUIThread = threading.Thread(target=reminderWindow)
    GUIThread.start()


    while play == 1:
        winsound.Beep(440, 250)
        time.sleep(0.25)

        if snooze == 1:
            dexSay.speak("Okay, I'll remind you again in 10 minutes", 'm', True)
            time.sleep(snoozeTime)
            snooze = 0
            playReminder()

    play = 1
    return


class DexReminderGUI(QMainWindow):

    def __init__(self):
        super(DexReminderGUI, self).__init__()
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
        global message
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

        font.setPixelSize(17)
        label3 = QLabel(message.upper())
        label3.setAlignment(Qt.AlignCenter)
        label3.setFont(font)
        self.setforeColor(label3)
        MainFrameLayout.addWidget(label3)


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
            mainWindow = DexReminderGUI()

            sys.exit(app.exec_())


def reminderWindow():
    if play == 1:
        reminderGUI = GUIThread()
        reminderGUI.run()
    return
