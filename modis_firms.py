"""An example of showing geographic data."""

import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
from PIL import Image
import datetime
import base64

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Fires worldwide 🌳🔥", page_icon=":fire:")

######################
# Page Title
######################

image = Image.open('MC.png')

st.image(image, use_column_width=False)

st.write(" ## MODIS FIRE LOCATIONS")

#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Data source:** [FIRMS: Fire Information for Resource Management System](https://firms.modaps.eosdis.nasa.gov/country/).
* **Python libraries:** pandas, streamlit, altair, datetime, Image, numpy, pydeck
* The **near real-time (NRT)** active fire locations are processed by LANCE using the standard **MODIS MOD14/MYD14 Fire and Thermal Anomalies product**. 
* Each active fire location represents the centroid of a **1km pixel** that is flagged by the algorithm as containing one or more fires within the pixel.** *
""")

@st.experimental_singleton
def load_countries():
    data = pd.read_csv('D:/Mitch/Repos/Streamlit/measuring_carbon/test/Modis_Fires/modis_firms/Countries/countries.csv')
    countries = data['Countries']
    latitude = data['latitude']
    longitude = data['longitude']
    iso_code = data['iso_code']
    return countries, latitude, longitude, iso_code

countries, latitude, longitude, iso_code = load_countries()

def choosing_variables():
    # Region selection
    with st.sidebar:
        st.sidebar.markdown("**First select the region you want to analyze:** 👇")
    
        # Country selection
        countries, latitude, longitude, iso_code = load_countries()
        all_options_country = countries.unique()
        select_country = st.multiselect("Country options (Leave blank to allow all countries)", all_options_country, ['United_States'])

        if len(select_country) > 0:
            temp_select_country = select_country
        else:
            temp_select_country = all_options_country

        # # Satellite selection
        # all_options_satellite = data['satellite'].unique()
        # select_satellite = st.multiselect("satellite options (Leave blank to allow all satellites)", all_options_satellite, ['Terra'])

        # if len(select_satellite) > 0:
        #     temp_select_satellite = select_satellite
        # else:
        #     temp_select_satellite = all_options_satellite

        return temp_select_country#, temp_select_satellite

# # # Hidding the possible options
temp_select_country = choosing_variables()
#, temp_select_satellite

# Sidebar - Year selection

initial_year  = st.sidebar.selectbox('Initial Year', list(reversed(range(2014,2022))))
end_year  = st.sidebar.selectbox('End Year', list(reversed(range(2014,2022))))

country = temp_select_country[0]
# st.write(country)

def load_data():
    data = pd.read_csv(r'D:/Mitch/Repos/Streamlit/measuring_carbon/test/Modis_Fires/modis_firms/' + country  +'/' + country + '.csv',
    # names = ['latitude', 'longitude', 'frp'],
    # skiprows=1,  # don't read header since names specified directly
    # usecols=[0, 1, 12],
    parse_dates = ['acq_date_time'],
    )
    return data

# # # STREAMLIT APP LAYOUT
data = load_data()

# st.write('Data', data)

@st.cache
def filterdata(data, initial_year = initial_year, end_year = end_year):
    # Passing the new Dataframe and filtering the years by selection:
    df_first = data[data['acq_date_time'].dt.year >= initial_year]
    df_second = df_first[df_first['acq_date_time'].dt.year <= end_year]
    return df_second

filterdata = filterdata(data)
# st.write('Filtered Data', filterdata)

# Defining the Latitude and Longitude to centre the map in the country

Countries = pd.read_csv('D:/Mitch/Repos/Streamlit/measuring_carbon/test/Modis_Fires/modis_firms/Countries/countries.csv')
# st.write(Countries)
lat0=Countries[Countries['Countries'] == country].iloc[0]['latitude']
lon0=Countries[Countries['Countries'] == country].iloc[0]['longitude']

## Sidebar - Zoom pixels to display
zoom = st.sidebar.slider('Zoom_scale', 1, 7, 3)

# Set the viewport location
view_state = pdk.ViewState(latitude=lat0, longitude=lon0, zoom=zoom, bearing=0, pitch=45)


# Define a layer to display on a map
layer = pdk.Layer(
    "ColumnLayer",
    data = filterdata[['longitude', 'latitude', 'frp', 'satellite']],
    get_position='[longitude, latitude]',
    elevation_scale=50,
    pickable=True,
    elevation_range=[50, 500],
    get_fill_color=[180, 0, 200, 140],
    extruded=True,
    radius=25,
    coverage=50,
    auto_highlight=True,
)

# Generating tooltip for each generated point in the map with the related satellite
tooltip = {
    "html": "satellite: <b>{satellite}</b>",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}

# Rendering the map 
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/dark-v10',
    tooltip=tooltip
))

# Download co-ordinates xco2 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
@st.experimental_memo
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="active_fires.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(filterdata), unsafe_allow_html=True)

# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.experimental_memo
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

# DISPLAY METHODS
st.subheader(f" {country} facts")
col1, col2 = st.columns(2)


def display_satellite_filter(df):
    satellite_list = [''] + list(['Terra', 'Aqua'])
    satellite = st.sidebar.radio('Satellite', satellite_list)
    return satellite

metric_title = f"{country} 's Mean Fire Radiative Power (FRP in MW)"

def display_fire_data(df, metric_title):
    mean = df['frp'].mean()
    st.metric(metric_title, '{:,}'.format(round(mean, 3)))
    return df

with col1:
    display_fire_data(filterdata, metric_title)