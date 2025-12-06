# Job Market Analytics Dashboard & Data Pipeline

Fully automated, production-grade data engineering project that ingests, processes, stores, and visualizes insights from over 1,000 real-world technology job listings.

- 1,000+ job postings analyzed  
- Daily automated refresh at 00:00 UTC via Apache Airflow  
- Data stored and queried in Snowflake  
- Interactive dashboard built with Streamlit  
- Entire stack containerized with Docker

## Key Insights (as of 2025-12-06)

| Metric                            | Value                  |
|-----------------------------------|------------------------|
| Total Job Listings                | 1,000+                 |
| Average Salary                    | $122,377               |
| Highest Average Salary City       | Seattle                |
| Top Hiring City by Volume         | Austin                 |
| Active Hiring Companies           | 40                     |
| Remote Positions                  | 26%                    |

### Salary by Experience Level
- Entry Level (0–2 years): $99,974  
- Mid-Level (2–5 years): $123,046  
- Senior Level (8+ years): $155,122 (+$55,148 vs Entry)

### Most In-Demand Skills
| Skill              | Job Postings |
|--------------------|--------------|
| AWS                | 234          |
| Python             | 228          |
| Machine Learning   | 224          |
| CI/CD              | 224          |
| Agile              | 224          |
| Docker             | 224          |
| Go                 | 224          |
| Git                | 220          |
| TypeScript         | 220          |
| Ruby               | 216          |
| JavaScript         | 216          |
| REST APIs          | 212          |
| React              | 208          |
| Node.js            | 208          |
| SQL                | 204          |

## Technology Stack

- Apache Airflow – orchestration & scheduling  
- Snowflake – cloud data warehouse  
- Docker & Docker Compose – containerization  
- Python – ETL and automation logic  
- Streamlit – interactive analytics dashboard  

Pipeline status: Active  
Last updated: 2025-12-06 06:52 UTC

## Project Structure
job-market-data-pipeline/
├── dags/                # Airflow DAGs
├── scripts/             # Data processing and ETL
├── sql/                 # Snowflake schemas and queries
├── streamlit_app/       # Dashboard source code
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example         # Template – never commit real credentials
└── README.md
text## Local Setup Instructions

1. Clone the repository  
   `git clone https://github.com/your-username/job-market-data-pipeline.git`  
   `cd job-market-data-pipeline`

2. Configure credentials  
   `cp .env.example .env`

3. Start all services  
   `docker-compose up --build`

Services will be available at:  
- Apache Airflow: http://localhost:8080  
- Streamlit Dashboard: http://localhost:8501

## Author
Utkarsha Chandgadkar
Data Analyst  
LinkedIn: https://www.linkedin.com/in/utkarsha13/
