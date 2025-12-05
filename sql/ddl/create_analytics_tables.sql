-- Analytics Tables
USE SCHEMA JOB_ANALYTICS.ANALYTICS;

-- Clean Job Listings
CREATE OR REPLACE TABLE JOB_LISTINGS_CLEAN (
    job_id NUMBER AUTOINCREMENT PRIMARY KEY,
    job_title VARCHAR(255),
    company VARCHAR(255),
    location VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    job_type VARCHAR(50),
    category VARCHAR(100),
    salary_min NUMBER(10,2),
    salary_max NUMBER(10,2),
    salary_avg NUMBER(10,2),
    experience_required NUMBER(5,2),
    publication_date DATE,
    skills_array ARRAY,
    skills_count NUMBER,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Salary Analysis by Location
CREATE OR REPLACE TABLE SALARY_BY_LOCATION (
    location VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    job_count NUMBER,
    avg_salary_min NUMBER(10,2),
    avg_salary_max NUMBER(10,2),
    avg_salary_midpoint NUMBER(10,2),
    median_salary NUMBER(10,2),
    min_salary NUMBER(10,2),
    max_salary NUMBER(10,2),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Salary Analysis by Job Title
CREATE OR REPLACE TABLE SALARY_BY_TITLE (
    job_title VARCHAR(255),
    job_count NUMBER,
    avg_salary_min NUMBER(10,2),
    avg_salary_max NUMBER(10,2),
    avg_salary_midpoint NUMBER(10,2),
    median_salary NUMBER(10,2),
    avg_experience NUMBER(5,2),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Skills Analysis
CREATE OR REPLACE TABLE SKILLS_DEMAND (
    skill_name VARCHAR(100),
    job_count NUMBER,
    avg_salary NUMBER(10,2),
    avg_experience NUMBER(5,2),
    top_job_titles ARRAY,
    top_companies ARRAY,
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Job Type Distribution
CREATE OR REPLACE TABLE JOB_TYPE_ANALYSIS (
    job_type VARCHAR(50),
    category VARCHAR(100),
    job_count NUMBER,
    avg_salary NUMBER(10,2),
    pct_of_total NUMBER(5,2),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Company Analysis
CREATE OR REPLACE TABLE COMPANY_INSIGHTS (
    company VARCHAR(255),
    total_positions NUMBER,
    avg_salary NUMBER(10,2),
    most_common_title VARCHAR(255),
    most_required_skills ARRAY,
    locations ARRAY,
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
