import unittest
import src.statistics_test as st
class TestUI(unittest.TestCase):
    def test_binnedDataTesting(self):
        allScores = range(1,101)
        st.binned_data.maxValue = max(allScores)
        st.binned_data.minValue = min(allScores)
        st.binned_data.numRange = st.binned_data.maxValue - st.binned_data.minValue
        st.binned_data.binRangeSize = st.binned_data.numRange / st.binned_data.numberOfBins
        tempLower = st.binned_data.minValue
        tempUpper = tempLower + st.binned_data.binRangeSize
        for i in range(0, st.binned_data.numberOfBins):
            st.binned_data.binRanges[i] = (tempLower, tempUpper)
            tempLower += st.binned_data.binRangeSize
            tempUpper += st.binned_data.binRangeSize
        bin1 = st.binned_data(allScores)
        self.assertNotEqual(bin1,None, "Binned data should not return None")
        self.assertEqual(bin1.size,100, "Binned data size should be 100")
        self.assertEqual(bin1.bins, [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0], "Binned data should be a list of 10s")
        self.assertEqual(bin1.chiSquaredTest([10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]), 0.0, "Chi squared result of equal data should be 0")
        self.assertEqual(bin1.chiSquaredTest([9.0, 9.0, 9.0, 9.0, 9.0, 11.0, 11.0, 11.0, 11.0, 11.0]), 0.9191919191919193, "Chi squared result of data should be ~0.9")