import statsmodels.api as sm


X = sm.add_constant(df['Number_of_EV_users'])
Y = df['Number_of_charging_stations']

model = sm.OLS(Y, X).fit()
