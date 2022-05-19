import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

#### PAGE SETTINGS ####
st.set_page_config(
     page_title="Property Dashboard",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
     }
 )


#### PANDAS IMPORT CSV ####
df = pd.read_csv('property_sales_data.csv')

#### DATA FOR MAPS ####
data = pd.DataFrame({
    'awesome cities' : list(df['Sales Area']),
    'lat' : list(df['Y']),
    'lon' : list(df['X'])
})


#### LEDFT SIDE BAR WIDGETS ####
image = Image.open('logosummetrics.jpg')

with st.sidebar:

    st.title('PROPERTY DASHBOARD')

    option = st.selectbox(
        'Select a branch:',
        ([x for x in df['Sales Area'].unique()]))

    data_filter = df.loc[df["Sales Area"] == option]
        
    data_two = pd.DataFrame({
                'awesome cities' : list(data_filter['Sales Area']),
                'lat' : list(data_filter['Y']),
                'lon' : list(data_filter['X'])
                })
    with st.container():
        st.image(image, caption='Dashboard created by Summetrics')
    

#### COLUMNS TOP DATA ####
t_2021 = data_filter['T 2021'].mean()
t_2020 = data_filter['T 2020'].mean()
t_2019 = data_filter['T 2019'].mean()
t_2018 = data_filter['T 2018'].mean()

sales_growth = [t_2018, t_2019, t_2020, t_2021]

x = ['2018', '2019', '2020', '2021']

c_2021 = data_filter['C 2021'].sum()
c_2020 = data_filter['C 2020'].sum()
c_2019 = data_filter['C 2019'].sum()
c_2018 = data_filter['C 2018'].sum()

#### COLUMNS TOP LAYOUT ####
col1, col2 = st.columns((2,1))

with col1:
    st.map(data_two)

with col2:
    st.write('Avg Sales Price', option)
    with st.container():
        source = pd.DataFrame({
                'Price (R)': [t_2018, t_2019, t_2020, t_2021],
                'Year': ['2018', '2019', '2020', '2021']
            })
        
        bar_chart = alt.Chart(source).mark_line(color="#FFAA00").encode(
                y='Price (R):Q',
                x='Year:O'
        ).properties(
                    height=180
        )
    
        st.altair_chart(bar_chart, use_container_width=True)

    st.write('Total Commision', option)
    with st.container():
        sourceb = pd.DataFrame({
                'Commission (R)': [c_2018, c_2019, c_2020, c_2021],
                'Year': ['2018', '2019', '2020', '2021']
            })
        
        bar_chartb = alt.Chart(sourceb).mark_bar(color="#FFAA00").encode(
                y='Commission (R):Q',
                x='Year:O'
        ).properties(
                    height=180
        )
    
        st.altair_chart(bar_chartb, use_container_width=True)


#### COLUMNS BOTTOM ###
met_avgsalesp = round(data_filter['Sales Price'].mean(),0)
units = len(data_filter.index)
commision = round((data_filter['Sales Price'].sum() * 0.07),0) 

growth_avgsalesp = round(((met_avgsalesp / data_filter['T 2020'].mean()) - 1) * 100, 0)
growth_commision = round(((commision / ((data_filter['T 2020'].sum()) * 0.065)) - 1) * 100, 0)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Units Sold", units)    

with col2:
    st.metric("Avg Sales Price", 'R ' + str(met_avgsalesp), str(growth_avgsalesp) + '%')

with col3:
    st.metric("Total Commision", 'R ' + str(commision), str(growth_commision) + '%')





