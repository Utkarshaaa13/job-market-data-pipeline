-- Skills Demand Analysis
USE SCHEMA JOB_ANALYTICS.ANALYTICS;

TRUNCATE TABLE SKILLS_DEMAND;

-- First, create a flattened skills table
CREATE OR REPLACE TEMPORARY TABLE SKILLS_FLATTENED AS
SELECT 
    job_id,
    job_title,
    company,
    salary_avg,
    experience_required,
    TRIM(skill.value::STRING) as skill_name
FROM JOB_LISTINGS_CLEAN,
LATERAL FLATTEN(input => skills_array) skill
WHERE skill.value IS NOT NULL AND TRIM(skill.value::STRING) != '';

-- Aggregate skills data
INSERT INTO SKILLS_DEMAND (
    skill_name,
    job_count,
    avg_salary,
    avg_experience,
    top_job_titles,
    top_companies
)
SELECT 
    skill_name,
    COUNT(DISTINCT job_id) as job_count,
    ROUND(AVG(salary_avg), 2) as avg_salary,
    ROUND(AVG(experience_required), 2) as avg_experience,
    ARRAY_AGG(DISTINCT job_title) WITHIN GROUP (ORDER BY job_title) as top_job_titles,
    ARRAY_AGG(DISTINCT company) WITHIN GROUP (ORDER BY company) as top_companies
FROM SKILLS_FLATTENED
GROUP BY skill_name
HAVING COUNT(DISTINCT job_id) >= 5
ORDER BY job_count DESC;
