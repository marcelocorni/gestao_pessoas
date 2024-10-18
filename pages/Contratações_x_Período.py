import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd

# Função principal para criar o gráfico de Gantt
def gantt_page():
    # Configuração da página
    st.set_page_config(page_title='Gestão de Pessoas - CAEd', page_icon=':bar_chart:', layout='wide')
    st.title("Customização de Gráfico de Contratações x Período")            
    st.image('images/logo_caed.png', width=100)
    

    # Dados iniciais
    default_data = [
        {"função": "APD-MOVIMENTADOR", "quantidade": 43, "início": "04/11/2024", "fim": "31/01/2025"},
        {"função": "APD-MOVIMENTADOR", "quantidade": 17, "início": "18/11/2024", "fim": "15/01/2025"},
        {"função": "APD-MOVIMENTADOR", "quantidade": 15, "início": "09/12/2024", "fim": "15/01/2025"},
        {"função": "APD", "quantidade": 15, "início": "04/11/2024", "fim": "31/01/2025"},
        {"função": "APD", "quantidade": 9, "início": "13/11/2024", "fim": "31/01/2025"},
        {"função": "APD", "quantidade": 16, "início": "02/12/2024", "fim": "17/01/2025"},
        {"função": "CONTROLADOR*", "quantidade": 2, "início": "04/11/2024", "fim": "31/01/2025"},
        {"função": "CONTROLADOR*", "quantidade": 5, "início": "11/11/2024", "fim": "31/01/2025"},
        {"função": "CONTROLADOR*", "quantidade": 2, "início": "21/11/2024", "fim": "31/01/2025"},
    ]

    # Carregar os dados padrões no session_state
    if 'dados' not in st.session_state:
        st.session_state.dados = default_data

    # Função para adicionar um novo registro
    def add_record():
        st.session_state.dados.append({
            "função": funcao,
            "quantidade": quantidade,
            "início": data_inicio,
            "fim": data_fim
        })


    with st.expander("Configurações gerais"):            
        # Personalizar o gráfico
        grafico_titulo = st.text_input("Título do gráfico", value="Título do Gráfico", key='titulo_a')
        label_x = st.text_input("Rótulo do eixo X", value="Eixo X", key='label_x_a')
        label_y = st.text_input("Rótulo do eixo Y", value="Eixo Y", key='label_y_a')
        # Checkbox para exibir os valores nas barras
        exibir_valores = st.checkbox("Exibir valores nas barras", value=True, key='exibir_valores_a')

    # Função para remover o último registro
    def remove_last_record():
        if len(st.session_state.dados) > 0:
            st.session_state.dados.pop()

    

    with st.expander("Adicione ou remova funções para o gráfico de Gantt:"):

        # Inputs para adicionar novos dados
        funcao = st.text_input("Função")
        quantidade = st.number_input("Quantidade", min_value=1, value=1)
        data_inicio = st.date_input("Data de Início", min_value=datetime(2024, 1, 1))
        data_fim = st.date_input("Data de Fim", min_value=datetime(2024, 1, 2))

        # Botões para adicionar ou remover
        st.button("Adicionar Registro", on_click=add_record)
        st.button("Remover Último Registro", on_click=remove_last_record)

        if not st.session_state.dados:
            st.warning("Nenhum registro adicionado. Por favor, insira os dados acima.")
            return
        
        # Exibir a tabela atual de registros
        st.write("Tabela Atual:")
        df = pd.DataFrame(st.session_state.dados)
        st.write(df)


    

        

    # Converter as datas de início e fim
    for item in st.session_state.dados:
        item["início"] = datetime.strptime(item["início"], "%d/%m/%Y") if isinstance(item["início"], str) else item["início"]
        item["fim"] = datetime.strptime(item["fim"], "%d/%m/%Y") if isinstance(item["fim"], str) else item["fim"]

    # Configurações para o gráfico de Gantt
    fig, ax = plt.subplots(figsize=(12, 6))

    # Cores para as barras
    cores = ['#004c6d', '#007ba2', '#00a1d5', '#f28f3b', '#f1c453', '#8d3b72', '#c76c3d']

    # Adicionar barras para cada função e intervalo
    for i, item in enumerate(st.session_state.dados):
        ax.barh(f"{item['função']} ({i+1})", item["fim"] - item["início"], left=item["início"], height=0.4, color=cores[i % len(cores)])
        if exibir_valores:
            ax.text(item["início"] + (item["fim"] - item["início"]) / 2, i, str(item["quantidade"]),
                    va='center', ha='center', color='white', fontsize=12)
        

    # Definir os limites manuais para o eixo X
    ax.set_xlim([min(item['início'] for item in st.session_state.dados), max(item['fim'] for item in st.session_state.dados)])

    # Adicionar linhas verticais pontilhadas nas datas de início e fim
    for item in st.session_state.dados:
        ax.axvline(item["início"], color='gray', linestyle='--', alpha=0.6)
        ax.axvline(item["fim"], color='gray', linestyle='--', alpha=0.6)

    # Colocar as datas de início e fim específicas no eixo X
    datas_unicas = sorted(set([item["início"] for item in st.session_state.dados] + [item["fim"] for item in st.session_state.dados]))
    ax.set_xticks(datas_unicas)
    ax.set_xticklabels(datas_unicas, rotation=45, ha='right')
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))

    # Ajustar as margens
    plt.tight_layout()

    # Títulos e legendas
    plt.title(grafico_titulo, fontsize=14)
    plt.xlabel(label_x)
    plt.ylabel(label_y)

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    gantt_page()
