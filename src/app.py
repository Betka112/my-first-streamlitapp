# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
import plotly.io as pio


# First some MPG Data Exploration
@st.cache
# decorator = what does it do?
def load_data(path):
    df = pd.read_csv(path)
    return df
# df is accesible in cache

#dictionary for kantons
cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais',
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich',
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève',
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz',
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}

df_raw = load_data(path="./data/renewable_power_plants_CH.csv")
# raw stays untouched
df = deepcopy(df_raw.replace({"canton": cantons_dict}))
# cache looks for changes

# Add title and header
st.title("Clean Energy Sources in Switzerland")
st.header("Types of Energy Sources in Swiss Kantons")

# it's possible to create a sidebar

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)

# you could store the info about the box in a variable
# and this creates the inter activity
if st.checkbox("Show Dataframe"):
    # it's a boolean when it's chceked it's True
    st.subheader("This is my dataset:")
    st.dataframe(data=df)
    # st.table(data=mpg_df)

# Setting up columns
left_column, right_column = st.columns(2)
# len dva stlpce


#left_column, middle_column, right_column = st.columns([3, 1, 1])
# vektor mi hovori ze ten lavy ma mat sirku 3 a tie zvysne dva iba 1

# Widgets: selectbox
#years = ["All"]+sorted(pd.unique(mpg_df['year']))
#year = left_column.selectbox("Choose a Year", years)
# vyraba vyrolovacie okno

# creating pivot table for the data
energy = pd.pivot_table(df, values='electrical_capacity', index=["canton"],columns=["energy_source_level_2"]).reset_index().copy(deep=True)
energy.head()

# Widgets: radio buttons
#kanton = left_column.radio(
 #   label='Show Kanton', options=energy.canton)

#en_source = right_column.radio(
 #   label='Show Energy Source', options=['Bioenergy', 'Hydro', 'Solar', 'Wind'])

#https://docs.streamlit.io/library/api-reference/widgets/st.multiselect
# multiselect
kanton = left_column.multiselect(
    label='Show Kanton', options=list(energy.canton))

en_source = right_column.multiselect(
    label='Show Energy Source', options=['Bioenergy', 'Hydro', 'Solar', 'Wind'])

# tu si vyberiem, ktory typ grafu chcem mat
#plot_types = ["Matplotlib", "Plotly"]
#plot_type = right_column.radio("Choose Plot Type", plot_types)

# Flow control and plotting
#if year == "All":
 #   reduced_df = mpg_df
#else:
 #   reduced_df = mpg_df[mpg_df["year"] == year]

#means = reduced_df.groupby('class').mean()

# In Matplotlib
#m_fig, ax = plt.subplots(figsize=(10, 8))
#ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)

#if show_means == "Yes":
 #   ax.scatter(means['displ'], means['hwy'], alpha=0.7, color="red")

#ax.set_title("Engine Size vs. Highway Fuel Mileage")
#ax.set_xlabel('Displacement (Liters)')
#ax.set_ylabel('MPG')

# In Plotly
#p_fig = px.scatter(reduced_df, x='displ', y='hwy', opacity=0.5,
 #                  range_x=[1, 8], range_y=[10, 50],
  #                 width=750, height=600,
   #                labels={"displ": "Displacement (Liters)",
    #                       "hwy": "MPG"},
     #              title="Engine Size vs. Highway Fuel Mileage")
#p_fig.update_layout(title_font_size=22)

#if show_means == "Yes":
 #   p_fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'],
  #                             mode="markers"))
   # p_fig.update_layout(showlegend=False)

hist_data = []

for en in en_source:
    hist_data.append(go.Bar(x=energy[energy['canton'].isin(kanton)]['canton'], y=energy[energy['canton'].isin(kanton)][en], name=en))

fig_en = go.Figure(
    data=hist_data,
    layout={
        'barmode': 'stack'
        # it puts the bars on top of each other

    }
)

fig_en.update_layout(hovermode="x unified")

# maybe if it's empty show all?

#fig_en = go.Figure(
 #   data=[
  #      go.Bar(x=energy['canton'], y=energy['Bioenergy'], name="Bioenergy"),
   #     go.Bar(x=energy['canton'], y=energy['Hydro'], name="Hydro"),
    #    go.Bar(x=energy['canton'], y=energy['Solar'], name="Solar"),
     #   go.Bar(x=energy['canton'], y=energy['Wind'], name="Wind")
   # ],
    #layout={
     #   'barmode': 'stack'
      #  # it puts the bars on top of each other

    #}
#)

#fig_en.update_layout(hovermode="x unified")


fig_en.show()


# Select which plot to show
#if plot_type == "Matplotlib":
 #   st.pyplot(m_fig)
#else:
#
# plot the graph in streamline
st.plotly_chart(fig_en)

# We can write stuff
url = "https://open-power-system-data.org/"
st.write("Data Source:", url)
# "This works too:", url

# Another header

st.header("Maps")

# Sample Streamlit Map


#st.subheader("Streamlit Map")

# automaticky rozlisuje ci je v mape langitude a lattude
# datasets are already included in plotly, and other libraries

#ds_geo = px.data.carshare()
#ds_geo['lat'] = ds_geo['centroid_lat']
#ds_geo['lon'] = ds_geo['centroid_lon']
#st.map(ds_geo)

# Sample Choropleth mapbox using Plotly GO

#st.subheader("Plotly Map")

#with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
 #   counties = json.load(response)
#df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
 #                dtype={"fips": str})

with open('./data/georef-switzerland-kanton.geojson') as f:
    geojson = json.load(f)

#plotly_map = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df.fips, z=df.unemp,
 #                                   colorscale="Viridis", zmin=0, zmax=12,
  #                                  marker_opacity=0.5, marker_line_width=0))
#plotly_map.update_layout(mapbox_style="carto-positron",
 #                 mapbox_zoom=3, mapbox_center={"lat": 37.0902, "lon": -95.7129},
  #                margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig = px.choropleth_mapbox(df, geojson=geojson, color="energy_source_level_2",
                    locations="canton", mapbox_style="carto-positron", featureidkey='properties.kan_name', center = {"lat": 46.8, "lon": 8.3})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

# toto prida plotly chart
st.plotly_chart(fig)
