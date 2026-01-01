from kaldo.conductivity import Conductivity
from kaldo.forceconstants import ForceConstants
from kaldo.phonons import Phonons
import kaldo.controllers.plotter as plotter
import numpy as np

nrep = 6
supercell = np.array([nrep, nrep, nrep])

forceconstants = ForceConstants.from_folder(folder='fc_BFO', supercell=supercell, format='lammps', only_second =True)
k_points = 16
kpts = [k_points, k_points, k_points]
temperature = 300

phonons = Phonons(forceconstants=forceconstants,
                  kpts=kpts,
                  is_classic=False,
                  temperature=temperature,
                  is_nw=True,
                  folder='ALD_BFO',
                  storage='numpy')
plotter.plot_dispersion(phonons,n_k_points=1000, is_showing=False)
print("Phonons spectra calcualtions finish!")
