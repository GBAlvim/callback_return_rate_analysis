import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

# Configuração da página
st.set_page_config(page_title="Análise de Ligações", layout="wide")

# Carregar e cache de dados
@st.cache_data
def load_data():
    file_path = "/mnt/c/Workspace/pessoal/projetos/callback_return_rate_analysis/call_data.csv"
    return pd.read_csv(file_path, sep="\t")

df = load_data()

# Ajuste de dados
df["LastCall"] = pd.to_datetime(df["LastCall"], errors="coerce")
df["Hora"] = df["LastCall"].dt.hour

# Título do Dashboard
st.title("📊 Dashboard de Análise de Ligações")

# Criação das Abas (Tabs)
tab1, tab2, tab3 = st.tabs(["📞 Status das Ligações", "📈 Análises Temporais", "📊 Outros Insights"])

# 📞 **Status das Ligações**
with tab1:
    st.subheader("Distribuição dos Status das Ligações")
    # Gráfico de barras com Plotly
    status_counts = df["Status_Ligacao"].value_counts()
    fig = px.bar(status_counts, x=status_counts.index, y=status_counts.values, 
                 labels={'x': 'Status da Ligação', 'y': 'Quantidade'},
                 title="Distribuição de Ligações por Status", 
                 color=status_counts.index, color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Duração Média das Ligações por Status")
    # Gráfico de barras horizontais com Plotly
    duration_avg = df.groupby("Status_Ligacao")["Duaration"].mean()
    fig = px.bar(duration_avg, x=duration_avg.values, y=duration_avg.index, 
                 labels={'x': 'Duração Média (s)', 'y': 'Status da Ligação'},
                 title="Duração Média das Ligações por Status", 
                 color=duration_avg.index, orientation='h', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

# 📈 **Análises Temporais**
with tab2:
    st.subheader("Número de Ligações ao Longo do Tempo")
    df["lcall"] = pd.to_datetime(df["lcall"], errors="coerce")
    df.set_index("lcall", inplace=True)
    
    # Gráfico de linha interativo
    daily_calls = df.resample("D").size()
    fig = px.line(daily_calls, x=daily_calls.index, y=daily_calls.values,
                  labels={'x': 'Data', 'y': 'Quantidade de Ligações'},
                  title="Número de Ligações ao Longo do Tempo", 
                  line_shape="linear", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Melhor Horário para Contato")
    # Gráfico de barras com Plotly para distribuição das ligações por hora
    hourly_counts = df["Hora"].value_counts().sort_index()
    fig = px.bar(hourly_counts, x=hourly_counts.index, y=hourly_counts.values,
                 labels={'x': 'Hora do Dia', 'y': 'Número de Ligações'},
                 title="Melhor Horário para Contato com os Clientes",
                 color=hourly_counts.index, color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

# 📊 **Outros Insights**
with tab3:
    st.subheader("Quantidade de Ligações por Tipo de Telefone")
    # Gráfico de barras com Plotly para quantidade de ligações por tipo de telefone
    phone_type_counts = df["Fone_Tipo"].value_counts()
    fig = px.bar(phone_type_counts, x=phone_type_counts.index, y=phone_type_counts.values,
                 labels={'x': 'Tipo de Telefone', 'y': 'Quantidade de Ligações'},
                 title="Quantidade de Ligações por Tipo de Telefone",
                 color=phone_type_counts.index, color_discrete_sequence=px.colors.qualitative.Dark24)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 Clientes que Mais Retornam")
    # Gráfico de barras para os top 10 clientes com Plotly
    top_10_clients = df["ID"].value_counts().head(10)
    fig = px.bar(top_10_clients, x=top_10_clients.index, y=top_10_clients.values,
                 labels={'x': 'ID do Cliente', 'y': 'Número de Retornos'},
                 title="Top 10 Clientes que Mais Retornam",
                 color=top_10_clients.index, color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("📢 **Gabriel Alvim** | Analista - Desenvolvedor de Software")
