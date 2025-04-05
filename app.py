import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial
st.set_page_config(page_title="Dashboard de Saúde Mental", layout="wide")

# Função para carregar os dados
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('dataset.csv')
        data = data[data['Profession'] == 'Student']
        data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1})
        data['Depression'] = data['Depression'].astype(int)
        data['Have you ever had suicidal thoughts ?'] = data['Have you ever had suicidal thoughts ?'].map({'Yes': 1, 'No': 0})
        data['Family History of Mental Illness'] = data['Family History of Mental Illness'].map({'Yes': 1, 'No': 0})
        data['Financial Stress'] = pd.to_numeric(data['Financial Stress'].replace('?', '1.0'), errors='coerce').fillna(1.0)
        return data
    except FileNotFoundError:
        st.error("Arquivo 'dataset.csv' não encontrado.")
        return None

# Carregar dados
data = load_data()
if data is None:
    st.stop()

# Título e introdução
st.title("Dashboard: Top 10 Insights sobre Saúde Mental")
st.markdown("Explore os fatores mais impactantes na saúde mental dos estudantes.")

# --- Filtros ---
st.sidebar.header("Filtros")
gender_filter = st.sidebar.selectbox("Gênero", ['Todos', 'Masculino', 'Feminino'], index=0)
age_range = st.sidebar.slider("Faixa Etária", min_value=int(data['Age'].min()), max_value=int(data['Age'].max()), value=(18, 34))
city_filter = st.sidebar.multiselect("Cidade", data['City'].unique(), default=data['City'].unique())
sleep_filter = st.sidebar.multiselect("Duração do Sono", data['Sleep Duration'].unique(), default=data['Sleep Duration'].unique())

# Aplicar filtros
filtered_data = data.copy()
if gender_filter != 'Todos':
    filtered_data = filtered_data[filtered_data['Gender'] == {'Masculino': 0, 'Feminino': 1}[gender_filter]]
filtered_data = filtered_data[(filtered_data['Age'] >= age_range[0]) & (filtered_data['Age'] <= age_range[1])]
filtered_data = filtered_data[filtered_data['City'].isin(city_filter)]
filtered_data = filtered_data[filtered_data['Sleep Duration'].isin(sleep_filter)]


# --- Métricas Resumidas ---
st.subheader("Resumo")
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
    labels={'Gender': 'Gênero (0=Masc, 1=Fem)', 'Depression': 'Taxa de Depressão (%)'},
    color='Depression', color_continuous_scale='Blues'
)
fig1.update_layout(yaxis_tickformat='.0%')
st.plotly_chart(fig1, use_container_width=True)

# 2. Distribuição de Depressão por Idade
fig2 = px.histogram(
    filtered_data, x='Age', color='Depression',
    title="2. Depressão por Idade",
    labels={'Age': 'Idade', 'Depression': 'Depressão (0=Não, 1=Sim)'},
    color_discrete_map={0: '#1f77b4', 1: '#ff7f0e'}
)
st.plotly_chart(fig2, use_container_width=True)

# 3. Pressão Acadêmica vs. Depressão
fig3 = px.histogram(
    filtered_data, x='Academic Pressure', y='Depression',
    title="3. Impacto da Pressão Acadêmica na Depressão",
    labels={'Academic Pressure': 'Pressão Acadêmica', 'Depression': 'Pessoas com Depressão'},
    color_discrete_map={0: '#1f77b4', 1: '#ff7f0e'}
)
st.plotly_chart(fig3, use_container_width=True)

depression_count = (
    filtered_data[filtered_data['Depression'] == 1]
    .groupby('Sleep Duration')
    .size()
    .reset_index(name='Count')
)

# 4. Duração do Sono vs. Depressão
fig4 = px.area(
    depression_count,
    x='Sleep Duration',
    y='Count',
    title="4. Sono e Depressão",
    labels={'Sleep Duration': 'Duração do Sono', 'Count': 'Número de Pessoas com Depressão'}
)
st.plotly_chart(fig4, use_container_width=True)

depression_count_city = (
    filtered_data[filtered_data['Depression'] == 1]
    .groupby('City')
    .size()
    .reset_index(name='Count')
)

# 5. Pensamentos Suicidas por Cidade (Top 10)
fig5 = px.bar(
    depression_count_city,
    x='City',
    y='Count',
    title="Pensamentos Suicidas por Cidade (Top 10)",
    labels={'City': 'Cidade', 'Count': 'Número de Pessoas com Pensamentos Suicidas'},
    color='Count', color_continuous_scale='Blues'
)
fig5.update_layout(yaxis_tickformat='.0%')
st.plotly_chart(fig5, use_container_width=True)

# 6. Estresse Financeiro vs. Depressão
fig6 = px.histogram(
    filtered_data, x='Financial Stress', y='Depression',
    title="6. Estresse Financeiro e Depressão",
    labels={'Financial Stress': 'Estresse Financeiro (1-5)', 'Depression': 'Depressão'}
)
st.plotly_chart(fig6, use_container_width=True)

# 7. Histórico Familiar vs. Depressão
fig7 = px.bar(
    filtered_data.groupby('Family History of Mental Illness')['Depression'].mean().reset_index(),
    x='Family History of Mental Illness', y='Depression',
    title="7. Histórico Familiar e Depressão",
    labels={'Family History of Mental Illness': 'Histórico (0=Não, 1=Sim)', 'Depression': 'Taxa de Depressão (%)'},
    color='Depression', color_continuous_scale='Blues'
)
fig7.update_layout(yaxis_tickformat='.0%')
st.plotly_chart(fig7, use_container_width=True)

# 8. CGPA vs. Depressão
fig8 = px.box(
    filtered_data,
    x='Depression',
    y='CGPA',
    title="Desempenho Acadêmico e Depressão",
    labels={'Depression': 'Depressão (0=Não, 1=Sim)', 'CGPA': 'Nota Média (CGPA)'},
    color='Depression',
    color_discrete_map={0: '#1f77b4', 1: '#ff7f0e'}
)
st.plotly_chart(fig8, use_container_width=True)

# 9. Horas de Estudo vs. Depressão
fig9 = px.histogram(
    filtered_data, x='Work/Study Hours', y='Depression',
    title="9. Horas de Estudo e Depressão",
    labels={'Work/Study Hours': 'Horas de Estudo', 'Depression': 'Depressão (0=Não, 1=Sim)'}
)
st.plotly_chart(fig9, use_container_width=True)

# 10. Correlações entre Fatores
numeric_cols = ['Age', 'Academic Pressure', 'CGPA', 'Work/Study Hours', 'Financial Stress', 'Depression', 
                'Have you ever had suicidal thoughts ?', 'Family History of Mental Illness']
corr_matrix = filtered_data[numeric_cols].corr()
fig10 = px.imshow(
    corr_matrix, text_auto='.2f', aspect="auto", color_continuous_scale='RdBu_r',
    title="10. Correlações entre Fatores-Chave"
)
st.plotly_chart(fig10, use_container_width=True)

# --- Exportação ---
st.subheader("Exportar Dados")
if st.button("Baixar Dados Filtrados (CSV)"):
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download", data=csv, file_name='dados_filtrados.csv', mime='text/csv')

# --- Documentação ---
st.sidebar.subheader("Sobre")
st.sidebar.markdown("""
•⁠  ⁠*Objetivo:* Mostrar os 10 insights mais revelantes sobre saúde mental.
•⁠  ⁠*Dataset:* Estudantes (Kaggle).
•⁠  ⁠*Ferramentas:* Pandas, Plotly, Streamlit.
""")