import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db_connection import get_connection
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

# Load API credentials from .env file. Never hardcode these.
load_dotenv()
APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

# Fail loudly if credentials are missing rather than making broken API calls.
if APP_ID is None or APP_KEY is None:
    raise SystemExit("APP_ID or APP_KEY missing. Check your .env file.")

# We pull from two countries and two job categories, so four API calls per run.
countries = ["us", "ca"]
categories = ["it-jobs", "accounting-finance-jobs", "engineering-jobs"]

# One connection for the entire run. Opening a new connection per iteration is unnecessary overhead.
conn = get_connection()
cursor = conn.cursor()

# ON CONFLICT DO NOTHING handles duplicates gracefully if the same posting appears across runs.
query = """
INSERT INTO bronze_job_postings (job_id, title, description, location, company, salary_min, salary_max, salary_is_predicted, created, category, ingested_at, country, redirect_url, contract_type)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (job_id) DO NOTHING
"""

for country in countries:
    for category in categories:
        params = {"app_id": APP_ID, "app_key": APP_KEY, "category": category, "results_per_page": 50}
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise SystemExit(f"Error Ecountered for '{country}': {response.status_code}")

        # Store the parsed response once. Calling .json() twice creates two separate dicts.
        data = response.json()

        for job in data["results"]:
            # Adzuna doesn't include country or ingestion time in the response, so we add them ourselves.
            job["country"] = country
            job["ingested_at"] = datetime.now().isoformat()

            # salary_min, salary_max, redirect_url, and contract_type are not always present, so we use .get().
            cursor.execute(query, (
                job["id"], job["title"], job["description"],
                job.get("location", {}).get("display_name"), job.get("company", {}).get("display_name"),
                job.get("salary_min"), job.get("salary_max"),
                job["salary_is_predicted"], job["created"],
                job["category"]["tag"], job["ingested_at"], job["country"],
                job.get("redirect_url"), job.get("contract_type")
            ))

        # Commit after each country/category batch so a crash midway doesn't roll back everything.
        conn.commit()

conn.close()
