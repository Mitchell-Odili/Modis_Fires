"""An example of showing geographic data."""

import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
from PIL import Image
import datetime

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

#---------------------------------#
# Page layout (continued)
# ## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
# col1 = st.sidebar
# col2, col3 = st.columns((1,1))

@st.experimental_singleton
def load_countries():
    data = pd.read_csv('D:\Mitch\Repos\Streamlit\measuring_carbon\countries.csv')
    return data

countries = load_countries()

@st.experimental_singleton
def load_data():
    data = pd.read_csv('modis_2015_United_States.csv',
    # names = ['latitude', 'longitude', 'frp'],
    # skiprows=1,  # don't read header since names specified directly
    # usecols=[0, 1, 12],
    parse_dates = ['acq_date'],
    )
    return data

# #---------------------------------#
# # Sidebar + Main panel


# # Generating tooltip for each generated point in the map with the related satellite
# tooltip = {
#     "html": "satellite: <b>{satellite}</b>",
#     "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
# }

# # FUNCTION FOR LOCATION MAPS
# def map(data, lat, lon, zoom):
#     st.write(
#         pdk.Deck(
#             map_style="mapbox://styles/mapbox/light-v9",
#             # map_style="mapbox://styles/mapbox/dark-v10",
#             tooltip=tooltip,
#             initial_view_state={
#                 "latitude": lat,
#                 "longitude": lon,
#                 "zoom": zoom,
#                 "pitch": 50,
               
                
#             },
#             layers=[
#                 pdk.Layer(
#                     # "HexagonLayer",
#                     # data=data,
#                     # get_position=["lon", "lat"],
#                     # radius=100,
#                     # elevation_scale=4,
#                     # elevation_range=[0, 1000],
#                     # pickable=True,
#                     # extruded=True,
#                     # layer = pdk.Layer(
#                     "ColumnLayer",
#                     data,
#                     get_position='[lon, lat]',
#                     elevation_scale=50,
#                     pickable=True,
#                     elevation_range=[50, 500],
#                     get_fill_color=[180, 0, 200, 140],
#                     extruded=True,
#                     radius=25,
#                     coverage=50,
#                     auto_highlight=True,
#                 ),
#             ],
#         )
#     )


# # FILTER DATA FOR A SPECIFIC MONTH, CACHE
# @st.experimental_memo
# def filterdata(df, month_selected):
#     return df[df["acq_date"].dt.month_name() == month_selected]

# # CALCULATE MIDPOINT FOR GIVEN SET OF DATA
# @st.experimental_memo
# def mpoint(lat, lon):
#     return (np.average(lat), np.average(lon))

# # FILTER DATA BY MONTH
# @st.experimental_memo
# # def histdata(df, month):
# #     filtered = data[
# #         (df["acq_date"].dt.month_name() >= month) & (df["acq_date"].dt.month_name() < (month + 1))
# #     ]

# def histdata(df, month):
#     filtered = data[
#         (df["acq_date"].dt.month_name() == month)
#     ]

#     hist = np.histogram(filtered["acq_date"].dt.day, bins=31, range=(1, 32))[0]

#     return pd.DataFrame({"days": range(31), "fires": hist})

# # # STREAMLIT APP LAYOUT
data = load_data()

# st.write('Data', data)

# # LAYING OUT THE TOP SECTION OF THE APP
# row1_1, row1_2 = st.columns((2, 3))

# # SEE IF THERE'S A QUERY PARAM IN THE URL (e.g. ?pickup_hour=2)
# # THIS ALLOWS YOU TO PASS A STATEFUL URL TO SOMEONE WITH A SPECIFIC MONTH SELECTED,
# # E.G. https://share.streamlit.io/streamlit/demo-uber-nyc-pickups/main?pickup_hour=2
# if not st.session_state.get("url_synced", False):
#     try:
#         month = int(st.experimental_get_query_params()["month"][0])
#         st.session_state["month"] = month
#         st.session_state["url_synced"] = True
#     except KeyError:
#         pass

# # IF THE SLIDER CHANGES, UPDATE THE QUERY PARAM
# def update_query_params():
#     month_selected = st.session_state["month"]
#     st.experimental_set_query_params(month=month_selected)


# with row1_1:
#     col1.title("1KM MODIS ACTIVE FIRE PRODUCT")
#     # month_selected = st.slider(
#     #     "Select month of interest", 0, 12, key="month", on_change=update_query_params
#     st.sidebar.markdown("**First select the date range you want to analyze:** 👇")
#     month_selected = col1.selectbox(
#         "Choose Month", ('January', 'February', 'March', 'April',
#         'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December') , key="month", on_change=update_query_params
#     )



# #---------------------------------#
# # Sidebar + Main panel

def choosing_variables():
    # Date selection
    with st.sidebar:
        st.sidebar.markdown("**First select the region you want to analyze:** 👇")
        # date = st.date_input("Choose date",datetime.date(2020, 8, 6))
    
        # Country selection
        countries = load_countries()
        all_options_country = countries['Countries'].unique()
        select_country = st.multiselect("Country options (Leave blank to allow all countries)", all_options_country, ['United_States'])

        if len(select_country) > 0:
            temp_select_country = select_country
        else:
            temp_select_country = all_options_country

        # Satellite selection
        all_options_satellite = data['satellite'].unique()
        select_satellite = st.multiselect("satellite options (Leave blank to allow all satellites)", all_options_satellite, ['Terra'])

        if len(select_satellite) > 0:
            temp_select_satellite = select_satellite
        else:
            temp_select_satellite = all_options_satellite

# #     # return date, temp_select_country, temp_select_satellite
        return temp_select_country, temp_select_satellite

# Defining initial date country and satellite variables
# date = datetime.datetime.strptime('19082022', "%d%m%Y").date()
# temp_select_country = ['United_States']
# temp_select_satellite = ['NOAA-20']

# # # Hidding the possible options
# # # date, temp_select_country, temp_select_satellite = choosing_variables()
temp_select_country, temp_select_satellite = choosing_variables()

# Sidebar - Year selection

initial_year  = st.sidebar.selectbox('Initial Year', list(reversed(range(2014,2022))))
end_year  = st.sidebar.selectbox('End Year', list(reversed(range(2014,2022))))
# unique_year = ['2015','2016','2017','2018','2019', '2020', '2021']
# selected_year = st.sidebar.multiselect('Year', unique_year, unique_year)

# # # Querying the df_heatSpots dataframe
# # df_heatSpots = data[(data['acq_date'].dt.date == date) & 
# #                     (countries['Name'].isin(temp_select_country))]
# #                     #  & (df_heatSpots['satelite'].isin(temp_select_satellite))]

# # col1.subheader('Spatial Subsetting of co-ordinates')


# # # ## Sidebar - Spatial Subsetting of co-ordinates
# # minimum_latitude_boundary = col1.number_input('Minimum Latitude boundary', float(-90), float(90), float(8.07))
# # maximum_latitude_boundary = col1.number_input('Maximum Latitude boundary', float(-90), float(90), float(37.1))
# # minimum_longitude_boundary = col1.number_input('Minimum Longitude boundary', float(-180), float(180), float(68.12))
# # maximum_longitude_boundary = col1.number_input('Maximum Longitude boundary', float(-180), float(180), float(97.42))

# # with row1_2:
# st.write(
#         """
#     ### Examining how Fires vary over time in California and at the five counties affected by the August Fire Complex.
#     Use the left drop down menu to view different slices of time and explore different locations.
#     """
#     )

# # LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
# row2_1, row2_2, row2_3, row2_4 = st.columns((2, 1, 1, 1))

# # SETTING THE ZOOM LOCATIONS FOR THE COUNTIES
# Lake_point = [39.1223, -122.6675]
# Mendocino_point = [39.6615, -123.7881]
# Tehama_point = [40.167, -122.4260]

# zoom_level = 12
# midpoint = mpoint(data["latitude"], data["longitude"])

# with row2_1:
#     # st.write(
#     #     f"""**All Doe Fire from {month_selected} and {(month_selected + 1)}**"""
#     # )

#     st.write(
#         f"""**Glenn County (Doe Fire)**"""
#     )
#     map(filterdata(data, month_selected), midpoint[0], midpoint[1], 11)

# with row2_2:
#     st.write("**Lake County**")
#     map(filterdata(data, month_selected), Lake_point[0], Lake_point[1], zoom_level)

# with row2_3:
#     st.write("**Mendocino County**")
#     map(filterdata(data, month_selected), Mendocino_point[0], Mendocino_point[1], zoom_level)

# with row2_4:
#     st.write("**Tehama County**")
#     map(filterdata(data, month_selected), Tehama_point[0], Tehama_point[1], zoom_level)

# # CALCULATING DATA FOR THE HISTOGRAM
# chart_data = histdata(data, month_selected)

# # LAYING OUT THE HISTOGRAM SECTION
# # st.write(
# #     f"""**Breakdown of fires per day between {month_selected} and {(month_selected + 1) }**"""
# # )

# st.write(
#     f"""**Breakdown of fires per day in {month_selected}**"""
# )

# st.altair_chart(
#     alt.Chart(chart_data)
#     .mark_area(
#         interpolate="step-after",
#     )
#     .encode(
#         x=alt.X("days:Q", scale=alt.Scale(nice=False)),
#         y=alt.Y("fires:Q"),
#         tooltip=["days", "fires"],
#     )
#     .configure_mark(opacity=0.2, color="red"),
#     use_container_width=True,
# )

# Defining the Latitude and Longitude to centre the map in the US
lat0=38
lon0=-96.5

# Set the viewport location
view_state = pdk.ViewState(latitude=lat0, longitude=lon0, zoom=3, bearing=0, pitch=45)


# Define a layer to display on a map
layer = pdk.Layer(
    "ColumnLayer",
    data = data[['longitude', 'latitude', 'frp', 'satellite']],
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
