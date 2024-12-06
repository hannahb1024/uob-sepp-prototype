from PyQt5.QtWidgets import *
from pyqtgraph.examples.MatrixDisplayExample import main_window
from qfluentwidgets import *
import statistics_test as st
import graphing as g

mainWindowLayout = QVBoxLayout()

class MarkerCard(ElevatedCardWidget): # https://qfluentwidgets.com/pages/components/cardwidget

    def __init__(self, marker: st.Marker, parent=None):
        super().__init__(parent)
        self.marker = marker
        self.markerName = BodyLabel("Name: " + marker.firstName + " " + marker.lastName, self)
        self.numTestsMarked = BodyLabel("Tests marked: " + str(len(marker.markedTests)), self)
        self.rank = BodyLabel("Rank: " + marker.role, self)
        self.trust = CheckBox("Trust")
        self.inspect = PushButton("Inspect")
        self.inspect.clicked.connect(lambda: inspectMarker(self.marker))

        self.trustAndInspectHorizontal = QWidget()
        self.trustAndInspectHorizontalLayout = QHBoxLayout()
        self.trustAndInspectHorizontalLayout.addWidget(self.trust)
        self.trustAndInspectHorizontalLayout.addWidget(self.inspect)
        self.trustAndInspectHorizontal.setLayout(self.trustAndInspectHorizontalLayout)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(10)

        self.vBoxLayout.addWidget(self.markerName)
        self.vBoxLayout.addWidget(self.numTestsMarked)
        self.vBoxLayout.addWidget(self.rank)
        self.vBoxLayout.addWidget(self.trustAndInspectHorizontal)

        self.setFixedSize(400, 180)

class MarkerListPlaceholder(ElevatedCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(425, 800)

def inspectMarker(marker: st.Marker):
    print("Inspecting marker...")

def loadDatabase(markerListPlaceholder):
    markerListPlaceholder.setParent(None)
    scrollArea = SingleDirectionScrollArea()
    scrollArea.setFixedSize(425, 800)

    view = QWidget()
    layout = QVBoxLayout(view)
    st.loadNewTest(0)
    for marker in st.getMarkers():
        layout.addWidget(MarkerCard(marker))

    scrollArea.setWidget(view)
    mainWindowLayout.addWidget(scrollArea)

def main():
    app = QApplication([])
    window = QWidget()
    window.setLayout(mainWindowLayout)

    markerListPlaceholder = MarkerListPlaceholder()

    loadDatabaseButton = PushButton("Load database")
    loadDatabaseButton.clicked.connect(lambda: loadDatabase(markerListPlaceholder))
    mainWindowLayout.addWidget(loadDatabaseButton)

    mainWindowLayout.addWidget(markerListPlaceholder)

    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
