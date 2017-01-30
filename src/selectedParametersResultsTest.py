import json
from classes.SelectedParametersResults import SelectedParametersResults

with open("selectedParametersResults.json") as json_file:
    data = json.load(json_file)

    # Energy
    residues_energy = data["energy"]["residues"]
    selectedResiduesEnergy = SelectedParametersResults()
    selectedResiduesEnergy.setResidues(residues_energy)
    selectedResiduesEnergy.printAll()

    # Hydrogen
    residues_hydrogen = data["hydrogen"]["residues"]
    selectedResiduesHydrogen = SelectedParametersResults()
    selectedResiduesHydrogen.setResidues(residues_hydrogen)
    selectedResiduesHydrogen.printAll()
