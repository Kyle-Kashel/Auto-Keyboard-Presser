from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pynput import *
from pynput.keyboard import *  # (Importing Key, Controller)
from pynput import keyboard
import threading
import time
import sys


class customTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""QTableWidget {background-color: rgb(80,80,80)}""")

        verticalScroll = QScrollBar()
        verticalScroll.setStyleSheet("""
        QScrollBar:vertical {
            border: none;
            background:transparent;
            width:5px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: rgb(34,145,240);
            min-height: 0px;
        }
        QScrollBar::add-line:vertical {
            background: rgb(34,145,240);
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            background: rgb(34,145,240);
            height: 0 px;
            subcontrol-position: top;
            subcontrol-origin: margin
        }""")

        horizontalScroll = QScrollBar()
        horizontalScroll.setStyleSheet("""QScrollBar:horizontal {border: none; background: transparent; height: 5px; 
        margin: 0px 0px 0px 0px
        } 
        QScrollBar::handle:horizontal {background: rgb(34,145,240); min-width: 0 px
        }
        QScrollBar::add-line:horizontal {background: rgb(34,145,240); width: 0 px; subcontrol-position: left; 
        subcontrol-origin: margin
        }
        QScrollBar::sub-line:horizontal {background: rgb(34,145,240); width: 0 px; subcontrol-position: right; 
        subcontrol-origin: margin
        }""")

        self.setVerticalScrollBar(verticalScroll)
        self.setHorizontalScrollBar(horizontalScroll)


class KeyboardRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('QWidget {background-color: rgb(30,30,30)}')
        self.move(650, 350)
        self.setFixedWidth(500)
        self.setFixedHeight(300)
        self.setWindowTitle('Auto Keyboard Recorder')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(".\\appIcon2.png"))
        self.oldPos = self.pos()
        self.mainFrame()
        self.windowTitleBar()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def windowTitleBar(self):
        self.titleBarFrame = QFrame(self)
        self.titleBarFrame.setStyleSheet('QFrame {background-color: rgb(20,20,20)}')
        self.titleBarFrame.setGeometry(0, 0, 500, 30)
        self.titleBarFrame.show()

        self.titleBarLabel = QLabel(self.titleBarFrame)
        self.titleBarLabel.setText('Auto Keyboard Presser v1.0')
        self.titleBarLabel.setStyleSheet('QLabel {background-color: transparent; color: rgb(120,120,120)}')
        self.titleBarLabel.setGeometry(35, 5, 200, 17)
        titleBarLabelFont = QFont('Calibri', 12)
        self.titleBarLabel.setFont(titleBarLabelFont)
        self.titleBarLabel.show()

        self.titleBarIcon = QLabel(self.titleBarFrame)
        self.titleBarIcon.setPixmap(QPixmap(".\\appIcon4.png"))
        self.titleBarIcon.setGeometry(5, 1, 30, 30)
        self.titleBarIcon.show()

        def minimizeWindow():
            self.showMinimized()

        self.titleBarButtonMinimize = QPushButton(self.titleBarFrame)
        self.titleBarButtonMinimize.setGeometry(438, 0, 30, 30)
        self.titleBarButtonMinimize.setText('-')
        titleBarButtonMinimizeFont = QFont('Calibri', 25)
        self.titleBarButtonMinimize.setFont(titleBarButtonMinimizeFont)
        self.titleBarButtonMinimize.setToolTip('Minimize Window')
        self.titleBarButtonMinimize.setStyleSheet(
            'QPushButton {background-color: rgb(20,20,20); color: rgb(100,100,100)}')
        self.titleBarButtonMinimize.setFlat(True)
        self.titleBarButtonMinimize.clicked.connect(minimizeWindow)
        self.titleBarButtonMinimize.show()
        self.titleBarButtonMinimize.setFocusPolicy(Qt.NoFocus)

        def closeWindow():
            self.close()

        self.titleBarButtonClose = QPushButton(self.titleBarFrame)
        self.titleBarButtonClose.setGeometry(468, 0, 30, 30)
        self.titleBarButtonClose.setText('x')
        titleBarButtonCloseFont = QFont('Calibri', 15)
        self.titleBarButtonClose.setFont(titleBarButtonCloseFont)
        self.titleBarButtonClose.setToolTip('Close Window')
        self.titleBarButtonClose.setStyleSheet(
            'QPushButton {background-color: rgb(20,20,20); color: rgb(100,100,100)}')
        self.titleBarButtonClose.setFlat(True)
        self.titleBarButtonClose.clicked.connect(closeWindow)
        self.titleBarButtonClose.show()
        self.titleBarButtonClose.setFocusPolicy(Qt.NoFocus)

    def mainFrame(self):
        self.frameWindow1 = QFrame(self)
        self.frameWindow1.setGeometry(5, 5, 490, 290)
        self.frameWindow1.setStyleSheet('QFrame {background-color: rgb(50,50,50)}')

        self.frameWindow2 = QFrame(self.frameWindow1)
        self.frameWindow2.setGeometry(5, 30, 250, 255)
        self.frameWindow2.setFrameShape(QFrame.Box)
        self.frameWindow2.setFrameShadow(QFrame.Raised)
        self.frameWindow2.setStyleSheet('QFrame {background-color: rgb(40,40,40)}')

        self.frameWindow2a = QFrame(self.frameWindow2)
        self.frameWindow2a.setGeometry(3, 32, 244, 220)
        self.frameWindow2a.setFrameShape(QFrame.Box)
        self.frameWindow2a.setFrameShadow(QFrame.Raised)
        self.frameWindow2a.setStyleSheet('QFrame {background-color: rgb(40,40,40)}')

        self.frameWindow2b = QFrame(self.frameWindow2)
        self.frameWindow2b.setGeometry(72, 8, 175, 20)
        self.frameWindow2b.setStyleSheet('QFrame {background-color: rgb(35,35,35)}}')

        self.frameWindow3 = QFrame(self.frameWindow1)
        self.frameWindow3.setGeometry(263, 30, 220, 255)
        self.frameWindow3.setFrameShape(QFrame.Box)
        self.frameWindow3.setFrameShadow(QFrame.Raised)
        self.frameWindow3.setStyleSheet('QFrame {background-color: rgb(20,20,20)}')

        self.frameWindow3a = QFrame(self.frameWindow3)
        self.frameWindow3a.setGeometry(0, 58, 220, 59)
        self.frameWindow3a.setStyleSheet('QFrame {background-color: rgb(20,20,20)}')

        self.frameWindow3b = QFrame(self.frameWindow3)
        self.frameWindow3b.setGeometry(0, 120, 220, 55)
        self.frameWindow3b.setStyleSheet('QFrame {background-color: rgb(20,20,20)}')

        self.frameWindow3c = QFrame(self.frameWindow3)
        self.frameWindow3c.setGeometry(2, 2, 216, 20)
        self.frameWindow3c.setStyleSheet('QFrame {background-color: rgb(35,35,35)}}')

        self.frameWindow4 = QFrame(self.frameWindow3)
        self.frameWindow4.setGeometry(2, 182, 216, 70)
        self.frameWindow4.setStyleSheet('QFrame {background-color: rgb(25,25,25)}}')

        self.actionTable()
        self.actionSelector()
        self.show()

    def actionTable(self):

        self.statusLabel = QLabel(self.frameWindow2b)
        self.statusLabel.setText('Status :')
        self.statusLabel.setGeometry(5, 2, 100, 12)
        statusLabelFont = QFont('Calibri', 10)
        self.statusLabel.setStyleSheet('QLabel {background-color: transparent; color: rgb(110,110,110)}')
        self.statusLabel.setFont(statusLabelFont)
        self.statusLabel.show()

        self.recordingStatus = QLabel(self.frameWindow2b)
        self.recordingStatus.setText('No Recorded Key Press')
        self.recordingStatus.setGeometry(50, 3, 150, 12)
        recordingStatusFont = QFont('Calibri', 9)
        self.recordingStatus.setFont(recordingStatusFont)
        self.recordingStatus.setStyleSheet('QLabel {background-color: transparent; color: rgb(95,95,95)}')
        self.recordingStatus.show()

        self.recordAction = QPushButton(self.frameWindow2)
        self.recordAction.setGeometry(5, 5, 30, 25)
        self.recordAction.setToolTip('Start Recording Key Presses')
        self.recordAction.setStyleSheet('QPushButton {color: rgb(34,145,240)}')
        self.recordAction.setIcon(QIcon('.\\Play1.png'))
        self.recordAction.setIconSize(QSize(60, 60))
        self.recordAction.clicked.connect(self.recordKeyPress)
        self.recordAction.setDisabled(False)
        self.recordAction.setFocusPolicy(Qt.NoFocus)

        self.stoprecordAction = QPushButton(self.frameWindow2)
        self.stoprecordAction.setGeometry(40, 5, 30, 25)
        self.stoprecordAction.setToolTip('Stop Recording')
        self.stoprecordAction.setStyleSheet('QPushButton {color: rgb(34,145,240)}')
        self.stoprecordAction.setIcon(QIcon('.\\Stop1.png'))
        self.stoprecordAction.setIconSize(QSize(35, 35))
        self.stoprecordAction.clicked.connect(self.stopRecording)
        self.stoprecordAction.setDisabled(True)
        self.stoprecordAction.setFocusPolicy(Qt.NoFocus)

    def actionSelector(self):

        self.stateLabel = QLabel(self.frameWindow3c)
        self.stateLabel.setText('App Status : ')
        self.stateLabel.setGeometry(5, 2, 100, 15)
        self.stateLabel.setStyleSheet('QLabel {background-color: transparent ; color: rgb(34,145,240)}')

        self.currentState = QLabel(self.frameWindow3c)
        self.currentState.setText('')
        self.currentState.setGeometry(68, 2, 150, 15)
        self.currentState.setStyleSheet('QLabel {background-color: transparent; color: rgb(180,180,180)}')

        self.startstopLabel = QLabel(self.frameWindow3)
        self.startstopLabel.setText('Start Delay (Seconds) :')
        self.startstopLabel.setStyleSheet('QLabel {background-color: transparent; color: rgb(34,145,240)}')
        self.startstopLabel.setGeometry(8, 32, 130, 15)

        self.startdelaySpinBox = QSpinBox(self.frameWindow3)
        self.startdelaySpinBox.setGeometry(140, 27, 55, 20)
        self.startdelaySpinBox.setStyleSheet('QSpinBox {background-color: rgb(150,150,150)}')
        self.startdelaySpinBox.setMaximum(999)
        self.startdelaySpinBox.setMinimum(0)
        self.startdelaySpinBox.setValue(2)
        self.startdelaySpinBox.setFocusPolicy(Qt.NoFocus)

        def delayRadioButton():
            if self.radioButtonUniform.isChecked() == True:
                self.delaySpinBox.setDisabled(False)

            else:
                self.delaySpinBox.setDisabled(True)

        self.pressDelayLabel = QLabel(self.frameWindow3a)
        self.pressDelayLabel.setText('Press Delay (Milliseconds):')
        self.pressDelayLabel.setGeometry(8, 0, 125, 15)
        self.pressDelayLabel.setStyleSheet('QLabel {background-color: transparent; color: rgb(34,145,240)}')

        self.pressDelayLabelIndividual = QLabel(self.frameWindow3a)
        self.pressDelayLabelIndividual.setText('Individual')
        self.pressDelayLabelIndividual.setGeometry(35, 17, 100, 15)
        self.pressDelayLabelIndividual.setStyleSheet('QLabel {background-color: transparent; color: rgb(160,160,160)}')

        self.radioButtonIndividual = QRadioButton(self.frameWindow3a)
        self.radioButtonIndividual.setGeometry(15, 17, 15, 18)
        self.radioButtonIndividual.clicked.connect(delayRadioButton)
        self.radioButtonIndividual.setFocusPolicy(Qt.NoFocus)
        self.radioButtonIndividual.setStyleSheet('QRadioButton {background-color: rgb(20,20,20); '
                                                 'color: rgb(34,145,240)} QRadioButton::indicator:unchecked {border: '
                                                 '1px solid gray}')

        self.pressDelayLabelUniform = QLabel(self.frameWindow3a)
        self.pressDelayLabelUniform.setText('Uniform:')
        self.pressDelayLabelUniform.setGeometry(35, 37, 100, 15)
        self.pressDelayLabelUniform.setStyleSheet('QLabel {background-color: transparent; color: rgb(160,160,160)}')

        self.delaySpinBox = QSpinBox(self.frameWindow3a)
        self.delaySpinBox.setGeometry(90, 37, 55, 20)
        self.delaySpinBox.setStyleSheet('QSpinBox {background-color: rgb(150,150,150)}')
        self.delaySpinBox.setMaximum(999999)
        self.delaySpinBox.setValue(500)
        self.delaySpinBox.setFocusPolicy(Qt.NoFocus)

        self.radioButtonUniform = QRadioButton(self.frameWindow3a)
        self.radioButtonUniform.setGeometry(15, 37, 15, 18)
        self.radioButtonUniform.setChecked(True)
        self.radioButtonUniform.clicked.connect(delayRadioButton)
        self.radioButtonUniform.setFocusPolicy(Qt.NoFocus)
        self.radioButtonUniform.setStyleSheet('QRadioButton {background-color: rgb(20,20,20); '
                                              'color: rgb(34,145,240)} QRadioButton::indicator:unchecked {border: '
                                              '1px solid gray}')

        def repeatRadioButton():
            if self.radioButtonRepeatContinue.isChecked() == True:
                self.repeatSpinBox.setDisabled(True)

            else:
                self.repeatSpinBox.setDisabled(False)

        self.pressLoopLabel = QLabel(self.frameWindow3b)
        self.pressLoopLabel.setText('Loop Frequency:')
        self.pressLoopLabel.setGeometry(8, 0, 125, 15)
        self.pressLoopLabel.setStyleSheet('QLabel {background-color: transparent; color: rgb(34,145,240)}')

        self.pressRepeatTimes = QLabel(self.frameWindow3b)
        self.pressRepeatTimes.setText('Repeat: ')
        self.pressRepeatTimes.setGeometry(35, 17, 100, 15)
        self.pressRepeatTimes.setStyleSheet('QLabel {background-color: transparent; color: rgb(160,160,160)}')

        self.repeatSpinBox = QSpinBox(self.frameWindow3b)
        self.repeatSpinBox.setGeometry(90, 17, 55, 20)
        self.repeatSpinBox.setStyleSheet('QSpinBox {background-color: rgb(150,150,150)}')
        self.repeatSpinBox.setDisabled(True)
        self.repeatSpinBox.setMaximum(999999)
        self.repeatSpinBox.setValue(1)
        self.repeatSpinBox.setFocusPolicy(Qt.NoFocus)

        self.repeatTimesLabel = QLabel(self.frameWindow3b)
        self.repeatTimesLabel.setText('time(s)')
        self.repeatTimesLabel.setGeometry(150, 17, 100, 15)
        self.repeatTimesLabel.setStyleSheet('QLabel {background-color: transparent; color: rgb(160,160,160)}')

        self.radioButtonRepeatTimes = QRadioButton(self.frameWindow3b)
        self.radioButtonRepeatTimes.setGeometry(15, 17, 15, 18)
        self.radioButtonRepeatTimes.clicked.connect(repeatRadioButton)
        self.radioButtonRepeatTimes.setFocusPolicy(Qt.NoFocus)
        self.radioButtonRepeatTimes.setStyleSheet('QRadioButton {background-color: rgb(20,20,20); '
                                                  'color: rgb(34,145,240)} QRadioButton::indicator:unchecked {border: '
                                                  '1px solid gray}')

        self.pressRepeatContinue = QLabel(self.frameWindow3b)
        self.pressRepeatContinue.setText('Repeat Continuously')
        self.pressRepeatContinue.setGeometry(35, 37, 100, 15)
        self.pressRepeatContinue.setStyleSheet('QLabel {background-color: transparent; color: rgb(160,160,160)}')

        self.radioButtonRepeatContinue = QRadioButton(self.frameWindow3b)
        self.radioButtonRepeatContinue.setGeometry(15, 37, 15, 18)
        self.radioButtonRepeatContinue.setChecked(True)
        self.radioButtonRepeatContinue.clicked.connect(repeatRadioButton)
        self.radioButtonRepeatContinue.setFocusPolicy(Qt.NoFocus)
        self.radioButtonRepeatContinue.setStyleSheet('QRadioButton {background-color: rgb(20,20,20); '
                                                     'color: rgb(34,145,240)} QRadioButton::indicator:unchecked {border: '
                                                     '1px solid gray}')

        self.startExecuteButton = QPushButton(self.frameWindow4)
        self.startExecuteButton.setGeometry(5, 5, 100, 60)
        self.startExecuteButton.setToolTip('Start Executing Key Presses')
        self.startExecuteButton.setStyleSheet('QPushButton {color: rgb(34,145,240)}')
        self.startExecuteButton.setIcon(QIcon(".\\Play1.png"))
        self.startExecuteButton.setIconSize(QSize(120, 120))
        self.startExecuteButton.clicked.connect(self.executeKeyPresses)
        self.startExecuteButton.setDisabled(True)
        self.startExecuteButton.setFocusPolicy(Qt.NoFocus)

        self.endExecuteButton = QPushButton(self.frameWindow4)
        self.endExecuteButton.setGeometry(110, 5, 100, 60)
        self.endExecuteButton.setToolTip('Stop Executing Key Presses')
        self.endExecuteButton.setStyleSheet('QPushButton {color: rgb(34,145,240)}')
        self.endExecuteButton.setIcon(QIcon(".\\Stop1.png"))
        self.endExecuteButton.setIconSize(QSize(60, 60))
        self.endExecuteButton.clicked.connect(self.stopKeyPresses)
        self.endExecuteButton.setDisabled(True)
        self.endExecuteButton.setFocusPolicy(Qt.NoFocus)

    def stopRecording(self):
        keyboard = Controller()  # for instant key presses #
        self.startExecuteButton.setDisabled(False)
        self.recordAction.setDisabled(False)
        self.stoprecordAction.setDisabled(True)
        self.recordingStatus.setText('Recording - Stopped')
        self.recordingStatus.setStyleSheet('QLabel {background-color: transparent; color: rgb(100,100,100)}')

        self.recordedActionTable = customTableWidget(self.frameWindow2a)
        self.recordedActionTable.setGeometry(1, 1, 243, 220)
        self.recordedActionTable.setColumnCount(2)
        self.recordedActionTable.setRowCount(0)
        actionTableHeaders = ['   Key Pressed   ', '     Press Delay     ', ' ... ']
        self.recordedActionTable.setHorizontalHeaderLabels(actionTableHeaders)
        self.recordedActionTableHeadersH = QTableWidget.horizontalHeader(self.recordedActionTable)

        self.recordedActionTableHeadersH.setStyleSheet('QTableWidget, QWidget {background-color:rgb(60,60,60);'
                                                       'color:rgb(180,180,180)}')

        self.recordedActionTableHeadersV = QTableWidget.verticalHeader(self.recordedActionTable)
        self.recordedActionTableHeadersV.setStyleSheet('QTableWidget, QWidget {background-color:rgb(60,60,60);'
                                                       'color:rgb(180,180,180)}')

        self.recordedActionTable.setColumnWidth(0, 125)
        self.recordedActionTable.setColumnWidth(1, 85)

        self.recordedActionTable.horizontalHeader().setFixedHeight(30)
        recordActionTableFont = self.recordedActionTable.horizontalHeader().font()
        recordActionTableFont.setPointSize(10)
        recordActionTableFont.setBold(True)
        self.recordedActionTable.horizontalHeader().setFont(recordActionTableFont)

        self.recordedActionTable.show()

        allrow = len(self.pressedList)
        for row in range(allrow):
            self.recordedActionTable.insertRow(row)
            if self.recordingStatus.text() == 'Recording - Stopped':
                self.pressedItems = QTableWidgetItem(str(self.pressedList[row]))
                self.pressedItems.setFlags(Qt.ItemIsEnabled)
                self.recordedActionTable.setItem(row, 0, self.pressedItems)

                self.delayTableSpinBox = QSpinBox()
                self.delayTableSpinBox.setStyleSheet(
                    'QSpinBox {background-color: rgb(100,100,100); color: rgb(10,10,10)}')
                self.delayTableSpinBox.setMaximum(999999)

                if self.radioButtonUniform.isChecked() == True:
                    self.delayTableSpinBox.setValue(self.delaySpinBox.value())
                    self.delayTableSpinBox.setReadOnly(True)
                    self.recordedActionTable.setCellWidget(row, 1, self.delayTableSpinBox)
                else:
                    self.delayTableSpinBox.setValue(500)
                    self.delayTableSpinBox.setReadOnly(False)
                    self.recordedActionTable.setCellWidget(row, 1, self.delayTableSpinBox)
            else:
                break

        self.newpressedList = []
        self.individualDelay = []

        for newRow in range(allrow):
            newItems = self.recordedActionTable.item(newRow, 0).text()
            convertNewItems = newItems.strip("'")
            self.newpressedList.append(convertNewItems)
        
        if self.radioButtonIndividual.isChecked() == True:
            for delayRow in range(allrow):
                individualDelay = self.recordedActionTable.cellWidget(delayRow, 1).value()
                self.individualDelay.append(individualDelay)

        # ===== to press something in the Keyboard to Clear on the List (To Prevent double entry)
        # ===== on function "recordKeyPress"
        keyboard.release(Key.esc)
        #

    def recordKeyPress(self):
        self.recordAction.setDisabled(True)
        self.startExecuteButton.setDisabled(True)
        self.stoprecordAction.setDisabled(False)
        if self.recordingStatus.text() == 'Recording - Stopped':
            if self.radioButtonIndividual.isChecked() == False:
                self.radioButtonIndividual.setDisabled(False)
                self.radioButtonUniform.setDisabled(False)
        self.recordingStatus.setText('Recording - Started')
        self.recordingStatus.setStyleSheet('QLabel {background-color: transparent; color: rgb(65,199,255)}')
        self.pressedList = []

        self.recordingTable = customTableWidget(self.frameWindow2a)
        self.recordingTable.setGeometry(0, 0, 243, 220)
        self.recordingTable.setColumnCount(1)
        self.recordingTable.setRowCount(0)
        actionTableHeaders = ['   Recording Key Presses   ']
        self.recordingTable.setHorizontalHeaderLabels(actionTableHeaders)
        self.recordingTableHeadersH = QTableWidget.horizontalHeader(self.recordingTable)

        self.recordingTableHeadersH.setStyleSheet('QTableWidget, QWidget {background-color:rgb(60,60,60);'
                                                  'color:rgb(180,180,180)}')

        self.recordingTableHeadersV = QTableWidget.verticalHeader(self.recordingTable)
        self.recordingTableHeadersV.setStyleSheet('QTableWidget, QWidget {background-color:rgb(60,60,60);'
                                                  'color:rgb(180,180,180)}')

        self.recordingTableHeadersH.setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.recordingTable.horizontalHeader().setFixedHeight(30)
        recordActionTableFont = self.recordingTable.horizontalHeader().font()
        recordActionTableFont.setPointSize(10)
        recordActionTableFont.setBold(True)
        self.recordingTable.horizontalHeader().setFont(recordActionTableFont)
        self.recordingTable.setStyleSheet('QTableWidget {background-color: rgb(80,80,80)}')

        self.recordingTable.show()

        def on_release(key):
            pressedKey = str(key)
            recordStatus = self.recordingStatus.text()
            if recordStatus == 'Recording - Stopped':
                return False
            else:
                if recordStatus == 'Recording - Started':
                    self.pressedList.append(pressedKey)
                    self.recordingTable.setRowCount(0)

                allrow = len(self.pressedList)
                for row in range(allrow):
                    if recordStatus == 'Recording - Started':
                        self.recordingTable.insertRow(row)
                        recordedKey = QTableWidgetItem(str(self.pressedList[row]))
                        recordedKey.setFlags(Qt.ItemIsEnabled)
                        self.recordingTable.setItem(row, 0, recordedKey)
                    else:
                        break

        keyboard.Listener(on_release=on_release)
        listener = keyboard.Listener(on_release=on_release)
        listener.start()

    def executeKeyPresses(self):
        self.recordAction.setDisabled(True)
        self.startExecuteButton.setDisabled(True)
        self.endExecuteButton.setDisabled(False)
        self.startdelaySpinBox.setDisabled(True)
        self.radioButtonIndividual.setDisabled(True)
        self.radioButtonUniform.setDisabled(True)
        self.delaySpinBox.setDisabled(True)
        self.radioButtonRepeatTimes.setDisabled(True)
        self.repeatSpinBox.setDisabled(True)
        self.radioButtonRepeatContinue.setDisabled(True)
        self.executionStatus = True
        startDelayMilliseconds = self.startdelaySpinBox.value()
        self.startDelay = startDelayMilliseconds

        if self.radioButtonUniform.isChecked() == True:
            delayPress = self.delaySpinBox.value()
            self.convertDelayPress = delayPress / 1000
        else:
            self.convertDelayPress = 0 / 1000

        if self.radioButtonRepeatContinue.isChecked() == True:
            pass
        else:
            self.repeatTimes = self.repeatSpinBox.value()
            self.repeatCounter = 1

        def runKeyPress():
            status = ''
            selectedModifierList = []
            keyboardController = Controller()
            self.currentState.setText('Command Started')
            time.sleep(self.startDelay)
            if self.radioButtonRepeatContinue.isChecked() == True:
                while self.executionStatus == True:
                    if self.radioButtonUniform.isChecked() == True:
                        for itemPress in self.newpressedList:
                            time.sleep(self.convertDelayPress)
                            if itemPress == 'Key.shift':
                                pressedButtonName = 'It is SHIFT_LEFT'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.shift
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.shift_r':
                                pressedButtonName = 'It is SHIFT_RIGHT'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.shift_r
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.shift_l':
                                pressedButtonName = 'It is SHIFT_LEFT'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.shift_l
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.ctrl':
                                pressedButtonName = 'It is CONTROL'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.ctrl
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.ctrl_l':
                                pressedButtonName = 'It is CONTROL_Left'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.ctrl_l
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.ctrl_r':
                                pressedButtonName = 'It is CONTROL_Right'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.ctrl_r
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.cmd':
                                pressedButtonName = 'It is Windows Key'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.cmd
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.cmd_l':
                                pressedButtonName = 'It is Windows Key'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.cmd_l
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.cmd_r':
                                pressedButtonName = 'It is Windows Key'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.cmd_r
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.alt_l':
                                pressedButtonName = 'It is ALT_Left'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.alt_l
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.alt_r':
                                pressedButtonName = 'It is ALT_Right'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.alt_r
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.alt':
                                pressedButtonName = 'It is ALT'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.alt
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.esc':
                                pressedButtonName = 'It is ESCAPE'
                                status = 'Not'
                                pressedItem = Key.esc
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.tab':
                                pressedButtonName = 'It is TAB'
                                status = 'Not'
                                pressedItem = Key.tab
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.caps_lock':
                                pressedButtonName = 'It is CAPS_LOCK'
                                status = 'Not'
                                pressedItem = Key.caps_lock
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.space':
                                pressedButtonName = 'It is SpaceBar'
                                status = 'Not'
                                pressedItem = Key.space
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.enter':
                                pressedButtonName = 'It is Enter'
                                status = 'Not'
                                pressedItem = Key.enter
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.backspace':
                                pressedButtonName = 'It is BackSpace'
                                status = 'Not'
                                pressedItem = Key.backspace
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f1':
                                pressedButtonName = 'It is F1'
                                status = 'Not'
                                pressedItem = Key.f1
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f2':
                                pressedButtonName = 'It is F2'
                                status = 'Not'
                                pressedItem = Key.f2
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f3':
                                pressedButtonName = 'It is F3'
                                status = 'Not'
                                pressedItem = Key.f3
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f4':
                                pressedButtonName = 'It is F4'
                                status = 'Not'
                                pressedItem = Key.f4
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f5':
                                pressedButtonName = 'It is F5'
                                status = 'Not'
                                pressedItem = Key.f5
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f6':
                                pressedButtonName = 'It is F6'
                                status = 'Not'
                                pressedItem = Key.f6
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f7':
                                pressedButtonName = 'It is F7'
                                status = 'Not'
                                pressedItem = Key.f7
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)
                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f8':
                                pressedButtonName = 'It is F8'
                                status = 'Not'
                                pressedItem = Key.f8
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f9':
                                pressedButtonName = 'It is F9'
                                status = 'Not'
                                pressedItem = Key.f9
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f10':
                                pressedButtonName = 'It is F10'
                                status = 'Not'
                                pressedItem = Key.f10
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f11':
                                pressedButtonName = 'It is F11'
                                status = 'Not'
                                pressedItem = Key.f11
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f12':
                                pressedButtonName = 'It is F12'
                                status = 'Not'
                                pressedItem = Key.f12
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.print_screen':
                                pressedButtonName = 'It is PRINT_SCREEN'
                                status = 'Not'
                                pressedItem = Key.print_screen
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.scroll_lock':
                                pressedButtonName = 'It is SCROLL_LOCK'
                                status = 'Not'
                                pressedItem = Key.scroll_lock
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.pause':
                                pressedButtonName = 'It is PAUSE'
                                status = 'Not'
                                pressedItem = Key.pause
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.insert':
                                pressedButtonName = 'It is INSERT'
                                status = 'Not'
                                pressedItem = Key.insert
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.home':
                                pressedButtonName = 'It is HOME'
                                status = 'Not'
                                pressedItem = Key.home
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.page_up':
                                pressedButtonName = 'It is PAGE_Up'
                                status = 'Not'
                                pressedItem = Key.page_up
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.delete':
                                pressedButtonName = 'It is DELETE'
                                status = 'Not'
                                pressedItem = Key.delete
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.end':
                                pressedButtonName = 'It is END'
                                status = 'Not'
                                pressedItem = Key.end
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.page_down':
                                pressedButtonName = 'It is PAGE_Down'
                                status = 'Not'
                                pressedItem = Key.page_down
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.up':
                                pressedButtonName = 'It is ArrowKey_Up'
                                status = 'Not'
                                pressedItem = Key.up
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.down':
                                pressedButtonName = 'It is ArrowKey_Down'
                                status = 'Not'
                                pressedItem = Key.down
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.left':
                                pressedButtonName = 'It is ArrowKey_Left'
                                status = 'Not'
                                pressedItem = Key.left
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.right':
                                pressedButtonName = 'It is ArrowKey_Right'
                                status = 'Not'
                                pressedItem = Key.right
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.num_lock':
                                pressedButtonName = 'It is NUMPAD_Lock'
                                status = 'Not'
                                pressedItem = Key.num_lock
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<96>':
                                pressedButtonName = 'It is Numpad_0'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=96)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<97>':
                                pressedButtonName = 'It is Numpad_1'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=97)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<98>':
                                pressedButtonName = 'It is Numpad_2'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=98)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<99>':
                                pressedButtonName = 'It is Numpad_3'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=99)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<100>':
                                pressedButtonName = 'It is Numpad_4'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=100)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<101>':
                                pressedButtonName = 'It is Numpad_5'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=101)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<102>':
                                pressedButtonName = 'It is Numpad_6'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=102)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<103>':
                                pressedButtonName = 'It is Numpad_7'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=103)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<104>':
                                pressedButtonName = 'It is Numpad_8'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=104)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<105>':
                                pressedButtonName = 'It is Numpad_9'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=105)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<12>':
                                pressedButtonName = 'It is Numpad_5 with Numpad_Off'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=12)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []
                            else:
                                pressedButtonName = str(itemPress)
                                status = 'Not'
                                pressButton = keyboardController.press(pressedButtonName)
                                keyboardController.release(pressedButtonName)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []
                        if self.executionStatus == False:
                            break
                            
                    else:
                        self.individualDelay = []
                        allrow = self.recordedActionTable.rowCount()
                        for delayRow in range(allrow):
                            individualDelay = self.recordedActionTable.cellWidget(delayRow, 1).value()
                            self.individualDelay.append(individualDelay)

                        combineList = [None]*(len(self.newpressedList) + len(self.individualDelay))
                        combineList[::2] = self.newpressedList
                        combineList[1::2] = self.individualDelay
                        
                        for items in combineList:
                            try:
                                if items >= 0:
                                    individualDelay = items / 1000
                                    time.sleep(individualDelay)
                                    
                            except TypeError:
                                if items == 'Key.shift':
                                    pressedButtonName = 'It is SHIFT_LEFT'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.shift
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.shift_r':
                                    pressedButtonName = 'It is SHIFT_RIGHT'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.shift_r
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.shift_l':
                                    pressedButtonName = 'It is SHIFT_LEFT'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.shift_l
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.ctrl':
                                    pressedButtonName = 'It is CONTROL'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.ctrl
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.ctrl_l':
                                    pressedButtonName = 'It is CONTROL_Left'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.ctrl_l
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.ctrl_r':
                                    pressedButtonName = 'It is CONTROL_Right'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.ctrl_r
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.cmd':
                                    pressedButtonName = 'It is Windows Key'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.cmd
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.cmd_l':
                                    pressedButtonName = 'It is Windows Key'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.cmd_l
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.cmd_r':
                                    pressedButtonName = 'It is Windows Key'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.cmd_r
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.alt_l':
                                    pressedButtonName = 'It is ALT_Left'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.alt_l
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.alt_r':
                                    pressedButtonName = 'It is ALT_Right'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.alt_r
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.alt':
                                    pressedButtonName = 'It is ALT'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.alt
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.esc':
                                    pressedButtonName = 'It is ESCAPE'
                                    status = 'Not'
                                    pressedItem = Key.esc
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.tab':
                                    pressedButtonName = 'It is TAB'
                                    status = 'Not'
                                    pressedItem = Key.tab
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.caps_lock':
                                    pressedButtonName = 'It is CAPS_LOCK'
                                    status = 'Not'
                                    pressedItem = Key.caps_lock
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.space':
                                    pressedButtonName = 'It is SpaceBar'
                                    status = 'Not'
                                    pressedItem = Key.space
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.enter':
                                    pressedButtonName = 'It is Enter'
                                    status = 'Not'
                                    pressedItem = Key.enter
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.backspace':
                                    pressedButtonName = 'It is BackSpace'
                                    status = 'Not'
                                    pressedItem = Key.backspace
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f1':
                                    pressedButtonName = 'It is F1'
                                    status = 'Not'
                                    pressedItem = Key.f1
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f2':
                                    pressedButtonName = 'It is F2'
                                    status = 'Not'
                                    pressedItem = Key.f2
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f3':
                                    pressedButtonName = 'It is F3'
                                    status = 'Not'
                                    pressedItem = Key.f3
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f4':
                                    pressedButtonName = 'It is F4'
                                    status = 'Not'
                                    pressedItem = Key.f4
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f5':
                                    pressedButtonName = 'It is F5'
                                    status = 'Not'
                                    pressedItem = Key.f5
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f6':
                                    pressedButtonName = 'It is F6'
                                    status = 'Not'
                                    pressedItem = Key.f6
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f7':
                                    pressedButtonName = 'It is F7'
                                    status = 'Not'
                                    pressedItem = Key.f7
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f8':
                                    pressedButtonName = 'It is F8'
                                    status = 'Not'
                                    pressedItem = Key.f8
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f9':
                                    pressedButtonName = 'It is F9'
                                    status = 'Not'
                                    pressedItem = Key.f9
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f10':
                                    pressedButtonName = 'It is F10'
                                    status = 'Not'
                                    pressedItem = Key.f10
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f11':
                                    pressedButtonName = 'It is F11'
                                    status = 'Not'
                                    pressedItem = Key.f11
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f12':
                                    pressedButtonName = 'It is F12'
                                    status = 'Not'
                                    pressedItem = Key.f12
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.print_screen':
                                    pressedButtonName = 'It is PRINT_SCREEN'
                                    status = 'Not'
                                    pressedItem = Key.print_screen
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.scroll_lock':
                                    pressedButtonName = 'It is SCROLL_LOCK'
                                    status = 'Not'
                                    pressedItem = Key.scroll_lock
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.pause':
                                    pressedButtonName = 'It is PAUSE'
                                    status = 'Not'
                                    pressedItem = Key.pause
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.insert':
                                    pressedButtonName = 'It is INSERT'
                                    status = 'Not'
                                    pressedItem = Key.insert
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.home':
                                    pressedButtonName = 'It is HOME'
                                    status = 'Not'
                                    pressedItem = Key.home
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.page_up':
                                    pressedButtonName = 'It is PAGE_Up'
                                    status = 'Not'
                                    pressedItem = Key.page_up
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.delete':
                                    pressedButtonName = 'It is DELETE'
                                    status = 'Not'
                                    pressedItem = Key.delete
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.end':
                                    pressedButtonName = 'It is END'
                                    status = 'Not'
                                    pressedItem = Key.end
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.page_down':
                                    pressedButtonName = 'It is PAGE_Down'
                                    status = 'Not'
                                    pressedItem = Key.page_down
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.up':
                                    pressedButtonName = 'It is ArrowKey_Up'
                                    status = 'Not'
                                    pressedItem = Key.up
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.down':
                                    pressedButtonName = 'It is ArrowKey_Down'
                                    status = 'Not'
                                    pressedItem = Key.down
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.left':
                                    pressedButtonName = 'It is ArrowKey_Left'
                                    status = 'Not'
                                    pressedItem = Key.left
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.right':
                                    pressedButtonName = 'It is ArrowKey_Right'
                                    status = 'Not'
                                    pressedItem = Key.right
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.num_lock':
                                    pressedButtonName = 'It is NUMPAD_Lock'
                                    status = 'Not'
                                    pressedItem = Key.num_lock
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<96>':
                                    pressedButtonName = 'It is Numpad_0'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=96)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<97>':
                                    pressedButtonName = 'It is Numpad_1'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=97)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<98>':
                                    pressedButtonName = 'It is Numpad_2'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=98)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<99>':
                                    pressedButtonName = 'It is Numpad_3'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=99)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<100>':
                                    pressedButtonName = 'It is Numpad_4'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=100)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<101>':
                                    pressedButtonName = 'It is Numpad_5'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=101)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<102>':
                                    pressedButtonName = 'It is Numpad_6'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=102)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<103>':
                                    pressedButtonName = 'It is Numpad_7'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=103)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<104>':
                                    pressedButtonName = 'It is Numpad_8'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=104)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<105>':
                                    pressedButtonName = 'It is Numpad_9'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=105)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<12>':
                                    pressedButtonName = 'It is Numpad_9'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=12)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                else:
                                    pressedButtonName = str(items)
                                    status = 'Not'
                                    pressButton = keyboardController.press(pressedButtonName)
                                    keyboardController.release(pressedButtonName)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []
                        if self.executionStatus == False:
                            break
                        

            ###############################################################################################
            # ============================= If Continuous Spin Box is Not Selected ======================= #
            ###############################################################################################
            else:
                while self.repeatCounter <= self.repeatTimes:
                    if self.radioButtonUniform.isChecked() == True:
                        for itemPress in self.newpressedList:
                            time.sleep(self.convertDelayPress)
                            if itemPress == 'Key.shift':
                                pressedButtonName = 'It is SHIFT_LEFT'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.shift
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.shift_r':
                                pressedButtonName = 'It is SHIFT_RIGHT'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.shift_r
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.shift_l':
                                pressedButtonName = 'It is SHIFT_LEFT'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.shift_l
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.ctrl':
                                pressedButtonName = 'It is CONTROL'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.ctrl
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.ctrl_l':
                                pressedButtonName = 'It is CONTROL_Left'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.ctrl_l
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.ctrl_r':
                                pressedButtonName = 'It is CONTROL_Right'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.ctrl_r
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.cmd':
                                pressedButtonName = 'It is Windows Key'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.cmd
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.cmd_l':
                                pressedButtonName = 'It is Windows Key'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.cmd_l
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.cmd_r':
                                pressedButtonName = 'It is Windows Key'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.cmd_r
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.alt_l':
                                pressedButtonName = 'It is ALT_Left'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.alt_l
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.alt_r':
                                pressedButtonName = 'It is ALT_Right'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.alt_r
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.alt':
                                pressedButtonName = 'It is ALT'
                                status = 'Modifier'
                                selectedModifierList.append(str(itemPress))
                                pressedItem = Key.alt
                                pressButton = keyboardController.press(pressedItem)

                            elif itemPress == 'Key.esc':
                                pressedButtonName = 'It is ESCAPE'
                                status = 'Not'
                                pressedItem = Key.esc
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.tab':
                                pressedButtonName = 'It is TAB'
                                status = 'Not'
                                pressedItem = Key.tab
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.caps_lock':
                                pressedButtonName = 'It is CAPS_LOCK'
                                status = 'Not'
                                pressedItem = Key.caps_lock
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.space':
                                pressedButtonName = 'It is SpaceBar'
                                status = 'Not'
                                pressedItem = Key.space
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.enter':
                                pressedButtonName = 'It is Enter'
                                status = 'Not'
                                pressedItem = Key.enter
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.backspace':
                                pressedButtonName = 'It is BackSpace'
                                status = 'Not'
                                pressedItem = Key.backspace
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f1':
                                pressedButtonName = 'It is F1'
                                status = 'Not'
                                pressedItem = Key.f1
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f2':
                                pressedButtonName = 'It is F2'
                                status = 'Not'
                                pressedItem = Key.f2
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f3':
                                pressedButtonName = 'It is F3'
                                status = 'Not'
                                pressedItem = Key.f3
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f4':
                                pressedButtonName = 'It is F4'
                                status = 'Not'
                                pressedItem = Key.f4
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f5':
                                pressedButtonName = 'It is F5'
                                status = 'Not'
                                pressedItem = Key.f5
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f6':
                                pressedButtonName = 'It is F6'
                                status = 'Not'
                                pressedItem = Key.f6
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f7':
                                pressedButtonName = 'It is F7'
                                status = 'Not'
                                pressedItem = Key.f7
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f8':
                                pressedButtonName = 'It is F8'
                                status = 'Not'
                                pressedItem = Key.f8
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f9':
                                pressedButtonName = 'It is F9'
                                status = 'Not'
                                pressedItem = Key.f9
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f10':
                                pressedButtonName = 'It is F10'
                                status = 'Not'
                                pressedItem = Key.f10
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f11':
                                pressedButtonName = 'It is F11'
                                status = 'Not'
                                pressedItem = Key.f11
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.f12':
                                pressedButtonName = 'It is F12'
                                status = 'Not'
                                pressedItem = Key.f12
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.print_screen':
                                pressedButtonName = 'It is PRINT_SCREEN'
                                status = 'Not'
                                pressedItem = Key.print_screen
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.scroll_lock':
                                pressedButtonName = 'It is SCROLL_LOCK'
                                status = 'Not'
                                pressedItem = Key.scroll_lock
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.pause':
                                pressedButtonName = 'It is PAUSE'
                                status = 'Not'
                                pressedItem = Key.pause
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.insert':
                                pressedButtonName = 'It is INSERT'
                                status = 'Not'
                                pressedItem = Key.insert
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.home':
                                pressedButtonName = 'It is HOME'
                                status = 'Not'
                                pressedItem = Key.home
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.page_up':
                                pressedButtonName = 'It is PAGE_Up'
                                status = 'Not'
                                pressedItem = Key.page_up
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.delete':
                                pressedButtonName = 'It is DELETE'
                                status = 'Not'
                                pressedItem = Key.delete
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.end':
                                pressedButtonName = 'It is END'
                                status = 'Not'
                                pressedItem = Key.end
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.page_down':
                                pressedButtonName = 'It is PAGE_Down'
                                status = 'Not'
                                pressedItem = Key.page_down
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.up':
                                pressedButtonName = 'It is ArrowKey_Up'
                                status = 'Not'
                                pressedItem = Key.up
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.down':
                                pressedButtonName = 'It is ArrowKey_Down'
                                status = 'Not'
                                pressedItem = Key.down
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.left':
                                pressedButtonName = 'It is ArrowKey_Left'
                                status = 'Not'
                                pressedItem = Key.left
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.right':
                                pressedButtonName = 'It is ArrowKey_Right'
                                status = 'Not'
                                pressedItem = Key.right
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == 'Key.num_lock':
                                pressedButtonName = 'It is NUMPAD_Lock'
                                status = 'Not'
                                pressedItem = Key.num_lock
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<96>':
                                pressedButtonName = 'It is Numpad_0'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=96)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<97>':
                                pressedButtonName = 'It is Numpad_1'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=97)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<98>':
                                pressedButtonName = 'It is Numpad_2'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=98)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<99>':
                                pressedButtonName = 'It is Numpad_3'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=99)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<100>':
                                pressedButtonName = 'It is Numpad_4'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=100)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<101>':
                                pressedButtonName = 'It is Numpad_5'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=101)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<102>':
                                pressedButtonName = 'It is Numpad_6'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=102)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<103>':
                                pressedButtonName = 'It is Numpad_7'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=103)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<104>':
                                pressedButtonName = 'It is Numpad_8'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=104)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<105>':
                                pressedButtonName = 'It is Numpad_9'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=105)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            elif itemPress == '<12>':
                                pressedButtonName = 'It is Numpad_5 with Numlock-Off'
                                status = 'Not'
                                pressedItem = keyboard.KeyCode(vk=12)
                                pressButton = keyboardController.press(pressedItem)
                                keyboardController.release(pressedItem)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []

                            else:
                                pressedButtonName = str(itemPress)
                                status = 'Not'
                                pressButton = keyboardController.press(pressedButtonName)
                                keyboardController.release(pressedButtonName)

                                if len(selectedModifierList) >= 1:
                                    if status == 'Not':
                                        for keyModifier in selectedModifierList:
                                            if keyModifier == str(Key.ctrl_l):
                                                keyboardController.release(Key.ctrl_l)
                                            elif keyModifier == str(Key.ctrl_r):
                                                keyboardController.release(Key.ctrl_r)
                                            elif keyModifier == str(Key.ctrl):
                                                keyboardController.release(Key.ctrl)
                                            elif keyModifier == str(Key.shift):
                                                keyboardController.release(Key.shift)
                                            elif keyModifier == str(Key.shift_l):
                                                keyboardController.release(Key.shift_l)
                                            elif keyModifier == str(Key.shift_r):
                                                keyboardController.release(Key.shift_r)
                                            elif keyModifier == str(Key.alt):
                                                keyboardController.release(Key.alt)
                                            elif keyModifier == str(Key.alt_l):
                                                keyboardController.release(Key.alt_l)
                                            elif keyModifier == str(Key.alt_r):
                                                keyboardController.release(Key.alt_r)
                                            elif keyModifier == str(Key.cmd_l):
                                                keyboardController.release(Key.cmd_l)
                                            elif keyModifier == str(Key.cmd_r):
                                                keyboardController.release(Key.cmd_r)
                                            elif keyModifier == str(Key.cmd):
                                                keyboardController.release(Key.cmd)
                                        selectedModifierList = []
                        self.repeatCounter += 1
                        if self.executionStatus == False:
                            break
                    else:
                        self.individualDelay = []
                        allrow = self.recordedActionTable.rowCount()
                        for delayRow in range(allrow):
                            individualDelay = self.recordedActionTable.cellWidget(delayRow, 1).value()
                            self.individualDelay.append(individualDelay)

                        combineList = [None] * (len(self.newpressedList) + len(self.individualDelay))
                        combineList[::2] = self.newpressedList
                        combineList[1::2] = self.individualDelay

                        for items in combineList:
                            try:
                                if items >= 0:
                                    individualDelay = items / 1000
                                    time.sleep(individualDelay)

                            except TypeError:
                                if items == 'Key.shift':
                                    pressedButtonName = 'It is SHIFT_LEFT'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.shift
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.shift_r':
                                    pressedButtonName = 'It is SHIFT_RIGHT'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.shift_r
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.shift_l':
                                    pressedButtonName = 'It is SHIFT_LEFT'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.shift_l
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.ctrl':
                                    pressedButtonName = 'It is CONTROL'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.ctrl
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.ctrl_l':
                                    pressedButtonName = 'It is CONTROL_Left'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.ctrl_l
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.ctrl_r':
                                    pressedButtonName = 'It is CONTROL_Right'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.ctrl_r
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.cmd':
                                    pressedButtonName = 'It is Windows Key'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.cmd
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.cmd_l':
                                    pressedButtonName = 'It is Windows Key'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.cmd_l
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.cmd_r':
                                    pressedButtonName = 'It is Windows Key'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.cmd_r
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.alt_l':
                                    pressedButtonName = 'It is ALT_Left'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.alt_l
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.alt_r':
                                    pressedButtonName = 'It is ALT_Right'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.alt_r
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.alt':
                                    pressedButtonName = 'It is ALT'
                                    status = 'Modifier'
                                    selectedModifierList.append(str(items))
                                    pressedItem = Key.alt
                                    pressButton = keyboardController.press(pressedItem)

                                elif items == 'Key.esc':
                                    pressedButtonName = 'It is ESCAPE'
                                    status = 'Not'
                                    pressedItem = Key.esc
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.tab':
                                    pressedButtonName = 'It is TAB'
                                    status = 'Not'
                                    pressedItem = Key.tab
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.caps_lock':
                                    pressedButtonName = 'It is CAPS_LOCK'
                                    status = 'Not'
                                    pressedItem = Key.caps_lock
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.space':
                                    pressedButtonName = 'It is SpaceBar'
                                    status = 'Not'
                                    pressedItem = Key.space
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.enter':
                                    pressedButtonName = 'It is Enter'
                                    status = 'Not'
                                    pressedItem = Key.enter
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.backspace':
                                    pressedButtonName = 'It is BackSpace'
                                    status = 'Not'
                                    pressedItem = Key.backspace
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f1':
                                    pressedButtonName = 'It is F1'
                                    status = 'Not'
                                    pressedItem = Key.f1
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f2':
                                    pressedButtonName = 'It is F2'
                                    status = 'Not'
                                    pressedItem = Key.f2
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f3':
                                    pressedButtonName = 'It is F3'
                                    status = 'Not'
                                    pressedItem = Key.f3
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f4':
                                    pressedButtonName = 'It is F4'
                                    status = 'Not'
                                    pressedItem = Key.f4
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f5':
                                    pressedButtonName = 'It is F5'
                                    status = 'Not'
                                    pressedItem = Key.f5
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f6':
                                    pressedButtonName = 'It is F6'
                                    status = 'Not'
                                    pressedItem = Key.f6
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f7':
                                    pressedButtonName = 'It is F7'
                                    status = 'Not'
                                    pressedItem = Key.f7
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f8':
                                    pressedButtonName = 'It is F8'
                                    status = 'Not'
                                    pressedItem = Key.f8
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f9':
                                    pressedButtonName = 'It is F9'
                                    status = 'Not'
                                    pressedItem = Key.f9
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f10':
                                    pressedButtonName = 'It is F10'
                                    status = 'Not'
                                    pressedItem = Key.f10
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f11':
                                    pressedButtonName = 'It is F11'
                                    status = 'Not'
                                    pressedItem = Key.f11
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.f12':
                                    pressedButtonName = 'It is F12'
                                    status = 'Not'
                                    pressedItem = Key.f12
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.print_screen':
                                    pressedButtonName = 'It is PRINT_SCREEN'
                                    status = 'Not'
                                    pressedItem = Key.print_screen
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.scroll_lock':
                                    pressedButtonName = 'It is SCROLL_LOCK'
                                    status = 'Not'
                                    pressedItem = Key.scroll_lock
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.pause':
                                    pressedButtonName = 'It is PAUSE'
                                    status = 'Not'
                                    pressedItem = Key.pause
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.insert':
                                    pressedButtonName = 'It is INSERT'
                                    status = 'Not'
                                    pressedItem = Key.insert
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.home':
                                    pressedButtonName = 'It is HOME'
                                    status = 'Not'
                                    pressedItem = Key.home
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.page_up':
                                    pressedButtonName = 'It is PAGE_Up'
                                    status = 'Not'
                                    pressedItem = Key.page_up
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.delete':
                                    pressedButtonName = 'It is DELETE'
                                    status = 'Not'
                                    pressedItem = Key.delete
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.end':
                                    pressedButtonName = 'It is END'
                                    status = 'Not'
                                    pressedItem = Key.end
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.page_down':
                                    pressedButtonName = 'It is PAGE_Down'
                                    status = 'Not'
                                    pressedItem = Key.page_down
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.up':
                                    pressedButtonName = 'It is ArrowKey_Up'
                                    status = 'Not'
                                    pressedItem = Key.up
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.down':
                                    pressedButtonName = 'It is ArrowKey_Down'
                                    status = 'Not'
                                    pressedItem = Key.down
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.left':
                                    pressedButtonName = 'It is ArrowKey_Left'
                                    status = 'Not'
                                    pressedItem = Key.left
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.right':
                                    pressedButtonName = 'It is ArrowKey_Right'
                                    status = 'Not'
                                    pressedItem = Key.right
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == 'Key.num_lock':
                                    pressedButtonName = 'It is NUMPAD_Lock'
                                    status = 'Not'
                                    pressedItem = Key.num_lock
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<96>':
                                    pressedButtonName = 'It is Numpad_0'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=96)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<97>':
                                    pressedButtonName = 'It is Numpad_1'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=97)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<98>':
                                    pressedButtonName = 'It is Numpad_2'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=98)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<99>':
                                    pressedButtonName = 'It is Numpad_3'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=99)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<100>':
                                    pressedButtonName = 'It is Numpad_4'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=100)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<101>':
                                    pressedButtonName = 'It is Numpad_5'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=101)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<102>':
                                    pressedButtonName = 'It is Numpad_6'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=102)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<103>':
                                    pressedButtonName = 'It is Numpad_7'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=103)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<104>':
                                    pressedButtonName = 'It is Numpad_8'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=104)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<105>':
                                    pressedButtonName = 'It is Numpad_9'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=105)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                elif items == '<12>':
                                    pressedButtonName = 'It is Numpad_5 with Numlock-Off'
                                    status = 'Not'
                                    pressedItem = keyboard.KeyCode(vk=12)
                                    pressButton = keyboardController.press(pressedItem)
                                    keyboardController.release(pressedItem)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []

                                else:
                                    pressedButtonName = str(items)
                                    status = 'Not'
                                    pressButton = keyboardController.press(pressedButtonName)
                                    keyboardController.release(pressedButtonName)

                                    if len(selectedModifierList) >= 1:
                                        if status == 'Not':
                                            for keyModifier in selectedModifierList:
                                                if keyModifier == str(Key.ctrl_l):
                                                    keyboardController.release(Key.ctrl_l)
                                                elif keyModifier == str(Key.ctrl_r):
                                                    keyboardController.release(Key.ctrl_r)
                                                elif keyModifier == str(Key.ctrl):
                                                    keyboardController.release(Key.ctrl)
                                                elif keyModifier == str(Key.shift):
                                                    keyboardController.release(Key.shift)
                                                elif keyModifier == str(Key.shift_l):
                                                    keyboardController.release(Key.shift_l)
                                                elif keyModifier == str(Key.shift_r):
                                                    keyboardController.release(Key.shift_r)
                                                elif keyModifier == str(Key.alt):
                                                    keyboardController.release(Key.alt)
                                                elif keyModifier == str(Key.alt_l):
                                                    keyboardController.release(Key.alt_l)
                                                elif keyModifier == str(Key.alt_r):
                                                    keyboardController.release(Key.alt_r)
                                                elif keyModifier == str(Key.cmd_l):
                                                    keyboardController.release(Key.cmd_l)
                                                elif keyModifier == str(Key.cmd_r):
                                                    keyboardController.release(Key.cmd_r)
                                                elif keyModifier == str(Key.cmd):
                                                    keyboardController.release(Key.cmd)
                                            selectedModifierList = []
                        self.repeatCounter += 1

                        if self.executionStatus == False:
                            break

        self.thread = threading.Thread(target=runKeyPress)
        self.thread.start()

    def stopKeyPresses(self):
        self.endExecuteButton.setDisabled(True)
        self.recordAction.setDisabled(False)
        self.startExecuteButton.setDisabled(False)
        self.startdelaySpinBox.setDisabled(False)
        if self.radioButtonIndividual.isChecked() == True:
            self.radioButtonUniform.setDisabled(False)
        self.delaySpinBox.setDisabled(False)
        self.radioButtonRepeatTimes.setDisabled(False)
        self.repeatSpinBox.setDisabled(False)
        self.radioButtonRepeatContinue.setDisabled(False)
        self.currentState.setText('Command Ended')

        if self.radioButtonRepeatContinue.isChecked() == True:
            self.executionStatus = False
        else:
            self.executionStatus = False


def mainApplication():
    application = QApplication(sys.argv)
    application.setStyle('Fusion')
    mainWindow = KeyboardRecorder()
    mainWindow.show()
    sys.exit(application.exec())


mainApplication()
