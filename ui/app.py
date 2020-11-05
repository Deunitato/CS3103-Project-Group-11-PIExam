import os, sys
from PyQt5 import QtWidgets, uic

class HomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(HomeWindow, self).__init__()
        uic.loadUi('ui/home.ui', self)

    def setQuestionWidget(self, widget):
        self.question_stackedWidget.addWidget(widget)
        self.question_stackedWidget.setCurrentWidget(widget)

class McqWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(McqWidget, self).__init__()
        uic.loadUi('ui/mcq.ui', self)
        self.setParent(parent)


class MrqWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MrqWidget, self).__init__()
        uic.loadUi('ui/mrq.ui', self)
        self.setParent(parent)
        self.setFrameShape(QtWidg)

class OpenEndedWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OpenEndedWidget, self).__init__()
        uic.loadUi('ui/open.ui', self)
        self.setParent(parent)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = HomeWindow()
    ui.show()

    ui.setQuestionWidget(McqWidget(ui))

    sys.exit(app.exec_())