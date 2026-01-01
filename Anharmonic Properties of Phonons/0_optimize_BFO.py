from ase.optimize import BFGS
from ase.io import read, write
from ase.io.lammpsdata import write_lammps_data
from ase.constraints import StrainFilter
from calorine.calculators import CPUNEP
import numpy as np
import os
import shutil

if __name__ == "__main__":

    if os.path.exists("fc_BFO"):
        shutil.rmtree("fc_BFO")
        os.mkdir("fc_BFO")
    else:
        os.mkdir("fc_BFO")

    raw_atoms = read("BFO.xyz")
    supercell = np.array([6, 6, 6])

    nep_calculator = CPUNEP('nep.txt')
    raw_atoms.calc = nep_calculator

    sf = StrainFilter(raw_atoms)
    dyn = BFGS(sf, trajectory='BFO.traj')
    dyn.run(fmax=0.0001)
    atoms = read('BFO.traj')

    write_lammps_data("BFO.lmp", atoms, specorder = ["Bi", "Fe", "O"])
    write("fc_BFO/replicated_atoms.xyz", atoms.repeat([6, 6, 6]))

    print('Supercell structures and LAMMPS input generated.')
    print('Supercell dimension is: ' + str(supercell))
