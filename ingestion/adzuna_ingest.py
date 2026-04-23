import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db_connection import get_connection
from dotenv import load_dotenv
import requests
import json 
from datetime import datetime



load_dotenv()
APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")


# Exit immediately if no contents in keys
if APP_ID is None or APP_KEY is None:
    raise SystemExit("APP_ID or APP_KEY missing. Check your .env file.")

# declare parameters
countries = ["us", "ca"]
categories = ["it-jobs", "accounting-finance-jobs"]
conn = get_connection() # open loop connection to the database
cursor = conn.cursor()
query = """
INSERT INTO bronze_job_postings (job_id, title, description,location, company, salary_min, salary_max, salary_is_predicted, created, category, ingested_at, country) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (job_id) DO NOTHING
"""


for country in countries:
    for category in categories:
        params = {"app_id" : APP_ID, "app_key": APP_KEY, "category" : category}
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise SystemExit(f"Error Ecountered for '{country}': {response.status_code}")
        data = response.json()

        # add country and time it was ingested at.
        for job in data["results"]:
            job["country"] = country
            job["ingested_at"] = datetime.now().isoformat()

            # execute sql to place data into table
            
            cursor.execute(query, (job["id"], job["title"], job["description"], job["location"]["display_name"], job["company"]["display_name"], job.get("salary_min"), job.get("salary_max"), job["salary_is_predicted"], job["created"], job["category"]["tag"], job["ingested_at"], job["country"]))
            
        # print(f"{country} / {category}: {len(data['results'])} jobs ingested")
        conn.commit()
conn.close() # close connection to the database

# BRONZE STATUS UP UNTIL THIS POINT