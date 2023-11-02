import statsmodels.api as sm

# Add a constant to the predictor variable
X = sm.add_constant(df['Number_of_EV_users'])

# Y is the response variable
Y = df['Number_of_charging_stations']

# Fit the regression model
model = sm.OLS(Y, X).fit()
