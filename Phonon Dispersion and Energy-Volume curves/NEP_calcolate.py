import numpy as np
from ase.io import read
from pynep.calculate import NEP

output_file = "nep_eos_data.txt"  
scales = [0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 
          1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07, 1.08, 1.09, 1.10]
# ===========================================

calc = NEP("nep.txt")

atoms_primitive = read("POSCAR") 


supercell_size = (6, 6, 6) 
atoms_super = atoms_primitive.repeat(supercell_size)

original_super_cell = atoms_super.get_cell()
total_atoms_super = len(atoms_super) # 应该是 135 个


print("-" * 65)
print(f"{'Scale':<10} {'Vol/Atom (A^3)':<20} {'E/Atom (eV)':<20}")
print("-" * 65)

results = []

for s in scales:
    linear_scale = s**(1/3.0)
    
    atoms_calc = atoms_super.copy()
    atoms_calc.set_cell(original_super_cell * linear_scale, scale_atoms=True)
    
    atoms_calc.set_calculator(calc)
    
    total_energy = atoms_calc.get_potential_energy()
    total_volume = atoms_calc.get_volume()
    
    e_per_atom = total_energy / total_atoms_super
    v_per_atom = total_volume / total_atoms_super
    
    results.append((s, v_per_atom, e_per_atom))
    
    print(f"{s:<10.2f} {v_per_atom:<20.4f} {e_per_atom:<20.6f}")

with open(output_file, "w") as f:
    f.write("Scale   Vol/Atom(A^3)   Energy/Atom(eV)\n")
    
    for res in results:
        f.write(f"{res[0]:.2f}   {res[1]:.6f}   {res[2]:.8f}\n")

print("-" * 65)