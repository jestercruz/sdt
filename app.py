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

# Create a list of unique vehicle types
vehicle_types = vehicles_known_year['type'].unique()

st.markdown('##### A scatterplot showing the median price of vehicles by type and model year')
# Create two selectboxes for the vehicle types
# Create two selectboxes for the vehicle types
vehicle_type1 = st.selectbox('Select first vehicle type', vehicle_types)
vehicle_type2 = st.selectbox('Select second vehicle type', vehicle_types)

# Create a button for resetting the selection
if st.button('Show All'):
    vehicle_type1 = None
    vehicle_type2 = None

# Filter the data to include only the selected vehicle types
if vehicle_type1 and vehicle_type2:
    filtered_vehicles = vehicles_known_year[vehicles_known_year['type'].isin([vehicle_type1, vehicle_type2])]
else:
    filtered_vehicles = vehicles_known_year
# Calculate the median price for each type and year
avg_price = filtered_vehicles.groupby(['type', 'model_year'])['price'].median().reset_index()

# Create the scatter plot
fig = px.scatter(avg_price, x="model_year", y="price", color="type")
fig.update_layout(title_text='Median Price by Vehicle Type and Model Year', xaxis_title='Model Year', yaxis_title='Average Price')
st.plotly_chart(fig)
st.markdown('The median price of vehicles has increased over time since about 2000. As a vehicle gets older than 2000, the price also generally increased. Additionally, it appears that SUVs, pickup, trucks, and off-roads have the highest median prices, while sedans, hatchbacks, and vans have the lowest median prices.')


st.markdown('##### A scatterplot showing the median price of vehicles by make and model year')
# Now calculate the median price for each make and year
avg_price_make_year = vehicles_known_year.groupby(['make', 'model_year'])['price'].median().reset_index()

# Create the scatter plot
fig = px.scatter(avg_price_make_year, x="model_year", y="price", color="make")
fig.update_layout(title_text='Median Price by Vehicle Make and Model Year', xaxis_title='Model Year', yaxis_title='Median Price')

# Plot!
st.plotly_chart(fig, use_container_width=True)
st.markdown('The median price of vehicles generally increases with the model year since around 2000. Luxury brands such as mercedes-benz and cadillac tend to have higher median prices than others, which indicates that the make of the vehicle has significant influcence on its price.')


st.markdown('##### A histogram of days a vehicle is listed based on the car\'s make')

# Create the histogram
fig = px.histogram(vehicles, x="days_listed", color="make")
fig.update_layout(title_text='Days Vehicle is Listed by Vehicle Make', xaxis_title='Days Listed', yaxis_title='Number of Days Listed')

# Plot!
st.plotly_chart(fig, use_container_width=True)
st.markdown('From this plot, it appears that the number of vehicles listed decreases as the number of days the vehicle is listed increases. This suggests that most vehicles are sold or removed from the listing within a short period of time. Most listings being there between 10 and 35 days.')

make = st.checkbox('Show by Make')
if make:
    show = 'make'
    st.markdown('##### A histogram of vehicle conditions based on the vehicle\'s make')
    fig = px.histogram(vehicles, x="condition", color=show, barmode='group')
    fig.update_layout(title_text='Vehicle Condition by Make', xaxis_title='Condition', yaxis_title='Number of Vehicles')
else:
    show = 'model'
    st.markdown('##### A histogram of vehicle conditions based on the vehicle\'s model')
    fig = px.histogram(vehicles, x="condition", color=show, barmode='group')
    fig.update_layout(title_text='Vehicle Condition by Model', xaxis_title='Condition', yaxis_title='Number of Vehicles')

# Plot!
st.plotly_chart(fig, use_container_width=True)
st.markdown('Most people would consider the vehicle that they list as good or excellent condition. The highest number of listings seems to be for pickup trucks such as the F-150, Silverado 1500 and Ram 1500.')

st.markdown('### Conclusion:')
st.markdown('The median price of vehicles are significantly affected by its model year and make. Luxury vehicles tend to have a higher median price vs non-luxury makes. Vehicles are mostly advertised for a short period of time. Trucks tend to be listed as excellent or good condition.')