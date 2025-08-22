# **Letterboxd Analysis**

Projeto de análise de dados baseado em 10.000 filmes do Letterboxd.  
O objetivo é explorar, processar e analisar informações de filmes usando um pipeline completo em **AWS (S3, Glue, Glue Data Catalog, Athena)**, com suporte a análises em **Python/Jupyter**.

Dataset original: [Letterboxd 10,000 Movies (Kaggle)](https://www.kaggle.com/datasets/ky1338/10000-movies-letterboxd-data)

---

# **Visão Geral do Projeto**

Este projeto cobre todo o ciclo de vida de dados:

- **Ingestão** – Dataset armazenado em **Amazon S3** na camada `raw-data/`.  
- **Transformações (ETL)** – Processamentos em duas etapas:  
  - **Glue Visual ETL**: remove colunas desnecessárias e ajusta tipos de dados (string → int).  
  - **Glue PySpark Job**: normaliza a coluna `countries`, transformando strings em arrays e explodindo os países em múltiplas linhas.  
- **Armazenamento Processado** – Dados organizados em `processed-data/` e `processed-data-final/` em formato **Parquet**.  
- **Catálogo de Dados** – Metadados armazenados no **AWS Glue Data Catalog**, em um database específico (`letterboxd-database`).  
- **Consulta SQL** – Utilização do **Athena** para explorar insights com queries SQL sobre as tabelas do catálogo.  
- **Análise Exploratória** – Jupyter Notebooks em Python para estatísticas e visualizações.  

---

# **Estrutura no S3**

- **raw-data/** → Dataset original (CSV)  
- **processed-data/** → Saída do Glue Visual ETL (Parquet)  
- **processed-data-final/** → Saída do Glue PySpark Job (Parquet com `countries` normalizado)  
- **athena-results/** → Scripts SQL usados no Athena  

---

# **Arquitetura Simplificada**

<img width="1358" height="430" alt="image" src="https://github.com/user-attachments/assets/6bdc67e9-f750-440b-b455-9451407b04ff" />

---

# **Stack Tecnológica**

- **AWS S3** → armazenamento de dados em camadas.  
<img width="1333" height="354" alt="image" src="https://github.com/user-attachments/assets/a10a0560-16a7-4c26-ad55-399580541a2c" />  
<img width="1427" height="475" alt="image" src="https://github.com/user-attachments/assets/f2f889de-263d-4e12-b7be-6b9f4f513f39" />

- **AWS Glue (Visual ETL + PySpark Script)** → transformação dos dados.  
<img width="1977" height="303" alt="image" src="https://github.com/user-attachments/assets/ec17526d-36a9-487a-a81b-5274f934c4b8" />

- **AWS Glue Data Catalog** → gerenciamento de metadados.  
  - Database: `letterboxd-database`  
  - Tabelas criadas automaticamente por **Crawler**, cobrindo `processed-data/` e `processed-data-final/`.  
  - Permite integração direta com o **Athena**, simplificando queries SQL sobre os dados processados.
<img width="831" height="530" alt="image" src="https://github.com/user-attachments/assets/5eda22ba-d4e6-44f0-b927-ae6084aaee65" />


- **AWS Athena** → consultas SQL sobre os Parquet processados.  
<img width="2000" height="961" alt="image" src="https://github.com/user-attachments/assets/64130135-1346-4daa-93a3-958a6d66875d" />

- **Python + Jupyter** → análises adicionais e visualizações.  
- **PySpark** → transformação customizada (normalização e explode da coluna `countries`).  

---

# **🔍 Principais Transformações**

- Conversão de colunas de **string → int** para consistência.  
- Normalização da coluna **`countries`**:  
  - Entrada: `"USA"`, `"['USA','UK']"`, `null`  
  - Saída: `["USA"]`, `["USA", "UK"]`, `[]`  
- Explosão da coluna `countries` → múltiplas linhas, cada filme-por-país.  
- Criação automática de **tabelas no Glue Data Catalog** a partir dos Parquets processados.  

---

# **Exemplos de Perguntas Respondidas com Athena**

- Quais os países mais frequentes nas produções?  
- Quais gêneros têm maiores médias de nota?  
- Distribuição de avaliações ao longo dos anos.  
- Relação entre estúdios e número de produções.  

---

# **Jupyter Notebooks**

Além do pipeline em AWS, o projeto conta com notebooks em Python para:  

- Estatísticas descritivas.  
- Visualizações (**matplotlib**).  
- Comparações regionais (ex.: filmes dos EUA vs. filmes do Brasil).  

---

# **Próximos Passos**

- Documentar notebooks de análise com exemplos de gráficos.  

---

# **Condiderações Finais**

Este projeto é fruto do meu aprendizado contínuo.  
Sei que ainda há muito a melhorar, tanto no código quanto na forma de estruturar análises e documentações.  
Estou aberto a **sugestões, feedbacks e novas ideias**.  

Meu objetivo é **evoluir como engenheiro de dados e analista**, aprendendo sempre com a prática e com quem já tem mais experiência na área.  
