################################
### Gets events from: ##########
### *  Northcote Social Club ###
### * The Workers Club #########
### * Corner Hotel #############
### * Croxton Bandroom #########
### * Max Watt's Melbourne #####
### * Gasometer ################
################################


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
from app.config import venues, addresses, venue_address_mapping, address_venue_mapping


# 2. Specify defaults
year = str(datetime.today().year)
options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("start-maximized")
options.add_argument("--disable-notifications")
venues_oztix = [
    i for i in venues if i in [
        "Northcote Social Club",
        "The Workers Club",
        "Corner Hotel",
        "Croxton Bandroom",
        "Max Watt's Melbourne",
        "Gasometer (Upstairs)",
        "Gasometer Downstairs"
    ]
]


def get_events_oztix():
    '''
        Gets events from oztix.com.au
    '''
    driver = webdriver.Chrome()
    driver.get("https://www.oztix.com.au/")
    time.sleep(1)
    df_final = pd.DataFrame({
        "Title": [""],
        "Date": [""],
        "Venue": [""],
        "Venue1": [""],
        "Link": [""]
    })
    for venue in venues_oztix:
        search = venue
        time.sleep(1)
        search_box = driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/header/div[3]/div/form/label/input'
        )
        search_box.send_keys(search)
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)
        soup = BeautifulSoup(
            driver.page_source, "html"
        )
        postings = soup.find_all("li", {"tabindex": "-1"})
        df = pd.DataFrame({
            "Title": [""],
            "Date": [""],
            "Venue": [""],
            "Venue1": [""],
            "Link": [""]
        })
        for post in postings:
            title = post.find(
                "h3", {"class": "event-details__name"}).text.strip()
            date = post.find("div", {"class": "event-when"}).text.strip()
            ven = venue.split(",", 1)[0]
            ven1 = post.find("p", {"class": "detail"}).text.strip()
            link = post.find(
                "a", {"class": "search-event_container"}).get("href")
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
        df_final = pd.concat([df_final, df], axis = 0).reset_index(drop = True)
        driver.find_element(
            By.XPATH,
            '//*[@id="app"]/div/header/div[1]/a'
        ).click()
        time.sleep(1)
    df_final = df_final[df_final["Title"] != ""].reset_index(drop=True)
    df_final["correct_venue_flag"] = np.zeros(df_final.shape[0])
    for i in range(df_final.shape[0]):
        if df_final["Venue"][i] in df_final["Venue1"][i]:
            df_final["correct_venue_flag"][i] = 1
        else:
            df_final["correct_venue_flag"][i] = 0
    df_final = df_final[df_final["correct_venue_flag"] == 1][[
        "Title",
        "Date",
        "Venue",
        "Link"
    ]].reset_index(drop=True)
    df_final["Date"] = df_final["Date"].str[:3] + " " + \
        df_final["Date"].str[3:] + str(datetime.today().year)
    return(df_final)