from CSVToDf import CSVToDf
from createSpilloverMatrix import createSpilloverMatrix
from createCompMatrix import createCompMatrix
from applyCompMatrix import applyCompMatrix

class concatFile:
    #list of flurochrome objects
    fluorochromes = []
    primary = []
    spilloverMatrix = []
    compensationMatrix=[]
    rawMatrix = []
    compVals = []
    def concatFile(flurochromeObjs):
        for i in flurochromeObjs:
            fluorochromes.add(i)
            if i.isPrimary == True:
                primary.add(i)
            rawMatrix.add(i.uncompData)
    createSpilloverMatrix(self.rawMatrix)
    createCompMatrix(self.spilloverMatrix)
    applyCompMatrix(self.compMatrix)
    dfToCSV(compVals)
    CSVtofcs(self.compVals)
    print("project processed")
    