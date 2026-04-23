CREATE TABLE IF NOT EXISTS bronze_job_postings (
    job_id              TEXT PRIMARY KEY,
    title               TEXT,
    description         TEXT,
    location            TEXT,
    company             TEXT,
    salary_min          FLOAT,
    salary_max          FLOAT,
    salary_is_predicted TEXT,
    created             TEXT,
    category            TEXT,
    ingested_at         TIMESTAMP,
    country             TEXT,
    redirect_url        TEXT,
    contract_type       TEXT
);
