-- Raw job postings exactly as returned by the Adzuna API.
-- Bronze is never modified after ingestion. It is the source of truth for reprocessing.
-- country and ingested_at are the only fields we add ourselves.
CREATE TABLE IF NOT EXISTS bronze_job_postings (
    job_id              TEXT PRIMARY KEY,   -- Adzuna's unique ID. Stored as TEXT, never cast to integer.
    title               TEXT,
    description         TEXT,              -- Truncated at around 500 characters by Adzuna's free tier.
    location            TEXT,              -- Flattened from location.display_name at ingestion time.
    company             TEXT,              -- Flattened from company.display_name at ingestion time.
    salary_min          FLOAT,             -- Not always present. Use .get() when reading in Python.
    salary_max          FLOAT,             -- Not always present. Use .get() when reading in Python.
    salary_is_predicted TEXT,              -- "0" or "1" as a string. Converted to boolean in Silver.
    created             TEXT,              -- Raw ISO date string from Adzuna. Converted to DATE in Silver.
    category            TEXT,              -- Flattened from category.tag. "it-jobs" or "accounting-finance-jobs".
    ingested_at         TIMESTAMP,         -- Set by us at pipeline run time.
    country             TEXT,              -- Set by us. Adzuna does not include this in the response.
    redirect_url        TEXT,              -- Link to the full job posting. May be null.
    contract_type       TEXT               -- e.g. "permanent", "contract". Not always present.
);
