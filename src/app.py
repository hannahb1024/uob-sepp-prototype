from PyQt5.QtWidgets import *
from qfluentwidgets import *
import statistics_test as st
import graphing as g

class MarkerCard(ElevatedCardWidget): # https://qfluentwidgets.com/pages/components/cardwidget

    def __init__(self, markerName: str, numTestsMarked: str, rank: str, parent=None):
        super().__init__(parent)
        self.markerName = BodyLabel("Name: " + markerName, self)
        self.numTestsMarked = BodyLabel("Tests marked: " + numTestsMarked, self)
        self.rank = BodyLabel("Rank: " + rank, self)
        self.trust = CheckBox("Trust")

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(10)

        self.vBoxLayout.addWidget(self.markerName)
        self.vBoxLayout.addWidget(self.numTestsMarked)
        self.vBoxLayout.addWidget(self.rank)
        self.vBoxLayout.addWidget(self.trust)

        self.setFixedSize(400, 120)

def main():
    app = QApplication([])
    window = QWidget()
    windowLayout = QVBoxLayout()
    window.setLayout(windowLayout)

    windowLayout.addWidget(PushButton("Load Database"))
    windowLayout.addWidget(PushButton("Connect to CSRS"))

    windowLayout.addWidget(MarkerCard("Bob Teacher", "69", "Module lead"))
    windowLayout.addWidget(MarkerCard("Bob Dylan", "70", "Module staff"))
    windowLayout.addWidget(MarkerCard("Bob Marley", "71", "Module staff"))
    windowLayout.addWidget(MarkerCard("Bob Ross", "72", "Module staff"))
    windowLayout.addWidget(MarkerCard("Bob Odenkirk", "73", "Module staff"))



    window.show()
    app.exec_()

if __name__ == '__main__':
    main()