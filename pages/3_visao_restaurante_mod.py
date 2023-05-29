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

st.set_page_config(page_title="Visão Restaurante", page_icon="🍲", layout="wide")
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


def haversine_distance(df1):
    df1['distance'] = df1[['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude',\
                           'Delivery_location_longitude']].\
    apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),\
                              (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

    avg_distance = np.round(df1['distance'].mean(),2)
    return avg_distance

            
            
def avg_std_time_delivery(df1, festival, op):             
    """
        Esta função calcula o tempo médio e o desvio padrão do tempo de entrega

        Imput: 
            -df: Dataframe com os dados necessários para o cálculo
            -festival: 'Yes' ou 'No'
            - op: Tipo de operação que precisa ser calculado
                'avg_time' - Calcula o tempo médio
                'std_time' - Calcula o desvio padrão
    """
    df_aux = df1[['Festival', 'Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)':['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux[df_aux['Festival']==festival][op],2)
    return df_aux         
            
            
            
            
            


df = pd.read_csv('train.csv')
df1 = df.copy()
print(df1.shape)

#limpando os dados
df1 = clean_code(df1)



# ======================================================================
# ======================================================================
# BARRA LATERAL
# ======================================================================
# ======================================================================

st.header('MarketPlace - Visão Restaurantes')
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


tab1, _, _ = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title('Overal Metrics')
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            #st.markdown('##### Coluna 1')
            delivery_unique = len(df1['Delivery_person_ID'].unique())
            col1.metric('Entregadores Unicos: ', delivery_unique)
            
        with col2:
            #st.markdown('##### Coluna 2') 
            avg_distance = haversine_distance(df1)            
            col2.metric('Distancia media: ', avg_distance)
            
        with col3:
            #st.markdown('##### Coluna 3')
            df_aux = avg_std_time_delivery(df1,'Yes', op='avg_time')
            col3.metric('Tempo medio de entrega no Festival', df_aux)
            
        with col4:
            #st.markdown('##### Coluna 4')
            df_aux = avg_std_time_delivery(df1, 'Yes', op='std_time')           
            col4.metric('STD de entrega no Festival', df_aux)            
                        
        with col5:
            df_aux = avg_std_time_delivery(df1,'No', op='avg_time')
            col5.metric('Tempo medio de entrega sem Festival', df_aux)
        with col6:
            df_aux = avg_std_time_delivery(df1, 'No', op='std_time')           
            col6.metric('STD de entrega sem Festival', df_aux)   
            
    with st.container():
        st.markdown('''___''')
        st.title('Tempo medio de entrega por cidade')
        
        
        
    with st.container():
        st.markdown('''___''')
        st.title('Distribuição do tempo')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('###### col1')
        with col2:
            st.markdown('###### col2')
    
    with st.container():
        st.markdown('''___''')
        st.title('Distribuição da distância')
        


