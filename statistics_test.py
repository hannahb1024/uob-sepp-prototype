import copy

def countInRange(list , min , max):#Counts the number of numbers withing the given range
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
    
    def chiSquaredTest(self,expected):#expected is a list of nums of the same size
        if expected==[]:#If the expected list is empty return an error value (-1)
            return -1
        chi_squared=0
        for i in range(0,self.numberOfBins-1):
            difference=self.bins[i]-expected[i]
            chi_squared+= (difference*difference) if expected[i]==0 else (difference*difference)/expected[i]#Duck tape fix for dividing by 0
        return chi_squared
    
    def add(self,binnedData):
        for i in range(0,binned_data.numberOfBins):
            self.bins[i]+=binnedData.bins[i]
        self.size+=binnedData.size

    def subtract(self,binnedData):
        for i in range(0,binned_data.numberOfBins):
            self.bins[i]-=binnedData.bins[i]
        self.size-=binnedData.size
    

class TestResult():#Essentially a nice tuple of teh form (int,int,int,int,int)
    def __init__(self,attributes):
        #Attributes is a string of the form int,int,int,int,int
        self.ID = int(attributes[0])
        self.studentID = int(attributes[1])
        self.score = int(attributes[2])
        self.markerID = int(attributes[3])
        self.testID = int(attributes[4])


def toScoreList(testResultList):#Takes a list of objects of type TestResult and returns a list of scores from the tests
    scoreList=[]
    for testResult in testResultList:
        scoreList.append(testResult.score)
    return scoreList


class Marker():
    def __init__(self,attributes):
        global data,nonExemplaryMarkers
        #attributes is a string of the form int,int,string,string,string
        self.markerID=int(attributes[0])
        self.moduleID=int(attributes[1])
        self.firstName=attributes[2]
        self.lastName=attributes[3]
        if attributes[4].endswith("\n"):#the last value can come out weird because its read from a file this sorts it
            self.role=attributes[4][:-1]
        else:
            self.role=attributes[4]

        self.isExemplary=False#default is no
        nonExemplaryMarkers.append(self)#global list for all non exemplary markers for general use and processing

        self.markedTests=[]#List of all tests this marker has marked
        for testResult in data:
            if testResult.markerID==self.markerID:
                self.markedTests.append(testResult)

        self.binnedData=binned_data(toScoreList(self.markedTests))#Process list of tests into binned data for chi-squared tests
        self.expectedResultAll = self.getExpectedResultAll()#Function that creates the expected result from all the other test results
        self.chiSquaredAll=self.binnedData.chiSquaredTest(self.expectedResultAll)
        self.expectedResultExemplary = []
        self.chiSquaredExemplary = -1
    
    def recalculateExemplaryValues(self):
        self.expectedResultExemplary=self.getExpectedResultExemplary()
        self.chiSquaredExemplary=self.binnedData.chiSquaredTest(self.expectedResultExemplary)


    def getExpectedResultAll(self):#returns a float/double list of size numberOfBins of the expected result 
        global allDataBin
        expectedResult=[]
        expectedResultSize=allDataBin.size - self.binnedData.size
        expectedResultMultiplier=self.binnedData.size/expectedResultSize#divide by difference in data times by size
        for i in range(0,binned_data.numberOfBins):
            expectedResult.append((allDataBin.bins[i] - self.binnedData.bins[i]) * expectedResultMultiplier)
        return expectedResult
    
    def getExpectedResultExemplary(self):
        global exemplaryDataBin
        expectedResult=[]
        expectedResultMultiplier=self.binnedData.size/exemplaryDataBin.size
        for i in range(0,binned_data.numberOfBins):
            expectedResult.append(exemplaryDataBin.bins[i]*expectedResultMultiplier)
        return expectedResult
    
    

    def __str__(self):
        return (str(self.markerID)+': '+self.firstName+' '+self.lastName+', Tests marked: '+str(self.binnedData.size))
        
    


#----------------------------------------------------------------
# These functions use the file system will need to change to sql
#---------------------------------------------------------------
def getTestID(s:str):#Extracts the test id from the test data string
    testAttibutes=s.split(",")
    return int(testAttibutes[4])

def getMarkerID(s:str):#Extracts the markerid from the marker data string
    markerAttributes=s.split(",")
    return int(markerAttributes[0])

def getData(testID):#Creates a list of TestResult objects 
    testDataFile=open("TestData.txt","r")
    fileData=[]
    for line in testDataFile:
        if (getTestID(line)==testID):
            fileData.append(TestResult(line.split(",")))
    testDataFile.close()
    return fileData


def getAllScores(testList):
    intList=[]
    for test in testList:
        intList.append(test.score)
    return intList

def addExemplaryMarker(marker:Marker):
    global nonExemplaryMarkers,exemplaryMarkers,exemplaryDataBin
    marker.isExemplary=True
    nonExemplaryMarkers.remove(marker)
    exemplaryMarkers.append(marker)
    if exemplaryDataBin==None:
        exemplaryDataBin=copy.deepcopy(marker.binnedData)
    else:
        exemplaryDataBin.add(marker.binnedData)
    for m in nonExemplaryMarkers:
        m.recalculateExemplaryValues()
    marker.chiSquaredExemplary=-1
    marker.expectedResultExemplary = []
    

def removeExemplaryMarker(marker:Marker):
    global nonExemplaryMarkers,exemplaryMarkers,exemplaryDataBin
    marker.isExemplary=False
    nonExemplaryMarkers.append(marker)
    exemplaryMarkers.remove(marker)
    if exemplaryMarkers==[]:
        exemplaryDataBin=None
    else:
       exemplaryDataBin.subtract(marker.binnedData) 
    for m in nonExemplaryMarkers:
            m.recalculateExemplaryValues()
                            

def promoteRole(role:str):
    global nonExemplaryMarkers
    for marker in nonExemplaryMarkers:
        if marker.role==role:
            addExemplaryMarker(marker)

def demoteRole(role:str):
    global exemplaryMarkers
    for marker in exemplaryMarkers:
        if marker.role==role:
            removeExemplaryMarker(marker)


#----------------------------------------------
#Main functions for loading classes and data
#----------------------------------------------
def getMarkers():#Returns a list of Marker objects based on global test data
    global data
    foundMarkers = set()
    for test in data:
        if not(test.markerID in foundMarkers):
            foundMarkers.add(test.markerID)
    markerDataFile=open("MarkerData.txt")

    markersList=[]

    for line in markerDataFile:
        if getMarkerID(line) in foundMarkers:
            markersList.append(Marker(line.split(",")))

    markerDataFile.close()
    return markersList


def loadNewTest(testID):#Loads all data and initialises all objects needed for the statistics test
    global data,allDataBin,markers
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

    markers = getMarkers()

    return


def printMarkers():
    global markers
    for marker in markers:
        print(marker)
        print(marker.chiSquaredAll)
        print(marker.chiSquaredExemplary)

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
    promoteRole("Module Lead")
    promoteRole("Module Staff")
    print(markers[0].expectedResultExemplary)
    demoteRole("Module Staff")
    print(markers[0].expectedResultExemplary)
    printMarkers()
    promoteRole("Module Staff")
    printMarkers()
    print(markers[0].binnedData.bins)
    print(markers[0].expectedResultAll)
    print(markers[0].binnedData.chiSquaredTest(markers[0].expectedResultAll))


if __name__ == '__main__':
    main()