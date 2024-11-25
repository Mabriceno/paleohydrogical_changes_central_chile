
import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd

from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from tqdm import tqdm
from ..utils.config import get_nc_files

def get_mask_chile_central(lat_values, lon_values):
    # Definir el polígono de Chile central (aproximadamente)
    central_chile_coords = [
        (-75, -40),  # Esquina inferior izquierda
        (-70, -40),  # Esquina inferior derecha
        (-70, -32),  # Esquina superior derecha
        (-75, -32)   # Esquina superior izquierda
    ]

    central_chile_polygon = Polygon(central_chile_coords)
    shapefile_path = "W:/Proyectos/paleoclimate_global_simulations_chile_central/data/country_shp/ne_110m_admin_0_countries.shp"
    world = gpd.read_file(shapefile_path)

    central_chile_shape = gpd.GeoDataFrame(geometry=[central_chile_polygon], crs="EPSG:4326")
    
    chile = world[world.NAME_EN == "Chile"]
    central_chile_mask = gpd.overlay(chile, central_chile_shape, how='intersection')
    mask = np.zeros((12, len(lat_values), len(lon_values)), dtype=bool)

    for i, lat in tqdm(enumerate(lat_values)):
        for j, lon in enumerate(lon_values):
            point = Point(lon, lat)
            if central_chile_mask.geometry.apply(lambda x: x.contains(point)).any():
                mask[:, i, j] = True
    return mask, central_chile_shape


def select_region(array, lat_i, lat_f, lon_i, lon_f, lats, lons):
    
    lat_i_idx, lat_f_idx = np.abs(lats - lat_i).argmin(), np.abs(lats - lat_f).argmin()
    lon_i_idx, lon_f_idx = np.abs(lons - lon_i).argmin(), np.abs(lons - lon_f).argmin()
    return array[:, lat_i_idx:lat_f_idx, lon_i_idx:lon_f_idx]


def fix_lon(lons, lon_i, lon_f):

    if np.all(lons >= 0):
        lon_i_fix = lon_i + 360
        lon_f_fix  = lon_f + 360
    else:
        lon_i_fix = lon_i
        lon_f_fix = lon_f

    return lon_i_fix, lon_f_fix

def fix_lat(lats, lat_i, lat_f):

    if lats[0] <= 0:
        lat_i_fix = lat_f
        lat_f_fix = lat_i
    else:
        lat_i_fix = lat_i
        lat_f_fix = lat_f

    return lat_i_fix, lat_f_fix

def precip_chile_cetral(ds, lat_key='lat', lon_key='lon', code_name ='pr'):
    """
    Calculate the precipitation index from a dataset.
    """
    lats = ds[lat_key].values
    lons = ds[lon_key].values
    pr = ds[code_name].values

    if lons[0] >= 0:
        lons= np.where(lons > 180, lons - 360, lons)

    # if mask_chile_central file does not exist, create it
    try:
        mask = np.load(f'W:/Proyectos/paleoclimate_global_simulations_chile_central/data/mask_chile_central_{code_name}.npy')
    except:
        mask, central_chile_shape = get_mask_chile_central(lats, lons)
        np.save(f'W:/Proyectos/paleoclimate_global_simulations_chile_central/data/mask_chile_central_{code_name}.npy', mask)
        pr_masked = np.where(mask, pr, np.nan)
        # Visualización para verificar la máscara en un paso de tiempo específico
        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes(projection=ccrs.PlateCarree())

        # Añadir las líneas costeras y bordes de los países
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')

        # Graficar la precipitación con la máscara aplicada
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        precip_plot = ax.pcolormesh(lon_grid, lat_grid, pr_masked[0], transform=ccrs.PlateCarree(), cmap='Blues')

        # Añadir el polígono de Chile central
        central_chile_shape.boundary.plot(ax=ax, edgecolor='red')

        # Configurar límites de la gráfica
        ax.set_extent([-80, -60, -45, -25], crs=ccrs.PlateCarree())

        # Añadir colorbar
        plt.colorbar(precip_plot, ax=ax, orientation='horizontal', pad=0.05)

        # Mostrar la gráfica
        plt.show()

    pr_masked = np.where(mask, pr, np.nan)
    pr_chile = np.nanmean(pr_masked, axis=(1, 2))
    precip = pr_chile

    return precip





experiments = ['midHolocene', 'piControl', 'historical', 'lgm']

for experiment in experiments:
    
    files = get_nc_files(f'data/processed/monthly_aggregated/{experiment}/tp/')
    year_preps = []
    months = []
    for file in tqdm(files):
        ds = xr.open_dataset(file)
        precips = precip_chile_cetral(ds, code_name='tp')
        dates = ds['time'].values
        for month_precip, date in zip(precips, dates):
            year_preps.append(month_precip)
            months.append(date)


        ds.close()
    
    df = pd.DataFrame({'date': months, 'precipitation': year_preps})
    df.to_csv(f'sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_{experiment}.csv', index=False)