# utils.py

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import pandas as pd
import numpy as np
from matplotlib.patheffects import withStroke

def plot_layer(ax, lons, lats, ocean_data, land_data, ocean_cmap, land_cmap, 
               vmin_land, vmax_land, vmin_ocean, vmax_ocean, 
               crs=ccrs.PlateCarree(), extent=None):
    """
    Plotea una capa oceánica y una continental en un mismo subplot.
    Args:
        ax: Axes de Matplotlib en el que se plotea.
        ocean_data: Datos de la capa oceánica.
        land_data: Datos de la capa continental.
        ocean_cmap: Colormap para la capa oceánica.
        land_cmap: Colormap para la capa continental.
        extent: Extensión geográfica de la capa [lon_min, lon_max, lat_min, lat_max].
    """
    # Establece el sistema de coordenadas geográficas
    if extent is not None:
        ax.set_extent(extent, crs=crs)
    
    # Añade un relieve sombreado más detallado
    # Plotea los datos oceánicos

    ocean_plot = ax.contourf(lons, lats, ocean_data[3], 
                               cmap=ocean_cmap, transform=ccrs.PlateCarree(),
                               vmin=vmin_ocean, vmax=vmax_ocean, extend='both', levels=19, zorder = 0)
    
    # Plotea los datos continentales
    land_plot = ax.contourf(lons, lats, land_data, 
                              cmap=land_cmap, transform=ccrs.PlateCarree(),
                              vmin=vmin_land, vmax=vmax_land, extend='both', levels=19)
    
    # Agrega características de costa y fronteras
    ax.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=0.5)

    

    #ax.add_feature(cfeature.BORDERS, color='gray')  
    #ax.stock_img(alpha=0.05)

     # Configura un efecto de sombra para la esfera
    '''for spine in ax.spines.values():
        spine.set_path_effects([withStroke(linewidth=20, foreground="black", alpha=0.5)])

    # Alternativamente, agregar una sombra al globo entero
    ax.patch.set_path_effects([withStroke(linewidth=30, foreground='black', alpha=0.5)])'''
    
    return ocean_plot, land_plot

def plot_layer_only_ocean(ax, lons, lats, ocean_data, ocean_cmap, 
               vmin_ocean, vmax_ocean, 
               crs=ccrs.PlateCarree(), extent=None):
    
    # Establece el sistema de coordenadas geográficas
    if extent is not None:
        ax.set_extent(extent, crs=crs)
    
    # Añade un relieve sombreado más detallado
    # Plotea los datos oceánicos

    ocean_plot = ax.contourf(lons, lats, ocean_data[3], 
                               cmap=ocean_cmap, transform=ccrs.PlateCarree(),
                               vmin=vmin_ocean, vmax=vmax_ocean, extend='both', levels=19, zorder = 0)
    
    # Agrega características de costa y fronteras
    ax.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=0.5)

    

    #ax.add_feature(cfeature.BORDERS, color='gray')  
    #ax.stock_img(alpha=0.05)

     # Configura un efecto de sombra para la esfera
    '''for spine in ax.spines.values():
        spine.set_path_effects([withStroke(linewidth=20, foreground="black", alpha=0.5)])

    # Alternativamente, agregar una sombra al globo entero
    ax.patch.set_path_effects([withStroke(linewidth=30, foreground='black', alpha=0.5)])'''
    
    return ocean_plot

def load_layer(file_path):
    
    layer = np.load(file_path)
    return layer


def apply_mask(layer, mask):
    """
    Aplica una máscara a una capa.
    Args:
        layer: Capa a la que se aplica la máscara.
        mask: Máscara a aplicar.
    """
    masked_layer = np.where(~mask, np.nan, layer)
    return masked_layer

def load_data(experiment, variable, conditions, region_mask=None):

    path = f'sub_projects/FONDECYT_11220930/results/conditions_mean/{experiment}/{variable}/'
    picontrol_path = f'sub_projects/FONDECYT_11220930/results/conditions_mean/piControl/{variable}/'
    data = {}
    for condition in conditions:
        data[condition] = (load_layer(f'{path}{variable}_{condition}.npy') - load_layer(f'{picontrol_path}{variable}_{condition}.npy'))
        if region_mask is not None:
            mask = np.load(f'sub_projects/FONDECYT_11220930/results/masks/{region_mask}_cmip6.npy')
            data[condition] = apply_mask(data[condition], mask)
    return data
        

def load_coord():
    """
    Función para cargar las coordenadas de las estaciones meteorológicas.
    """
    

    file_path  = 'data/processed/monthly_aggregated/historical/ua/ua_1850.nc'
    ds = xr.open_dataset(file_path)

    return np.array(ds['lon'].values),np.array(ds['lat'].values), np.array(ds['plev'].values)
    