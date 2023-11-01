import pandas as pd
import matplotlib.pyplot as plt

# Example loading data into df_history
df_history = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_Electric_Vehicle_Population_Size_History.csv")
df_population = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_Electric_Vehicle_Population_Data.csv")
df_stations = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Electric_Vehicle_Charging_Stations.csv")

# Your plotting code remains unchanged
df_history.set_index('date').plot(y=['plug_in_hybrid_electric', 'battery_electric_vehicle', 'electric_vehicle_total'])
plt.title('EV Growth Over Time')
plt.ylabel('Number of Vehicles')
plt.show()

df_population.groupby('County').size().plot(kind='bar', title='Number of EVs by County')

df_population.groupby('Model Year').size().plot(kind='bar', title='Growth of EVs Over Years')

df_population.groupby('Make').size().sort_values(ascending=False).head(10).plot(kind='bar', title='Top 10 EV Brands/Models')
plt.show()

# Number of Charging Stations by City
df_stations.groupby('City').size().plot(kind='bar', title='Number of Charging Stations by City')

# Distribution of Charging Infrastructures
df_stations[['EV Level1 EVSE Num', 'EV Level2 EVSE Num', 'EV DC Fast Count']].sum().plot(kind='bar', title='Types of Charging Infrastructure')
plt.show()
