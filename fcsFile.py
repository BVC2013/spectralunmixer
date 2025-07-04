from fcsToCSV import fcsToCSV
from CSVToDf import CSVToDf
from createSpilloverMatrix import createSpilloverMatrix
from createCompMatrix import createCompMatrix
from applyCompMatrix import applyCompMatrix
class fcsFile:
    #raw data, make this a df
    rawMatrix = []
    #spillover matrix, make this a df
    spilloverMatrix = []
    #true values, make this a df
    actualValues = []
    compMatrix = []
    def fcsFile(self,filepath):
        self.rawMatrix = CSVToDf(fcsToCSV(filepath))
        self.spilloverMatrix = createSpilloverMatrix(self.rawMatrix)
        self.compMatrix = createCompMatrix(self.spilloverMatrix)
        self.actualValues = applyCompMatrix(self.compMatrix)


        