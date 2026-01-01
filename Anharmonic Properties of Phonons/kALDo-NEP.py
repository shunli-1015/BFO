from ase.io import read
from ase.visualize.plot import plot_atoms
from pylab import *
import warnings
warnings.filterwarnings("ignore")

def cumulative_cond_cal(observables, kappa_tensor, prefactor=1/3):


    kappa = np.einsum('maa->m', prefactor * kappa_tensor)

    observables_argsort_indices = np.argsort(observables)
    cumulative_kappa = np.cumsum(kappa[observables_argsort_indices])
    
    return observables[observables_argsort_indices], cumulative_kappa


def set_fig_properties(ax_list, panel_color_str='black', line_width=2):
    tl = 4
    tw = 2
    tlm = 2

    for ax in ax_list:
        ax.tick_params(which='major', length=tl, width=tw)
        ax.tick_params(which='minor', length=tlm, width=tw)
        ax.tick_params(which='both', axis='both', direction='in',
                       right=True, top=True)
        ax.spines['bottom'].set_color(panel_color_str)
        ax.spines['top'].set_color(panel_color_str)
        ax.spines['left'].set_color(panel_color_str)
        ax.spines['right'].set_color(panel_color_str)

        ax.spines['bottom'].set_linewidth(line_width)
        ax.spines['top'].set_linewidth(line_width)
        ax.spines['left'].set_linewidth(line_width)
        ax.spines['right'].set_linewidth(line_width)

        for t in ax.xaxis.get_ticklines(): t.set_color(panel_color_str)
        for t in ax.yaxis.get_ticklines(): t.set_color(panel_color_str)
        for t in ax.xaxis.get_ticklines(): t.set_linewidth(line_width)
        for t in ax.yaxis.get_ticklines(): t.set_linewidth(line_width)


data_folder = "./"

dispersion = np.loadtxt(data_folder  + 'plots/16_16_16/dispersion')
q = np.loadtxt(data_folder  + 'plots/16_16_16/q')
Q = np.loadtxt(data_folder  + 'plots/16_16_16/Q_val')
point_names = np.loadtxt(data_folder  + 'plots/16_16_16/point_names', dtype=str)

point_names_list = []
for point_name in point_names:
    if point_name == 'G':
        point_name = r'$\Gamma$'
    elif point_name == 'U':
        point_name = 'U=K'
    point_names_list.append(point_name)


frequency =  np.load(
    data_folder + 'ALD_BFO/16_16_16/frequency.npy',
    allow_pickle=True)
group_velocity = np.load(
    data_folder + 'ALD_BFO/16_16_16/velocity.npy')

cv =  np.load(
    data_folder + 'ALD_BFO/16_16_16/300/quantum/heat_capacity.npy',
    allow_pickle=True)

phase_space = np.load(data_folder +
 'ALD_BFO/16_16_16/300/quantum/_ps_and_gamma.npy',
                      allow_pickle=True)[:,0]

group_velcotiy_norm = np.linalg.norm(
    group_velocity.reshape(-1, 3), axis=1) / 10.0


figure(figsize=(12, 3))
subplot(1,3, 1)
set_fig_properties([gca()])
scatter(frequency.flatten(order='C')[3:], 1e23*cv.flatten(order='C')[3:], 
        facecolor='w', edgecolor='b', s=10, marker='8')
ylabel (r"$C_{v}$ ($10^{23}$ J/K)")
xlabel('Frequency (THz)', fontsize=14)
ylim(0.9*1e23*cv.flatten(order='C')[3:].min(), 1.05*1e23*cv.flatten(order='C')[3:].max())

subplot(1 ,3, 2)
set_fig_properties([gca()])
scatter(frequency.flatten(order='C'),
        group_velcotiy_norm, facecolor='w', edgecolor='b', s=10, marker='^')
xlabel('Frequency (THz)', fontsize=14)
ylabel(r'$|v| \ (\frac{km}{s})$', fontsize=14)

subplot(1 ,3, 3)
set_fig_properties([gca()])
scatter(frequency.flatten(order='C'),
        phase_space, facecolor='w', edgecolor='b', s=10, marker='o')
xlabel('Frequency (THz)', fontsize=14)
ylabel('Phase space', fontsize=14)
subplots_adjust(wspace=0.33)
show()
import numpy as np
import pandas as pd

data_folder = "./"


frequency = np.load(data_folder + 'ALD_BFO/16_16_16/frequency.npy', allow_pickle=True)
phase_space = np.load(data_folder + 'ALD_BFO/16_16_16/300/quantum/_ps_and_gamma.npy', allow_pickle=True)[:, 0]

df_phase_space = pd.DataFrame({
    'Frequency (THz)': frequency.flatten(order='C'),
    'Phase Space': phase_space
})

df_phase_space.to_csv('frequency_vs_phase_space.csv', index=False)


# ----------------------
scattering_rate = np.load(
    data_folder + 'ALD_BFO/16_16_16/300/quantum/bandwidth.npy', 
    allow_pickle=True
)

life_time = scattering_rate **(-1)

df_lifetime = pd.DataFrame({
    'Frequency (THz)': frequency.flatten(order='C'),
    'Life Time (ps)': life_time.flatten()
})
df_lifetime = df_lifetime.dropna()  #

df_lifetime.to_csv('phonon_lifetime_data.csv', index=False)



df_scattering = pd.DataFrame({
    'Frequency (THz)': frequency.flatten(order='C'),
    'Scattering Rate (THz)': scattering_rate.flatten()
})
df_scattering = df_scattering.replace([np.inf, -np.inf], np.nan).dropna()

df_scattering.to_csv('scattering_rate_data.csv', index=False)



mean_free_path = []
for i in range(3):
    mean_free_path.append(np.loadtxt(
        data_folder + 'ALD_BFO/16_16_16/300/quantum/inverse/mean_free_path_' + str(i) + '.dat'
    ))

mean_free_path = np.array(mean_free_path).T
mean_free_path_norm = np.linalg.norm(mean_free_path.reshape(-1, 3), axis=1) / 10.0

df_mfp = pd.DataFrame({
    'Frequency (THz)': frequency.flatten(order='C'),
    'Mean Free Path (nm)': mean_free_path_norm.flatten()
})
df_mfp = df_mfp.replace([np.inf, -np.inf], np.nan).dropna()

df_mfp.to_csv('mean_free_path_data.csv', index=False)

group_velocity = np.load(data_folder + 'ALD_BFO/16_16_16/velocity.npy')

group_velocity_norm = np.linalg.norm(group_velocity.reshape(-1, 3), axis=1) / 10.0

df_group_velocity = pd.DataFrame({
    'Frequency (THz)': frequency.flatten(order='C'),
    'Group Velocity (km/s)': group_velocity_norm.flatten()
})
df_group_velocity = df_group_velocity.replace([np.inf, -np.inf], np.nan).dropna()

df_group_velocity.to_csv('group_velocity_data.csv', index=False)
