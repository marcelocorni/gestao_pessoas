import streamlit as st
import pandas as pd

# Função para carregar e armazenar o CSV no cache
@st.cache_data
def load_data(file):
    df = pd.read_csv(file, delimiter=';')  # Carrega o CSV com delimitador ;
    return df

def main():
    # Configuração da página
    st.set_page_config(page_title='Gestão de Pessoas - CAEd', page_icon=':bar_chart:', layout='wide')
    
    st.title('Carregamento de dados para os Gráficos de Colaboradores')
    st.image('images/logo_caed.png', width=100)
    

    # Requerer o upload de um arquivo CSV
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
    
    if uploaded_file is not None:
        # Carregar o CSV e armazenar no cache
        df = load_data(uploaded_file)

        # Armazenar o DataFrame no session_state para uso em outras páginas
        st.session_state['dataframe'] = df


    if 'dataframe' in st.session_state:
        df = st.session_state['dataframe']
        # Exibir o DataFrame carregado
        st.write("Arquivo CSV carregado com sucesso!")
        st.write(df)

if __name__ == "__main__":
    main()
