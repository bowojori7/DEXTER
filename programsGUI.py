import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


globalFoundProgramList = sys.argv[1:]
print(globalFoundProgramList)

#Add programsFound GUI
class programsFoundGUI(QMainWindow):

    def __init__(self):
        super(programsFoundGUI, self).__init__()
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

        font.setPixelSize(13)
        label2 = QLabel()

        i = 0
        while i != len(globalFoundProgramList):
            globalFoundProgramList[i] = str(i+1) + '.\t' + globalFoundProgramList[i]
            i = i+1


        label2.setText('.\n'.join(globalFoundProgramList))
        label2.setAlignment(Qt.AlignCenter)
        label2.setFont(font)
        self.setforeColor(label2)
        MainFrameLayout.addWidget(label2)

        self.setGeometry(QDesktopWidget().screenGeometry().width() - self.geometry().width() * 2,
                         self.geometry().height(), 0, 0)

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
        mainWindow = programsFoundGUI()
        # mainWindow.centre()
        mainWindow.show()

        sys.exit(app.exec_())


def GUI():

    programsGUI = GUIThread()
    programsGUI.run()
    return

GUI()
