-- Skill mention frequency per category and country per snapshot date.
-- Each row represents one skill in one market segment on one day.
-- skill_posting_count is a lower bound because Adzuna truncates descriptions at around 500 characters,
-- so skills mentioned after that cutoff are invisible to us. The trend direction is still reliable
-- because the truncation is consistent across all snapshots.
CREATE TABLE IF NOT EXISTS gold_skill_frequency (
    snapshot_date       DATE,
    skill               TEXT,
    country             TEXT,
    category            TEXT,
    skill_posting_count INT,    -- Number of postings mentioning this skill. Lower bound due to truncation.
    total_postings      INT,    -- Total Silver postings for this country/category. Denominator for pct.
    pct_of_postings     FLOAT,  -- skill_posting_count / total_postings * 100.
    aggregated_at       TIMESTAMP,
    PRIMARY KEY (snapshot_date, skill, country, category)
);
