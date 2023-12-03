import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.header('Car Sales Advertisements')

vehicles = pd.read_csv('vehicles_us.csv')
# Showing quick information about the data
vehicles.info()

# Clean / Fix the data
# Convert 'date_posted' column into datetime type
vehicles['date_posted'] = pd.to_datetime(vehicles['date_posted'], format='%Y-%m-%d')

# Fill in missing values on 'model_year', 'odometer', 'is_4wd', and 'cylinders'
# with 0 and convert them into type int
vehicles['model_year'] = vehicles['model_year'].fillna(0)
if np.array_equal(vehicles['model_year'], vehicles['model_year'].astype('int')):
    vehicles['model_year'] = vehicles['model_year'].astype(int)
vehicles['odometer'] = vehicles['odometer'].fillna(0)
if np.array_equal(vehicles['odometer'], vehicles['odometer'].astype('int')):
    vehicles['odometer'] = vehicles['odometer'].astype(int)
vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0)
if np.array_equal(vehicles['is_4wd'], vehicles['is_4wd'].astype('int')):
    vehicles['is_4wd'] = vehicles['is_4wd'].astype(int)
vehicles['cylinders'] = vehicles['cylinders'].fillna(0)
if np.array_equal(vehicles['cylinders'], vehicles['cylinders'].astype('int')):
    vehicles['cylinders'] = vehicles['cylinders'].astype(int)

# Fill in missing paint_color values with 'unknown'
vehicles['paint_color'] = vehicles['paint_color'].fillna('unknown')

# Split the model column so that the first word becomes the make and the rest
# is the actual model
vehicles[['make', 'model']] = vehicles['model'].str.split(' ', n=1, expand=True)

# Create a DataFrame where model year is known (not filled with 0 from earlier)
vehicles_known_year = vehicles[vehicles['model_year'] != 0]

if st.checkbox('Median Price of Vehicles by Type and Model Year'):
    st.markdown('##### A scatterplot showing the median price of vehicles by type and model year')
    # First, we need to calculate the median price for each type and year
    avg_price_type_year = vehicles_known_year.groupby(['type', 'model_year'])['price'].median().reset_index()

    # Then, we create the scatter plot
    fig = px.scatter(avg_price_type_year, x="model_year", y="price", color="type")
    fig.update_layout(title_text='Median Price by Vehicle Type and Model Year', xaxis_title='Model Year', yaxis_title='Median Price')

    # Plot!
    st.plotly_chart(fig, use_container_width=True)

if st.checkbox('Median Price by Vehicle Make and Model Year'):
    st.markdown('##### A scatterplot showing the median price of vehicles by make and model year')
    # Now calculate the median price for each make and year
    avg_price_make_year = vehicles_known_year.groupby(['make', 'model_year'])['price'].median().reset_index()

    # Create the scatter plot
    fig = px.scatter(avg_price_make_year, x="model_year", y="price", color="make")
    fig.update_layout(title_text='Median Price by Vehicle Make and Model Year', xaxis_title='Model Year', yaxis_title='Median Price')

    # Plot!
    st.plotly_chart(fig, use_container_width=True)

if st.checkbox('Days Vehicle is Listed by Vehicle Make'):
    st.markdown('##### A histogram of days a vehicle is listed based on the car\'s make')

    # Create the histogram
    fig = px.histogram(vehicles, x="days_listed", color="make")
    fig.update_layout(title_text='Days Vehicle is Listed by Vehicle Make', xaxis_title='Days Listed', yaxis_title='Count')

    # Plot!
    st.plotly_chart(fig, use_container_width=True)

if st.checkbox('Vehicle Condition by Model'):
    st.markdown('##### A histogram of vehicle conditions based on the vehicle\'s model')
    fig = px.histogram(vehicles, x="condition", color="model", barmode='group')
    fig.update_layout(title_text='Vehicle Condition by Model', xaxis_title='Condition', yaxis_title='Count')

    # Plot!
    st.plotly_chart(fig, use_container_width=True)