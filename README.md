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

## 🏗️ How It Works (Simple Flow)
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

**Think of it like a factory:**
- **Raw materials** = CSV file
- **Assembly line** = Airflow pipeline
- **Storage** = Snowflake database
- **Showroom** = Streamlit dashboard

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

### **Two-Layer Design:**

**Layer 1: RAW_DATA (Bronze)**
- Stores exact copy of CSV
- No changes to original data
- Used for re-processing if needed

**Layer 2: ANALYTICS (Gold)**
- Clean, transformed data
- Ready for analysis
- **Tables created:**
  - `JOB_LISTINGS_CLEAN` - Parsed locations, skills arrays, salary averages
  - `SALARY_BY_LOCATION` - Average salaries by city
  - `SKILLS_DEMAND` - Most in-demand technical skills
  - `COMPANY_INSIGHTS` - Top hiring companies and patterns
  - `JOB_TYPE_ANALYSIS` - Remote vs on-site trends

---

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

**Question: Why Streamlit and not Tableau?**

| Feature | Tableau | Streamlit (What I Built) |
|---------|---------|--------------------------|
| **Cost** | Expensive ($$$) | Free ✅ |
| **Setup** | Desktop installation | Cloud-hosted |
| **Connection** | Connects to Snowflake | Connects to Snowflake |
| **Coding** | Drag-and-drop | Python code |
| **For this project** | Not needed | Perfect for portfolio! ✅ |

**Both connect to Snowflake (the data warehouse), NOT Airflow.**
- Airflow = Runs the pipeline
- Snowflake = Stores the data
- Streamlit/Tableau = Shows the charts

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
- Building production-grade data pipelines
- Orchestrating complex workflows with Airflow
- Designing star schema data models
- Writing efficient SQL transformations
- Containerization with Docker
- Cloud data warehousing with Snowflake
- Interactive dashboards with Python

### **Real-World Challenges Solved:**
1. **Duplicate Data:** Added deduplication logic to remove 83 duplicate records
2. **Data Quality:** Filtered out 0 invalid salary entries
3. **Idempotency:** Used TRUNCATE-INSERT pattern for safe re-runs
4. **Performance:** Batch inserts (1000 rows/batch) for speed
5. **Scalability:** Separated RAW and ANALYTICS layers for growth

---

## 🔮 Future Enhancements

- [ ] Add CI/CD pipeline with GitHub Actions
- [ ] Implement incremental loading (only new data)
- [ ] Add Great Expectations for data quality tests
- [ ] Build ML model for salary prediction
- [ ] Add email alerts on pipeline failures
- [ ] Deploy Airflow to Astronomer Cloud

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `airflow/dags/job_data_pipeline.py` | Main pipeline orchestration |
| `sql/transformations/clean_job_data.sql` | Data cleaning logic |
| `streamlit_app/dashboard.py` | Interactive dashboard |
| `scripts/load_initial_data.py` | CSV to Snowflake loader |
| `docker-compose.yml` | Airflow container setup |

---

## 👨‍💻 Author

**Utkarsha Chandgadkar**

- GitHub: [@Utkarshaaa13](https://github.com/Utkarshaaa13)
- LinkedIn: [Your Profile](YOUR_LINKEDIN_URL)
- Email: your.email@example.com

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- Apache Airflow community for excellent documentation
- Snowflake for cloud data warehouse platform
- Streamlit for rapid dashboard development

---


