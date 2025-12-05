-- Salary Analysis by Job Title
USE SCHEMA JOB_ANALYTICS.ANALYTICS;

-- By Job Title
TRUNCATE TABLE SALARY_BY_TITLE;

INSERT INTO SALARY_BY_TITLE (
    job_title,
    job_count,
    avg_salary_min,
    avg_salary_max,
    avg_salary_midpoint,
    median_salary,
    avg_experience
)
SELECT 
    job_title,
    COUNT(*) as job_count,
    ROUND(AVG(salary_min), 2) as avg_salary_min,
    ROUND(AVG(salary_max), 2) as avg_salary_max,
    ROUND(AVG(salary_avg), 2) as avg_salary_midpoint,
    ROUND(MEDIAN(salary_avg), 2) as median_salary,
    ROUND(AVG(experience_required), 2) as avg_experience
FROM JOB_LISTINGS_CLEAN
GROUP BY job_title
HAVING COUNT(*) >= 3
ORDER BY job_count DESC;

-- Job Type Distribution
TRUNCATE TABLE JOB_TYPE_ANALYSIS;

INSERT INTO JOB_TYPE_ANALYSIS (
    job_type,
    category,
    job_count,
    avg_salary,
    pct_of_total
)
WITH total_jobs AS (
    SELECT COUNT(*) as total FROM JOB_LISTINGS_CLEAN
)
SELECT 
    job_type,
    category,
    COUNT(*) as job_count,
    ROUND(AVG(salary_avg), 2) as avg_salary,
    ROUND((COUNT(*) * 100.0 / (SELECT total FROM total_jobs)), 2) as pct_of_total
FROM JOB_LISTINGS_CLEAN
GROUP BY job_type, category
ORDER BY job_count DESC;

-- Company Insights
TRUNCATE TABLE COMPANY_INSIGHTS;

INSERT INTO COMPANY_INSIGHTS (
    company,
    total_positions,
    avg_salary,
    most_common_title,
    most_required_skills,
    locations
)
WITH company_stats AS (
    SELECT 
        company,
        COUNT(*) as total_positions,
        AVG(salary_avg) as avg_salary,
        MODE(job_title) as most_common_title,
        ARRAY_AGG(DISTINCT location) as locations
    FROM JOB_LISTINGS_CLEAN
    GROUP BY company
),
company_skills AS (
    SELECT 
        c.company,
        ARRAY_AGG(DISTINCT TRIM(skill.value::STRING)) WITHIN GROUP (ORDER BY TRIM(skill.value::STRING)) as all_skills
    FROM JOB_LISTINGS_CLEAN c,
    LATERAL FLATTEN(input => c.skills_array) skill
    WHERE skill.value IS NOT NULL
    GROUP BY c.company
)
SELECT 
    cs.company,
    cs.total_positions,
    ROUND(cs.avg_salary, 2) as avg_salary,
    cs.most_common_title,
    csk.all_skills as most_required_skills,
    cs.locations
FROM company_stats cs
LEFT JOIN company_skills csk ON cs.company = csk.company
WHERE cs.total_positions >= 3
ORDER BY cs.total_positions DESC;
