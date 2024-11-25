import pandas as pd
import numpy as np 
import xarray as xr
from tqdm import tqdm

from xarray.coding.times import SerializationWarning
import warnings

warnings.filterwarnings("ignore", category=SerializationWarning)

df_lgm = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_lgm_rpi_monthly.csv')
df_piControl = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_piControl_rpi_monthly.csv')
df_midHolocene = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_midHolocene_rpi_monthly.csv')
df_historical = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_historical_rpi_monthly.csv')

dfs = {'lgm': df_lgm, 'piControl': df_piControl, 'midHolocene': df_midHolocene, 'historical': df_historical}

def means_layers(df, variable, experiment):
    
    path_in = "W:/Proyectos/paleoclimate_global_simulations_chile_central/data/processed/monthly_aggregated/"
    path_out  = 'W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/'
    
    wet = []
    dry = []
    anual = []
    for i in tqdm(range(0, len(df['date']))):
        #example of date 1850-01-31T00:00:00.000000000
        year = str(df['date'][i]).split('-')[0]
        month_i = int(str(df['date'][i]).split('-')[1])-1
        file_path = f'{path_in}{experiment}/{variable}/{variable}_{year}.nc'
        ds = xr.open_dataset(file_path)
        data = np.array(ds[variable].values)
        layer = data[month_i]
        anual.append(layer)
        if df['rpi'][i] > 200:
            wet.append(layer)
        elif df['rpi'][i] < 10:
            dry.append(layer)

    wet = np.nanmean(np.array(wet), axis=0)
    dry = np.nanmean(np.array(dry), axis=0)
    anual = np.nanmean(np.array(anual), axis=0)

    np.save(f'{path_out}{experiment}/{variable}/{variable}_wet_monthly.npy', wet)
    np.save(f'{path_out}{experiment}/{variable}/{variable}_dry_monthly.npy', dry)
    np.save(f'{path_out}{experiment}/{variable}/{variable}_anual_monthly.npy', anual)



def main():

    for experiment in ['historical', 'midHolocene', 'lgm', 'piControl']:
        print(f'Processing {experiment}...')
        means_layers(dfs[experiment], 'ua', experiment)
        means_layers(dfs[experiment], 'tp', experiment)




if __name__ == '__main__':
    main()




