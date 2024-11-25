import xarray as xr
import numpy as np
import pandas as pd
import os

from tqdm import tqdm

from ..utils.config import get_nc_files
from ..utils.conditions import add_to_season

#ignore SerializationWarning: Unable to decode time axis into full numpy.datetime64 objects, continuing using cftime.datetime objects instead, reason: dates out of range
from xarray.coding.times import SerializationWarning
import warnings

warnings.filterwarnings("ignore", category=SerializationWarning)

output = 'sub_projects/FONDECYT_11220930/results/conditions_mean/'

def process_conditions_mean(output_dir, variable, id_variables, experiments, treshold):

    for variable, id_variable in zip(variables, id_variables):
        for experiment in experiments:
            print(f"Processing {variable} for {experiment}")

            conditions_layers = {'annual':[], 'DJF':[], 'JJA':[], 'MAM':[], 'SON':[]}	
            
            file_path = f'data/processed/monthly_aggregated/{experiment}/{id_variable}/'
            nc_files = get_nc_files(file_path)

            output_dir = os.path.join(output, experiment, id_variable)
            os.makedirs(output_dir, exist_ok=True)

            for nc_file in tqdm(nc_files):
                
                ds = xr.open_dataset(nc_file)
                months = ds['time.month'].values
                for layer, month in zip(np.array(ds[id_variable].values), months):
                    conditions_layers = add_to_season(conditions_layers, layer, month)
                    conditions_layers['annual'].append(layer)
                    
            for key in conditions_layers.keys():
                #define the spacial axis with two last dimensions
                conditions_layers[key] = np.array(conditions_layers[key])
                layer_mean = np.mean(conditions_layers[key], axis=0)
                np.save(f'{output_dir}/{id_variable}_{key}.npy', layer_mean)
                


    
variables = ['Precipitation', 'Eastward Wind']
id_variables = ['tp', 'ua']
experiments = ['midHolocene', 'piControl', 'historical', 'lgm']
treshold = 300

process_conditions_mean(output, variables, id_variables, experiments, treshold)