-- Average salary metrics per category and country per snapshot date.
-- Only postings with both salary_min and salary_max are included.
-- Salaries are never mixed across countries since USD and CAD are not comparable.
CREATE TABLE IF NOT EXISTS gold_salary_trend (
    snapshot_date           DATE,
    category                TEXT,
    country                 TEXT,
    total_salary_postings   INT,    -- Postings with any salary data. Denominator for all salary metrics.
    posting_count_predicted INT,    -- How many salaries are Adzuna estimates vs employer-reported.
                                    -- High ratio means most figures are modeled, not directly observed.
    avg_midpoint            FLOAT,  -- Average of (salary_min + salary_max) / 2. Use this for trend charts.
    avg_salary_min          FLOAT,
    avg_salary_max          FLOAT,
    aggregated_at           TIMESTAMP,
    PRIMARY KEY (snapshot_date, category, country)
);
