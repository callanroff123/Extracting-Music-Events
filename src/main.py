# Allow relative imports
import os
import sys
ENV = os.environ.get("VIRTUAL_ENV")
ENV_SPLIT = ENV.split("/")
PYTHONPATH = "/".join(i for i in ENV_SPLIT if i != "venv")
os.environ["PYTHONPATH"] = PYTHONPATH
sys.path.append(PYTHONPATH)


# 1. Import modules
from src.post_extraction_tasks import clean_and_export, send_email, push_output_to_db


# 2. Execute end-to-end app pipeline
# TO-DO: Build a local airflow job. Each function should be its own DAG.
if __name__ == "__main__":
    clean_and_export.export_events()
    send_email.run_send_email()
    push_output_to_db.run_postgres_push()