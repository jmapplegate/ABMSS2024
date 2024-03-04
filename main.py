# main.py

import numpy as np
import pandas as pd

#### import functions from model files
from series_parameters import series_params
from initialisation_functions import *
from firm_functions import *
from household_functions import *
from market_functions import *
from simulation import simulation

from numpy.random import default_rng
from operator import itemgetter

import warnings
warnings.filterwarnings('ignore')

#### series setup
directory, series_name, seed, reps, n_sets, series_params_list = series_params()

#### verify directory exists
from pathlib import Path
Path(directory).mkdir(parents=True, exist_ok=True)

#### initialise rng to be used by simulation series
rng = default_rng(seed)

print('This experiment consists of {} simulations'.format(n_sets * reps))
print('consisting of {} parameter sets.'.format(n_sets))

#### intitialise storage vehicle for series results
series_results = []

#### main body of multi parameter set code
for params in series_params_list:
    sim_results = simulation(*params, rng)
    series_results = series_results + sim_results

print('\nFinished series.')

macro_labels = ['set', 'run', 'step', 't_max', 'n', 'H_max', 'A', 'gamma', 'mu', 'S_N', 'omega_0', 'p_0', 'delta_0', 
                'theta', 'min_pct', 'pct_change',
                'I', 'pi', 'total_pi', 'omega', 'p', 'H_D', 'S_S', 'S_P', 'S_hat', 'N', 'H_S', 'H_M', 'S_D', 'S_M',
                'total_H_N', 'total_H_O','total_m', 'med_m', 'mean_m', 'max_m', 'min_m', 'mean_U', 'mean_alpha']

#### Transform list of lists into dataframes
series_results_frame = pd.DataFrame(series_results, columns = macro_labels)

#### For troubleshooting
#print(series_results_frame)

#### Save dataframe to directory as csv file.
print('Writing to files.')
prefix = directory + 'series_' + series_name
series_results_frame.to_csv(prefix + '.csv', index = False)
print('Series results written to', prefix + '.csv')