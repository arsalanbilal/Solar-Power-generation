import joblib
import pandas as pd
import numpy as np
import streamlit as st

model=joblib.load('solarproject.pkl')

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




if st.button('Predict'):
    features = np.array([[distance_to_solar_noon, temperature, wind_speed,
       sky_cover, visibility, humidity, average_wind_speed,
       average_pressure]])
    Gb = model.fit(x_train, y_train)
    prediction = model.predict(features)

    st.success(f'The predicted power generation is {prediction}')
