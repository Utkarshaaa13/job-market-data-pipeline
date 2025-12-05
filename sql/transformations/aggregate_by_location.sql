-- Salary Analysis by Location
USE SCHEMA JOB_ANALYTICS.ANALYTICS;

TRUNCATE TABLE SALARY_BY_LOCATION;

INSERT INTO SALARY_BY_LOCATION (
    location,
    city,
    country,
    job_count,
    avg_salary_min,
    avg_salary_max,
    avg_salary_midpoint,
    median_salary,
    min_salary,
    max_salary
)
SELECT 
    location,
    city,
    country,
    COUNT(*) as job_count,
    ROUND(AVG(salary_min), 2) as avg_salary_min,
    ROUND(AVG(salary_max), 2) as avg_salary_max,
    ROUND(AVG(salary_avg), 2) as avg_salary_midpoint,
    ROUND(MEDIAN(salary_avg), 2) as median_salary,
    MIN(salary_min) as min_salary,
    MAX(salary_max) as max_salary
FROM JOB_LISTINGS_CLEAN
GROUP BY location, city, country
HAVING COUNT(*) >= 3
ORDER BY job_count DESC;
