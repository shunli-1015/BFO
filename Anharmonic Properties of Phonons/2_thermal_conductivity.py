from kaldo.conductivity import Conductivity
from kaldo.forceconstants import ForceConstants
from kaldo.phonons import Phonons
import numpy as np
nrep = 6
supercell = np.array([nrep, nrep, nrep])
forceconstants = ForceConstants.from_folder(folder='fc_BFO', supercell=supercell, format='lammps')
k_points = 16
kpts = [k_points, k_points, k_points]
temperature = 300

phonons = Phonons(forceconstants=forceconstants,
                  kpts=kpts,
                  is_classic=False,
                  temperature=temperature,
                  is_nw=False,
                  folder='ALD_BFO',
                  storage='numpy')

inverse_conductivity = Conductivity(phonons=phonons, method='inverse').conductivity
inverse_conductivity_matrix = inverse_conductivity.sum(axis=0)
print('Infinite size conductivity from inversion (W/m-K): %.3f' % np.mean([inverse_conductivity_matrix[0,0], 
    inverse_conductivity_matrix[1, 1], 
    inverse_conductivity_matrix[2, 2]]))

