import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/de_db')

# Query the de_data table
df = pd.read_sql_table('de_data', engine)

st.title("Crime Data Dashboard")

# Q1: District with the highest crime frequency
st.header("District with the Highest Crime Frequency")
crime_freq = df.groupby('district_name').size().reset_index(name='Crime Frequency')
crime_freq.rename(columns={'district_name': 'District Name'}, inplace=True)
st.dataframe(crime_freq.sort_values(by='Crime Frequency', ascending=False))

fig1 = px.pie(
    crime_freq,
    names='District Name',
    values='Crime Frequency',
    title='Crime Frequency by District',
    color_discrete_sequence=px.colors.qualitative.Plotly
)
st.plotly_chart(fig1)

# Q2: Day of the week with the highest crime frequency
st.header("Day of the Week with the Highest Crime Frequency")
day_freq = df.groupby('day_of_week').size().reset_index(name='Crime Frequency')
day_freq.rename(columns={'day_of_week': 'Day of Week'}, inplace=True)
st.dataframe(day_freq.sort_values(by='Crime Frequency', ascending=False))

fig2 = px.pie(
    day_freq,
    names='Day of Week',
    values='Crime Frequency',
    title='Crime Frequency by Day of Week',
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig2)

# Q3: District with the highest average distance to police patrol
st.header("District with the Highest Average Distance to Police Patrol (km)")
avg_distance = df.groupby('district_name')['nearest_police_patrol'].mean().reset_index()
avg_distance.rename(columns={'district_name': 'District Name', 'nearest_police_patrol': 'Avg Distance (km)'}, inplace=True)
st.dataframe(avg_distance.sort_values(by='Avg Distance (km)', ascending=False))

fig3 = px.pie(
    avg_distance,
    names='District Name',
    values='Avg Distance (km)',
    title='Average Distance to Police Patrol by District',
    color_discrete_sequence=px.colors.qualitative.Vivid
)
st.plotly_chart(fig3)

