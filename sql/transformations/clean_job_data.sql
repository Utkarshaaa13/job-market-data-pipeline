-- Clean and transform raw job data
USE SCHEMA JOB_ANALYTICS.ANALYTICS;

TRUNCATE TABLE JOB_LISTINGS_CLEAN;

INSERT INTO JOB_LISTINGS_CLEAN (
    job_title,
    company,
    location,
    city,
    state,
    country,
    job_type,
    category,
    salary_min,
    salary_max,
    salary_avg,
    experience_required,
    publication_date,
    skills_array,
    skills_count
)
SELECT 
    TRIM(job_title) as job_title,
    TRIM(company) as company,
    TRIM(location) as location,
    -- Parse city from location
    CASE 
        WHEN POSITION(',' IN location) > 0 THEN TRIM(SPLIT_PART(location, ',', 1))
        ELSE TRIM(location)
    END as city,
    -- Parse state from location
    CASE 
        WHEN POSITION(',' IN location) > 0 THEN TRIM(SPLIT_PART(location, ',', 2))
        ELSE NULL
    END as state,
    -- Determine country
    CASE 
        WHEN location LIKE '%Germany%' THEN 'Germany'
        WHEN location LIKE '%Canada%' THEN 'Canada'
        WHEN location LIKE '%UK%' OR location LIKE '%United Kingdom%' THEN 'United Kingdom'
        WHEN location LIKE '%Remote%' THEN 'Remote'
        WHEN location = '' OR location IS NULL THEN 'Unknown'
        ELSE 'United States'
    END as country,
    COALESCE(NULLIF(TRIM(job_type), ''), 'Not Specified') as job_type,
    COALESCE(NULLIF(TRIM(category), ''), 'Not Specified') as category,
    salary_min,
    salary_max,
    (salary_min + salary_max) / 2 as salary_avg,
    experience_required,
    -- Convert publication_date to proper date format
    TRY_TO_DATE(publication_date, 'MM/DD/YYYY') as publication_date,
    -- Split skills into array
    CASE 
        WHEN skills IS NOT NULL AND TRIM(skills) != '' 
        THEN SPLIT(TRIM(skills), ',')
        ELSE ARRAY_CONSTRUCT()
    END as skills_array,
    -- Count skills
    CASE 
        WHEN skills IS NOT NULL AND TRIM(skills) != '' 
        THEN ARRAY_SIZE(SPLIT(TRIM(skills), ','))
        ELSE 0
    END as skills_count
FROM JOB_ANALYTICS.RAW_DATA.JOB_LISTINGS_RAW
WHERE job_title IS NOT NULL
  AND company IS NOT NULL
  AND salary_min > 0
  AND salary_max > salary_min;
