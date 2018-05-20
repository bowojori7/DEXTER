from Ears import Ears
from Mouth import Mouth
from FindModule import findModule
from FindModule import listModules
from MODULES import ActivateDex, DexAlarm, DexRemind, DexControl
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


from importlib import import_module
import time
import requests
import threading
import logging
import pythoncom
from pyHook import HookManager, GetKeyState, HookConstants
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dexSay = Mouth()
dexHear = Ears()

class Brain():
    def __init__(self):
        self.dexActive = False

        self.moduleList = listModules()
        self.activeModule = None

        self.workingInternet = None
        self.push2talk_active = False
        self.dexMode = None

    def dex_init(self):
        # '''Start dexter'''
        #
        self.backgroundChecks()

        dexSay.startMessage()

        GUIThread = threading.Thread(target=introWindow)
        GUIThread.start()

        self.workingInternet = self.checkInternet()
        time.sleep(1)
        if self.workingInternet:
            dexSay.speak('Connection Established', 'f', True)
            time.sleep(0.5)
        else:
            dexSay.speak('Connection failed', 'f', True)
            time.sleep(0.5)

        dexSay.speak("Starting Dexter", 'f', True)

        if os.path.isfile('DexMode.txt') == True:
            modeFile = open("DexMode.txt", 'r')
            if modeFile.read() == '2':
                dexSay.speak('Push to Talk mode activated', 'f', True)
                # dexSay.speak('Hold Control and caps lock twice to call me', 'm', True)
            else:
                dexSay.speak('Always listen mode activated', 'f', True)
                dexSay.greet()
            modeFile.close()

        self.run()

    def run(self):
        while True:
            if os.path.isfile('DexMode.txt') == False:
                DexControl.setMode(None)
            if os.path.isfile('DexMode.txt') == True:
                if os.stat('DexMode.txt').st_size == 0:
                    DexControl.setMode(None)

            modeFile = open("DexMode.txt", 'r')
            self.dexMode = modeFile.read()
            modeFile.close()

            if self.workingInternet == True:
                if self.dexMode == '2':
                    self.runPush2talk()
                else:
                    self.runInternet()
            else:
                self.runNoInternet()

    def runInternet(self):
        data = None

        try:
            data = dexHear.listen(self.dexActive)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f', self.dexActive)
                self.run()
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f', self.dexActive)
                self.run()
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', self.dexActive)
                self.run()

        if data == 'RequestError':
            self.workingInternet = False
            time.sleep(0.5)
            dexSay.speak('Internet connection lost', 'f', self.dexActive)
            self.run()
        elif data == None:
            self.run()
        else:
            logger.info(data)

        self.process(data)


    def runPush2talk(self):
        while True:
            if self.push2talk_active == True:
                self.push2talk_active = False
                break

        self.dexActive = True
        data = None

        try:
            data = dexHear.listen(self.dexActive)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             self.dexActive)
                self.run()
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             self.dexActive)
                self.run()
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', self.dexActive)
                self.run()

        if data == 'RequestError':
            self.workingInternet = False
            time.sleep(0.5)
            dexSay.speak('Internet connection lost', 'f', self.dexActive)
            self.run()
        elif data == None:
            self.run()
        else:
            logger.info(data)

        self.process(data)

    #
    # just keep checking the activated variable in the runpush to talk function in a while True loop
    #     so if the activated is 1 break out of the loop
    #     listen and do the same thing runInternet does blah blah
    #     and go back to run... just lilke runInternet
    # now the user ccan change modes
    # by saying dexter swith mode to ....
    # the switch mode function in the dex control module should just write to a file
    # at first the file is supposed to be empty( on the first ever run)
    # but if the file is not empty then its either 1- always listen or 2 - push to talk
    # The brain then checks this file everytime run runs to see what mode should be used.


    def OnKeyboardEvent(self, event):
        self.push2talk_active = False
        # in case you want to debug: uncomment next line
        # print repr(event), event.KeyID, HookConstants.IDToName(event.KeyID), event.ScanCode , event.Ascii, event.flags
        try:
            if GetKeyState(HookConstants.VKeyToID('VK_CAPITAL')) and GetKeyState(HookConstants.VKeyToID('VK_CONTROL')):
                self.push2talk_active = True

            if self.push2talk_active == True:
                logger.info('shortcut activated')
        except:
            pass
        return True


    def runNoInternet(self):
        while True:
            self.checkInternet()
            if self.workingInternet == False:
                continue
            if self.workingInternet == True:
                break

        self.run()


    def process(self, data):
        '''
        Process the input data

        check if it was only the trigger keyword that was said (if the moduleAccept = 0)
        if it was then make dexActive true and play a double beep.
        listen with the run() function again

        Check the module to use to handle the data
        Handle the data by calling the modules handle function

        '''
        result = None

        self.activeModule = findModule(data, self.dexActive)


        if self.activeModule == False:
            '''The appropriate module for handling the function was not found'''
            logger.info("module not found")
            dexSay.speak("Sorry, I dont know how to handle "+ data +" yet", 'm', self.dexActive)
            self.dexActive = False
        else:
            '''Handle the data by calling the modules handle function'''

            module = self.moduleList[int(self.activeModule)]

            mod = import_module(module)
            handle = getattr(mod, 'handle')

            if self.activeModule == '1':
                self.dexActive = ActivateDex.handle(data, self.dexActive)

                self.run()
            elif self.activeModule == '1':
                self.dexActive = handle(data, self.dexActive)
            else:
                result = handle(data, self.dexActive)
                print(result)
            '''Recheck for internet connection'''
            self.workingInternet = self.checkInternet()

            if result == 'task complete':
                self.dexActive = False


    def checkInternet(self):
        '''Check for internet connection'''

        try:
            requests.get("http://www.google.com", timeout=3)
            if self.workingInternet == False:
                self.workingInternet = True
                dexSay.speak('Internet connection established.', 'f', True)
                self.run()

            return True

        except requests.ConnectionError:
            if self.workingInternet == True:
                self.workingInternet = False
                dexSay.speak('Internet connection lost', 'f', True)
                self.run()

        except:
            if self.workingInternet == True:
                self.workingInternet = False
                dexSay.speak('Internet connection lost', 'f', True)
                self.run()

        return False


    def checkP2T(self):
        # create a hook manager
        hm = HookManager()
        # watch for all keyboard events
        hm.KeyDown = self.OnKeyboardEvent
        # set the hook
        hm.HookKeyboard()
        # wait forever
        pythoncom.PumpMessages()
        #


    def backgroundChecks(self):
        '''Run the following processes in the background'''

        # call checkInternet() every 5 seconds

        internetThread = threading.Timer(5, self.checkInternet)
        internetThread.daemon = True
        internetThread.start()

        P2T_thread = threading.Thread(target=self.checkP2T)
        P2T_thread.daemon = True
        P2T_thread.start()

        DexAlarm.triggerCheckAlarm()
        DexRemind.triggerCheckReminder()







#Add intro GUI
class DexIntroGUI(QMainWindow):

    def __init__(self):
        super(DexIntroGUI, self).__init__()
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


        self.setGeometry(400, 300, 0, 0)


    def centre(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


    def closeEvent(self, event):
        pass


class GUIThread(QThread):

    def __init__(self):
        QThread.__init__(self)


    def run(self):
        app = QApplication(sys.argv)
        mainWindow = DexIntroGUI()
        mainWindow.centre()
        mainWindow.show()
        QTimer.singleShot(15000, mainWindow.close)

        sys.exit(app.exec_())


def introWindow():

    answerGUI = GUIThread()
    answerGUI.run()
    return