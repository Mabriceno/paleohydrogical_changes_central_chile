# Climate Precipitation Analysis

## Evaluación de los Controladores Climáticos de las Precipitaciones en Chile Central a lo Largo de Diferentes Épocas Climáticas

### Descripción del Proyecto

Este proyecto tiene como objetivo evaluar cómo han variado los controladores de las precipitaciones en Chile central durante diferentes periodos climáticos: el Último Máximo Glacial (LGM), el Holoceno Medio, el periodo preindustrial (piControl) y la era moderna (ERA5). Se analizan variables como la precipitación, patrones de viento, presión atmosférica y temperatura superficial del mar, así como índices climáticos relevantes.

### Descripción de Directorios y Archivos

- **data/**: Contiene datos necesarios para el análisis, organizados por periodos climáticos y tipos de datos.
- **scripts/**: Scripts en Python organizados por función para preprocesamiento, análisis y visualización de datos.
- **notebooks/**: Notebooks Jupyter para exploración de datos, análisis preliminar y visualización de resultados.
- **results/**: Resultados del análisis, incluidos gráficos, tablas y reportes.
- **README.md**: Este archivo de documentación.

### Requisitos

- Python 3.7 o superior
- Bibliotecas: `xarray`, `numpy`, `pandas`, `matplotlib`, `scipy`, `netCDF4`, `jupyter`

### Instrucciones para Ejecutar el Proyecto

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Mabriceno/paleoclimate_chile_central_precipp_analysis.git
   cd climate_precipitation_analysis

2.  **Instalar dependecias** 
    ```bash
    pip install -r requirements.txt

3. **Preprocesar los datos**
    Ejecutar los scripts de preprocesamiento en el directorio `scripts/data_preprocessing/`.

4. **Realizar análisis**
    Ejecutar los scripts de análisi en el directorio `scripts/analysis/`.

5. **Generar visualizaciones**
    Ejecutar los scripts de visualización en el directorio `scripts/visualization/`.

6. **Explorar datos y resultados**
    Abrir y ejecutar los notebooks en el directorio `notebooks/`.

### Consideraciones

- **error al ejecutar scripts**: Si al ejecutar un script obtiene errores como "ImportError: attempted relative import with no known parent package" considere ejecutarlo desde la raíz del proyecto usando `python -m`. Por ejemplo si desea ejecutar `monthly_aggregation.py` utilice:
    ```bash
    python -m scripts.data_preprocessing.monthly_aggregation

### Contacto

Para cualquier pregunta o sugerencia, puedes contactarme en mabricenoyanez@gmail.com


Este `README.md` proporciona una guía clara sobre la estructura del proyecto, los requisitos y los pasos necesarios para ejecutar el análisis. También incluye información de contacto para soporte adicional.
