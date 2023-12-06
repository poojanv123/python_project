import streamlit as st
import pandas as pd
import geopy
import geopy.distance
import networkx as nx
import numpy as np
import networkx.algorithms.approximation as nx_app
import folium
from streamlit_folium import folium_static
import base64
from streamlit_js_eval import streamlit_js_eval

#Get data for tourist cities with their geo location
tourist_cities = pd.read_excel('tourist_cities_latlong.xlsx',sheet_name="Sheet1")

#Add sidebar
st.sidebar.title("")
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://a.cdn-hotels.com/gdcs/production107/d507/f99efdcd-6fcc-4a97-a00c-cb6a491554b7.jpg?impolicy=fcrop&w=1600&h=1066&q=medium")
    }
   .sidebar .sidebar-content {
        background: url("https://cdn.britannica.com/54/75854-050-E27E66C0/Eiffel-Tower-Paris.jpg?w=300")
    }
    </style>
    """,
    unsafe_allow_html=True
)
def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
side_bg = 'paris.png'
sidebar_bg(side_bg)

#Initialize variables
city=[]
city_days=[]
day=[]
duration=0
if 'page' not in st.session_state: st.session_state.page = 0
def nextPage():  st.session_state.page += 1
def firstPage():  st.session_state.page =0

#Select country and duration
if st.session_state.page ==0:
    st.subheader("Which country would like to visit?",divider="grey")
    selected_country= st.selectbox('Select Country', list(tourist_cities['Country'].unique()),key="selected_country")
    duration = st.number_input("Enter the duration of the trip in days:",min_value=1,max_value=100,key="duration")
    st.toggle("Next Page",key=0,on_change=nextPage)
if "selected_country" in st.session_state: selected_country = st.session_state.selected_country
if "duration" in st.session_state: duration = st.session_state.duration

#Select start city and duration of stay
if st.session_state.page == 1:
    st.subheader("Yay!! You are going to "+str(selected_country)+" for "+str(duration)+" days. Now let's plan your itinerary.",divider="grey")
    st.selectbox('Select Start City',[''] + list(tourist_cities.loc[tourist_cities['Country']==selected_country,'City']),key="mybox")
    st.number_input("Enter number of days you wish to spend in the start city:",min_value=1,max_value=duration+1, key="myslider")
    st.toggle("Next Page",key=1,on_change=nextPage,value=False)

if hasattr(st.session_state,"mybox"):
    city.append(st.session_state["mybox"])
    city_days.append(st.session_state["myslider"])
    day.append(1)

i=0

#Select all the cities you would like to visit
while duration > sum(city_days):
    key1 = "city"+str(i)
    key2 = "city_days"+str(i)
    if st.session_state.page == len(city_days)+1:
        st.subheader("Where would you like to go next?",divider="grey")
        #Calculate distances of cities from previously selected city
        city_dist = {c:round(geopy.distance.geodesic((float(tourist_cities.loc[tourist_cities['City'] == city[i],'Latitude']), float(tourist_cities.loc[tourist_cities['City'] == city[i],'Longitude'])),
                                    (float(tourist_cities.loc[tourist_cities['City'] == c,'Latitude']), float(tourist_cities.loc[tourist_cities['City'] == c,'Longitude']))).km,2)
                                    for c in tourist_cities.loc[(tourist_cities['Country'] == selected_country) & (tourist_cities['City'].isin(city) == False),'City']}
        city_options = dict(sorted(city_dist.items(), key=lambda x:x[1])[1:6])
        col01, c,col02= st.columns((3,1,3))
        st.subheader("Nearest cities from "+ city[i] + " with distances in kilometers:",divider="grey")
        col1, col2, col3,col4 = st.columns((3,2,1,3))
        with col1:
            st.write("["+list(city_options.keys())[0]+"]"+"(https://www.google.com/search?q="+str(list(city_options.keys())[0]).replace(" ","+")+"+places+to+visit"+")")
            st.caption(str(list(city_options.values())[0])+"km")
            st.write("["+list(city_options.keys())[1]+"]"+"(https://www.google.com/search?q="+str(list(city_options.keys())[1]).replace(" ","+")+"+places+to+visit"+")")
            st.caption(str(list(city_options.values())[1])+"km")
            st.write("["+list(city_options.keys())[2]+"]"+"(https://www.google.com/search?q="+str(list(city_options.keys())[2]).replace(" ","+")+"+places+to+visit"+")")
            st.caption(str(list(city_options.values())[2])+"km")
        with col2:    
            st.write("["+list(city_options.keys())[3]+"]"+"(https://www.google.com/search?q="+str(list(city_options.keys())[3]).replace(" ","+")+"+places+to+visit"+")")
            st.caption(str(list(city_options.values())[3])+"km")
            st.write("["+list(city_options.keys())[4]+"]"+"(https://www.google.com/search?q="+str(list(city_options.keys())[4]).replace(" ","+")+"+places+to+visit"+")")
            st.caption(str(list(city_options.values())[4])+"km")
        with col3:
            selected_cities = tourist_cities[tourist_cities['City'].isin(list(city_options.keys())+list(city[i]))]
            folium_coordinates = []
            for x,y in zip(selected_cities['Latitude'], selected_cities['Longitude']):
                folium_coordinates.append([x,y])
        
            m = folium.Map(location = [selected_cities['Latitude'].iloc[0], selected_cities['Longitude'].iloc[0]],   
                    tiles = "OpenStreetMap", 
                    zoom_start= 6.5
                    )
  
            for coordinate, capital in zip(folium_coordinates, selected_cities['City']):
                folium.Marker(location = coordinate,
                    popup = folium.map.Popup(capital,parse_html = True)).add_to(m)
            st_data= folium_static(m, width=300,height=300)
        with col01:
            st.selectbox('Choose a City', [""]+list(dict(city_options).keys()), key=key1)
            st.number_input('Enter the number of days you want to spend in this city:',min_value=1,max_value=duration-sum(city_days),key=key2)        
            st.toggle("Next Page",key=i+2,on_change=nextPage,value=False)
        with c:
            st.text("")
        with col02:   
            #Display itinerary in a table
            st.subheader("      Your Itinerary")
            df = pd.DataFrame({"City Name":city ,"Day of visit":day ,"Duration of Stay":city_days})
            st.dataframe(df.style.background_gradient(cmap='tab20c',gmap=df['Day of visit']),hide_index=True)
            st.caption("Remaining Days: "+str(duration-sum(city_days)))

    if hasattr(st.session_state,key1):
        city.append(st.session_state[key1])
        city_days.append(st.session_state[key2])
        day.append(sum(city_days[:-1])+1)
    i+=1

#Get optimized itinerary
if duration == sum(city_days ) > 0:
    travel_data = tourist_cities[tourist_cities['City'].isin(city)]
    travel_data.reset_index(inplace=True, drop=True)
    G = nx.Graph()
    nodes = np.arange(0,len(travel_data['City']))
    G.add_nodes_from(nodes)
    coordinates = [(row['Latitude'], row['Longitude']) for i,row in travel_data.iterrows()]
    for i in nodes:
        for j in nodes:
            if i!=j:
                G.add_edge(i, j, weight = geopy.distance.geodesic((travel_data['Latitude'][i], travel_data['Longitude'][i]),
                                        (travel_data['Latitude'][j], travel_data['Longitude'][j])).km)
    cycle = nx_app.christofides(G, weight="weight")
    output_data = pd.DataFrame({"City Name":city ,"Day of visit":[0]*len(city),"Duration of Stay":city_days})

    for i in range(0,len(output_data)):
        if i==0:
            output_data['Day of visit'][i]=1
        else:
            output_data["Day of visit"][i] = sum(output_data["Duration of Stay"][:i])+1
    output_data['cycle'] = cycle[:-1]
    output_data.set_index('cycle',inplace=True)
    output_data.sort_index(ascending=True,inplace=True) 
    st.header("Final Optimized Itinerary",divider="grey")
    st.caption("For your "+ str(duration)+" days trip to "+selected_country)
    total_dist = 0
    for i in range(0,len(cycle)-2):
        total_dist = total_dist + geopy.distance.geodesic((travel_data['Latitude'][i], travel_data['Longitude'][i]),
                                        (travel_data['Latitude'][i+1], travel_data['Longitude'][i+1])).km
    h1,h2 = st.columns(2)
    with h1:
        st.dataframe(output_data.style.background_gradient(cmap='Blues', vmin=0, vmax=10,gmap=output_data['Day of visit']),hide_index=True)
        st.caption("Total Distance Travelled: "+ str(round(total_dist,0))+ "km")
    folium_coordinates = []
    for x,y in zip(travel_data['Latitude'], travel_data['Longitude']):
        folium_coordinates.append([x,y])
    route = []
    for stop in cycle:
        route.append(folium_coordinates[stop])
        
    m1 = folium.Map(location = [travel_data['Latitude'][0], travel_data['Longitude'][0]],   
                    tiles = "OpenStreetMap", 
                    zoom_start= 6.5
                    )
  
    for coordinate, capital in zip(folium_coordinates, travel_data['City']):
        folium.Marker(location = coordinate,
                    popup = folium.map.Popup(capital,parse_html = True)).add_to(m1)
    #Display map
    folium.PolyLine(route).add_to(m1)
    with h2:
        st_data= folium_static(m1, width=300,height=300)
    st.selectbox("Plan Another trip?", ["","Yes"],on_change=firstPage())


