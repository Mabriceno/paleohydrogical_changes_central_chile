import numpy as np
import xarray as xr


def add_to_season(dict, layer, month):

    if month in [12, 1, 2]:
        dict['DJF'].append(layer)
    elif month in [3, 4, 5]:
        dict['MAM'].append(layer)
    elif month in [6, 7, 8]:
        dict['JJA'].append(layer)
    elif month in [9, 10, 11]:
        dict['SON'].append(layer)
    else:
        raise ValueError("Month not recognized")
    
    return dict


