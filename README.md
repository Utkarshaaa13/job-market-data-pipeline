# 💼 Job Market Analytics Pipeline

> An automated data pipeline that analyzes job market trends using real-world data engineering tools.

**🔗 Live Dashboard:** [View Here](https://job-market-data-pipeline-cjtaczhgq4ryb2gyrdtsi4.streamlit.app/)

---

## 📊 What This Project Does

This project takes raw job listing data and automatically transforms it into actionable insights:

- **Data Source:** 250 job listings (167 unique positions)
- **Analysis:** Salary trends, in-demand skills, top companies, location insights
- **Automation:** Runs daily to keep insights fresh
- **Visualization:** Interactive dashboard with charts

---

## 🎯 Key Insights Discovered

| Insight | Finding |
|---------|---------|
| **Average Salary** | $122,377 |
| **Top Paying City** | Seattle ($159,761) |
| **Most In-Demand Skill** | Machine Learning (284 jobs) |
| **Highest Paying Skill** | Cloud Architecture ($145,000+) |
| **Top Hiring Company** | DataInc (100 positions) |
| **Salary Growth** | Entry level: $99,974 → Senior: $155,122 (+55%) |
| **Job Types** | Remote: 22% | Full-time: 19% | Contract: 20% |

---

## 🏗️ Flow Diagram
```
Step 1: CSV File (Raw Data)
   ↓
Step 2: Python Script → Loads data into Snowflake
   ↓
Step 3: Airflow → Runs automated transformations daily
   ↓
Step 4: Snowflake → Stores clean, analyzed data
   ↓
Step 5: Streamlit Dashboard → Shows interactive charts

```

---

## 🛠️ Technologies Used

| Tool | Purpose | Why This Tool? |
|------|---------|----------------|
| **Python** | Data processing | Read CSV, handle data types, connect to Snowflake |
| **Snowflake** | Data warehouse | Store and transform large datasets efficiently |
| **Apache Airflow** | Automation | Schedule pipeline to run daily automatically |
| **Docker** | Containerization | Run Airflow consistently on any computer |
| **Streamlit** | Visualization | Create interactive dashboard without JavaScript |
| **SQL** | Data transformation | Clean data, calculate aggregates, join tables |

---

## 📂 Project Structure
```
job-market-pipeline/
│
├── data/                          # Raw CSV data
├── sql/                           # Database setup and transformations
│   ├── ddl/                       # Create tables
│   └── transformations/           # Clean and aggregate data
├── airflow/dags/                  # Pipeline automation
├── streamlit_app/                 # Interactive dashboard
├── docs/                          # Documentation
└── scripts/                       # Python data loading scripts
```

---

## 🗄️ Data Architecture

**Medallion Architecture (Two-Layer Implementation)**

This project uses the **Medallion Architecture** pattern - a modern data lakehouse design widely adopted by companies using Databricks, Snowflake, and cloud data platforms. This layered approach separates raw data from business-ready analytics tables, enabling data quality, reproducibility, and scalability.

### **Layer 1: RAW_DATA (Bronze Layer)**
- Stores exact copy of CSV data
- No transformations applied
- Immutable source of truth
- Enables re-processing and auditing
- **Table:** `JOB_LISTINGS_RAW`

### **Layer 2: ANALYTICS (Gold Layer)**
- Clean, transformed, business-ready data
- Optimized for analysis and reporting
- Aggregated tables for specific use cases

**Tables created:**
- `JOB_LISTINGS_CLEAN` - Deduplicated jobs with parsed locations, skills arrays, and salary calculations
- `SALARY_BY_LOCATION` - Average salaries aggregated by city
- `SKILLS_DEMAND` - Most in-demand technical skills with job counts
- `COMPANY_INSIGHTS` - Top hiring companies and hiring patterns
- `JOB_TYPE_ANALYSIS` - Distribution of remote vs on-site positions

**Why this architecture?**
- ✅ **Reproducibility:** Can rebuild Gold layer from Bronze anytime
- ✅ **Data Quality:** Raw data preserved while analytics tables stay clean
- ✅ **Scalability:** Easy to add Silver layer or new transformations as needed
- ✅ **Industry Standard:** Same pattern used by Databricks, Snowflake, AWS

## 🔄 Pipeline Workflow (What Airflow Does)
```
┌─────────────┐
│    Start    │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Load CSV to         │
│ Snowflake RAW_DATA  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Clean & Transform   │
│ (Parse locations,   │
│  convert skills)    │
└──────┬──────────────┘
       │
       ├────────┬────────┐
       ▼        ▼        ▼
┌──────────┐ ┌──────┐ ┌─────────┐
│ Location │ │Skills│ │ Company │
│ Analysis │ │ Anal.│ │ Insights│
└────┬─────┘ └───┬──┘ └────┬────┘
     │           │         │
     └───────┬───┴─────────┘
             ▼
     ┌──────────────┐
     │ Data Quality │
     │    Check     │
     └──────┬───────┘
            ▼
        ┌───────┐
        │  End  │
        └───────┘
```

**Runs automatically every day at midnight UTC**

---

## 📊 Dashboard vs Business Intelligence Tools

Built with Streamlit - a Python framework for creating interactive data dashboards.
Features:

Real-time KPIs: Total jobs, average salary, top city, active companies
Interactive Charts:

Top 10 cities by salary (horizontal bar chart)
Most in-demand skills (horizontal bar chart)
Job type distribution (donut chart)
Top hiring companies (vertical bar chart)
Salary progression by experience (bar chart with insights)


Direct Snowflake Connection: Queries live data from analytics tables
Cloud Hosted: Free deployment on Streamlit Cloud
Auto-refresh: Updates when pipeline runs

---

## 🚀 Quick Start (Run Locally)

### **Prerequisites:**
- Docker Desktop
- Python 3.11+
- Snowflake account

### **Setup:**
```bash
# Clone repository
git clone https://github.com/Utkarshaaa13/job-market-data-pipeline.git
cd job-market-data-pipeline

# Create environment file
cp .env.example .env
# Edit .env with your Snowflake credentials

# Start Airflow
docker-compose up -d

# Access Airflow UI
# Open: http://localhost:8080
# Username: airflow, Password: airflow

# Run Streamlit Dashboard Locally
pip install -r requirements.txt
streamlit run streamlit_app/dashboard.py
```

---

## 📸 Screenshots

### **Airflow Pipeline (All Tasks Successful)**
![Airflow DAG](docs/screenshots/airflow-dag.png)

### **Streamlit Dashboard**
![Dashboard](docs/screenshots/streamlit-dashboard.png)

### **Snowflake Data Warehouse**
![Snowflake](docs/screenshots/snowflake-tables.png)

---

## 💡 What I Learned

### **Technical Skills:**
- Building end-to-end data pipelines from scratch
- Orchestrating complex workflows with Apache Airflow
- Designing star schema data models for analytics
- Writing efficient SQL transformations in Snowflake
- Containerizing applications with Docker
- Creating interactive dashboards with Python
- Deploying cloud-based data solutions

### **Real-World Problem Solving:**
- **Data Quality:** Filtered invalid salary entries and handled NULL values
- **Deduplication:** Removed 83 duplicate records using SQL window functions
- **Idempotency:** Designed pipeline to run safely multiple times using TRUNCATE-INSERT pattern
- **Performance:** Implemented batch processing (1000 rows/batch) for faster data loading
- **Scalability:** Built two-layer architecture (RAW → ANALYTICS) for future growth
- **Debugging:** Resolved Docker resource constraints and Snowflake connection issues
- **Automation:** Scheduled daily pipeline runs with retry logic and error handling




## 👨‍💻 Author

**Utkarsha Chandgadkar**

- GitHub: [@Utkarshaaa13](https://github.com/Utkarshaaa13)
- LinkedIn: [Your Profile](https://www.linkedin.com/in/utkarsha13/)
- Email: utkarshachandgadkar@gmail.com

---

## 📄 License

This project is open source and available under the MIT License.

---

## Acknowledgments ##

- Apache Airflow community for excellent documentation
- Snowflake for cloud data warehouse platform
- Streamlit for rapid dashboard development

---


