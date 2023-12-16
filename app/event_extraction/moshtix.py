############################
### Gets events from: ######
### * Brunswick Ballroom ###
### * The Toff in Town #####
### * Northcote Theatre ####
### * The Night Cat ########
### * Howler ###############
### * Kindred Bandroom #####
### * 170 Russell ##########
############################


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
venues_moshtix = [
    i for i in venues if i in [
        "Brunswick Ballroom",
        "The Toff in Town",
        "Northcote Theatre",
        "The Night Cat",
        "Howler",
        "Kindred Bandroom",
        "170 Russell"
    ]
]


def get_events_moshtix():
    '''
        Gets events from moshtix.com
    '''
    driver = webdriver.Chrome()
    driver.get("https://www.moshtix.com.au/v2/")
    time.sleep(1)
    df_final = pd.DataFrame({
        "Title": [""],
        "Date": [""],
        "Venue": [""],
        "Link": [""]
    })
    for venue in venues_moshtix:
        search = venue
        search_box = driver.find_element(
            By.XPATH,
            '//*[@id="query"]'
        )
        search_box.send_keys(search)
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)
        soup = BeautifulSoup(
            driver.page_source, "html"
        )
        postings = soup.find_all("div", {"class": "searchresult clearfix"})
        df = pd.DataFrame({
            "Title": [""],
            "Date": [""],
            "Venue": [""],
            "Link": [""]
        })
        for post in postings:
            title = post.find(
                "h2", {"class": "main-event-header"}).text.strip()
            date = post.find(
                "h2", {"class": "main-artist-event-header"}).text.strip()
            date = date.split(",", 1)[0]
            ven = venue.split(",", 1)[0]
            link = post.find(
                "h2", {"class": "main-event-header"}).find("a").get("href")
            df = pd.concat(
                [df, pd.DataFrame({
                    "Title": title,
                    "Date": date,
                    "Venue": ven,
                    "Link": link
                }, index = [0])], axis = 0
            ).reset_index(drop = True)
            df = df.reset_index(drop=True)
        df_final = pd.concat([df_final, df], axis = 0).reset_index(drop = True)
        driver.find_element(
            By.XPATH,
            '//*[@id="header"]/nav/ul/li[1]/a'
        ).click()
        time.sleep(1)
    return(df_final[df_final["Title"] != ""].reset_index(drop=True))