#########################
### Gets events from: ###
### * The Forum #########
#########################


# 1. Load required libraries.
from pathlib import Path
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
import lxml
import html
import time
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller
from src.config import venues, addresses, venue_address_mapping, address_venue_mapping


# 2. Specify defaults
year = str(datetime.today().year)
options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("start-maximized")
options.add_argument("--disable-notifications")
venues_ticketek = [i for i in venues if i in ["Forum Melbourne"]]


def get_events_ticketek():
    '''
        Gets events from premier.ticketek.com.au (for the Forum only)
    '''
    driver = webdriver.Chrome()
    driver.get("https://premier.ticketek.com.au")
    time.sleep(2)
    df = pd.DataFrame({
        "Title": [""],
        "Date": [""],
        "Venue": [""],
        "Venue1": [""],
        "Link": [""]
    })
    venue = "Forum Melbourne"
    search = venue
    search_box = driver.find_element(
        By.XPATH,
        '/html/body/form/header/div/div[3]/div/input'
    )
    search_box.send_keys(search)
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)
    soup = BeautifulSoup(
        driver.page_source, "html"
    )
    results_raw = soup.find_all(
        "div", {"class": "contentEvent"}
    )
    result_titles = [results_raw[i].find("h6").text.strip() for i in range(len(results_raw))]
    result_index = result_titles.index(venue)
    result_link = "https://premier.ticketek.com.au" + soup.find_all(
        "a", {"class": "blueGradientButton"}
    )[result_index].get("href")
    driver.get(result_link)
    soup = BeautifulSoup(
        driver.page_source, "html"
    )
    postings = soup.find_all(
        "div", {"class": "show"}
    )
    for post in postings:
        text = post.find(
            "div", {"class": "text-content"}
        )
        title = text.find("h3").text.strip()
        ven = venue.split(",", 1)[0]
        ven1 = text.find_all("p")[-1].text.strip()
        date = text.find_all("p")[-2].text.strip()
        link = post.find(
            "a", {"class": "btn btn-primary"}
        ).get("href")
        df = pd.concat(
            [df, pd.DataFrame({
                "Title": title,
                "Date": date,
                "Venue": ven,
                "Venue1": ven1,
                "Link": link
            }, index = [0])], axis = 0
        ).reset_index(drop = True)
        df = df.reset_index(drop=True)
    df = df[df["Title"] != ""].reset_index(drop=True)
    df["correct_venue_flag"] = np.zeros(df.shape[0])
    for i in range(df.shape[0]):
        if df["Venue"][i] in df["Venue1"][i]:
            df["correct_venue_flag"][i] = 1
        else:
            df["correct_venue_flag"][i] = 0
    df = df[[
        "Title",
        "Date",
        "Venue",
        "Link"]]
    return(df)