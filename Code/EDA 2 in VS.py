import pandas as pd
import matplotlib.pyplot as plt

# loading data 
df_history = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_data\\Cleaned_Electric_Vehicle_Population_Size_History.csv")
df_population = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_data\\Cleaned_Electric_Vehicle_Population_Data.csv")
df_stations = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Electric_Vehicle_Charging_Stations.csv")

# Population_Size_History
df_history.set_index('date').plot(y=['plug_in_hybrid_electric', 'battery_electric_vehicle', 'electric_vehicle_total'])
plt.title('EV Growth Over Time')
plt.ylabel('Number of Vehicles')
plt.show()

# Population
df_population.groupby('County').size().plot(kind='bar', title='Number of EVs by County')

df_population.groupby('Model Year').size().plot(kind='bar', title='Growth of EVs Over Years')

df_population.groupby('Make').size().sort_values(ascending=False).head(10).plot(kind='bar', title='Top 10 EV Brands/Models')
plt.show()

# charging Stations 
df_stations.groupby('City').size().plot(kind='bar', title='Number of Charging Stations by City')

df_stations[['EV Level1 EVSE Num', 'EV Level2 EVSE Num', 'EV DC Fast Count']].sum().plot(kind='bar', title='Types of Charging Infrastructure')
plt.show()

df_stations['Open Date'] = pd.to_datetime(df_stations['Open Date'])

stations_count_by_date = df_stations.groupby('Open Date').size()

cumulative_stations = stations_count_by_date.cumsum()

plt.figure(figsize=(12, 6))
cumulative_stations.plot()
plt.title('Cumulative Number of Charging Stations Over Time')
plt.xlabel('Date')
plt.ylabel('Total Number of Charging Stations')
plt.grid(True)
plt.show()