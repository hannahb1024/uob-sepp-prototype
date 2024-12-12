import copy
import src.DBConnect as dbc

def countInRange(list, min, max):  # Counts the number of numbers withing the given range
    count = 0
    for item in list:
        if (min <= item) and (item < max):
            count += 1
    return count


class binned_data():
    maxValue = 0
    minValue = 0
    numRange = 0
    numberOfBins = 10
    binRangeSize = 0
    binRanges = [(0, 0)] * numberOfBins

    def __init__(self, scores_list):

        self.bins = [None] * binned_data.numberOfBins
        self.size = len(scores_list)

        if self.size <= 0:
            print("List is empty cannot bin values")
        else:
            binLower = binned_data.minValue
            binUpper = binned_data.minValue + binned_data.binRangeSize
            for i in range(0, binned_data.numberOfBins - 1):
                self.bins[i] = countInRange(scores_list, binLower, binUpper)
                binLower = binUpper
                binUpper += binned_data.binRangeSize
            self.bins[binned_data.numberOfBins - 1] = countInRange(scores_list, binLower, binUpper + 1)

    def chiSquaredTest(self, expected):  # expected is a list of nums of the same size
        if expected == []:  # If the expected list is empty return an error value (-1)
            return -1
        chi_squared = 0
        for i in range(0, self.numberOfBins - 1):
            difference = self.bins[i] - expected[i]
            chi_squared += (difference * difference)/0.1 if expected[i] <= 0.1 else (difference * difference) / expected[
                i]  # Duck tape fix for dividing by 0
        return chi_squared

    def add(self, binnedData):
        for i in range(0, binned_data.numberOfBins):
            self.bins[i] += binnedData.bins[i]
        self.size += binnedData.size

    def subtract(self, binnedData):
        for i in range(0, binned_data.numberOfBins):
            self.bins[i] -= binnedData.bins[i]
        self.size -= binnedData.size


class TestResult():  # Essentially a nice tuple of teh form (int,int,int,int,int)
    def __init__(self, attributes):
        # Attributes is a string of the form int,int,int,int,int
        self.ID = int(attributes[0])
        self.studentID = int(attributes[1])
        self.score = int(attributes[2])
        self.markerID = int(attributes[3])
        self.testID = int(attributes[4])


def toScoreList(
        testResultList):  # Takes a list of objects of type TestResult and returns a list of scores from the tests
    scoreList = []
    for testResult in testResultList:
        scoreList.append(testResult.score)
    return scoreList


class Marker():
    def __init__(self, attributes):
        global data, nonExemplaryMarkers
        # attributes is a string of the form int,int,string,string,string
        self.markerID = int(attributes[0])
        self.moduleID = int(attributes[1])
        self.firstName = attributes[2]
        self.lastName = attributes[3]
        if attributes[4].endswith("\n"):  # the last value can come out weird because its read from a file this sorts it
            self.role = attributes[4][:-1]
        else:
            self.role = attributes[4]

        self.isExemplary = False  # default is no
        nonExemplaryMarkers.append(self)  # global list for all non exemplary markers for general use and processing

        self.markedTests = []  # List of all tests this marker has marked
        for testResult in data:
            if testResult.markerID == self.markerID:
                self.markedTests.append(testResult)

        self.binnedData = binned_data(
            toScoreList(self.markedTests))  # Process list of tests into binned data for chi-squared tests
        self.expectedResultAll = self.getExpectedResultAll()  # Function that creates the expected result from all the other test results
        self.chiSquaredAll = self.binnedData.chiSquaredTest(self.expectedResultAll)
        self.expectedResultExemplary = []
        self.chiSquaredExemplary = -1

    def recalculateExemplaryValues(self):
        self.expectedResultExemplary = self.getExpectedResultExemplary()
        self.chiSquaredExemplary = self.binnedData.chiSquaredTest(self.expectedResultExemplary)

    def getExpectedResultAll(self):  # returns a float/double list of size numberOfBins of the expected result
        global allDataBin
        expectedResult = []
        expectedResultSize = allDataBin.size - self.binnedData.size
        expectedResultMultiplier = self.binnedData.size / expectedResultSize  # divide by difference in data times by size
        for i in range(0, binned_data.numberOfBins):
            expectedResult.append((allDataBin.bins[i] - self.binnedData.bins[i]) * expectedResultMultiplier)
        return expectedResult

    def getExpectedResultExemplary(self):
        global exemplaryDataBin
        expectedResult = []
        expectedResultMultiplier = self.binnedData.size / exemplaryDataBin.size
        for i in range(0, binned_data.numberOfBins):
            expectedResult.append(exemplaryDataBin.bins[i] * expectedResultMultiplier)
        return expectedResult

    def getConcernLevel(self):
        global criticalValues
        if self.isExemplary:
            return 0  # Exemplary markers ar etrusted so have no concern.
        concern = 1
        for tup in criticalValues:
            if self.chiSquaredExemplary < tup[0] and self.chiSquaredAll < tup[0]:
                return concern
            concern += 1
        return concern  # Currently max concern is 6 and that happens when theres a 0.1% chance the markers data is valid

    def adjustScoresToExemplary(self):
        return self.adjustScoresToData(self.expectedResultExemplary)

    def adjustScoresToAll(self):
        return self.adjustScoresToData(self.expectedResultAll)

    def adjustScoresToData(self, dataToAdjustTo):
        if dataToAdjustTo == []:
            return 0

        OPTIMAL_CHI_SQUARED = 13.442
        originalScores = getAllScores(self.markedTests)
        bestScores = originalScores
        bestChiSquared = binned_data(bestScores).chiSquaredTest(dataToAdjustTo)
        addingConstant = binned_data.binRangeSize/5

        while True:
            increasedScores = list(map(lambda x: min((x + addingConstant),binned_data.maxValue), bestScores))
            reducedScores = list(map(lambda x: max((x - addingConstant),binned_data.minValue), bestScores))
            chiSquaredIncreasedScores = binned_data(increasedScores).chiSquaredTest(dataToAdjustTo)
            chiSquaredReducedScores = binned_data(reducedScores).chiSquaredTest(dataToAdjustTo)

            if abs(chiSquaredReducedScores - OPTIMAL_CHI_SQUARED) < (chiSquaredIncreasedScores - OPTIMAL_CHI_SQUARED):
                candidateBestScores = reducedScores
                candidateBestChiSquared = chiSquaredReducedScores
            else:
                candidateBestScores = increasedScores
                candidateBestChiSquared = chiSquaredIncreasedScores

            if abs(candidateBestChiSquared - 13.442) <= abs(bestChiSquared - 13.442):
                bestScores = candidateBestScores
                bestChiSquared = binned_data(bestScores).chiSquaredTest(dataToAdjustTo)
            else:
                return (bestScores[0] - originalScores[0])

    def __str__(self):
        return (str(self.markerID) + ': ' + self.firstName + ' ' + self.lastName + ', Tests marked: ' + str(
            self.binnedData.size))


# ----------------------------------------------------------------
# These functions use the file system will need to change to sql
# ---------------------------------------------------------------
def getTestID(s: str):  # Extracts the test id from the test data string
    ids = dbc.testIDCollect()
    cleaned = []
    for item in ids:
        cleaned.append(str(item[0]))
    return cleaned


def getMarkerID(s: str):  # Extracts the markerid from the marker data string
    #markerAttributes = s.split(",")
    return int(s[0])


def getData(testID):  # Creates a list of TestResult objects. NEEDS TO BE UPDATED FOR DATABASE
    #testDataFile = open("data/TestData.txt", "r")  # Loads the file
    fileData = []
    # for line in testDataFile:  # Create a new TestResult object and add it to the return list if its ID matches
    #     if (getTestID(line) == testID):
    #         fileData.append(TestResult(line.split(",")))  # -----------   IMPORTANT!!! ------------
    # testDataFile.close()  # The testResult contructor takes a list of strings and extracts the data from that if you change the
    # return fileData  # datatype being read then you will need to update the constructor. Relevant lines 58-62
    testTable = dbc.testCollect(testID)
    for item in testTable:
        fileData.append(TestResult(item)) #Tuple? List?
    print(fileData)
    return fileData


def getAllScores(testList):  # Function for extracting the list of scores from a list of TestResult objects
    intList = []
    for test in testList:
        intList.append(test.score)
    return intList


def addExemplaryMarker(
        marker: Marker):  # To be ran every time a marker is marked as exemplary, passing that marker into the function
    global nonExemplaryMarkers, exemplaryMarkers, exemplaryDataBin
    marker.isExemplary = True
    nonExemplaryMarkers.remove(marker)
    exemplaryMarkers.append(marker)
    if exemplaryDataBin == None:
        exemplaryDataBin = copy.deepcopy(marker.binnedData)
    else:
        exemplaryDataBin.add(marker.binnedData)
    for m in nonExemplaryMarkers:
        m.recalculateExemplaryValues()
    marker.chiSquaredExemplary = -1
    marker.expectedResultExemplary = []


def removeExemplaryMarker(
        marker: Marker):  # To be ran every time a marker is unmarked as exemplary, passing that marker into the function
    global nonExemplaryMarkers, exemplaryMarkers, exemplaryDataBin
    marker.isExemplary = False
    nonExemplaryMarkers.append(marker)
    exemplaryMarkers.remove(marker)
    if exemplaryMarkers == []:
        exemplaryDataBin = None
        for m in nonExemplaryMarkers:
            m.expectedResultExemplary = []
            m.chiSquaredExemplary = -1
    else:
        exemplaryDataBin.subtract(marker.binnedData)
        for m in nonExemplaryMarkers:
            m.recalculateExemplaryValues()


def promoteRole(markerRole: str):  # Function for testing - marks every marker with the given role as exemplary
    global nonExemplaryMarkers
    tempList = []
    for potentialMarker in nonExemplaryMarkers:
        if potentialMarker.role == markerRole:
            tempList.append(potentialMarker)
    for item in tempList:
        addExemplaryMarker(item)


def demoteRole(markerRole: str):  # Function for testing - unmarks every marker with the given role from being exemplary
    global exemplaryMarkers
    tempList = []
    for potentialMarker in exemplaryMarkers:
        if potentialMarker.role == markerRole:
            tempList.append(potentialMarker)
    for item in tempList:
        removeExemplaryMarker(item)


def demoteAll():  # Function for testing - unmarks every marker from being exemplary
    global exemplaryMarkers
    tempList = exemplaryMarkers.copy
    for potentialMarker in tempList:
        print(potentialMarker)
        removeExemplaryMarker(potentialMarker)


# ----------------------------------------------
# Main functions for loading classes and data
# ----------------------------------------------
def getMarkers():  # Returns a list of Marker objects. NEEDS TO BE UPDATED FOR DATABASE
    global data
    foundMarkers = set()  # Collect every unique marker ID
    for test in data:
        if not (test.markerID in foundMarkers):
            foundMarkers.add(test.markerID)

    # markerDataFile = open("data/MarkerData.txt")
    markersList = []
    # for line in markerDataFile:  # Create a new marker object if the line matches a unique marker ID
    #     if getMarkerID(line) in foundMarkers:
    #         markersList.append(Marker(line.split(",")))  # -----------   IMPORTANT!!! ------------
    # #                             The Marker constructor takes a list of strings and extracts data from that. If you change the datatype
    # markerDataFile.close()  # being read you will need to change the constructor. Relevant lines 76-83
    # return markersList
    markerTable = dbc.markerData()
    for item in markerTable:
        if getMarkerID(item) in foundMarkers:
            markersList.append(Marker(item))
    return markersList


def loadNewTest(testID):  # Loads all data and initialises all objects needed for the statistics test
    global data, allDataBin, markers
    data = getData(testID)
    if data == []:
        print("No data test found with that ID.")
        return
    allScores = getAllScores(data)
    binned_data.maxValue = max(allScores)
    binned_data.minValue = min(allScores)
    binned_data.numRange = binned_data.maxValue - binned_data.minValue
    binned_data.binRangeSize = binned_data.numRange / binned_data.numberOfBins
    tempLower = binned_data.minValue
    tempUpper = tempLower + binned_data.binRangeSize
    for i in range(0, binned_data.numberOfBins):
        binned_data.binRanges[i] = (tempLower, tempUpper)
        tempLower += binned_data.binRangeSize
        tempUpper += binned_data.binRangeSize
    allDataBin = binned_data(allScores)

    markers = getMarkers()

    return


def getConcern(marker: Marker):
    match marker.getConcernLevel():
        case 0:
            print("🔵")
        case 1:
            print("🟢")
        case 2:
            print("🟡")
        case 3:
            print("🟠")
        case 4:
            print("🟧")
        case 5:
            print("🔴")
        case 6:
            print("🟥")


def printMarkers():
    global markers
    for mk in markers:
        print(mk)
        print(mk.chiSquaredAll)
        print(mk.chiSquaredExemplary)
        getConcern(mk)


data = []
allDataBin = None
markers = []
nonExemplaryMarkers = []
exemplaryMarkers = []
exemplaryDataBin = None
criticalValues = [(13.442, 0.2), (15.987, 0.1), (18.307, 0.05), (23.209, 0.01),
                  (29.588, 0.001)]  # The right value is the probibility the chi squared exceeds the right value


def main():
    loadNewTest(1)
    print("========================================================")
    printMarkers()
    print("========================================================")
    promoteRole("Module Lead")
    printMarkers()
    print("========================================================")
    promoteRole("Module Staff")
    printMarkers()
    print("========================================================")
    demoteRole("Module Lead")
    printMarkers()
    print("========================================================")

    print(allDataBin.bins)
    print(binned_data.binRanges)

    print(exemplaryMarkers)
    print(markers[0].binnedData.bins)
    print(markers[0].adjustScoresToAll())
    print(markers[0].binnedData.chiSquaredTest(markers[0].expectedResultAll))
    print(markers[0].adjustScoresToExemplary())
    print(markers[0].expectedResultAll)


if __name__ == '__main__':
    main()
