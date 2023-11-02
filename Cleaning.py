import pandas as pd

# Assuming the files are named history.csv, population.csv, and stations.csv respectively
df_history = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Electric_Vehicle_Population_Size_History.csv")
df_population = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Electric_Vehicle_Population_Data.csv")
df_stations = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Electric_Vehicle_Charging_Stations.csv", low_memory=False)

# Electric_Vehicle_Population_Size_History
df_history.dropna(inplace=True)

df_history['date'] = df_history['date'].str.replace('T00:00:00.000', '', regex=True)

df_history['date'] = pd.to_datetime(df_history['date'])

df_history['Calculated EV Total'] = df_history['plug_in_hybrid_electric'] + df_history['battery_electric_vehicle']

df_history['Correct Total'] = df_history['Calculated EV Total'] == df_history['electric_vehicle_total']

# Electric_Vehicle_Population_Data
df_population = df_population[df_population['State'] == 'WA']
columns_to_drop = ["Base MSRP", "Legislative District", "DOL Vehicle ID", "Vehicle Location", "Electric Utility", "2020 Census Tract"]
df_population = df_population.drop(columns=columns_to_drop)

# Electric_Vehicle_Charging_Stations

duplicate_vins = df_population[df_population.duplicated(subset='VIN (1-10)', keep=False)]
print(duplicate_vins)

df_stations = df_stations[df_stations['State'] == 'WA']

columns_to_remove = [
    "Plus4", "Status Code", "Expected Date", "BD Blends", "NG Fill Type Code", 
    "NG PSI", "EV Other Info", "EV Network Web", "Federal Agency ID", 
    "Federal Agency Name", "Hydrogen Status Link", "NG Vehicle Class", 
    "LPG Primary", "E85 Blender Pump", "Country", 
    "Intersection Directions (French)", "Access Days Time (French)", 
    "BD Blends (French)", "Groups With Access Code (French)", "Hydrogen Is Retail", 
    "Access Detail Code", "Federal Agency Code", "Facility Type", "CNG Dispenser Num", 
    "CNG On-Site Renewable Source", "CNG Total Compression Capacity", "CNG Storage Capacity", 
    "LNG On-Site Renewable Source", "E85 Other Ethanol Blends", "EV Pricing", 
    "EV Pricing (French)", "LPG Nozzle Types", "Hydrogen Pressures", 
    "Hydrogen Standards", "CNG Fill Type Code", "CNG PSI", "CNG Vehicle Class", 
    "LNG Vehicle Class", "EV On-Site Renewable Source", "Restricted Access"
]

df_stations = df_stations.drop(columns=columns_to_remove)


df_history.to_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_Electric_Vehicle_Population_Size_History.csv", index=False)
df_population.to_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_Electric_Vehicle_Population_Data.csv", index=False)
df_stations.to_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_Electric_Vehicle_Charging_Stations.csv", index=False)
