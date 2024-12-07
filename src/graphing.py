from PyQt5.QtWidgets import *
import PyQt5.QtCore as core
from qfluentwidgets import *
from pyqtgraph import *
import statistics_test as st

class MarkerGraph(ElevatedCardWidget):

    def __init__(self, marker: st.Marker):
        super().__init__()
        self.m = marker
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
        expMarkerMarks = st.binned_data(self.m.expectedResultExemplary).bins
        allMarkerMarks = st.binned_data(self.m.expectedResultAll).bins
        theirMarkerMarks = self.m.binnedData.bins
        
        theirX = []

        for k in st.binned_data.binRanges:
            theirX.append((k[0] + k[1])/2)

        expBG = BarGraphItem(x = theirX, height = expMarkerMarks, width = 5, brush = 'g')
        allBG = BarGraphItem(x = theirX, height = allMarkerMarks, width = 5, brush = 'b')
        self.theirBG = BarGraphItem(x = theirX, height = theirMarkerMarks, width = 5, brush = 'r')

        graph.addItem(expBG)
        graph.addItem(allBG)
        graph.addItem(self.theirBG)

        return graph
    
    def sliderChange(self):
        self.updateGraph(self.slider.value())

    def updateToFitExp(self): #Hill climbing functions used and cllaed here
        self.updateGraph(self.slider.value()+3)
        self.slider.setValue(self.slider.value()+3)

    def updateToFitAll(self): #Hill climbing functions used and cllaed here
        self.updateGraph(self.slider.value()-3)
        self.slider.setValue(self.slider.value()-3)

    def updateGraph(self, sv : int):
        dif = sv-self.mod
        self.mod = sv
        
        for elm in range(len(self.sc)):
            self.sc[elm] += dif
        
        self.m.binnedData = st.binned_data(self.sc)

        self.theirBG.setOpts(height=self.m.binnedData.bins)
