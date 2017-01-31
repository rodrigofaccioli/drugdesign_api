from VS import VS

class ResultMolecule(VS):
    def __init__(self, id):
        self.VS = VS(id)
        self.molecule = ""
        self.value = 0
        self.image1 = ""
        self.image2 = ""

    def setMolecule(self, mol):
        self.molecule = mol

    def setValue(self, value):
        self.value = value

    def setImage1(self, image):
        self.image1 = image

    def setImage2(self, image):
        self.image2 = image

    def getMolecule(self):
        return self.molecule

    def getValue(self):
        return self.value

    def getImage1(self):
        return self.image1

    def getImage2(self):
        return self.image2

    def dic2obj(self, dic):
        self.setMolecule( dic["molecule"] )
        self.setValue( dic["value"] )
        self.setImage1( dic["image1"] )
        self.setImage2( dic["image2"] )

    def printAll(self):
        men = "ID: " + str(self.VS.id) + " Molecule: " + str( self.getMolecule() )+ " Value: "+ str( self.getValue() ) + " image1: "+ str( self.getImage1() ) + " image2: "+ str( self.getImage2() )
        print men
