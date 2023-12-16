##############################################################################################################
### This program extracts music events from some of my favourite venues across Melbourne. ####################
### The aim is to compile the events into an organised output table, which can be filtered easily by date. ###
### This should save time spent browsing across multiple event webpages. #####################################
##############################################################################################################


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


# 2. Specify defaults
year = str(datetime.today().year)
options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("start-maximized")
options.add_argument("--disable-notifications")
venues = [
    "Brunswick Ballroom",
    "The Night Cat",
    "Croxton Bandroom",
    "Corner Hotel",
    "Northcote Theatre",
    "Northcote Social Club",
    "The Workers Club",
    "The Retreat",
    "Sub Club",
    "Miscellania",
    "Melbourne Recital Centre",
    "280 Sydney Rd",
    "Max Watt's Melbourne",
    "Sidney Myer Music Bowl",
    "Forum Melbourne",
    "Howler",
    "The Toff in Town"
]
addresses = [
    "2/401 Swanston St, VIC, Australia",
    "314 Sydney Rd, VIC, Australia",
    "137-141 Johnston St, VIC, Australia",
    "607 High St, VIC, Australia",
    "57 Swan St, VIC, Australia",
    "216 High St, VIC, Australia",
    "301 High St, VIC, Australia",
    "51 Brunswick St, VIC, Australia",
    "280 Sydney Road, VIC, Australia",
    "Flinders Ct, VIC, Australia",
    "31 Sturt St, VIC, Australia",
    "125 Swanston St, VIC, Australia",
    "Linlithgow Ave, VIC, Australia",
    "154 Flinders St, VIC, Australia",
    "7-11 Dawson St, VIC, Australia",
    "2/252 Swanston St, VIC, Australia"
]
address_venue_mapping = {
    "2/401 Swanston St": "Miscellania",
    "314 Sydney Rd": "Brunswick Ballroom",
    "137-141 Johnston St": "The Night Cat",
    "607 High St": "Croxton Bandroom",
    "57 Swan St": "Corner Hotel",
    "216 High St": "Northcote Theatre",
    "301 High St": "Northcote Social Club",
    "51 Brunswick St": "The Workers Club",
    "280 Sydney Road": "The Retreat",
    "Flinders Ct": "Sub Club",
    "31 Sturt St": "Melbourne Recital Centre",
    "125 Swanston St, VIC, Australia": "Max Watt's Melbourne",
    "Linlithgow Ave, VIC, Australia": "Sidney Myer Music Bowl",
    "154 Flinders St, VIC, Australia": "Forum Melbourne",
    "7-11 Dawson St, VIC, Australia": "Howler",
    "2/252 Swanston St, VIC, Australia": "The Toff in Town"
}
venue_address_mapping = {
    "Miscellania": "2/401 Swanston St",
    "Brunswick Ballroom": "314 Sydney Rd",
    "The Night Cat":"137-141 Johnston St",
    "Croxton Bandroom": "607 High St",
    "Corner Hotel": "57 Swan St",
    "Northcote Theatre": "216 High St",
    "Northcote Social Club": "301 High St",
    "The Workers Club": "51 Brunswick St",
    "The Retreat": "280 Sydney Road",
    "Sub Club": "Flinders Ct",
    "Melbourne Recital Centre": "31 Sturt St",
    "Max Watt's Melbourne": "125 Swanston St, VIC, Australia",
    "Sidney Myer Music Bowl": "Linlithgow Ave, VIC, Australia",
    "Forum Melbourne": "154 Flinders St, VIC, Australia",
    "Howler": "7-11 Dawson St, VIC, Australia",
    "The Toff in Town": "2/252 Swanston St, VIC, Australia"
}

def get_events_humanitix():
    '''
        Gets events from humanitix.com
        Here we need to input the addresses, rather than the names of the venues
        !!! NEEDS FIXING !!!
    '''
    try:
        driver = webdriver.Chrome()
    except:
        driver = webdriver.Chrome(
            executable_path="C:\\Users\\callanroff\\Desktop\\learnings\\Web Scraping/chromedriver_mac64\\chromedriver",
            chrome_options=options
        )
    driver.get("https://www.humanitix.com/au")
    time.sleep(1)
    df_final = pd.DataFrame({
        "Title": [""],
        "Date": [""],
        "Venue": [""],
        "Venue1": [""],
        "Link": [""]
    })
    for venue in ["Miscellania"]:
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
            #search_box.send_keys(Keys.ENTER)
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
                        #df = df.append({
                        #   "Title": title,
                        #    "Date": date,
                        #    "Venue": ven,
                        #    "Venue1": ven1,
                        #    "Link": link
                        #}, ignore_index=True)
                        df = df.reset_index(drop=True)
                else:
                    pass
                df_final = pd.concat([df_final, df], axis = 0).reset_index(drop = True)
                #df_final = df_final.append(df, ignore_index=True)
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


get_events_humanitix()