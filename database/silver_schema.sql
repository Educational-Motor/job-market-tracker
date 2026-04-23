CREATE TABLE IF NOT EXISTS silver_job_postings (
    job_id              TEXT PRIMARY KEY,
    title               TEXT,
    description         TEXT,
    location            TEXT,
    company             TEXT,
    salary_min          FLOAT,
    salary_max          FLOAT,
    salary_is_predicted BOOLEAN,
    created             DATE,
    category            TEXT,
    country             TEXT,
    work_type           TEXT,
    skills              TEXT[],
    transformed_at      TIMESTAMP
);
