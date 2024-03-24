#########################################
### Gets events from: ###################
### * Miscellania (2/401 Swanston St) ###
#########################################


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
venues_humanitix = [i for i in venues if i in ["Miscellania"]]


def get_events_humanitix():
    '''
        Gets events from humanitix.com
    '''
    driver = webdriver.Chrome()
    driver.get("https://www.humanitix.com/au")
    time.sleep(1)
    df_final = pd.DataFrame({
        "Title": [""],
        "Date": [""],
        "Venue": [""],
        "Venue1": [""],
        "Link": [""]
    })
    for venue in venues_humanitix:
        try:
            search = venue
            driver.find_element(
                By.XPATH,
                '/html/body/div/main/div[1]/div[2]/div[2]/a[1]'
            ).click()
            time.sleep(1)
            search_box = driver.find_element(
                By.XPATH,
                '/html/body/div/main/section[1]/div/form/div[1]/input'
            )
            loc_box = driver.find_element(
                By.XPATH,
                '/html/body/div/main/section[1]/div/form/div[3]/div/div/div[1]/div[2]/div/input'
            )
            search_box.send_keys(search)
            loc_box.send_keys("Melbourne")
            driver.find_element(
                By.XPATH,
                '/html/body/div/main/section[1]/div/form/div[3]/button[2]'
            ).click()
            time.sleep(1)
            soup = BeautifulSoup(
                driver.page_source, "html"
            )
            try:
                postings = soup.find(
                    "div", {"class": "sc-7cff7b5b-1 fTZqOn"}).find_all("a")
                df = pd.DataFrame({
                    "Title": [""],
                    "Date": [""],
                    "Venue": [""],
                    "Venue1": [""],
                    "Link": [""]
                })
                if len(postings) > 0:
                    for post in postings:
                        title = post.find(
                            "h6", {"class": "sc-404b905e-0 sc-eb5cf798-4 hkMovf jGLtBE"}).text.strip()
                        date = post.find(
                            "p", {"class": "sc-8821f522-0 sc-eb5cf798-3 swyla bpXsMF"}).text.strip()
                        ven = venue.split(",", 1)[0]
                        ven1 = post.find(
                            "p", {"class": "sc-8821f522-0 sc-eb5cf798-5 swyla hwxiUz"}).text.strip()
                        link = post.get("href")
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
                else:
                    pass
                df_final = pd.concat([df_final, df], axis = 0).reset_index(drop = True)
                driver.find_element(
                    By.XPATH,
                    '/html/body/div/header/a'
                ).click()
                time.sleep(1)
            except:
                driver.find_element(
                    By.XPATH,
                    '/html/body/div/header/a'
                ).click()
        except:
            pass
    df_final = df_final[df_final["Title"] != ""].reset_index(drop=True)
    df_final["correct_venue_flag"] = np.zeros(df_final.shape[0])
    for i in range(df_final.shape[0]):
        try:
            x = venue_address_mapping[df_final["Venue"][i]]
        except:
            x = "------------------------------------------"
        if (df_final["Venue"][i] in df_final["Venue1"][i]) or (x in df_final["Venue1"][i]):
            df_final["correct_venue_flag"][i] = 1
        else:
            df_final["correct_venue_flag"][i] = 0
    df_final = df_final[df_final["correct_venue_flag"] == 1][[
        "Title",
        "Date",
        "Venue",
        "Link"
    ]].reset_index(drop=True)
    df_final["Date"] = [item[1] + " " + item[2] + " " + item[3][:-1]
                        for item in df_final["Date"].str.split(" ")]
    return(df_final)