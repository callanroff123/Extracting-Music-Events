# Import required libraries 
import os
from pathlib import Path


# Speicify path defaults
APP_PATH = Path(os.environ["PYTHONPATH"])
OUTPUT_PATH = APP_PATH / "output/"
CHROMEDRIVER_PATH = APP_PATH / "chromedriver_mac64/chromedriver"


# Email
SMTP_SERVER = "smtp.gmail.com"
PORT = 465
