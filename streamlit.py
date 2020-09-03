import pyTigerGraph as tg
import streamlit as st
import pandas as pd
import flat_table
import altair as alt
import plotly.figure_factory as ff
from bokeh.plotting import figure
import plotly.express as px
import plotly.graph_objects as go
import argparse
import json


st.title('Dynamically Visualize South Korea COVID-19 data using TigerGraph and Streamlit')

min_age, max_age = st.sidebar.slider("Select Age Range", 0, 104, [10, 20])
sex = st.sidebar.multiselect('Sex', ['male', 'female'])



with open ('streamlit.txt', 'r') as file:
    x = file.read().split(' ')
print(x)

host = x[0]
username = x[1]
password = x[2]
graphname = x[3]
cert = False
if x[4] == 'True':
    cert = True


graph = tg.TigerGraphConnection(host=host, username=username, graphname=graphname, password=password, useCert=cert)
API_Secret = graph.createSecret()
API_Token = graph.getToken(API_Secret, setToken=True, lifetime=None)[0]

results = graph.runInstalledQuery("streamlit")

df = pd.DataFrame(results[0]["s2"])

data = flat_table.normalize(df) 
data = data[['v_id', 'attributes.Age', 'attributes.Sex', 'attributes.Location.latitude', 'attributes.Location.longitude']] 

# Filtering the data based on the sex filter input
if(len(sex)==1): 
    data = data[data['attributes.Sex']==sex[0]] 

data = data[data['attributes.Age'].between(left=min_age, right=max_age)] 

gender = data['attributes.Sex']
age = data['attributes.Age']

g = gender.value_counts()

graphgender = pd.DataFrame({'Sex':g.index, 'Count':g.values})

st.write('Bar chart of Male and Females')
st.bar_chart(gender)

# grabbing location data for map 
locations = data[['attributes.Location.latitude', 'attributes.Location.longitude']] 
locations = locations.rename({'attributes.Location.latitude': 'lat', 'attributes.Location.longitude': 'lon'}, axis=1)

# Using the streamlit map widget with locations input
st.map(locations) 

s = age.value_counts()
age = pd.DataFrame({'Age':s.index, 'Count':s.values})

st.write('Bar Chart Age Distribution')
fig = px.bar(age, x="Age", y="Count")
st.plotly_chart(fig)



st.write('Scatter Plot of Age')
fig = px.scatter(age, x="Age", y="Count")
st.plotly_chart(fig)

# Table of data Counts by Age
st.write(age)

# Table of data
st.write(data)
