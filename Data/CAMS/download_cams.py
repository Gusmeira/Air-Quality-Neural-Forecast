import os
import cdsapi

c = cdsapi.Client(timeout=600)

years = range(2020, 2021)

for year in years:
    # ---- GASES ----
    target_gas = fr"C:\temp\pollutants_gases_{year}.nc"
    if os.path.exists(target_gas):
        os.remove(target_gas)

    c.retrieve(
        'cams-global-reanalysis-eac4',
        {
            'format': 'netcdf',
            'variable': [
                'ozone',
                'nitrogen_dioxide',
                'nitrogen_monoxide',
                'sulphur_dioxide',
                'carbon_monoxide',
            ],
            'model_level': ['60'],  # lowest model level (closest to surface)
            'date': f'{year}-01-01/{year}-12-31',
            'time': ['00:00', '06:00', '12:00', '18:00'],
            'type': 'analysis',
            'area': [-22.0, -54.5, -27.0, -48.0],
            'grid': [0.75, 0.75],
        },
        target_gas
    )

    # ---- PARTICULATES ----
    target_pm = fr"C:\temp\pollutants_pm_{year}.nc"
    if os.path.exists(target_pm):
        os.remove(target_pm)

    c.retrieve(
        'cams-global-reanalysis-eac4',
        {
            'format': 'netcdf',
            'variable': [
                'particulate_matter_2.5um',
                'particulate_matter_10um',
            ],
            'date': f'{year}-01-01/{year}-12-31',
            'time': ['00:00', '06:00', '12:00', '18:00'],
            'type': 'analysis',
            'area': [-22.0, -54.5, -27.0, -48.0],
            'grid': [0.75, 0.75],
        },
        target_pm
    )



# # === 2️⃣ Meteorologia ===
# c.retrieve(
#     'cams-global-reanalysis-eac4',
#     {
#         'format': 'netcdf',
#         'variable': [
#             '2m_temperature',
#             '10m_u_component_of_wind',
#             '10m_v_component_of_wind',
#             'total_column_water_vapour',
#             'total_precipitation',
#             'surface_solar_radiation_downwards',
#             'surface_uv_radiation',
#         ],
#         'date': '2024-12-01/2024-12-31',
#         'time': ['00:00', '06:00', '12:00', '18:00'],
#         'type': 'analysis',
#         'area': [-20.0, -54.0, -27.0, -48.0],
#         'grid': [0.75, 0.75],
#     },
#     r"C:\temp\cams_sp_jan2025_meteo.nc"
# )
