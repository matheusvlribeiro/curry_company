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

st.set_page_config(page_title="Visão Empresa", page_icon="🎲", layout="wide")
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


def order_metric(df1):
    df_aux = df1[['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
    fig = px.bar(df_aux, x = 'Order_Date', y='ID')
    return fig


def traffic_order_share(df1):
    df_aux = df1[['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux['entregas_percent'] = df_aux['ID']/df_aux['ID'].sum()
    fig = px.pie(df_aux, values = 'entregas_percent', names = 'Road_traffic_density')
    return fig
            
def traffic_order_city(df1):
    df_aux = df1[['ID', 'Road_traffic_density', 'City']].groupby(['Road_traffic_density', 'City']).count().reset_index()
    fig = px.scatter(df_aux, x='City', y = 'Road_traffic_density', size = 'ID', color='City') 
    return fig

def order_share_by_week(df1):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    fig = px.line(df_aux, x = 'week_of_year', y = 'ID')
    return fig

def order_share_by_week_2(df1):
    df_aux_1 = df1[['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux_2 = df1[['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
    df_aux = pd.merge(df_aux_1, df_aux_2, how='inner', on='week_of_year')
    df_aux['order_by_deliver'] = df_aux['ID']/df_aux['Delivery_person_ID']

    fig = px.line(df_aux, x='week_of_year', y = 'order_by_deliver')
    return fig


def country_maps(df1):
        df_aux = df1[['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude' ]].groupby(['City', 'Road_traffic_density']).median().reset_index()
        map = folium.Map()
    
        for index, location_info in df_aux.iterrows():
            folium.Marker([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']], \
                          popup=location_info[['City', 'Road_traffic_density']]).add_to(map)

        folium_static(map, width = 1024, height=600)
# ================================= INICIO DA ESTRUTURA LOGICA DO CODIGO ===================================


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

st.header('MarketPlace - Visão Cliente')
image = Image.open('logo.png')

st.sidebar.image(image, width = 200)




st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('''---''')

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?', 
    value = pd.Timestamp(2022, 4, 13).to_pydatetime(), 
    min_value = pd.Timestamp(2022,2, 11).to_pydatetime(), 
    max_value = pd.Timestamp(2022, 4, 6).to_pydatetime(), 
    format = 'DD-MM-YYYY')

st.header(date_slider)
st.sidebar.markdown('''---''')


traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito', 
    ['Low', 'Medium', 'High', 'Jam'], 
    default = 'Low')


st.sidebar.markdown('''---''')
st.sidebar.markdown('### Powered by Comunidade DS')

#filtro 
df1 = df1[df1['Order_Date']<date_slider]
df1 = df1[df1['Road_traffic_density'].isin(traffic_options)]





# ==============================================================
# ==============================================================
#LAYOUT NO STREAMLIT
# ==============================================================
# ==============================================================



tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])


with tab1:
    with st.container():
        #1-Quantidade de pedidos por dia
        st.markdown('# Orders by Day')        
        fig = order_metric(df1)
        st.plotly_chart(fig, use_container_width = True)

    with st.container():
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('# Traffic Order Share ')
            #2 - QUantidade de pedidos por tipo de trafego
            fig = traffic_order_share(df1)                
            st.plotly_chart(fig, use_container_width = True)

        with col2:
            st.markdown('# Traffic Order City')
            #3 - Comparação de volumes de pedido por cidade e tipo de trafego
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width = True)
    
with tab2:
    with st.container():
        # 1-  Quanridade de pedidos por semana
        st.markdown('# Order by Week')
        fig = order_share_by_week(df1)        
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        #2 - A quantidade de pedidos por entregador por semana
        st.markdown('# Order Share by Week')
        fig = order_share_by_week_2(df1) 
        st.plotly_chart(fig, use_container_width=True)
        
            
        
        
        

with tab3:
    st.header('Country Maps')
    country_maps(df1)
    

























