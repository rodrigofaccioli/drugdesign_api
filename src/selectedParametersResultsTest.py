import json
from classes.SelectedParametersResults import SelectedParametersResults

with open("selectedParametersResults.json") as json_file:
    data = json.load(json_file)

    # Energy
    vs_id_energy = data["energy"]["vsId"]
    residues_energy = data["energy"]["residues"]
    range_energy_min = data["energy"]["rangeMin"]
    range_energy_max = data["energy"]["rangeMax"]

    selectedResiduesEnergy = SelectedParametersResults(vs_id_energy)
    selectedResiduesEnergy.setResidues(residues_energy)
    selectedResiduesEnergy.setRange(range_energy_min, range_energy_max)
    selectedResiduesEnergy.setOption("energy")
    selectedResiduesEnergy.printAll()

    # Hydrogen
    vs_id_hydrogen = data["hydrogen"]["vsId"]
    residues_hydrogen = data["hydrogen"]["residues"]
    range_hydrogen_min = data["hydrogen"]["rangeMin"]
    range_hydrogen_max = data["hydrogen"]["rangeMax"]

    selectedResiduesHydrogen = SelectedParametersResults(vs_id_hydrogen)
    selectedResiduesHydrogen.setResidues(residues_hydrogen)
    selectedResiduesHydrogen.setRange(range_hydrogen_min, range_hydrogen_max)
    selectedResiduesHydrogen.setOption("hydrogen")
    selectedResiduesHydrogen.printAll()
