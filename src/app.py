# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
import numpy as np
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
energy['dom']=energy[["Bioenergy","Hydro","Solar","Wind"]].idxmax(axis=1)
energy = energy.fillna(0)
energy['Total'] = energy.Bioenergy+energy.Hydro+energy.Solar+energy.Wind

# get percentage
power = ["Bioenergy","Hydro","Solar","Wind"]
for p in power:
    energy[p+'_per'] = (energy[p]/energy["Total"])*100

energy = np.round(energy, decimals=2)

if st.checkbox("Show Dataframe"):
    # it's a boolean when it's chceked it's True
    st.subheader("This is my dataset:")
    st.dataframe(data=energy)
    # st.table(data=mpg_df)

colors = {"Bioenergy":"brown",
          "Hydro":"blue",
          "Solar":"yellow",
          "Wind":"grey"}
# Widgets: radio buttons
#kanton = left_column.radio(
 #   label='Show Kanton', options=energy.canton)

#en_source = right_column.radio(
 #   label='Show Energy Source', options=['Bioenergy', 'Hydro', 'Solar', 'Wind'])

#https://docs.streamlit.io/library/api-reference/widgets/st.multiselect
# multiselect

all_kan = list(energy.canton)
all_kan.append("All")



kanton = left_column.multiselect(
    label='Show Kanton', options=all_kan)

en_source = right_column.multiselect(
    label='Show Energy Source', options=['Bioenergy', 'Hydro', 'Solar', 'Wind','All'])

if 'All' in en_source:
    en_source=['Bioenergy', 'Hydro', 'Solar', 'Wind']
if "All" in kanton:
    kanton=list(energy.canton)
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
    hist_data.append(
        go.Bar(
            x=energy[energy['canton'].isin(kanton)]['canton'],
            y=energy[energy['canton'].isin(kanton)][en],
            name=en,
            marker_color=colors[en]
        )
    )

fig_en = go.Figure(
    data=hist_data,
    layout={
        'barmode': 'stack'
        # it puts the bars on top of each other

    }
)

fig_en.update_layout(hovermode="x unified")
fig_en.update_layout(
    title={"text": "Electrical Capacity of Selected Energy Sources in Cantons", "font": {"size": 24}},
    xaxis={"title": {"text": "Cantons", "font": {"size": 16}}, "tickangle": 45},
    yaxis={"title": {"text": "Electrical Capacity", "font": {"size": 16}}},
)

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

st.header("Electrical Capacity of Cantons")

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

fig = px.choropleth_mapbox(energy,
                           geojson=geojson,
                           color="dom",
                           #range_color=colors,
                           color_discrete_sequence=colors,
                           locations="canton",
                           mapbox_style="carto-positron",
                           featureidkey='properties.kan_name',
                           center = {"lat": 46.8, "lon": 8.3},
                           zoom=6,
                           opacity=0.7,
                           hover_name="canton",
                           #hover_data=["Bioenergy",
                            #           "Hydro",
                             #          "Solar",
                              #         "Wind"],
                           hover_data={"Bioenergy_per":True,
                                       "Hydro_per":True,
                                       "Solar_per":True,
                                       "Wind_per":True,
                                       "Total":True,
                                       "dom":False,
                                       "canton":False},
                           labels={"dom": "Dominant Energy Source",
                                   "Bioenergy_per":"Bioenergy in %",
                                   "Hydro_per": "Hydro in %",
                                   "Solar_per": "Solar in %",
                                   "Wind_per": "Wind in %"},
                           title="<b>Electrical Capacity of Energy Sources in Cantons</b>"
                           )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

# toto prida plotly chart
st.plotly_chart(fig)

st.header("Total Electrical Capacity of Cantons")

fig2 = px.choropleth_mapbox(energy,
                           geojson=geojson,
                           color="Total",
                           locations="canton",
                           mapbox_style="carto-positron",
                           featureidkey='properties.kan_name',
                           center = {"lat": 46.8, "lon": 8.3},
                           zoom=6,
                           opacity=0.7,
                           hover_name="canton",
                           #hover_data=["Bioenergy",
                            #           "Hydro",
                             #          "Solar",
                              #         "Wind"],
                           hover_data={"Bioenergy":True,
                                       "Hydro":True,
                                       "Solar":True,
                                       "Wind":True,
                                       "Total":True,
                                       "dom":False,
                                       "canton":False},
                           #labels={"dom": "Dominant Energy Source"},
                           title="<b>Total Electrical Capacity of Cantons</b>"
                           )
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig2.show()

# toto prida plotly chart
st.plotly_chart(fig2)
