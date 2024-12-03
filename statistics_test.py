

def countInRange(list , min , max):
    count = 0
    for item in list:
        if (min<=item) and (item < max):
            count += 1
    return count

class binned_data():
    maxValue = 0
    minValue = 0
    numRange = 0
    numberOfBins = 10
    binRangeSize = 0
    binRanges = [(0,0)]*numberOfBins


    def __init__(self, scores_list):
        
        self.bins = [None]*binned_data.numberOfBins
        self.size = len(scores_list)
        self.compressed=False

        if self.size<=0:
            print("List is empty cannot bin values")
        else:
            binLower=binned_data.minValue
            binUpper=binned_data.minValue+binned_data.binRangeSize
            for i in range(0,binned_data.numberOfBins-1):
                self.bins[i]=countInRange(scores_list,binLower,binUpper)
                binLower=binUpper
                binUpper+=binned_data.binRangeSize
            self.bins[binned_data.numberOfBins-1]=countInRange(scores_list,binLower,binUpper+1)
    
    def compress(self):
        for i in range(0,self.numberOfBins-1):
            self.bins[i] /= self.size
        self.compressed=True

    def toExpected(self,expectedSize):
        if not(self.compressed):
            self.compress()
        for i in range(0,self.numberOfBins-1):
            self.bins[i] *= expectedSize
        self.size=expectedSize
        self.compressed=False
    
    def chiSquaredTest(self,expected):
        chi_squared=0
        for i in range(0,self.numberOfBins-1):
            difference=self.bins[i]-expected.bins[i]
            chi_squared+=(difference*difference)/expected.bins[i]
        return chi_squared
    
class TestResult():
    def __init__(self,attributes):
        self.ID = int(attributes[0])
        self.studentID = int(attributes[1])
        self.score = int(attributes[2])
        self.markerID = int(attributes[3])
        self.testID = int(attributes[4])

def toScoreList(testResultList):
    scoreList=[]
    for testResult in testResultList:
        scoreList.append(testResult.score)
    return scoreList

class Marker():
    def __init__(self,markerID):
        global data,nonExemplaryMarkers
        self.markerID=markerID
        self.isValid=False
        nonExemplaryMarkers.append(self)
        self.markedTests=[]
        for testResult in data:
            if testResult.markerID==self.markerID:
                self.markedTests.append(testResult)
        self.binnedData=binned_data(toScoreList(self.markedTests))
        self.expectedResult = None
        self.getExpectedResult()
    
    def getExpectedResult(self):
        global allDataBin
        expectedResult=[]
        expectedResultMultiplier=self.binnedData.size*(allDataBin.size - self.binnedData.size)#divide by difference in data times by size
        for i in range(0,binned_data.numberOfBins):
            expectedResult.append((allDataBin.bins[i] - self.binnedData.bins[i]) * expectedResultMultiplier)
        self.expectedResult = expectedResult
        
    




def getTestID(s:str):
    testAttibutes=s.split(",")
    return int(testAttibutes[4])

def getData(testID):
    testDataFile=open("TestData.txt","r")
    fileData=[]
    for line in testDataFile:
        #print(line)
        if (getTestID(line)==testID):
            fileData.append(TestResult(line.split(",")))
    testDataFile.close()
    return fileData


def getAllScores(testList):
    intList=[]
    for test in testList:
        intList.append(test.score)
    return intList

def getMarkers():
    global data,markers
    foundMarkers = set()
    for test in data:
        if not(test.markerID in foundMarkers):
            markers.append(Marker(test.markerID))
            foundMarkers.add(test.markerID)


def loadNewTest(testID):
    global data,allDataBin
    data = getData(testID)
    if data==[]:
        print("No data test found with that ID.")
        return
    allScores = getAllScores(data)
    binned_data.maxValue=max(allScores)
    binned_data.minValue=min(allScores)
    binned_data.numRange=binned_data.maxValue-binned_data.minValue
    binned_data.binRangeSize=binned_data.numRange/binned_data.numberOfBins
    tempLower=binned_data.minValue
    tempUpper=tempLower+binned_data.binRangeSize
    for i in range(0,binned_data.numberOfBins):
        binned_data.binRanges[i]=(tempLower,tempUpper)
        tempLower+=binned_data.binRangeSize
        tempUpper+=binned_data.binRangeSize
    allDataBin = binned_data(allScores)

    getMarkers()

    return



data=[]
allDataBin = None
markers = []
nonExemplaryMarkers=[]
exemplaryMarkers=[]
exemplaryDataBin = None



def main():
    loadNewTest(0)
    print(allDataBin.bins)
    print(binned_data.binRanges)
    loadNewTest(1)
    print(allDataBin.bins)
    print(binned_data.binRanges)
    loadNewTest(8)
    print(allDataBin.bins)
    print(binned_data.binRanges)
    loadNewTest(12)
    print(allDataBin.bins)
    print(binned_data.binRanges)
    loadNewTest(15)
    loadNewTest(20)


if __name__ == '__main__':
    main()