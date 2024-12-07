from PyQt5.QtWidgets import *
from PyQt5 import uic

class Gui(QMainWindow):
    def __init__(self):
        super(Gui, self).__init__()
        uic.loadUi("main.ui", self)
        self.show()

def main():
    app = QApplication([])
    window = Gui()
    app.exec_()

if __name__ == '__main__':
    main()