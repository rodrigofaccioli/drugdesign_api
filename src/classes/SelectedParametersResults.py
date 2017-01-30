from VS import VS

class SelectedParametersResults(VS):
    def __init__(self, id):
        self.VS = VS(id)
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

    def getResidues(self):
        return self.getResidues()

    def getRange():
        return self.range

    def getOption(self):
        return self.option

    def printAll(self):
        Allres = ""
        for item in self.res:
            if Allres.strip():
                Allres = Allres + " , "
            Allres = Allres + str(item)
        men = "ID: " + str(self.VS.id) + " Residues: " + Allres + " Range: " + str(self.range) + " Option: " + str(self.option)
        print men
