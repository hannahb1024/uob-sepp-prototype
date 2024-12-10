import PyQt5.QtCore as core
from PyQt5.QtWidgets import *
from qfluentwidgets import *
import statistics_test as st
import graphing as g

def exampleTestingFunction():
    return "Hello, world!"

class PlaceholderCard(ElevatedCardWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)

class MarkerCard(ElevatedCardWidget): # https://qfluentwidgets.com/pages/components/cardwidget
    def __init__(self, marker: st.Marker, mainWindowOwner, parent=None):
        super().__init__(parent)
        self.mainWindowOwner = mainWindowOwner
        self.marker = marker
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
        self.markerName = BodyLabel("Name: " + self.marker.firstName + " " + self.marker.lastName, self)
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
        self.mainWindowOwner.replaceGraph(g.MarkerGraph(self.marker))

class mainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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

        loadDatabaseButton = PushButton("Load database")
        loadDatabaseButton.clicked.connect(self.loadDatabase)
        self.leftPaneView.addWidget(loadDatabaseButton)

        self.leftPaneView.addWidget(self.markerListPlaceholder)
        self.rightPaneView.addWidget(self.currentDisplayingGraph)

        mainWindowView.addWidget(leftPane)
        mainWindowView.addWidget(rightPane)


    def loadDatabase(self):
        self.markerListPlaceholder.setParent(None)
        scrollArea = SingleDirectionScrollArea()
        scrollArea.setFixedSize(425, 800)

        view = QWidget()
        layout = QVBoxLayout(view)
        st.loadNewTest(0)
        for marker in st.getMarkers():
            layout.addWidget(MarkerCard(marker, self))

        scrollArea.setWidget(view)
        self.leftPaneView.addWidget(scrollArea)

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
