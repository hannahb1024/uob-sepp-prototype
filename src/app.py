from PyQt5.QtWidgets import *
from qfluentwidgets import *
import src.statistics_test as st
import src.graphing as g
import src.DBConnect as dbc

def exampleTestingFunction():
    return "Hello, world!"

class PlaceholderCard(ElevatedCardWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)

class MarkerCard(ElevatedCardWidget): # https://qfluentwidgets.com/pages/components/cardwidget
    def __init__(self, marker: st.Marker, testid , mainWindowOwner,parent=None):
        super().__init__(parent)
        self.mainWindowOwner = mainWindowOwner
        self.marker = marker
        self.testId = testid
        self.trustIsChecked = False
        
        self.generateLabels()
        self.addButtons()

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(10)

        self.vBoxLayout.addWidget(self.markerName)
        self.vBoxLayout.addWidget(self.numTestsMarked)
        self.vBoxLayout.addWidget(self.rank)
        self.vBoxLayout.addWidget(self.trustAndInspectHorizontal)

        self.setFixedSize(400, 180)

    def addButtons(self):
        self.trust = CheckBox("Trust")
        self.inspect = PushButton("Inspect")

        self.inspect.clicked.connect(self.inspectMarker)
        self.trust.toggled.connect(self.toggleTrusted)

        self.trustAndInspectHorizontal = QWidget()
        self.trustAndInspectHorizontalLayout = QHBoxLayout()
        self.trustAndInspectHorizontalLayout.addWidget(self.trust)
        self.trustAndInspectHorizontalLayout.addWidget(self.inspect)
        self.trustAndInspectHorizontal.setLayout(self.trustAndInspectHorizontalLayout)
    
    def generateLabels(self):
        self.markerName = BodyLabel("Name: " + self.marker.firstName + " " + self.marker.lastName + " " + st.getConcern(self.marker), self)
        self.numTestsMarked = BodyLabel("Tests marked: " + str(len(self.marker.markedTests)), self)
        self.rank = BodyLabel("Rank: " + self.marker.role, self)

    def toggleTrusted(self):
        if self.trustIsChecked:
            st.removeExemplaryMarker(self.marker)
            self.trustIsChecked = False
        else:
            st.addExemplaryMarker(self.marker)
            self.trustIsChecked = True

    def inspectMarker(self):
        self.mainWindowOwner.replaceGraph(g.MarkerGraph(self.marker, self.testId))

class mainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.makersGrabbed = False
        self.markerCards = []
        mainWindowView = QHBoxLayout()
        self.leftPaneView = QVBoxLayout()
        self.rightPaneView = QVBoxLayout()

        self.setLayout(mainWindowView)

        leftPane = QWidget()
        rightPane = QWidget()
        leftPane.setLayout(self.leftPaneView)
        rightPane.setLayout(self.rightPaneView)

        self.markerListPlaceholder = PlaceholderCard(425, 800)
        self.currentDisplayingGraph = PlaceholderCard(800, 838)

        self.loadDatabaseButton = PushButton("Load database")
        self.loadDatabaseButton.clicked.connect(self.loadDatabase)
        self.leftPaneView.addWidget(self.loadDatabaseButton)

        self.dropDown = QComboBox()
        self.dropDown.addItems(self.getCleanedTestIds())
        self.leftPaneView.addWidget(self.dropDown)

        self.leftPaneView.addWidget(self.markerListPlaceholder)
        self.rightPaneView.addWidget(self.currentDisplayingGraph)

        mainWindowView.addWidget(leftPane)
        mainWindowView.addWidget(rightPane)


    def getCleanedTestIds(self):
        ids = dbc.testIDCollect()
        cleaned = []
        for item in ids:
            cleaned.append(str(item[0]))
        return cleaned

    def loadDatabase(self):
        self.markerListPlaceholder.setParent(None)
        self.markerListPlaceholder = SingleDirectionScrollArea()
        self.markerListPlaceholder.setFixedSize(425, 800)

        view = QWidget()
        layout = QVBoxLayout(view)
        st.loadNewTest(int(self.dropDown.currentText()))
        for marker in st.getMarkers():
            markerCardToAdd = MarkerCard(marker, int(self.dropDown.currentText()), self)
            layout.addWidget(markerCardToAdd)
            self.markerCards.append(markerCardToAdd)

        self.markerListPlaceholder.setWidget(view)
        self.leftPaneView.addWidget(self.markerListPlaceholder)

    def replaceGraph(self, graph):
        self.currentDisplayingGraph.setParent(None)
        self.currentDisplayingGraph = graph
        self.rightPaneView.addWidget(graph)


def main():
    app = QApplication([])
    window = mainWindow()

    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
