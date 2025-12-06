# 📊 Data Model Documentation

## Overview

Simple two-layer architecture for job market analytics.

---

## 🏗️ Architecture
```
RAW_DATA (Bronze)          ANALYTICS (Gold)
     ↓                           ↓
JOB_LISTINGS_RAW  →  JOB_LISTINGS_CLEAN  →  [Aggregation Tables]
(250 rows)              (167 unique jobs)
```

**Pattern:** Medallion Architecture (Bronze → Gold)

---

## 📋 Table Schemas

### **Bronze Layer: RAW_DATA.JOB_LISTINGS_RAW**

**Purpose:** Store original CSV data unchanged

| Column | Type | Example |
|--------|------|---------|
| job_title | VARCHAR | "Senior Data Engineer" |
| company | VARCHAR | "TechCorp" |
| location | VARCHAR | "Austin, TX" |
| salary_min | NUMBER | 120000 |
| salary_max | NUMBER | 180000 |
| skills | VARCHAR | "Python, SQL, Airflow" |
| load_timestamp | TIMESTAMP | Auto-generated |

---

### **Gold Layer: ANALYTICS.JOB_LISTINGS_CLEAN**

**Purpose:** Clean, deduplicated jobs with parsed fields

| Column | Type | How Created |
|--------|------|-------------|
| job_id | NUMBER | Auto-increment |
| job_title | VARCHAR | From raw data |
| company | VARCHAR | From raw data |
| city | VARCHAR | `SPLIT_PART(location, ',', 1)` |
| state | VARCHAR | `SPLIT_PART(location, ',', 2)` |
| salary_avg | NUMBER | `(salary_min + salary_max) / 2` |
| skills_array | ARRAY | `SPLIT(skills, ',')` |
| skills_count | NUMBER | `ARRAY_SIZE(skills_array)` |

**Filters Applied:**
- Remove NULL job titles and companies
- Remove invalid salaries (salary_min > 0, salary_max > salary_min)
- Deduplicate by job_title + company using `ROW_NUMBER()`

**Result:** 250 rows → 167 unique jobs

---

### **Gold Layer: Aggregation Tables**

#### `SALARY_BY_LOCATION`
```sql
SELECT city, AVG(salary_avg), COUNT(*) 
FROM JOB_LISTINGS_CLEAN 
GROUP BY city
```

| Column | Description |
|--------|-------------|
| city | City name |
| avg_salary_midpoint | Average salary |
| job_count | Number of jobs |

---

#### `SKILLS_DEMAND`
```sql
SELECT skill_name, COUNT(*), AVG(salary_avg)
FROM JOB_LISTINGS_CLEAN,
LATERAL FLATTEN(skills_array)
GROUP BY skill_name
```

| Column | Description |
|--------|-------------|
| skill_name | Skill/technology |
| job_count | Jobs requiring this skill |
| avg_salary | Average salary for this skill |

---

#### `COMPANY_INSIGHTS`
```sql
SELECT company, COUNT(*), AVG(salary_avg)
FROM JOB_LISTINGS_CLEAN
GROUP BY company
```

| Column | Description |
|--------|-------------|
| company | Company name |
| total_positions | Open positions |
| avg_salary | Average salary offered |

---

## 🔄 Data Flow
```
CSV File (250 rows)
    ↓
RAW_DATA.JOB_LISTINGS_RAW
    ↓
Clean + Deduplicate
    ↓
ANALYTICS.JOB_LISTINGS_CLEAN (167 rows)
    ↓
    ├─→ SALARY_BY_LOCATION
    ├─→ SKILLS_DEMAND
    ├─→ COMPANY_INSIGHTS
    ├─→ JOB_TYPE_ANALYSIS
    └─→ SALARY_BY_TITLE
```

---

## 🎯 Key Transformations

**Location Parsing:**
```
"Austin, TX" → city: "Austin", state: "TX"
```

**Skills Array:**
```
"Python, SQL, AWS" → ["Python", "SQL", "AWS"]
```

**Deduplication:**
```
Same job posted twice → Keep only first occurrence
250 rows → 167 unique jobs
```

**Salary Average:**
```
Min: $120K, Max: $180K → Avg: $150K
```

---

## 📊 Sample Data

**JOB_LISTINGS_CLEAN:**
```
job_id | job_title            | city    | salary_avg | skills_array
1      | Senior Data Engineer | Austin  | 150000     | [Python, SQL, Airflow]
2      | ML Engineer          | Seattle | 165000     | [Python, TensorFlow, AWS]
```

**SALARY_BY_LOCATION:**
```
city       | avg_salary_midpoint | job_count
Seattle    | 159761              | 25
Austin     | 145230              | 45
```

**SKILLS_DEMAND:**
```
skill_name         | job_count | avg_salary
Machine Learning   | 284       | 142500
Python             | 245       | 135000
```

---

**Author:** Utkarsha Chandgadkar  
**Last Updated:** December 2025
