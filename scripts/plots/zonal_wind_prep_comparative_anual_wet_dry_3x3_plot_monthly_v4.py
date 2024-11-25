# main.py

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from utils_plot import plot_layer, load_layer, apply_mask, load_data, load_coord, plot_layer_only_ocean
from matplotlib.colors import BoundaryNorm
from styles import get_cmap_styles, get_extent
import numpy as np

def set_data(experiments, variables, regions, conditions):
    
    data = {}
    for experiment in experiments:
        data[experiment] = {}
        for variable, region in zip(variables, regions):
            data[experiment][variable] = load_data(experiment, variable, conditions, region)
            
    return data
    

def main():
    # Configura la figura con 4x3 subplots
    crs = ccrs.NearsidePerspective(central_longitude=-110, 
                                   central_latitude=-55, 
                                   satellite_height=38000000, false_easting=0, false_northing=0, globe=None)
    
    fig, axes = plt.subplots(3, 3, figsize=(6, 7), subplot_kw={'projection': crs}, dpi=300)
    
    
    #title
    #fig.suptitle('Zonal Wind and Precipitation Anomaly', fontsize=16)

    # Cargar los estilos de colormap
    ocean_cmap, land_cmap = get_cmap_styles()
    variables = ['ua', 'tp']
    regions = ['ocean', 'land']
    experiments = ['historical', 'midHolocene', 'lgm']
    conditions = ['anual_monthly', 'dry_monthly', 'wet_monthly']
    conditions_labels = ['Anual', 'Dry', 'Wet']
    titles = [['Historical Mean Anomaly', 'Historical Dry Anomaly', 'Historical Wet Anomaly'],
             ['MidHolocene Mean Anomaly', 'MidHolocene Dry Anomaly', 'MidHolocene Wet Anomaly'],
             ['LGM Mean Anomaly', 'LGM Dry Anomaly', 'LGM Wet Anomaly']]
    #extent on sudamerica
    #extent = [-175, -55 , -75, -10]
   
    data = set_data(experiments, variables, regions, conditions)
    lons, lats, plevs = load_coord()
    # Generar el plot 3x3
    vmin_land, vmax_land = -30, 30 #-0.125, 0.125
    vmin_ocean, vmax_ocean = -3, 3
    for i, experiment in enumerate(data.keys()):
            for j, condition in enumerate(conditions):

                ocean_data = np.clip(data[experiment]['ua'][condition], vmin_ocean, vmax_ocean)
                
                ocean_plot = plot_layer_only_ocean(axes[i, j], lons, lats, ocean_data, ocean_cmap, vmin_ocean, vmax_ocean, crs=crs, extent=None)
                axes[i, j].set_title(f'({titles[i][j]})', fontsize=9)

     # Ajustar los espacios entre subplots
    #plt.tight_layout()

    ocean_levels = [-3, -1.8, -0.9, 0, 0.9, 1.8, 3]                      
    

        #add colorbar for ocean and land in the bottom of the plot


    # Barra de color para el océano
    cbar_ax = fig.add_axes([0.32, 0.06, 0.4, 0.02])
    cbar_ocean = fig.colorbar(ocean_plot, cax=cbar_ax, orientation='horizontal', extend='both',
                        ticks=np.round(ocean_levels, 1),
                        label=r'Zonal Wind [$m \dot s^{-1}$]',
                        pad=0,
                        shrink=0.7)
    
    # Ajustar los espacios entre subplots
    plt.subplots_adjust(left=0.04, right=0.99, top=0.95, bottom=0.1, wspace=0.05, hspace=0.17)
    
    # Mostrar la figura
    #plt.show()
    plt.savefig('sub_projects/FONDECYT_11220930/figs/zonal_wind_prep_comparative_anual_wet_dry_3x3_plot_monthly_v4.png', 
                dpi=600) #72 to low quality, 300 to high quality and 600 to very high quality
    plt.savefig('sub_projects/FONDECYT_11220930/figs/zonal_wind_prep_comparative_anual_wet_dry_3x3_plot_monthly_v4.pdf',
                dpi=600) #72 to low quality, 300 to high quality and 600 to very high quality

if __name__ == "__main__":
    main()
