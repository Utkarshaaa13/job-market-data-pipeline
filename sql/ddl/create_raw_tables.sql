-- Raw Job Listings Table
USE SCHEMA JOB_ANALYTICS.RAW_DATA;

CREATE OR REPLACE TABLE JOB_LISTINGS_RAW (
    job_title VARCHAR(255),
    company VARCHAR(255),
    location VARCHAR(255),
    job_type VARCHAR(50),
    category VARCHAR(100),
    salary_min NUMBER(10,2),
    salary_max NUMBER(10,2),
    experience_required NUMBER(5,2),
    publication_date VARCHAR(50),
    skills VARCHAR(1000),
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    source_file VARCHAR(255)
);

-- Create file format for CSV
CREATE OR REPLACE FILE FORMAT CSV_FORMAT
TYPE = 'CSV'
FIELD_DELIMITER = '\t'
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
NULL_IF = ('NULL', 'null', '')
EMPTY_FIELD_AS_NULL = TRUE
TRIM_SPACE = TRUE;

-- Create stage for data loading
CREATE OR REPLACE STAGE JOB_DATA_STAGE
FILE_FORMAT = CSV_FORMAT;
