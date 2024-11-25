import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from tqdm import tqdm
import xarray as xr

def get_mask_continent_ocean(lat_values, lon_values, shapefile_path):
    # Leer el shapefile global de países
    world = gpd.read_file(shapefile_path)
    
    # Crear máscara de océano y continente
    continent_mask = np.zeros((len(lat_values), len(lon_values)), dtype=bool)
    ocean_mask = np.ones((len(lat_values), len(lon_values)), dtype=bool)

    # Iterar sobre latitudes y longitudes
    for i, lat in tqdm(enumerate(lat_values), desc="Latitudes"):
        for j, lon in enumerate(lon_values):
            point = Point(lon, lat)
            # Verificar si el punto está en tierra (intersección con geometrías del shapefile)
            if world.geometry.apply(lambda x: x.contains(point)).any():
                continent_mask[i, j] = True
                ocean_mask[i, j] = False

    return continent_mask, ocean_mask

def plot_mask(mask, title):
    plt.figure(figsize=(12, 6))
    plt.imshow(mask, extent=[lon_values.min(), lon_values.max(), lat_values.min(), lat_values.max()], origin='lower')
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.colorbar(label='Mask')
    plt.show()

# Definir coordenadas de latitud y longitud
file_path  = 'data/processed/monthly_aggregated/historical/pr/pr_1850.nc'
ds = xr.open_dataset(file_path)
lat_values = ds['lat'].values
lon_values = ds['lon'].values

if lon_values[0] >= 0:
        lon_values = np.where(lon_values > 180, lon_values- 360, lon_values)


# Ruta al shapefile global
shapefile_path = "W:/Proyectos/paleoclimate_global_simulations_chile_central/data/country_shp/ne_110m_admin_0_countries.shp"

# Obtener las máscaras de continente y océano
continent_mask, ocean_mask = get_mask_continent_ocean(lat_values, lon_values, shapefile_path)


#save masks
np.save('sub_projects/FONDECYT_11220930/results/masks/land_cmip6.npy', continent_mask)
np.save('sub_projects/FONDECYT_11220930/results/masks/ocean_cmip6.npy', ocean_mask)
# Graficar las máscaras
plot_mask(continent_mask, 'Continent Mask')
plot_mask(ocean_mask, 'Ocean Mask')
