import xarray as xr
import os
import numpy as np
from tqdm import tqdm

from xarray.coding.times import SerializationWarning
import warnings

warnings.filterwarnings("ignore", category=SerializationWarning)

def get_nc_files(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.nc')]

experiments = ['historical', 'piControl', 'midHolocene', 'lgm']

for experiment in experiments:
    layer_pr, layer_ua = np.zeros((1, 96, 192)), np.zeros((1, 8, 96, 192))
    n_layers = 0
    path_pr, path_ua = f'W:/CMIP6\MPI-ESM1-2-LR/{experiment}/day/pr/r1i1p1f1/', f'W:/CMIP6\MPI-ESM1-2-LR/{experiment}/day/ua/r1i1p1f1/'
    files_pr, files_ua = get_nc_files(path_pr), get_nc_files(path_ua)

    for file_pr, file_ua in tqdm(zip(files_pr, files_ua)):
        ds_pr, ds_ua = xr.open_dataset(file_pr), xr.open_dataset(file_ua)
        layer_pr += np.sum(ds_pr['pr'].values, axis=0)
        n_layers += len(ds_pr['pr'].values)
        layer_ua += np.sum(ds_ua['ua'].values, axis=0)
        ds_pr.close()
        ds_ua.close()

    
    mean_layer_pr = layer_pr / n_layers
    mean_layer_ua = layer_ua / n_layers

    path_out_pr = f'sub_projects/FONDECYT_11220930/results/conditions_mean/{experiment}/pr/'
    path_out_ua = f'sub_projects/FONDECYT_11220930/results/conditions_mean/{experiment}/ua/'
    if not os.path.exists(path_out_pr):
        os.makedirs(path_out_pr)

    if not os.path.exists(path_out_ua):
        os.makedirs(path_out_ua)


    np.save(f'sub_projects/FONDECYT_11220930/results/conditions_mean/{experiment}/pr/pr_daily_mean.npy', mean_layer_pr)
    np.save(f'sub_projects/FONDECYT_11220930/results/conditions_mean/{experiment}/ua/ua_daily_mean.npy', mean_layer_ua)