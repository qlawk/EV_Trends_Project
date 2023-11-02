import pandas as pd

# Reading the Excel file
df_income = pd.read_excel("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Income and Poverty Estimates for U.S. States and Counties.xlsx")

# Data where 'indicator' starts with 'AGE'
df_age = df_income[df_income['indicator'].str.startswith('AGE')]

# Data where 'indicator' starts with 'SEX'
df_sex = df_income[df_income['indicator'].str.startswith('SEX')]

# Data where 'indicator' starts with 'RACE'
df_race = df_income[df_income['indicator'].str.startswith('RACE')]

# Saving the dataframes to CSV files
df_age.to_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Income and Poverty by age.csv", index=False)
df_sex.to_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Income and Poverty by sex.csv", index=False)
df_race.to_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Income and Poverty by race.csv", index=False)
