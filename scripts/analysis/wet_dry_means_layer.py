import pandas as pd
import numpy as np 
import xarray as xr
from tqdm import tqdm

from xarray.coding.times import SerializationWarning
import warnings

warnings.filterwarnings("ignore", category=SerializationWarning)

df_lgm = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_lgm_rpi.csv')
df_piControl = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_piControl_rpi.csv')
df_midHolocene = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_midHolocene_rpi.csv')
df_historical = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_historical_rpi.csv')

dfs = {'lgm': df_lgm, 'piControl': df_piControl, 'midHolocene': df_midHolocene, 'historical': df_historical}

def means_layers(df, variable, experiment, method= 'mean'):
    
    path_in = "W:/Proyectos/paleoclimate_global_simulations_chile_central/data/processed/monthly_aggregated/"
    path_out  = 'W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/'
    
    wet = []
    dry = []
    anual = []
    for i in tqdm(range(0, len(df['date']))):
        year = df['date'][i]
        file_path = f'{path_in}{experiment}/{variable}/{variable}_{year}.nc'
        ds = xr.open_dataset(file_path)
        data = np.array(ds[variable].values)
        if method == 'mean':
            layer = np.nanmean(data, axis=0)
        elif method == 'sum':
            layer = np.nansum(data, axis=0)
        anual.append(layer)
        if df['rpi'][i] > 120:
            wet.append(layer)
        elif df['rpi'][i] < 80:
            dry.append(layer)

    wet = np.nanmean(np.array(wet), axis=0)
    dry = np.nanmean(np.array(dry), axis=0)
    anual = np.nanmean(np.array(anual), axis=0)

    np.save(f'{path_out}{experiment}/{variable}/{variable}_wet.npy', wet)
    np.save(f'{path_out}{experiment}/{variable}/{variable}_dry.npy', dry)
    np.save(f'{path_out}{experiment}/{variable}/{variable}_anual.npy', anual)



def main():

    for experiment in ['historical', 'midHolocene', 'lgm', 'piControl']:
        print(f'Processing {experiment}...')
        means_layers(dfs[experiment], 'ua', experiment, methodd='mean')
        means_layers(dfs[experiment], 'tp', experiment, method='sum')




if __name__ == '__main__':
    main()




