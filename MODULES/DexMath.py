from Mouth import Mouth
from Ears import Ears
import wolframalpha
import threading
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

dexSay = Mouth()
dexHear = Ears()

moduleID = '3'

def getID():
    return moduleID

def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''
    if dexActive == False:
        return False
    if dexActive == True:
        if dexMath(data, 1) != 'Error':
            return True

        return False

def handle(data, dexActive):
    '''
    1. Figure out what control function is needed
    2. Call the function
    '''

    if dexMath(data, 1) != 'Error':
        dexMath(data, 0)
        return 'task complete'

answer = ''
query = ''
def dexMath(data, check):
    '''Open Start Menu and search for query'''
    global answer
    global query
    query = data
    try:
        # wolfram alpha
        app_id = "QA77UY-54HYQAGQVA"
        client = wolframalpha.Client(app_id)
        result = client.query(query)
        answer = next(result.results).text

        if check == 0:
            GUIThread = threading.Thread(target=answerWindow)
            GUIThread.start()
            dexSay.speak(str(answer), 'm', True)



    except:
        if check == 1:
            return "Error"


#ADD  GUI to show 'answer'

class DexAnswerGUI(QMainWindow):

    def __init__(self):
        super(DexAnswerGUI, self).__init__()
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
        global answer
        global query

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
        label2 = QLabel(query + "?")
        label2.setAlignment(Qt.AlignCenter)
        label2.setFont(font)
        self.setforeColor(label2)
        MainFrameLayout.addWidget(label2)

        font.setPixelSize(15)
        label2 = QLabel(answer)
        label2.setAlignment(Qt.AlignCenter)
        label2.setFont(font)
        self.setforeColor(label2)
        MainFrameLayout.addWidget(label2)


        font.setPixelSize(13)
        label2 = QLabel('ESC TO EXIT')
        label2.setAlignment(Qt.AlignCenter)
        label2.setFont(font)
        self.setforeColor(label2)
        MainFrameLayout.addWidget(label2)

        self.setGeometry(QDesktopWidget().screenGeometry().width()-self.geometry().width()*2, self.geometry().height(), 0, 0)

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
        mainWindow = DexAnswerGUI()
        # mainWindow.centre()
        mainWindow.show()

        sys.exit(app.exec_())


def answerWindow():

    answerGUI = GUIThread()
    answerGUI.run()
    return
