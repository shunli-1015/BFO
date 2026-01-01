import numpy as np
from ase.io import read
from ase import Atoms
from pynep.calculate import NEP
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
import sys
import matplotlib.pyplot as plt

nep_model_file = "nep.txt"
poscar_file = "POSCAR"   # 

supercell_matrix = [[8, 0, 0], 
                    [0, 8, 0], 
                    [0, 0, 8]]

displacement_distance = 0.001

path_string = "0.0 0.0 0.0   0.5 0.0 0.0   0.333333 0.333333 0.0   0.0 0.0 0.0   0.0 0.0 0.5"
labels_string = "$\Gamma$ M K $\Gamma$ A"
# ===========================================

def main():
    print(f"Loading NEP model: {nep_model_file}...")
    try:
        calc = NEP(nep_model_file)
        unitcell = read(poscar_file)
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    print(f"Initializing Phonopy (Supercell: {supercell_matrix})...")
    phonon = Phonopy(PhonopyAtoms(symbols=unitcell.get_chemical_symbols(),
                                  cell=unitcell.get_cell(),
                                  scaled_positions=unitcell.get_scaled_positions()),
                     supercell_matrix=supercell_matrix)

    print("Generating displacements and calculating forces...")
    phonon.generate_displacements(distance=displacement_distance)
    supercells = phonon.supercells_with_displacements
    
    forces_set = []
    for i, sc in enumerate(supercells):
        sc_ase = Atoms(numbers=sc.numbers, cell=sc.cell, 
                       scaled_positions=sc.scaled_positions, pbc=True)
        sc_ase.calc = calc
        forces_set.append(sc_ase.get_forces())
        
        print(f"  - Calculated supercell {i+1}/{len(supercells)}")

    phonon.forces = forces_set
    phonon.produce_force_constants()

    print("Calculating band structure...")
    try:
        raw_points = [float(x) for x in path_string.split()]
        points = []
        for i in range(0, len(raw_points), 3):
            points.append([raw_points[i], raw_points[i+1], raw_points[i+2]])
        
        bands = []
        for i in range(len(points) - 1):
            bands.append([points[i], points[i+1]])
            
        labels = labels_string.split()
        
        print(f"  - Detected {len(points)} high-symmetry points.")
        print(f"  - Generated {len(bands)} path segments.")

    except Exception as e:
        print(f"Path parsing error: {e}")
        return

    phonon.run_band_structure(bands, 
                              path_connections=None, 
                              labels=labels,
                              n_points=1001) # 高密度采样

    output_file = "band_nep.yaml"
    phonon.write_yaml_band_structure(filename=output_file)
    
    print("Plotting preview...")
    plot = phonon.plot_band_structure()
    plot.title("Phonon Dispersion (NEP)")
    plot.ylabel("Frequency (THz)")
    plot.savefig("phonon_nep_preview.png", dpi=1200)
    
    print("="*50)
    print(f"Done! Saved to {output_file} and phonon_nep_preview.png")
    print("="*50)

if __name__ == "__main__":
    main()