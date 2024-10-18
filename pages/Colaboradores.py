import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Função principal para carregar o DataFrame e gerar os gráficos
def graph_page():    
    # Configuração da página
    st.set_page_config(page_title='Gestão de Pessoas - CAEd', page_icon=':bar_chart:', layout='wide')
    st.title("Customização de Gráficos de Colaboradores")
    st.image('images/logo_caed.png', width=100)

    # Verifica se o DataFrame está presente no session_state
    if 'dataframe' in st.session_state:
        df = st.session_state['dataframe']

        # Exibe o DataFrame carregado
        st.write("Dados carregados:")
        st.write(df)

        st.subheader("Gráficos de barras")

        with st.expander("Configurações do gráfico de barras"):            
            # Selecionar as colunas para o eixo X e Y
            colunas = df.columns.tolist()
            eixo_x = st.selectbox("Selecione a coluna para o eixo X", colunas, key='eixo_x_a')
            eixo_y = st.selectbox("Selecione a coluna para o eixo Y", colunas, key='eixo_y_a')

            # Personalizar o gráfico
            grafico_titulo = st.text_input("Título do gráfico", value="Título do Gráfico", key='titulo_a')
            label_x = st.text_input("Rótulo do eixo X", value="Eixo X", key='label_x_a')
            label_y = st.text_input("Rótulo do eixo Y", value="Eixo Y", key='label_y_a')

        # Configurar as cores e parâmetros do gráfico
        color_map = px.colors.sequential.Teal
        fig = px.histogram(df, x=eixo_x, y=eixo_y, color=eixo_x, color_discrete_sequence=color_map)
        fig.update_layout(bargap=0.1)
        fig.update_layout(showlegend=False)

        # Atualizar os labels e título
        fig.update_xaxes(title_text=label_x)
        fig.update_yaxes(title_text=label_y)
        fig.update_layout(title=grafico_titulo)

        # Exibir o valor de apd_contratados_previstos para cada barra com valores inteiros
        fig.update_traces(texttemplate='%{y}', textposition='inside')

        fig.update_layout(
            xaxis_tickangle=45
        )

        # Mostrar o gráfico
        st.plotly_chart(fig)


        st.subheader("Gráfico de Linhas")

        with st.expander("Configurações do gráfico de linhas"):
            # Selecionar as colunas para o eixo X e Y
            colunas = df.columns.tolist()
            eixo_x = st.selectbox("Selecione a coluna para o eixo X", colunas, key='eixo_x_b')
            eixo_y_previsao = st.selectbox("Selecione a coluna para o eixo Y (Previsão)", colunas, key='eixo_y_previsao_b')        
            previsao_titulo = st.text_input("Título Legenda (Previsão)", value="Previsão", key='titulo_legenda_previsao_b')        
            eixo_y_diferenca = st.selectbox("Selecione a coluna para o eixo Y (Diferença)", colunas, key='eixo_y_diferenca_b')
            diferenca_titulo = st.text_input("Título Legenda (Diferença)", value="Diferença", key='titulo_legenda_diferenca_b')
            eixo_y_contratados = st.selectbox("Selecione a coluna para o eixo Y (Contratados)", colunas, key='eixo_y_contratados_b')
            contratados_titulo = st.text_input("Título Legenda (Contratados)", value="Contratados", key='titulo_legenda_contratados_b')

            # Personalizar o gráfico
            grafico_titulo = st.text_input("Título do gráfico", value="Título do Gráfico", key='titulo_b')
            label_x = st.text_input("Rótulo do eixo X", value="Eixo X", key='label_x_b')
            label_y = st.text_input("Rótulo do eixo Y", value="Eixo Y", key='label_y_b')

        # Criar figura
        fig = go.Figure()

        # Adicionar a primeira linha 'apd_mov_previsao' com valores exibidos nos marcadores
        fig.add_trace(go.Scatter(
            x=df[eixo_x],
            y=df[eixo_y_previsao],
            mode='lines+markers+text',  # Exibir linhas, marcadores e texto
            name=previsao_titulo,
            text=df[eixo_y_previsao],  # Valores a serem exibidos
            textposition="top right",  # Posição do texto
            marker=dict(size=8),
            hovertemplate='Demanda Prevista: %{y}<extra></extra>'  # Exibir valor ao passar o mouse
        ))

        # Adicionar a segunda linha 'apd_mov_diferenca' com valores exibidos nos marcadores
        fig.add_trace(go.Scatter(
            x=df[eixo_x],
            y=df[eixo_y_diferenca],
            mode='lines+markers+text',  # Exibir linhas, marcadores e texto
            name=diferenca_titulo,
            text=df[eixo_y_diferenca],  # Valores a serem exibidos
            textposition='bottom right',  # Posição do texto
            marker=dict(size=8),
            hovertemplate='Diferença: %{y}<extra></extra>'  # Exibir valor ao passar o mouse
        ))

        # Adicionar a terceira linha 'apd_mov_contratados_previstos' com valores exibidos nos marcadores
        fig.add_trace(go.Scatter(
            x=df[eixo_x],
            y=df[eixo_y_contratados],
            mode='lines+markers+text',  # Exibir linhas, marcadores e texto
            name=contratados_titulo,
            text=df[eixo_y_contratados],  # Valores a serem exibidos
            textposition="top left",  # Posição do texto
            marker=dict(size=8),
            hovertemplate='Ativos Previstos: %{y}<extra></extra>'  # Exibir valor ao passar o mouse
        ))

        # Atualizar o layout para manter a legenda e ajustar o título
        fig.update_layout(
            title=grafico_titulo,
            xaxis_title=label_x,
            yaxis_title=label_y,
            showlegend=True,  # Legenda visível
            height=600,  # Aumentar a altura do gráfico
            margin=dict(l=40, r=40, t=40, b=120),  # Ajustar as margens    
            xaxis_tickangle=45  # Inclinar os rótulos do eixo x para evitar sobreposição
        )

        # Ajustar a escala do eixo y para dar mais espaço entre os números
        fig.update_yaxes(range=[-50, 150])  # Ajuste a faixa conforme necessário

        # Exibir o gráfico
        st.plotly_chart(fig)

    else:
        st.write("Nenhum dado encontrado. Por favor, carregue o arquivo CSV na página anterior.")

if __name__ == "__main__":
    graph_page()