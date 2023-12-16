#########################
### Gets events from: ###
### * The Retreat #######
### * Sub Club ##########
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
from app.config import venues, addresses, venue_address_mapping, address_venue_mapping


# 2. Specify defaults
year = str(datetime.today().year)
options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("start-maximized")
options.add_argument("--disable-notifications")
venues_eventbrite = [
    i for i in venues if i in [
        "280 Sydney Rd",
        "Sub Club"
    ]
]


def get_events_eventbrite():
    '''
        Gets events from eventbrite.com.au
    '''
    driver = webdriver.Chrome()
    time.sleep(1)
    df_final = pd.DataFrame({
        "Title": [""],
        "Date": [""],
        "Venue": [""],
        "Venue1": [""],
        "Link": [""]
    })
    for venue in venues_eventbrite:
        try:
            driver.get(f"https://www.eventbrite.com.au/d/australia--melbourne/{venue.replace(' ', '-')}/")
            time.sleep(1)
            soup = BeautifulSoup(
                driver.page_source, "html"
            )
            postings = soup.find_all(
                "li", {"class": "search-main-content__events-list-item search-main-content__events-list-item__mobile"})
            df = pd.DataFrame({
                "Title": [""],
                "Date": [""],
                "Venue": [""],
                "Venue1": [""],
                "Link": [""]
            })
            for post in postings:
                title = post.find(
                    "h2", {"class": "Typography_root__4bejd #3a3247 Typography_body-lg__4bejd event-card__clamp-line--two Typography_align-match-parent__4bejd"}).text.strip()
                ven = venue.split(",", 1)[0]
                ven1 = post.find_all(
                    "p", {"class": "Typography_root__4bejd #585163 Typography_body-md__4bejd event-card__clamp-line--one Typography_align-match-parent__4bejd"})[0].text.strip()
                date = post.find_all(
                    "p", {"class": "Typography_root__4bejd #585163 Typography_body-md__4bejd event-card__clamp-line--one Typography_align-match-parent__4bejd"})[1].text.strip()
                link = post.find(
                    "a", {"class": "event-card-link"}).get("href")
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
            time.sleep(1)
        except:
            pass
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
    df_final["Date"] = df_final["Date"].str.replace(",", "")
    df_final["Date"] = df_final["Date"].str[4:10] + " " + \
        str(datetime.today().year)
    return(df_final)
