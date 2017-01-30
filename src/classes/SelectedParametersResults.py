from VS import VS

class SelectedParametersResults(VS):
    def __init__(self):
        self.res = []
        self.range = []
        self.option = ""

    def setResidues(self, listRes):
        self.res = listRes

    def setAddResidue(self, res):
        self.res.append(res)

    def setRange(self, min, max):
        self.range.append(min)
        self.range.append(max)

    def setOption(self, op):
        self.option = op

    def setIdVS(self, id):
        self.idVS = id

    def getResidues(self):
        return self.getResidues()

    def getRange():
        return self.range

    def getOption(self):
        return self.option

    def printAll(self):
        men = ""
        for item in self.res:
            if men.strip():
                men = men + " , "
            men = men + str(item)
        print men
