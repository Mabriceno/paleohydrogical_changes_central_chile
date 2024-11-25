import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
def compute_monthly_rpi(df):
    """
    Compute the Regional Precipitation Index (RPI) on a monthly basis for a given dataframe.

    Parameters:
    df (pd.DataFrame): DataFrame containing 'date' and 'precipitation' columns.

    Returns:
    pd.DataFrame: DataFrame with 'date', 'precipitation', and 'rpi' columns.
    """
    # Parse 'date' into datetime
    #df['date'] = pd.to_datetime(df['date'])

    # Extract month
    df['month'] = [int(str(date).split('-')[1]) for date in df['date']]

    # Compute mean precipitation for each month
    monthly_means = df.groupby('month')['precipitation'].mean()

    # Map the monthly mean precipitation to each row
    df['mean_precipitation'] = df['month'].map(monthly_means)

    # Compute RPI
    df['rpi'] = (df['precipitation'] / df['mean_precipitation']) * 100

    return df[['date', 'precipitation', 'rpi']]

# File paths
base_path = 'W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/'

# Read CSV files
df_lgm = pd.read_csv(base_path + 'central_chile_precipitation_lgm.csv')
df_piControl = pd.read_csv(base_path + 'central_chile_precipitation_piControl.csv')
df_midHolocene = pd.read_csv(base_path + 'central_chile_precipitation_midHolocene.csv')
df_historical = pd.read_csv(base_path + 'central_chile_precipitation_historical.csv')

# Compute monthly RPI for each dataframe
print('Computing RPI for LGM...')
df_lgm_rpi = compute_monthly_rpi(df_lgm)

print('Computing RPI for piControl...')
df_piControl_rpi = compute_monthly_rpi(df_piControl)
plt.hist(df_piControl_rpi['rpi'], bins=50)
#line percentile 20
plt.axvline(np.percentile(df_piControl_rpi['rpi'], 5), color='r', linestyle='dashed', linewidth=1)
print(np.percentile(df_piControl_rpi['rpi'], 5))
#line percentile 80
plt.axvline(np.percentile(df_piControl_rpi['rpi'], 95), color='r', linestyle='dashed', linewidth=1)
print(np.percentile(df_piControl_rpi['rpi'], 95))
plt.show()
print('Computing RPI for midHolocene...')
df_midHolocene_rpi = compute_monthly_rpi(df_midHolocene)
plt.hist(df_midHolocene_rpi['rpi'], bins=50)
plt.show()
print('Computing RPI for historical...')
df_historical_rpi = compute_monthly_rpi(df_historical)
plt.hist(df_historical_rpi['rpi'], bins=50)
plt.show()

# Save results to CSV
df_lgm_rpi.to_csv(base_path + 'central_chile_precipitation_lgm_rpi_monthly.csv', index=False)
df_piControl_rpi.to_csv(base_path + 'central_chile_precipitation_piControl_rpi_monthly.csv', index=False)
df_midHolocene_rpi.to_csv(base_path + 'central_chile_precipitation_midHolocene_rpi_monthly.csv', index=False)
df_historical_rpi.to_csv(base_path + 'central_chile_precipitation_historical_rpi_monthly.csv', index=False)
