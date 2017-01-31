from VS import VS

class SelectedParametersResults(VS):
    def __init__(self, id):
        self.VS = VS(id)
        self.res = []
        self.range = []
        self.option = ""

    def setResidues(self, listRes):
        for res in listRes:
            self.setAddResidue(str(res))

    def setAddResidue(self, res):
        self.res.append(res)

    def setRange(self, min, max):
        self.range.append(float(min))
        self.range.append(float(max))

    def setOption(self, op):
        self.option = str(op)

    def getResidues(self):
        return self.getResidues()

    def getRange():
        return self.range

    def getOption(self):
        return self.option

    def buildMessage(self):
        return "ID: " + str(self.VS.id) + " Residues: " + str(self.res) + " Range: " + str(self.range) + " Option: " + str(self.option)

    def printAll(self):
        print self.buildMessage()
