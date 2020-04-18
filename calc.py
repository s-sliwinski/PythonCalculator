from PyQt5.QtWidgets import *
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import QIcon
import sys
from functools import partial


class CalcGui(QMainWindow):
    def __init__(self):
        super().__init__()
        ### window options ###
        self.setWindowTitle("pyCalculator")
        self.setFixedSize(300,400)
        ### layouts ###
        self.mainlayout = QVBoxLayout()
        ### central widget options ###
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(self.mainlayout)
        ### add display ###
        self.display = QLineEdit()
        self.display.setFixedHeight(40)
        self.display.setAlignment(Qt.AlignRight)
        self.mainlayout.addWidget(self.display)
        ### add buttons ###
        self.createButtons()

    def createButtons(self):
        buttonsLayout = QGridLayout()
        self.buttons = {}
        tmpbtn = {'7': (0, 0), '8': (0, 1), '9': (0, 2), '+': (0, 3), '-': (0, 4),
                  '4': (1, 0), '5': (1, 1), '6': (1, 2), '*': (1, 3), '/': (1, 4),
                  '1': (2, 0), '2': (2, 1), '3': (2, 2), '(': (2, 3), ')': (2, 4),
                  '0': (3, 0), '00': (3, 1), '.': (3, 2), 'C': (3, 3), '=': (3, 4),}

        ### creating keybord ###
        for btn, pos in tmpbtn.items():
            self.buttons[btn] = QPushButton(btn)
            self.buttons[btn].setFixedSize(50,50)
            buttonsLayout.addWidget(self.buttons[btn], pos[0], pos[1])


        self.mainlayout.addLayout(buttonsLayout)

    def setDisplay(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def getDisplay(self):
        return self.display.text()

    def clearDisplay(self):
        self.display.clear()

class CalcCtrl:
    def __init__(self, model, gui):
        self.model = model
        self.gui = gui
        self.connectSignals()

    def buildExpression(self, keybordKey):
        text  = self.gui.getDisplay() + keybordKey
        self.gui.setDisplay(text)

    def connectSignals(self):
        for btnKey, btn in self.gui.buttons.items():
            if btnKey not in ['=', 'C']:
                btn.clicked.connect(partial(self.buildExpression, btnKey))

        self.gui.buttons['C'].clicked.connect(self.gui.clearDisplay)
        self.gui.buttons['='].clicked.connect(self.calculate)
        self.gui.display.returnPressed.connect(self.calculate)

    def calculate(self):
        result = self.model.evaluateExpression(self.gui.getDisplay())
        self.gui.setDisplay(result)

class CalcMdl:
    def evaluateExpression(self, expression):
        try:
            result = str(eval(expression, {}, {}))
        except Exception:
            result = "ERROR"

        return result

def main():
    calc = QApplication(sys.argv)
    gui = CalcGui()
    gui.show()
    model = CalcMdl()
    ctrl = CalcCtrl(model, gui)
    calc.exec_()

if __name__ == '__main__':
    main()
