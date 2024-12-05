from PyQt5.QtWidgets import *
import PyQt5.QtCore as core
from qfluentwidgets import *
from pyqtgraph import *
import statistics_test as st

class MarkerGraph(ElevatedCardWidget):

    def __init__(self, marker: st.Marker):
        super().__init__()
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

        self.slider.valueChanged.connect(lambda : print(self.slider.value()/2))

        self.saveButton = PushButton("Save")

        self.expButton = PushButton("Optimal due to exemplary markers")

        self.allButton = PushButton("Optimal due to all markers")
        
        self.graphLayout.addWidget(self.getGraph(marker))
        self.graphLayout.addWidget(self.slider)
        self.graphLayout.addWidget(self.saveButton)
        self.graphLayout.addWidget(self.expButton)
        self.graphLayout.addWidget(self.allButton)

    
    def getGraph(self, marker: st.Marker):
        graph = PlotWidget()
        expMarkerMarks = st.binned_data(marker.expectedResultExemplary)
        allMarkerMarks = st.binned_data(marker.expectedResultAll)
        theirMarkerMarks = marker.binnedData
        
        expX = []
        allX = []
        theirX = []

        for i in expMarkerMarks.binRanges:
            expX.append((i[0] + i[1])/2)
        for j in allMarkerMarks.binRanges:
            allX.append((j[0] + j[1])/2)
        for k in theirMarkerMarks.binRanges:
            theirX.append((k[0] + k[1])/2)

        expBG = BarGraphItem(x = expX, height = expMarkerMarks.bins, width = 5, brush = 'g')
        allBG = BarGraphItem(x = allX, height = allMarkerMarks.bins, width = 5, brush = 'b')
        theirBG = BarGraphItem(x = theirX, height = theirMarkerMarks.bins, width = 5, brush = 'r')

        graph.addItem(expBG)
        graph.addItem(allBG)
        graph.addItem(theirBG)

        return graph
    