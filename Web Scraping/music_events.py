##############################################################################################################
### This program extracts music events from some of my favourite venues across Melbourne. ####################
### The aim is to compile the events into an organised output table, which can be filtered easily by date. ###
### This should save time spent browsing across multiple event webpages. #####################################
##############################################################################################################

# 1. Load required libraries.
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
import lxml
import html
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller

# 2. Specify credentials and defaults
options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("start-maximized")
options.add_argument("--disable-notifications")
venues = [
    "Brunswick Ballroom",
    "The Night Cat",
    "The Croxton Bandroom",
    "Corner Hotel",
    "Northcote Theatre",
    "Northcote Social Club",
    "The Workers Club",
    "The Retreat",
    "Sub Club",
    "Miscellania",
    "Melbourne Recital Centre"
]

# 3a. Get events from moshtix.com.au


def get_events_moshtix():
    driver = webdriver.Chrome(
        executable_path="C:\\Users\\callanroff\\Desktop\\learnings\\Web Scraping/chromedriver_mac64\\chromedriver",
        chrome_options=options
    )
    driver.get("https://www.moshtix.com.au/v2/")
    time.sleep(1)
    df_final = pd.DataFrame({
        "Title": [""],
        "Date": [""],
        "Venue": [""],
        "Link": [""]
    })
    for venue in venues:
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
            df = df.append({
                "Title": title,
                "Date": date,
                "Venue": ven,

                "Link": link
            }, ignore_index=True)
            df = df.reset_index(drop=True)
        df_final = df_final.append(df, ignore_index=True)
        driver.find_element(
            By.XPATH,
            '//*[@id="header"]/nav/ul/li[1]/a'
        ).click()
        time.sleep(1)
    return(df_final[df_final["Title"] != ""].reset_index(drop=True))

# 3b. Get events from oztix.com.au


def get_events_oztix():
    driver = webdriver.Chrome(
        executable_path="C:\\Users\\callanroff\\Desktop\\learnings\\Web Scraping/chromedriver_mac64\\chromedriver",
        chrome_options=options
    )
    driver.get("https://www.oztix.com.au/")
    time.sleep(1)
    df_final = pd.DataFrame({
        "Title": [""],
        "Date": [""],
        "Venue": [""],
        "Venue1": [""],
        "Link": [""]
    })
    for venue in venues:
        search = venue
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
            df = df.append({
                "Title": title,
                "Date": date,
                "Venue": ven,
                "Venue1": ven1,
                "Link": link
            }, ignore_index=True)
            df = df.reset_index(drop=True)
        df_final = df_final.append(df, ignore_index=True)
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

# 4. Concatenate results across various websites, and remove duplicate events (by date and venue).


def get_all_events():
    df_moshtix = get_events_moshtix()
    df_oztix = get_events_oztix()
    df = pd.concat([df_moshtix, df_oztix], axis=0).reset_index(drop=True)
    return(df)

# 5. Export output to CSV format.


def export_events():
    df = get_all_events()
    df.to_csv("music_events.csv")
