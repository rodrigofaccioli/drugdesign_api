import json
from classes.ResultResidues import ResultResidues

with open("selectedResidues.json") as json_file:
    data = json.load(json_file)

    # Energy
    residues_energy = data["energy"]["residues"]
    selectedResiduesEnergy = ResultResidues()
    selectedResiduesEnergy.setResidues(residues_energy)
    selectedResiduesEnergy.printAll()

    # Hydrogen
    residues_hydrogen = data["hydrogen"]["residues"]
    selectedResiduesHydrogen = ResultResidues()
    selectedResiduesHydrogen.setResidues(residues_hydrogen)
    selectedResiduesHydrogen.printAll()
