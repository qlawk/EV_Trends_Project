import pandas as pd
import statsmodels.api as sm

ev = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_data\\ev_county_clean_final.csv")
income = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_data\\wa_median_income.csv")
sex = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_data\\Population by gender.csv")
age = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_data\\Population by age.csv")

# added ev total to model df
ev_model = ev[ev['Date'] == 'December 31 2021']
ev_model = ev_model.drop(columns=['Date','Battery Electric Vehicles (BEVs)','Plug-In Hybrid Electric Vehicles (PHEVs)','Non-Electric Vehicle Total','Total Vehicles'])
ev_model = ev_model.rename(columns={'Electric Vehicle (EV) Total': 'EV Total'})

# Extract population data for 18 to 34 years
age_young = age[age['Indicator Name'] == '18 to 34 years'].copy()
age_young = age_young.drop(columns=['Location', 'Location - RegionId', 'Indicator Name', 'Indicator - Reference Name', 'Measure', 'Measure Name', 'Measure - Units', 'Scale', 'Units'])
age_young.rename(columns={'2021': 'age_young'}, inplace=True)

# Extract population data for 35 to 64 years
age_old = age[age['Indicator Name'] == '35 to 64 years'].copy()
age_old = age_old.drop(columns=['Location', 'Location - RegionId', 'Indicator Name', 'Indicator - Reference Name', 'Measure', 'Measure Name', 'Measure - Units', 'Scale', 'Units'])
age_old.rename(columns={'2021': 'age_old'}, inplace=True)

# merged income df, cleaned df
ev_model = ev_model.merge(income, on='County')
ev_model = ev_model.drop(columns=['Unnamed: 0','2022'])
ev_model = ev_model.rename(columns={'2021': 'Median Income'})

# changed median income from str to int
ev_model['Median Income'] = ev_model['Median Income'].str.replace(',', '')
ev_model['Median Income'] = ev_model['Median Income'].astype(int)

# Merge these data with your main dataframe ev_model
ev_model = pd.merge(ev_model, age_young[['County', 'age_young']], on='County', how='left')
ev_model = pd.merge(ev_model, age_old[['County', 'age_old']], on='County', how='left')

# dropped all columns except for chosen
sex = sex.loc[:, sex.columns.intersection(['County','Indicator Name','2021'])]
sex = sex.dropna()

# removed total state info, formated county 
sex = sex[sex['County'].str.contains('County')]

# changing population number from float to int
sex['2021'] = sex['2021'].astype(int)

# merged male pop. by county to ev model df
sex_m = sex[sex['Indicator Name'] == 'Male']
sex_m = sex_m.drop(columns='Indicator Name')
sex_m = sex_m.rename(columns={'County': 'County','2021': 'Male Pop.'})
ev_model = ev_model.merge(sex_m, on='County')

# merged female pop. by county to ev model df
sex_f = sex[sex['Indicator Name'] == 'Female']
sex_f = sex_f.drop(columns='Indicator Name')
sex_f = sex_f.rename(columns={'County': 'County','2021': 'Female Pop.'})
ev_model = ev_model.merge(sex_f, on='County')

# added total pop. as another variable
ev_model['Pop.'] = ev_model['Male Pop.'] + ev_model['Female Pop.']

# changed male, female pop to ratios
ev_model['Male Pop.'] = ev_model['Male Pop.'] / ev_model['Pop.']
ev_model['Female Pop.'] = ev_model['Female Pop.'] / ev_model['Pop.']
ev_model = ev_model.rename(columns={'Male Pop.': 'Male Ratio', 'Female Pop.': 'Female Ratio'})

X = ev_model.drop(['County', 'EV Total'], axis=1)

y = ev_model['EV Total']

# lm = sm.OLS(y, sm.add_constant(X))
mn = sm.OLS(y, sm.add_constant(X))

model = mn.fit()
print_model = model.summary()
print(print_model)


