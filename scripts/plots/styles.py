# styles.py


def modify_cmap_to_white_center(cmap, start_fraction=0.4, end_fraction=0.6):
    """
    Modifica un colormap interpolando los colores centrales a blanco.
    
    Parameters:
    - cmap: El colormap original.
    - start_fraction: La fracción del colormap donde comenzará el color blanco.
    - end_fraction: La fracción del colormap donde terminará el color blanco.
    
    Returns:
    - new_cmap: El nuevo colormap con blanco en el centro.
    """
    import matplotlib.colors as mcolors
    import numpy as np
    # Extraer los colores del colormap original
    colors = cmap(np.linspace(0, 1, 256))

    # Definir los índices para el centro del colormap
    start_idx = int(256 * start_fraction)
    end_idx = int(256 * end_fraction)

    # Reemplazar los colores centrales por blanco
    colors[start_idx:end_idx, :] = np.array([1, 1, 1, 1])  # RGBA para blanco

    # Crear un nuevo colormap con los colores modificados
    new_cmap = mcolors.LinearSegmentedColormap.from_list("white_centered_cmap", colors)

    return new_cmap

def get_custom_cmap():
    """
    
    """
    from matplotlib import cm
    import numpy as np
    import matplotlib.colors as mcolors
    
    # Extraer los colores de los mapas de colores
    colors1 = cm.Blues_r(np.linspace(0, 1, 256))
    colors2 = cm.hot_r(np.linspace(0, 1, 256))
    
    # Unir los colores de los mapas de colores
    colors = np.vstack((colors1, colors2))
    
    # Crear un nuevo colormap con los colores unidos
    custom_cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors)
    
    return custom_cmap

def get_cmap_styles():
    """
    Devuelve los estilos de colormap para las capas oceánicas y continentales.
    """
    from matplotlib import cm

    # Mapas de colores para las capas oceánicas y continentales
    land_cmap = cm.BrBG
    ocean_cmap = cm.RdBu_r
    ocean_cmap = modify_cmap_to_white_center(ocean_cmap, start_fraction=0.45, end_fraction=0.55)
    land_cmap = modify_cmap_to_white_center(land_cmap, start_fraction=0.45, end_fraction=0.55)
    
    return ocean_cmap, land_cmap


def get_extent(region):
    """
    Devuelve la extensión geográfica para diferentes regiones predefinidas.
    Args:
        region: Nombre de la región ('global', 'south_america', etc.)
    """
    extents = {
        'global': [-180, 180, -90, 90],
        'south_america': [-90, -30, -60, 15],
        'north_atlantic': [-100, 20, 0, 80]
    }
    
    return extents.get(region, [-180, 180, -90, 90])
