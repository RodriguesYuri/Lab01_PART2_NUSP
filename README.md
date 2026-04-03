# Ingestão de Dados End-to-End Containerizada (NYC Taxi) | Containerized End-to-End Data Ingestion (NYC Taxi)

*Read this in other languages: [English](#-english-version) | [Português](#-versão-em-português)*

--

## 🇧🇷 Versão em Português

**Repositório:** Lab01_PART2_NUSP

Este projeto implementa um pipeline completo de Engenharia de Dados para extração, armazenamento, validação e visualização dos dados de corridas de táxi de Nova Iorque (Yellow Taxi). Toda a infraestrutura está isolada e orquestrada utilizando Docker.

### Tecnologias Utilizadas
* **Python (uv):** Extração e processamento de dados.
* **PostgreSQL:** Armazenamento relacional de dados.
* **Docker & Docker Compose:** Containerização e orquestração.
* **Great Expectations:** Observabilidade e testes de qualidade de dados.
* **Metabase:** Visualização de dados e Dashboards de BI.

### Como reproduzir o ambiente

Para garantir que o projeto funciona corretamente na sua máquina, certifique-se de que tem o **Docker** e o **Docker Compose** instalados.

**1. Como construir a imagem Docker**
O projeto utiliza um `Dockerfile` para isolar a aplicação Python e um ficheiro `docker-compose.yml` para orquestrar os serviços. Para construir a imagem da aplicação de ingestão, abra o terminal na raiz do projeto e execute:

```bash
docker compose build
```

**2. Como subir os containers**
Após a construção da imagem, é necessário iniciar os serviços (Banco de Dados PostgreSQL, Aplicação de Ingestão e Metabase). Para subir todos os containers em segundo plano, utilize o comando:

```bash
docker compose up -d
```

**3. Como executar as validações do Great Expectations**
A camada de observabilidade foi implementada na camada Raw utilizando o Great Expectations. Foi criado um script dedicado com 5 expectativas (regras de validação).
Para executar os testes de qualidade de dados e gerar o Data Docs (relatório em HTML), execute o script de validação:

```bash
uv run python validate_raw.py
```

Após a execução, navegue até à pasta `gx/uncommitted/data_docs/local_site/` e abra o ficheiro `index.html` no seu navegador para visualizar o relatório de aprovação.

### Visualização de Dados (Metabase)
A infraestrutura inclui uma instância do Metabase para a camada de Business Intelligence.
Com os containers a rodar, aceda a `http://localhost:3000` no seu navegador para explorar o banco de dados e visualizar os gráficos criados.

### Demonstração dos Resultados
Para facilitar a avaliação da entrega do laboratório, abaixo estão os registos visuais das implementações em funcionamento:

**Dashboard de BI (Metabase)**
Visualização do dashboard exploratório final gerado com os insights dos dados da camada Silver:
![Dashboard](documentation\dashboard.png)

**Validação de Dados (Great Expectations)**
Relatório de qualidade de dados gerado com sucesso após a validação das regras estipuladas para a camada Raw:
![GX Documatation](documentation\gx_documentation.jpg)

--

## 🇺🇸 English Version

**Repository:** Lab01_PART2_NUSP

This project implements a complete Data Engineering pipeline for extracting, storing, validating, and visualizing New York Yellow Taxi ride data. The entire infrastructure is isolated and orchestrated using Docker.

### Tecnologias Utilizadas
* **Python (uv):** Data extraction and processing.
* **PostgreSQL:** Relational data storage.
* **Docker & Docker Compose:** Containerization and orchestration.
* **Great Expectations:** Data quality testing and observability.
* **Metabase:** Data visualization and BI Dashboards.

### How to reproduce the environment

To ensure the project runs correctly on your machine, make sure you have Docker and Docker Compose installed.

**1. How to build the Docker image**
The project uses a `Dockerfile` to isolate the Python application and a `docker-compose.yml` file to orchestrate the services. To build the ingestion application image, open the terminal in the project root and run:
```bash
docker compose build
```

**2. How to spin up the containers**
After building the image, you need to start the services (PostgreSQL Database, Ingestion Application, and Metabase). To start all containers in the background, run the following command:

```bash
docker compose up -d
```

**3. How to run Great Expectations validations**
The observability layer was implemented in the Raw layer using Great Expectations. A dedicated script was created containing 5 expectations (validation rules). To run the data quality tests and generate the Data Docs (HTML report), execute the validation script:

```bash
uv run python validate_raw.py
```

After execution, navigate to the `gx/uncommitted/data_docs/local_site/` folder and open the `index.html` file in your browser to view the approval report.

### Data Visualization (Metabase)
The infrastructure includes a Metabase instance for the Business Intelligence layer. With the containers running, access `http://localhost:3000` in your browser to explore the database and view the created charts.

### Results Demonstration
To facilitate the evaluation of the lab submission, below are the visual records of the running implementations:

**BI Dashboard (Metabase)**
View of the final exploratory dashboard generated with insights from the Silver and Gold layers data:
![Dashboard](..\documentation\dashboard.png)

**Data Validation (Great Expectations)**
Data quality report successfully generated after validating the rules established for the Raw layer:
![GX Documatation](..\documentation\gx_documentation.jpg)