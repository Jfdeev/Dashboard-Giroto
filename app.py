import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial do Streamlit
st.set_page_config(page_title="Dashboard de Saúde Mental", layout="wide")

# Função para carregar e tratar os dados
@st.cache_data
def load_data():
    """
    Carrega o dataset, filtra estudantes e mapeia variáveis categóricas para numéricas.
    Trata valores inválidos em 'Financial Stress' substituindo '?' por 1.0.
    """
    try:
        data = pd.read_csv('dataset.csv')
        # Filtrar apenas estudantes
        data = data[data['Profession'] == 'Student']
        # Mapeamento de variáveis categóricas
        data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1})
        data['Depression'] = data['Depression'].astype(int)
        data['Have you ever had suicidal thoughts ?'] = data['Have you ever had suicidal thoughts ?'].map({'Yes': 1, 'No': 0})
        data['Family History of Mental Illness'] = data['Family History of Mental Illness'].map({'Yes': 1, 'No': 0})
        data['Financial Stress'] = pd.to_numeric(data['Financial Stress'].replace('?', '1.0'), errors='coerce').fillna(1.0)
        return data
    except FileNotFoundError:
        st.error("Arquivo 'dataset.csv' não encontrado. Verifique o caminho.")
        return None
    except KeyError as e:
        st.error(f"Coluna ausente no dataset: {e}")
        return None

# Carregar dados
data = load_data()
if data is None:
    st.stop()

# Título e introdução detalhada
st.title("Dashboard: Top 10 Insights sobre Saúde Mental dos Estudantes")
st.markdown("""
Este dashboard explora os fatores mais impactantes na saúde mental de estudantes, como depressão, pensamentos suicidas, 
pressão acadêmica, sono, estresse financeiro e hábitos alimentares. Use os filtros na barra lateral para personalizar a análise 
e descubra padrões que podem informar políticas educacionais e de bem-estar.
""")

# --- Filtros Avançados ---
st.sidebar.header("Filtros Interativos")
gender_filter = st.sidebar.selectbox("Gênero", ['Todos', 'Masculino', 'Feminino'], index=0)
age_range = st.sidebar.slider("Faixa Etária", min_value=int(data['Age'].min()), max_value=int(data['Age'].max()), value=(18, 34))
city_filter = st.sidebar.multiselect("Cidade", data['City'].unique(), default=data['City'].unique())
sleep_filter = st.sidebar.multiselect("Duração do Sono", data['Sleep Duration'].unique(), default=data['Sleep Duration'].unique())
pressure_filter = st.sidebar.multiselect("Pressão Acadêmica", data['Academic Pressure'].unique(), default=data['Academic Pressure'].unique())
stress_filter = st.sidebar.multiselect("Estresse Financeiro", [1.0, 2.0, 3.0, 4.0, 5.0], default=[1.0, 2.0, 3.0, 4.0, 5.0])

# Aplicar filtros
filtered_data = data.copy()
if gender_filter != 'Todos':
    filtered_data = filtered_data[filtered_data['Gender'] == {'Masculino': 0, 'Feminino': 1}[gender_filter]]
filtered_data = filtered_data[(filtered_data['Age'] >= age_range[0]) & (filtered_data['Age'] <= age_range[1])]
filtered_data = filtered_data[filtered_data['City'].isin(city_filter)]
filtered_data = filtered_data[filtered_data['Sleep Duration'].isin(sleep_filter)]
filtered_data = filtered_data[filtered_data['Academic Pressure'].isin(pressure_filter)]
filtered_data = filtered_data[filtered_data['Financial Stress'].isin(stress_filter)]

# --- Métricas Resumidas ---
st.subheader("Resumo Geral")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Taxa de Depressão", f"{filtered_data['Depression'].mean() * 100:.1f}%")
with col2:
    st.metric("Pensamentos Suicidas", f"{filtered_data['Have you ever had suicidal thoughts ?'].mean() * 100:.1f}%")
with col3:
    st.metric("Média de CGPA", f"{filtered_data['CGPA'].mean():.2f}")

# --- Gráficos ---
st.subheader("Top 10 Insights")

# 1. Taxa de Depressão por Gênero
fig1 = px.bar(
    filtered_data.groupby('Gender')['Depression'].mean().reset_index(),
    x='Gender', y='Depression',
    title="1. Depressão por Gênero",
    labels={'Gender': 'Gênero (0=Masculino, 1=Feminino)', 'Depression': 'Taxa de Depressão (%)'},
    color='Depression', color_continuous_scale='Blues',
    text=filtered_data.groupby('Gender')['Depression'].mean().apply(lambda x: f"{x*100:.1f}%")
)
fig1.update_traces(textposition='auto')
fig1.update_layout(yaxis_tickformat='.0%')
st.plotly_chart(fig1, use_container_width=True)

# 2. Distribuição de Depressão por Idade
fig2 = px.histogram(
    filtered_data, x='Age', color='Depression',
    title="2. Depressão por Idade",
    labels={'Age': 'Idade', 'Depression': 'Depressão (0=Sem, 1=Com)'},
    color_discrete_map={0: '#1f77b4', 1: '#ff7f0e'},
    marginal="box"  # Adiciona boxplot na margem para mais contexto
)
st.plotly_chart(fig2, use_container_width=True)

# 3. Pressão Acadêmica vs. Depressão
fig3 = px.bar(
    filtered_data.groupby('Academic Pressure')['Depression'].mean().reset_index(),
    x='Academic Pressure', y='Depression',
    title="3. Pressão Acadêmica Aumenta a Depressão?",
    labels={'Academic Pressure': 'Nível de Pressão (ex.: Baixa, Média, Alta)', 'Depression': 'Taxa de Depressão (%)'},
    color='Depression', color_continuous_scale='Blues',
    text=filtered_data.groupby('Academic Pressure')['Depression'].mean().apply(lambda x: f"{x*100:.1f}%")
)
fig3.update_traces(textposition='auto')
fig3.update_layout(yaxis_tickformat='.0%')
st.plotly_chart(fig3, use_container_width=True)

# 4. Duração do Sono vs. Depressão
fig4 = px.histogram(
    filtered_data, x='Sleep Duration', color='Depression',
    title="4. Menos Sono Está Ligado à Depressão?",
    labels={'Sleep Duration': 'Duração do Sono (horas)', 'Depression': 'Depressão (0=Sem, 1=Com)', 'count': 'Contagem'},
    color_discrete_map={0: '#1f77b4', 1: '#ff7f0e'},
    barmode='stack',
    text_auto=True  # Adiciona contagem nas barras
)
st.plotly_chart(fig4, use_container_width=True)

depression_count_city = (
    filtered_data[filtered_data['Depression'] == 1]
    .groupby('City')
    .size()
    .reset_index(name='Count')
)

# 5. Pensamentos Suicidas por Cidade
fig5 = px.bar(
    depression_count_city,
    x='City',
    y='Count',
    title="Pensamentos Suicidas por Cidade",
    labels={'City': 'Cidade', 'Count': 'Número de Pessoas com Pensamentos Suicidas'},
    color='Count', color_continuous_scale='Blues'
)
fig5.update_traces(textposition='auto')
fig5.update_layout(yaxis_tickformat=',')
st.plotly_chart(fig5, use_container_width=True)

# 6. Estresse Financeiro vs. Depressão
fig6 = px.bar(
    filtered_data.groupby('Financial Stress')['Depression'].mean().reset_index(),
    x='Financial Stress', y='Depression',
    title="6. Estresse Financeiro Elevado Gera Mais Depressão?",
    labels={'Financial Stress': 'Estresse Financeiro (1=Baixo, 5=Alto)', 'Depression': 'Taxa de Depressão (%)'},
    color='Depression', color_continuous_scale='Blues',
    text=filtered_data.groupby('Financial Stress')['Depression'].mean().apply(lambda x: f"{x*100:.1f}%")
)
fig6.update_traces(textposition='auto')
fig6.update_layout(yaxis_tickformat='.0%')
st.plotly_chart(fig6, use_container_width=True)

# 7. Histórico Familiar vs. Depressão
fig7 = px.bar(
    filtered_data.groupby('Family History of Mental Illness')['Depression'].mean().reset_index(),
    x='Family History of Mental Illness', y='Depression',
    title="7. Histórico Familiar Dobra o Risco de Depressão?",
    labels={'Family History of Mental Illness': 'Histórico Familiar (0=Não, 1=Sim)', 'Depression': 'Taxa de Depressão (%)'},
    color='Depression', color_continuous_scale='Blues',
    text=filtered_data.groupby('Family History of Mental Illness')['Depression'].mean().apply(lambda x: f"{x*100:.1f}%")
)
fig7.update_traces(textposition='auto')
fig7.update_layout(yaxis_tickformat='.0%')
st.plotly_chart(fig7, use_container_width=True)

# 8. CGPA vs. Depressão
fig8 = px.box(
    filtered_data, x='Depression', y='CGPA',
    title="8. Depressão Afeta o Desempenho Acadêmico?",
    labels={'Depression': 'Depressão (0=Sem, 1=Com)', 'CGPA': 'Nota Média (0-10)'},
    color='Depression', color_discrete_map={0: '#1f77b4', 1: '#ff7f0e'}
)
st.plotly_chart(fig8, use_container_width=True)

# 9. Horas de Estudo vs. Depressão
# Agrupar horas em faixas mais refinadas
filtered_data['Work/Study Hours Binned'] = pd.cut(filtered_data['Work/Study Hours'], 
                                                  bins=[0, 4, 8, 12, float('inf')], 
                                                  labels=['0-4h', '5-8h', '9-12h', '13+h'])
fig9 = px.bar(
    filtered_data.groupby('Work/Study Hours Binned')['Depression'].mean().reset_index(),
    x='Work/Study Hours Binned', y='Depression',
    title="9. Mais Horas de Estudo, Mais Depressão?",
    labels={'Work/Study Hours Binned': 'Horas de Estudo por Dia', 'Depression': 'Taxa de Depressão (%)'},
    color='Depression', color_continuous_scale='Blues',
    text=filtered_data.groupby('Work/Study Hours Binned')['Depression'].mean().apply(lambda x: f"{x*100:.1f}%")
)
fig9.update_traces(textposition='auto')
fig9.update_layout(yaxis_tickformat='.0%')
st.plotly_chart(fig9, use_container_width=True)

# 10. Hábitos Alimentares vs. Depressão
fig10 = px.bar(
    filtered_data.groupby('Dietary Habits')['Depression'].mean().reset_index(),
    x='Dietary Habits', y='Depression',
    title="10. Dieta Saudável Reduz a Depressão?",
    labels={'Dietary Habits': 'Hábitos Alimentares', 'Depression': 'Taxa de Depressão (%)'},
    color='Depression', color_continuous_scale='Blues',
    text=filtered_data.groupby('Dietary Habits')['Depression'].mean().apply(lambda x: f"{x*100:.1f}%")
)
fig10.update_traces(textposition='auto')
fig10.update_layout(yaxis_tickformat='.0%')
st.plotly_chart(fig10, use_container_width=True)

# --- Exportação ---
st.subheader("Exportar Dados")
if st.button("Baixar Dados Filtrados (CSV)"):
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download", data=csv, file_name='dados_filtrados.csv', mime='text/csv')

# --- Documentação ---
st.sidebar.subheader("Sobre o Projeto")
st.sidebar.markdown("""
- **Objetivo:** Analisar os 10 fatores mais impactantes na saúde mental de estudantes.
- **Dataset:** Dados de estudantes (Kaggle), com variáveis como depressão, sono, pressão acadêmica e dieta.
- **Ferramentas:** 
  - **Pandas:** Manipulação de dados.
  - **Plotly:** Visualizações interativas.
  - **Streamlit:** Interface dinâmica.
- **Insights:** Explore como gênero, idade, sono e mais afetam a depressão e pensamentos suicidas.
""")