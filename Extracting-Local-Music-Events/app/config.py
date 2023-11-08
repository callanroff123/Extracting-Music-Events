# Import required libraries 
import os
from pathlib import Path


# Speicify path defaults
APP_PATH = Path(os.environ["PYTHONPATH"])
OUTPUT_PATH = APP_PATH / "output/"


# Email
SMTP_SERVER = "smtp.gmail.com"
PORT = 465
