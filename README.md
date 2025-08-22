# **🎬 Letterboxd Analysis**

Projeto de análise de dados baseado em 10.000 filmes do Letterboxd.  
O objetivo é explorar, processar e analisar informações de filmes usando um pipeline completo em **AWS (S3, Glue, Athena)**, com suporte a análises em **Python/Jupyter**.

Dataset original: [Letterboxd 10,000 Movies (Kaggle)](https://www.kaggle.com/datasets/ky1338/10000-movies-letterboxd-data)

---

# **🚀 Visão Geral do Projeto**

Este projeto cobre todo o ciclo de vida de dados:

- **Ingestão** – Dataset armazenado em **Amazon S3** na camada `raw-data/`.  
- **Transformações (ETL)** – Processamentos em duas etapas:  
  - **Glue Visual ETL**: remove colunas desnecessárias e ajusta tipos de dados (string → int).  
  - **Glue PySpark Job**: normaliza a coluna `countries`, transformando strings em arrays e explodindo os países em múltiplas linhas.  
- **Armazenamento Processado** – Dados organizados em `processed-data/` e `processed-data-final/` em formato **Parquet**.  
- **Consulta SQL** – Utilização do **Athena** para explorar insights com queries SQL.  
- **Análise Exploratória** – Jupyter Notebooks em Python para estatísticas e visualizações.  

---

# **📂 Estrutura no S3**


- **raw-data/** → Dataset original (CSV)  
- **processed-data/** → Saída do Glue Visual ETL (Parquet)  
- **processed-data-final/** → Saída do Glue PySpark Job (Parquet com `countries` normalizado)  
- **athena-results/** → Scripts SQL usados no Athena  

---

# **🛠️ Stack Tecnológica**

- **AWS S3** → armazenamento de dados em camadas.  
- **AWS Glue (Visual ETL + PySpark Script)** → transformação dos dados.  
- **AWS Athena** → consultas SQL sobre os Parquet processados.  
- **Python + Jupyter** → análises adicionais e visualizações.  
- **PySpark** → transformação customizada (normalização e explode da coluna `countries`).  

---

# **🔍 Principais Transformações**

- Conversão de colunas de **string → int** para consistência.  
- Normalização da coluna **`countries`**:  
  - Entrada: `"USA"`, `"['USA','UK']"`, `null`  
  - Saída: `["USA"]`, `["USA", "UK"]`, `[]`  
- Explosão da coluna `countries` → múltiplas linhas, cada filme-por-país.  

---

# **📊 Exemplos de Perguntas Respondidas com Athena**

- Quais os países mais frequentes nas produções?  
- Quais gêneros têm maiores médias de nota?  
- Distribuição de avaliações ao longo dos anos.  
- Relação entre estúdios e número de produções.  

---

# **📓 Jupyter Notebooks**

Além do pipeline em AWS, o projeto conta com notebooks em Python para:  

- Estatísticas descritivas.  
- Visualizações (**matplotlib, seaborn, plotly**).  
- Comparações regionais (ex.: filmes dos EUA vs. filmes do Brasil).  

---

# **📌 Próximos Passos**

- Documentar notebooks de análise com exemplos de gráficos.  
- Publicar dashboards no Power BI / Tableau com os dados processados.
  
---

# **💡 Mensagem Final**

Este projeto é fruto do meu aprendizado contínuo.  
Sei que ainda há muito a melhorar, tanto no código quanto na forma de estruturar análises e documentações.  
Estou aberto a **sugestões, feedbacks e novas ideias**.  

Meu objetivo é **evoluir como engenheiro de dados e analista**, aprendendo sempre com a prática e com quem já tem mais experiência na área.  

