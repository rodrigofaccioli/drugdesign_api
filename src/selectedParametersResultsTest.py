import json
from classes.SelectedParametersResults import SelectedParametersResults

with open("selectedParametersResults.json") as json_file:
    data = json.load(json_file)

    # Energy
    residues_energy = data["energy"]["residues"]
    selectedResiduesEnergy = SelectedParametersResults("Demo")
    selectedResiduesEnergy.setResidues(residues_energy)
    selectedResiduesEnergy.printAll()

    # Hydrogen
    residues_hydrogen = data["hydrogen"]["residues"]
    selectedResiduesHydrogen = SelectedParametersResults("Demo")
    selectedResiduesHydrogen.setResidues(residues_hydrogen)
    selectedResiduesHydrogen.printAll()
