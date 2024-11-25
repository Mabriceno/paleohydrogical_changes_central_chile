import pandas as pd
import numpy as np 




df_lgm = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_lgm.csv')
df_piControl = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_piControl.csv')
df_midHolocene = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_midHolocene.csv')
df_historical = pd.read_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_historical.csv')

years_lgm = np.unique(np.array([x.split('-')[0] for x in df_lgm['date'].values]))
print(years_lgm)
years_piControl = np.unique(np.array([x.split('-')[0] for x in df_piControl['date'].values]))
years_midHolocene = np.unique(np.array([x.split('-')[0] for x in df_midHolocene['date'].values]))
years_historical = np.unique(np.array([x.split('-')[0] for x in df_historical['date'].values]))

total_anual_series_lgm = np.array([np.sum(x) for x in np.split(df_lgm['precipitation'].values, len(df_lgm['precipitation'].values)/12) ])
total_anual_series_piControl = np.array([np.sum(x) for x in np.split(df_piControl['precipitation'].values, len(df_piControl['precipitation'].values)/12) ])
total_anual_series_midHolocene = np.array([np.sum(x) for x in np.split(df_midHolocene['precipitation'].values, len(df_midHolocene['precipitation'].values)/12) ])
total_anual_series_historical = np.array([np.sum(x) for x in np.split(df_historical['precipitation'].values, len(df_historical['precipitation'].values)/12) ])

rpi_lgm = (total_anual_series_lgm/np.mean(total_anual_series_lgm))*100
rpi_piControl = (total_anual_series_piControl/np.mean(total_anual_series_piControl))*100
rpi_midHolocene = (total_anual_series_midHolocene/np.mean(total_anual_series_midHolocene))*100
rpi_historical = (total_anual_series_historical/np.mean(total_anual_series_historical))*100

#save news csvs
print(len(years_lgm), len(total_anual_series_lgm), len(rpi_lgm))
df_out_lgm = pd.DataFrame({'date': years_lgm, 'total_precipitation': total_anual_series_lgm, 'rpi': rpi_lgm})
df_out_piControl = pd.DataFrame({'date': years_piControl, 'total_precipitation': total_anual_series_piControl, 'rpi': rpi_piControl})
df_out_midHolocene = pd.DataFrame({'date': years_midHolocene, 'total_precipitation': total_anual_series_midHolocene, 'rpi': rpi_midHolocene})
df_out_historical = pd.DataFrame({'date': years_historical, 'total_precipitation': total_anual_series_historical, 'rpi': rpi_historical})


df_out_lgm.to_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_lgm_rpi.csv', index=False)
df_out_piControl.to_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_piControl_rpi.csv', index=False)
df_out_midHolocene.to_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_midHolocene_rpi.csv', index=False)
df_out_historical.to_csv('W:/Proyectos/paleoclimate_global_simulations_chile_central/sub_projects/FONDECYT_11220930/results/conditions_mean/central_chile_precipitation_historical_rpi.csv', index=False)


