-- Total job postings per category and country per snapshot date.
-- This tracks market volume over time, not which specific roles are trending.
-- Category granularity is intentional. Free-text title classification would introduce
-- invented taxonomy that can't be defended. Adzuna's own categories are the canonical source.
CREATE TABLE IF NOT EXISTS gold_role_demand (
    snapshot_date   DATE,
    category        TEXT,
    country         TEXT,
    total_postings  INT,        -- Total Silver postings for this category/country as of snapshot_date.
    aggregated_at   TIMESTAMP,
    PRIMARY KEY (snapshot_date, category, country)
);
