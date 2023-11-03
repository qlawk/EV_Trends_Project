import pandas as pd
import statsmodels.api as sm

def load_all_datas():
    ev = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_data\\ev_county_clean_final.csv")
    income = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_data\\wa_median_income.csv")
    gender = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_data\\Population by gender.csv")
    age = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\Cleaned_data\\Population by age.csv")
    charge = pd.read_csv("C:\\Users\\17789\\LHL\\EV charging in Washington state\\data\\test2.csv")

    # Packing all variables into a dictionary
    data = {
        'ev': ev,
        'income': income,
        'gender': gender,
        'age': age,
        'charge': charge
    }
    
    return data

# added ev total to model df
def modify_ev_data(ev_data):
    ev_model = ev_data[ev_data['Date'] == 'December 31 2021']
    ev_model = ev_model.drop(columns=['Date','Battery Electric Vehicles (BEVs)','Plug-In Hybrid Electric Vehicles (PHEVs)','Non-Electric Vehicle Total','Total Vehicles'])
    ev_model = ev_model.rename(columns={'Electric Vehicle (EV) Total': 'EV Total'})

    return ev_model

# Extract population data for age group
# def extract_population_data(age_data):
#     age_young_data = age_data[age_data['Indicator Name'] == '18 to 34 years'].copy()
#     age_young_data = age_young_data.drop(columns=['Location', 'Location - RegionId', 'Indicator Name', 'Indicator - Reference Name', 'Measure', 'Measure Name', 'Measure - Units', 'Scale', 'Units'])
#     age_young_data.rename(columns={'2021': 'age_young'}, inplace=True)

# Extract population data for age group
def extract_population_data(age_data, age_group):
    if (age_group == "Young Pop."): 
        indicName = '18 to 34 years'
    else:
        indicName = '35 to 64 years'

    extracted_age_data = age_data[age_data['Indicator Name'] == indicName].copy()
    extracted_age_data = extracted_age_data.drop(columns=['Location', 'Location - RegionId', 'Indicator Name', 'Indicator - Reference Name', 'Measure', 'Measure Name', 'Measure - Units', 'Scale', 'Units'])
    extracted_age_data.rename(columns={'2021': age_group}, inplace=True)

    return extracted_age_data

# Extract the number of stations from 2021
def extract_number_stations_2021(charge):
    charge_2021 = charge[pd.to_datetime(charge['Open Date']).dt.year == 2021]
    num_stations_2021 = len(charge_2021)

    return num_stations_2021

# merged income df, cleaned df
def merge_income_data_and_clean(income_data, ev_model):
    ev_model = ev_model.merge(income_data, on='County')
    ev_model = ev_model.drop(columns=['Unnamed: 0','2022'])
    ev_model = ev_model.rename(columns={'2021': 'Median Income'})

    # changed median income from str to int
    ev_model['Median Income'] = ev_model['Median Income'].str.replace(',', '')
    ev_model['Median Income'] = ev_model['Median Income'].astype(int)

    return ev_model

# Merge these data with your main dataframe ev_model
def merge_ev_data_with_age_group_datas(ev_model, age_young_data, age_old_data):
    ev_model = pd.merge(ev_model, age_young_data[['County', 'Young Pop.']], on='County', how='left')
    ev_model = pd.merge(ev_model, age_old_data[['County', 'Old Pop.']], on='County', how='left')

    return ev_model

# dropped all columns except for chosen
def clean_up_gender_data_model(gender_data):
    gender_data = gender_data.loc[:, gender_data.columns.intersection(['County','Indicator Name','2021'])]
    gender_data = gender_data.dropna()

    # removed total state info, formated county 
    gender_data = gender_data[gender_data['County'].str.contains('County')]

    # changing population number from float to int
    gender_data['2021'] = gender_data['2021'].astype(int)

    return gender_data

# merged male pop. by county to ev model df
def separate_gender_datas(gender_data, gender):
    if (gender == 'Male'):
        column_name = 'Male Pop.'
    else:
        column_name = 'Female Pop.'

    seperated_gender_data = gender_data[gender_data['Indicator Name'] == gender]
    seperated_gender_data = seperated_gender_data.drop(columns='Indicator Name')
    seperated_gender_data = seperated_gender_data.rename(columns={'County': 'County','2021': column_name})

    return seperated_gender_data

# # merged female pop. by county to ev model df
# gender_f = gender[gender['Indicator Name'] == 'Female']
# gender_f = gender_f.drop(columns='Indicator Name')
# gender_f = gender_f.rename(columns={'County': 'County','2021': 'Female Pop.'})
# ev_model = ev_model.merge(gender_f, on='County')

def modify_gender_columns_to_ratio(ev_model):
    # added total pop. as another variable
    ev_model['Gender Pop.'] = ev_model['Male Pop.'] + ev_model['Female Pop.']

    # changed male, female pop to ratios
    ev_model['Male Pop.'] = ev_model['Male Pop.'] / ev_model['Gender Pop.']
    ev_model['Female Pop.'] = ev_model['Female Pop.'] / ev_model['Gender Pop.']
    ev_model = ev_model.rename(columns={'Male Pop.': 'Male Ratio', 'Female Pop.': 'Female Ratio'})

    return ev_model

def modify_age_columns_to_ratio(ev_model):
    # added total pop. as another variable
    ev_model['Age Pop.'] = ev_model['Old Pop.'] + ev_model['Young Pop.']

    # changed age_young, age_old  to ratios
    ev_model['Old Pop.'] = ev_model['Old Pop.'] / ev_model['Age Pop.']
    ev_model['Young Pop.'] = ev_model['Young Pop.'] / ev_model['Age Pop.']
    ev_model = ev_model.rename(columns={'Old Pop.': 'Old Age Ratio', 'Young Pop.': 'Young Age Ratio'})

    return ev_model

def perform_regression_modeling(ev_model):
    X = ev_model.drop(['County', 'EV Total'], axis=1)
    y = ev_model['EV Total']

    mn = sm.OLS(y, sm.add_constant(X))

    model = mn.fit()
    print_model = model.summary()
    print(print_model)

if __name__ == '__main__':
    all_data = load_all_datas()

    # Accessing the data
    ev_data = all_data['ev']
    income_data = all_data['income']
    gender_data = all_data['gender']
    age_data = all_data['age']
    charge_data = all_data['charge']

    ev_model = modify_ev_data(ev_data)
    ev_model['Num_Stations_2021'] = extract_number_stations_2021(charge_data)
    ev_model = merge_income_data_and_clean(income_data, ev_model)

    age_young_data = extract_population_data(age_data, "Young Pop.")
    age_old_data = extract_population_data(age_data, "Old Pop.")
    ev_model = merge_ev_data_with_age_group_datas(ev_model, age_young_data, age_old_data)
    
    gender_data = clean_up_gender_data_model(gender_data)
    separated_gender_data = separate_gender_datas(gender_data, 'Male')
    ev_model = ev_model.merge(separated_gender_data, on='County')

    separated_gender_data = separate_gender_datas(gender_data, 'Female')
    ev_model = ev_model.merge(separated_gender_data, on='County')

    ev_model = modify_gender_columns_to_ratio(ev_model)
    ev_model = modify_age_columns_to_ratio(ev_model)
    perform_regression_modeling(ev_model)