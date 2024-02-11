# Until we figure out how to get the dang venv working grrrrr
import os
import sys
sys.path.append("/Users/callanroff/Desktop/Extracting-Music-Events")
os.environ["PYTHONPATH"]="/Users/callanroff/Desktop/Extracting-Music-Events"


# 1. Import modules
from app.post_extraction_tasks import clean_and_export, send_email, push_output_to_db


# 2. Execute end-to-end app pipeline
# TO-DO: Build a local airflow job. Each function should be its own DAG.
if __name__ == "__main__":
    clean_and_export.export_events()
    send_email.run_send_email()
    push_output_to_db.run_postgres_push()