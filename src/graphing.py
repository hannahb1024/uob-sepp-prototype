from PyQt5.QtWidgets import *
import PyQt5.QtCore as core
from qfluentwidgets import *
from pyqtgraph import *
import statistics_test as st
import DBConnect as dbc

class MarkerGraph(ElevatedCardWidget):

    def __init__(self, marker: st.Marker, testid):
        super().__init__()
        self.m = marker
        self.tid = testid
        self.sc = st.toScoreList(self.m.markedTests)
        self.mod = 0

        self.graphLayout = QVBoxLayout(self)
        self.graphLayout.setSpacing(10)

        self.slider = QSlider(self)
        self.slider.setOrientation(core.Qt.Orientation.Horizontal)
        self.slider.setMinimum(-40)
        self.slider.setMaximum(40)
        self.slider.setValue(0)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(2)
        self.slider.setTickPosition(QSlider.TicksBothSides)

        self.slider.valueChanged.connect(self.sliderChange)

        self.saveButton = PushButton("Save")
        self.saveButton.pressed.connect(self.updateDB)

        self.expButton = PushButton("Optimal due to exemplary markers")
        self.expButton.pressed.connect(self.updateToFitExp)

        self.allButton = PushButton("Optimal due to all markers")
        self.allButton.pressed.connect(self.updateToFitAll)
        
        self.graph = self.getGraph()

        self.graphLayout.addWidget(self.graph)
        self.graphLayout.addWidget(self.slider)
        self.graphLayout.addWidget(self.saveButton)
        self.graphLayout.addWidget(self.expButton)
        self.graphLayout.addWidget(self.allButton)

    
    def getGraph(self):
        graph = PlotWidget()
        expMarkerMarks = self.m.expectedResultExemplary
        allMarkerMarks = self.m.expectedResultAll
        theirMarkerMarks = self.m.binnedData.bins
        
        theirX = []
        expX = []
        allX = []

        for k in st.binned_data.binRanges:
            theirX.append((k[0] + k[1])/2)
            expX.append(((k[0] + k[1])/2)+1)
            allX.append(((k[0] + k[1])/2)-1)

        if expMarkerMarks != [None] * 10:
            expBG = BarGraphItem(x = expX, height = expMarkerMarks, width = 1, brush = 'g')
            graph.addItem(expBG)
            
        allBG = BarGraphItem(x = allX, height = allMarkerMarks, width = 1, brush = 'b')
        graph.addItem(allBG)

        self.theirBG = BarGraphItem(x = theirX, height = theirMarkerMarks, width = 1, brush = 'r')
        graph.addItem(self.theirBG)

        return graph
    
    def sliderChange(self):
        self.updateGraph(self.slider.value())

    def updateToFitExp(self): #Hill climbing functions used and cllaed here
        self.updateGraph(self.m.adjustScoresToExemplary())
        self.slider.setValue(int(self.m.adjustScoresToExemplary()))

    def updateToFitAll(self): #Hill climbing functions used and cllaed here
        self.updateGraph(self.m.adjustScoresToAll())
        self.slider.setValue(int(self.m.adjustScoresToAll()))

    def updateDB(self):
        dbc.updateDatabase(self.m.markerID, self.tid, self.mod)


    def updateGraph(self, sv : int):
        dif = sv-self.mod
        self.mod = sv
        
        for elm in range(len(self.sc)):
            self.sc[elm] += dif
        
        self.m.binnedData = st.binned_data(self.sc)

        self.theirBG.setOpts(height=self.m.binnedData.bins)
