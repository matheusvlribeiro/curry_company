#libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np 
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Visão Entregadores", page_icon="🚴🏻‍♂️", layout="wide")
# ======================================================================
# ======================================================================
# FUNÇÕES
# ======================================================================
# ======================================================================

def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o Dataframe
    
    Tipos de limpeza:
    1- Remoção dos dados NaNs
    2 - Mudança do tipo da coluna de dados
    3 - Remoção dos espaços das variáveis de texto
    4 - Formatação da data e limpeza da coluna de tempo
    
    Input: Dataframe
    Output: Dataframe
    
    """
    
    #1 - retirando os 'NaN's
    linhas_selecionadas = (df1['Delivery_person_Age'] !='NaN ')
    df1 = df1[linhas_selecionadas]

    linhas_selecionadas = (df1['Road_traffic_density'] !='NaN ')
    df1 = df1[linhas_selecionadas]

    linhas_selecionadas = (df1['City'] !='NaN ')
    df1 = df1[linhas_selecionadas]

    linhas_selecionadas = (df1['Festival'] !='NaN ')
    df1 = df1[linhas_selecionadas]

    linhas_selecionadas = (df1['multiple_deliveries'] !='NaN ')
    df1 = df1[linhas_selecionadas]

    #2 - convertendo as colunas de texto para numeros

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    df1['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')

    #3 - Removendo os espaços dentro de strings/textos/objects

    df1['ID'] = df1['ID'].str.strip()
    df1['Road_traffic_density'] = df1['Road_traffic_density'].str.strip()
    df1['Type_of_order'] = df1['Type_of_order'].str.strip()
    df1['Type_of_vehicle'] = df1['Type_of_vehicle'].str.strip()
    df1['City'] = df1['City'].str.strip()
    df1['Festival'] = df1['Festival'].str.strip()


    #4 - Limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1

def top_delivers(df1, top_asc):
    df2 = df1[['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID'])\
    .mean().sort_values(['City', 'Time_taken(min)'], ascending=top_asc).reset_index()

    df_aux01 = df2[df2['City']=='Metropolitian'].head(10)
    df_aux02 = df2[df2['City']=='Urban'].head(10)
    df_aux03 = df2[df2['City']=='Semi-Urban'].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return df3











df = pd.read_csv('dataset/train.csv')
df1 = df.copy()
print(df1.shape)

#limpando os dados
df1 = clean_code(df1)


# ======================================================================
# ======================================================================
# BARRA LATERAL
# ======================================================================
# ======================================================================

st.header('MarketPlace - Visão Entregadores')
image = Image.open('logo.png')

st.sidebar.image(image, width = 200)




st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('''---''')

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?', 
    value = pd.datetime(2022, 4, 13), 
    min_value = pd.datetime(2022,2, 11), 
    max_value = pd.datetime(2022, 4, 6), 
    format = 'DD-MM-YYYY')

st.header(date_slider)
st.sidebar.markdown('''---''')


traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito', 
    ['Low', 'Medium', 'High', 'Jam'], 
    default = 'Low')

weather_options = st.sidebar.multiselect(
    'Quais as condições do clima', 
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'], 
    default = 'conditions Fog')


st.sidebar.markdown('''---''')
st.sidebar.markdown('### Powered by Comunidade DS')

#filtro 
df1 = df1[df1['Order_Date']<date_slider]
df1 = df1[df1['Road_traffic_density'].isin(traffic_options)]
df1 = df1[df1['Weatherconditions'].isin(weather_options)]




# ==============================================================
# ==============================================================
#LAYOUT NO STREAMLIT
# ==============================================================
# ==============================================================




tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap = 'large')
        with col1:            
            maior_idade = df1['Delivery_person_Age'].max()
            col1.metric('Maior de idade:', maior_idade)
        with col2:
            menor_idade = df1['Delivery_person_Age'].min()
            col2.metric('Menor de idade:', menor_idade)
        with col3:
            melhor_cond = df1['Vehicle_condition'].max()
            col3.metric('Melhor condição: ', melhor_cond)            
        with col4:
            pior_cond = df1['Vehicle_condition'].min()
            col4.metric('Pior condição: ', pior_cond)
            
            
            
    with st.container():
        st.markdown('''___''')
        st.title('Avaliações')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliação média por entregador')
            df_avg_ratings_per_deliver = df1[['Delivery_person_Ratings', 'Delivery_person_ID']]\
              .groupby('Delivery_person_ID').mean().reset_index()           
            st.dataframe(df_avg_ratings_per_deliver)
            
        with col2:
            st.markdown('##### Avaliação média por trânsito')
            df_avg_std_rating_by_traffic = df1[['Delivery_person_Ratings', 'Road_traffic_density']]\
              .groupby('Road_traffic_density').agg({'Delivery_person_Ratings':['mean', 'std']})      
            df_avg_std_rating_by_traffic.columns = ['Delivery_mean', 'Delivery_std']
            st.dataframe(df_avg_std_rating_by_traffic)
            
            
            st.markdown('##### Avaliação média por clima')
            df_avg_std_rating_by_weather = df1[['Delivery_person_Ratings', 'Weatherconditions']]\
              .groupby('Weatherconditions').agg({'Delivery_person_Ratings':['mean', 'std']}) 
            df_avg_std_rating_by_weather.columns = ['Delivery_mean', 'Delivery_std']
            st.dataframe(df_avg_std_rating_by_weather)
            
    
    
    with st.container():
        st.markdown('''___''')
        st.title('Velocidade de Entrega')
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Top entregadores mais rápidos')
            df3 = top_delivers(df1, top_asc= True)
            st.dataframe(df3)
        with col2:           
            
            df3 = top_delivers(df1, top_asc= False)
            st.dataframe(df3)
            
