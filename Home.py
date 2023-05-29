import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home", 
    page_icon = "🎶", 
    layout = "wide"
)

#image_path = '/home/matheus/repos/ftc_python/ciclo_07/logo.png'
image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width = 120)


# =======================================
# Barra Lateral
# =======================================

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Comoo utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento
        - Visão Tática: Indicadores semanais de crescimento
        - Visão Geográfica: Insights de geolocalização
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante: 
        - Indicadores semanais de crescimeto
    """)