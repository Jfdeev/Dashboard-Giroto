# Dashboard: Top 10 Insights sobre Saúde Mental dos Estudantes

Este projeto é um **dashboard interativo** desenvolvido com Streamlit, Pandas e Plotly, projetado para explorar os 10 fatores mais impactantes na saúde mental de estudantes. Ele analisa variáveis como depressão, pensamentos suicidas, pressão acadêmica, duração do sono, estresse financeiro e hábitos alimentares, oferecendo uma ferramenta dinâmica para educadores, pesquisadores e estudantes entenderem padrões críticos.

# Deploy do Projeto


## Objetivo
O objetivo é fornecer uma interface visual que revele os principais drivers da saúde mental em estudantes, permitindo análises personalizadas por meio de filtros interativos. O dashboard visa identificar grupos vulneráveis e informar estratégias de bem-estar baseadas em dados.

## Dataset
- **Fonte:** Dados de estudantes (adaptado de um dataset do Kaggle).
- **Colunas Principais:**
  - `Gender` (Gênero: 0=Masculino, 1=Feminino)
  - `Age` (Idade)
  - `City` (Cidade)
  - `Academic Pressure` (Pressão Acadêmica)
  - `CGPA` (Nota Média)
  - `Sleep Duration` (Duração do Sono)
  - `Dietary Habits` (Hábitos Alimentares)
  - `Have you ever had suicidal thoughts ?` (Pensamentos Suicidas: 0=Não, 1=Sim)
  - `Work/Study Hours` (Horas de Estudo)
  - `Financial Stress` (Estresse Financeiro: 1 a 5)
  - `Family History of Mental Illness` (Histórico Familiar: 0=Não, 1=Sim)
  - `Depression` (Depressão: 0=Não, 1=Sim)

## Top 10 Insights
O dashboard destaca os seguintes insights, cada um com um gráfico otimizado:
1. **Depressão por Gênero** (Barra): Taxa de depressão por gênero.
2. **Depressão por Idade** (Histograma): Distribuição etária da depressão.
3. **Pressão Acadêmica** (Barra): Impacto da pressão na taxa de depressão.
4. **Duração do Sono** (Barra Empilhada): Relação entre sono e depressão.
5. **Pensamentos Suicidas por Cidade** (Barra): Top 10 cidades com maior risco.
6. **Estresse Financeiro** (Barra): Efeito do estresse financeiro na depressão.
7. **Histórico Familiar** (Barra): Influência do histórico familiar.
8. **CGPA** (Boxplot): Comparação de desempenho acadêmico com depressão.
9. **Horas de Estudo** (Barra): Taxa de depressão por faixas de horas.
10. **Hábitos Alimentares** (Barra): Impacto da dieta na depressão.

## Funcionalidades
- **Filtros Interativos:** Gênero, faixa etária, cidade, duração do sono, pressão acadêmica e estresse financeiro.
- **Métricas Resumidas:** Taxa de depressão, pensamentos suicidas e média de CGPA.
- **Gráficos Anotados:** Valores percentuais e contagens exibidos diretamente nos gráficos.
- **Exportação:** Opção de baixar os dados filtrados em CSV.

## Pré-requisitos
- **Python 3.8+**
- Bibliotecas necessárias:
  - `streamlit`
  - `pandas`
  - `plotly`

## Instalação
1. Clone o repositório ou copie o código para o seu ambiente: