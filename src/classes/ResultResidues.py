class ResultResidues():
    def __init__(self):
        self.res = []

    def setResidues(self, listRes):
        self.res = listRes

    def setAddResidue(self, res):
        self.res.append(res)

    def getResidues(self):
        return self.getResidues()

    def printAll(self):
        men = ""
        for item in self.res:
            if men.strip():
                men = men + " , "
            men = men + str(item)
        print men
