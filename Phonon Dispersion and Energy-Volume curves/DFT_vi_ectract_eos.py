import os
import re

NUM_ATOMS = 5

output_file = "dft_eos_data.txt"
results = []

print(f": {NUM_ATOMS}")

for folder in sorted(os.listdir(".")):
    if folder.startswith("vol_") and os.path.isdir(folder):
        outcar_path = os.path.join(folder, "OUTCAR")

        if os.path.exists(outcar_path):
            try:
                scale_str = folder.replace("vol_", "")

                final_energy = None
                final_volume = None

                
                with open(outcar_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        
                        if "volume of cell :" in line:
                            parts = line.split()
                            
                            if len(parts) >= 5:
                                final_volume = float(parts[4])

                        
                        if "free  energy   TOTEN" in line:
                            parts = line.split()
                            
                            if len(parts) >= 5:
                                final_energy = float(parts[4])

                
                if final_energy is not None and final_volume is not None:
                    v_per_atom = final_volume / NUM_ATOMS
                    e_per_atom = final_energy / NUM_ATOMS
                    results.append((scale_str, v_per_atom, e_per_atom))
                    print(f"succeed: {folder}")
                else:
                    print(f"warning: {folder} ")

            except Exception as e:
                print(f"Processing {folder} is wrong: {e}")


results.sort(key=lambda x: float(x[0]))

with open(output_file, "w") as f:
    f.write("Scale   Vol/Atom(A^3)   Energy/Atom(eV)\n")
    print("\nLast Result:")
    print(f"{'Scale':<8} {'Vol/Atom':<15} {'E/Atom':<15}")
    print("-" * 40)

    for r in results:
        line = f"{r[0]:<8} {r[1]:<15.4f} {r[2]:<15.6f}"
        print(line)
        f.write(f"{r[0]}   {r[1]:.6f}   {r[2]:.8f}\n")

print(f"\n: {output_file}")