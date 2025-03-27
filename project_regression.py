# -*- coding: utf-8 -*-
"""Project Regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1u1ADC5-lgdixIQi5-4NlZ8kXHtfqJ384
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

solar = pd.read_csv('/content/solarpowergeneration.csv')

info = solar.info()

columns = solar.columns

solar['average-wind-speed-(period)'].value_counts()

solar['average-wind-speed-(period)'].mean()

solar['average-wind-speed-(period)'].median()

solar['average-wind-speed-(period)'].fillna(0.0, inplace=True)

solar.info()

features = solar.drop(columns=['power-generated'])
features

correlation = solar.corr()

# Heatmap to visualize the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
plt.title("Correlation Heatmap")
plt.show()

# Using seaborn's pairplot to visualize relationships between all features and target variable
sns.pairplot(solar)
plt.show()

# Plot pairwise relationships between features and target variable
sns.pairplot(solar, vars=['temperature', 'wind-speed', 'sky-cover', 'humidity', 'visibility', 'distance-to-solar-noon'], hue='power-generated')
plt.show()

# Box plots to check for outliers
plt.figure(figsize=(15, 10))
sns.boxplot(data=solar)
plt.title('Box Plots for All Columns')
plt.tight_layout()
plt.show()

# Identifying outliers using the IQR method
Q1 = solar.quantile(0.25)
Q3 = solar.quantile(0.75)
IQR = Q3 - Q1
print(IQR)

z_scores = np.abs(stats.zscore(solar))
outliers = (z_scores > 3).sum(axis=0)
print(f"Number of outliers in each feature:\n{outliers}")

wind_direction_mapping = {
    'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
    'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
    'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
    'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
}

# Replace wind direction strings with numeric values
solar['wind-direction'] = solar['wind-direction'].map(wind_direction_mapping)

# Now you can calculate the mean and assign it back
solar['wind-direction'] = solar['wind-direction'].apply(lambda x: solar['wind-direction'].mean())

z_scores = np.abs(stats.zscore(solar))
outliers = (z_scores > 3).sum(axis=0)
print(f"Number of outliers in each feature:\n{outliers}")

solar['visibility'] = solar['visibility'].apply(lambda x: solar['visibility'].mean())

solar['humidity'] = solar['humidity'].apply(lambda x: solar['humidity'].mean())

solar['wind-direction'] = solar['wind-direction'].apply(lambda x: solar['wind-direction'].mean())

solar['wind-speed'] = solar['wind-speed'].apply(lambda x: solar['wind-speed'].mean())

solar['average-wind-speed-(period)'] = solar['average-wind-speed-(period)'].apply(lambda x: solar['average-wind-speed-(period)'].mean())

solar['average-pressure-(period)'] = solar['average-pressure-(period)'].apply(lambda x: solar['average-pressure-(period)'].mean())

z_scores = np.abs(stats.zscore(solar))
outliers = (z_scores > 3).sum(axis=0)
print(f"Number of outliers in each feature:\n{outliers}")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Melt the DataFrame to have 'value' and 'variable' columns
melted_solar = pd.melt(solar)

# Create the box plot
plt.figure(figsize=(15, 10))
sns.boxplot(x='value', y='variable', data=melted_solar)
plt.title('Box Plots for All Columns')
plt.tight_layout()
plt.show()

scalar = StandardScaler()
scaled = scalar.fit_transform(solar)

from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy='mean')
solar_imputed = imputer.fit_transform(solar)

X = solar.drop(columns=['power-generated'])
Y = solar['power-generated']

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
x_train = imputer.fit_transform(x_train)
x_test = imputer.transform(x_test)

linear_model = LinearRegression()
linear_model.fit(x_train, y_train)

y_pred = linear_model.predict(x_test)

print(" Linear Regression")
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)
r2 = r2_score(y_test, y_pred)
print("R-squared:", r2)

"""### Gradient Boosting Regressor :-"""

from sklearn.ensemble import GradientBoostingRegressor

gbr = GradientBoostingRegressor()
gbr.fit(x_train, y_train)

y_pred1 = gbr.predict(x_test)

print(" Gradiant Boosting Regressor")
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)
r2 = r2_score(y_test, y_pred)
print("R-squared:", r2)

from sklearn.model_selection import GridSearchCV

parameters = {
             'learning_rate' : [0.1, 0.05, 0.01],
             'max_depth' : [3, 5, 10],
             'min_samples_split' : [2, 5, 10],
             'min_samples_leaf' : [1, 5, 10],
             'n_estimators' : [50, 100, 200]
             }

grid_search = GridSearchCV(estimator=gbr, param_grid=parameters, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(x_train, y_train)

best_params = grid_search.best_params_

best_score = grid_search.best_score_

y_pred1 = grid_search.predict(x_test)

mse = mean_squared_error(y_test, y_pred)

r2 = r2_score(y_test, y_pred1)

!pip install scikit-learn

"""### Random forest & Decison Tree Regressor :-"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score



rf = RandomForestRegressor()

# Define parameter grid
rf_param_grid = {
    'n_estimators': [50, 100, 200, 500],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Using RandomizedSearchCV (faster)
rf_random_search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=rf_param_grid,
    n_iter=10,
    scoring='r2',
    cv=5,
    random_state=42,
    n_jobs=-1
)
rf_random_search.fit(x_train, y_train)

# Best parameters
print("Best RandomForest Parameters:", rf_random_search.best_params_)

# Train best model
best_rf = rf_random_search.best_estimator_
y_pred_rf = best_rf.predict(x_test)

# Evaluation
print("RandomForest R² Score:", r2_score(y_test, y_pred_rf))
print("RandomForest MAE:", mean_absolute_error(y_test, y_pred_rf))
print("RandomForest RMSE:", np.sqrt(mean_squared_error(y_test, y_pred_rf)))

# =======================
# 🔹 DecisionTreeRegressor Hyperparameter Tuning
# =======================

dt = DecisionTreeRegressor()

# Define parameter grid
dt_param_grid = {
    'max_depth': [5, 10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Using GridSearchCV (more exhaustive search)
dt_grid_search = GridSearchCV(
    estimator=dt,
    param_grid=dt_param_grid,
    scoring='r2',
    cv=5,
    n_jobs=-1
)
dt_grid_search.fit(x_train, y_train)

# Best parameters
print("Best DecisionTree Parameters:", dt_grid_search.best_params_)

# Train best model
best_dt = dt_grid_search.best_estimator_
y_pred_dt = best_dt.predict(x_test)

# Evaluation
print("DecisionTree R² Score:", r2_score(y_test, y_pred_dt))
print("DecisionTree MAE:", mean_absolute_error(y_test, y_pred_dt))
print("DecisionTree RMSE:", np.sqrt(mean_squared_error(y_test, y_pred_dt)))

import joblib

joblib.dump(gbr,'solarproject.pkl')

model=joblib.load('solarproject.pkl')

!pip install streamlit

!pip install matplotlib-venn

import streamlit as st
import pandas as pd

st.title('Solar Power Generation Prediction')
st.info('This is a Gradiant Boosting Machine Learning App')

st.sidebar.title("Settings")

uploaded_file = st.sidebar.file_uploader("Choose a file", type = ['csv', 'xlsx'])

if uploaded_file is not None:
   if uploaded_file.name.endswith('.csv'):
      df = pd.read_csv(uploaded_file)
   elif uploaded_file.name.endswith('.xlsx'):
    df = pd.read_excel(uploaded_file)
   else:
    st.error("Please upload a valid file")
else:
  st.warning("No file uploaded. Please upload a 'csv' OR 'xlsx' format file ")


st.success(" File loaded Successfully!")


with st.expander('**Data**'):
   st.write('**Raw Data**')
   solar = pd.read_csv('/content/solarpowergeneration.csv')
   solar

with st.expander('**X**'):
   st.write('**X**')
   X_raw = solar.drop('power-generated', axis=1)
   X_raw

with st.expander('**Y**'):
   st.write('**y**')
   y_raw = solar['power-generated']
   y_raw

with st.expander('**Data Visulisation**'):
   st.write('Solar Power Generation over time')
   st.bar_chart(solar)



# Input features
with st.sidebar:
  st.header('Input features')
distance_to_solar_noon=st.sidebar.slider('distance-to-solar-noon', min_value=0.0, max_value=24.0, value=1.0)
temperature=st.sidebar.number_input('temperature', min_value=0.0, max_value=100.0, value=1.0)
#wind_direction=st.number_input('wind-direction',min_value=0,max_value=100,value=0)
wind_direction_mapping=st.sidebar.number_input('wind_direction_mapping', min_value=0.0, max_value=360.0, value=1.0)
wind_speed=st.sidebar.slider('wind-speed', min_value=0.0, max_value=50.0, value=1.0)
sky_cover=st.sidebar.slider('sky-cover', min_value=0.0, max_value=1.0, value=0.1)
visibility=st.sidebar.slider('visibility',min_value=0.0,max_value=10.0,value=1.0)
humidity=st.sidebar.number_input('humidity', min_value=0.0, max_value=1.0, value=0.1)
average_wind_speed=st.sidebar.slider('average-wind-speed-(period)', min_value=0.0, max_value=50.0, value=1.0)
average_pressure=st.sidebar.number_input('average-pressure-(period)', min_value=800.0, max_value=1200.0, value=801.0)
#power_generated=st.number_input('power-generated',min_value=0,max_value=40000,value=0)


 # Create a DataFrame for the input features
data = {'distance_to_solar_noon': distance_to_solar_noon,
          'temperature': temperature,
          #'wind_direction': wind_direction,
          'wind_direction_mapping': wind_direction_mapping,
          'wind_speed': wind_speed,
          'sky_cover': sky_cover,
          'visibility': visibility,
          'humidity': humidity,
          'average_wind_speed': average_wind_speed,
          'average_pressure': average_pressure
}

input_df = pd.DataFrame(data, index=[0])
input_penguins = pd.concat([input_df, X_raw], axis=0)

with st.expander('Input features'):
  st.write('**Input penguin**')
  input_df


if st.button('Predict'):
    features = np.array([[distance_to_solar_noon, temperature, wind_speed,
       sky_cover, visibility, humidity, average_wind_speed,
       average_pressure]])
    Gb = model.fit(x_train, y_train)
    prediction = model.predict(features)

    st.success(f'The predicted power generation is {prediction}')

!pip install streamlit -q

"""### Model Deployment using Streamlit :-"""

!wget -q -O - ipv4.icanhazip.com