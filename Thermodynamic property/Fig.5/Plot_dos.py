from gpyumd.load import load_vac, load_dos
from pylab import * 
import numpy as np
vac = load_vac(200)["run0"]
dos = load_dos(400)["run0"]

figure(figsize=(10, 4))
subplot(1, 2, 1)
plot(vac["t"], vac["VACx"]/vac["VACx"].max(), label="x")
plot(vac["t"], vac["VACy"]/vac["VACy"].max(), label="y")
plot(vac["t"], vac["VACz"]/vac["VACz"].max(), label="z")
ylabel('VAC (Normalized)')
xlabel('Correlation Time (ps)')
legend()

subplot(1, 2, 2)
plot(dos["nu"], dos["DOSx"], label="x")
plot(dos["nu"], dos["DOSy"], label="y")
plot(dos["nu"], dos["DOSz"], label="z")
ylabel('PDOS (1/THz)')
xlabel(r'$\omega$/2$\pi$ (THz)')
legend()
savefig("DOS.pdf", bbox_inches='tight')
# 导出PDOS数据到文本文件
np.savetxt("PDOS_x.txt", np.column_stack((dos["nu"], dos["DOSx"])), header="Frequency (THz) PDOS_x (1/THz)", comments='')
np.savetxt("PDOS_y.txt", np.column_stack((dos["nu"], dos["DOSy"])), header="Frequency (THz) PDOS_y (1/THz)", comments='')
np.savetxt("PDOS_z.txt", np.column_stack((dos["nu"], dos["DOSz"])), header="Frequency (THz) PDOS_z (1/THz)", comments='')
