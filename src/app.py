from PyQt5.QtWidgets import *
from qfluentwidgets import *
import statistics_test as st
import graphing as g



class MarkerCard(ElevatedCardWidget): # https://qfluentwidgets.com/pages/components/cardwidget

    def __init__(self, marker: st.Marker, mainWindowOwner, parent=None):
        super().__init__(parent)
        self.mainWindowOwner = mainWindowOwner
        self.marker = marker
        self.markerName = BodyLabel("Name: " + marker.firstName + " " + marker.lastName, self)
        self.numTestsMarked = BodyLabel("Tests marked: " + str(len(marker.markedTests)), self)
        self.rank = BodyLabel("Rank: " + marker.role, self)
        self.trust = CheckBox("Trust")
        self.inspect = PushButton("Inspect")
        self.inspect.clicked.connect(lambda: inspectMarker(self.marker, self.mainWindowOwner))

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

class PlaceholderCard(ElevatedCardWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)

def inspectMarker(marker: st.Marker, mainWindowOwner):
    print("Inspecting marker...")
    mainWindowOwner.graphViewPlaceholder.setParent(None)
    mainWindowOwner.rightPaneView.addWidget(g.MarkerGraph(marker))

def loadDatabase(mainWindowOwner):
    mainWindowOwner.markerListPlaceholder.setParent(None)
    scrollArea = SingleDirectionScrollArea()
    scrollArea.setFixedSize(425, 800)

    view = QWidget()
    layout = QVBoxLayout(view)
    st.loadNewTest(0)
    for marker in st.getMarkers():
        layout.addWidget(MarkerCard(marker, mainWindowOwner))

    scrollArea.setWidget(view)
    mainWindowOwner.leftPaneView.addWidget(scrollArea)

class mainWindow(QWidget):
    def __init__(self, parent=None):

        mainWindowView = QHBoxLayout()
        self.leftPaneView = QVBoxLayout()
        self.rightPaneView = QVBoxLayout()

        super().__init__(parent)
        self.setLayout(mainWindowView)

        leftPane = QWidget()
        rightPane = QWidget()
        leftPane.setLayout(self.leftPaneView)
        rightPane.setLayout(self.rightPaneView)

        self.markerListPlaceholder = PlaceholderCard(425, 800)
        self.graphViewPlaceholder = PlaceholderCard(800, 838)

        loadDatabaseButton = PushButton("Load database")
        loadDatabaseButton.clicked.connect(lambda: loadDatabase(self))
        self.leftPaneView.addWidget(loadDatabaseButton)

        self.leftPaneView.addWidget(self.markerListPlaceholder)
        self.rightPaneView.addWidget(self.graphViewPlaceholder)

        mainWindowView.addWidget(leftPane)
        mainWindowView.addWidget(rightPane)


def main():
    app = QApplication([])
    window = mainWindow()

    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
