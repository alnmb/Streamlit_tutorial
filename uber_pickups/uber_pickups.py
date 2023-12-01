import streamlit as st
import pandas as pd
import numpy as np

#Every good app has a title, so let's add one:
st.title('Uber pickups in NYC')

#Now it's time to run Streamlit from the command line
#streamlit run uber_pickups.py

#fetching some data
# 1. let's start by writing a function to load the data.
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

    return data

# 2. Now let's test the function and review the output.

#Create a text element and let the reader know the data is loading
data_load_state = st.text('Loading data...')

# Load 10,000 rows of data into the dataframe
data = load_data(10000)

# Notify the reader that the data was succesfuly loaded.
data_load_state.text('Done! (using st.cache_data)')

# Use a button to toggle data
# let's use the st.checkbox function to add a checkbox to your app
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Draw an histogram
# 1. To start, let's add a subheader just below the raw data section
st.subheader('Number of pickups by hour')

# 2 Use NumPy to generate a histogram that breaks down pickup times binned by hour
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# 3 Now let's use Streamlist st.bar_chart method to draw this histogram
st.bar_chart(hist_values)

# Plot data on a map
# Plot the data of where the pickups where in the city

# 1 Add a subheader for the section
st.subheader('Map of all pickups')

# 2 Use the st.map function to plot the data
st.map(data)

# 3 redraw the map to show the concentration of pickups at 17:00

st.subheader('Map of all pickups')
#hour_to_filter = 17
hour_to_filter = st.slider('hour',0,23,17) # min:0h, max:23h, default:17h

filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00 ')
st.map(filtered_data)

# Filter results with a slider
# To filter dynamically the map using an slider


