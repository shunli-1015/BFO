import os
import shutil
from ase.io import read, write

atoms = read("POSCAR")
original_cell = atoms.get_cell()

scales = [0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.00, 1.01,  1.02, 1.03, 1.04, 1.05, 1.06, 1.07, 1.08, 1.09, 1.10]

for s in scales:
    linear_scale = s**(1/3.0)
    
    folder_name = f"vol_{s:.2f}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    atoms_copy = atoms.copy()
    atoms_copy.set_cell(original_cell * linear_scale, scale_atoms=True)
    
    write(os.path.join(folder_name, "POSCAR"), atoms_copy, format="vasp")
    
    for file in ["INCAR", "POTCAR", "KPOINTS"]:
        if os.path.exists(file):
            shutil.copy(file, os.path.join(folder_name, file))
        else:
            print(f"warning: {file} not in this folder！")

    print(f"Created inputs for scale {s:.2f} in folder {folder_name}")