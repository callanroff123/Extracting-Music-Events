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
from datetime import timedelta
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
    "Croxton Bandroom",
    "Corner Hotel",
    "Northcote Theatre",
    "Northcote Social Club",
    "The Workers Club",
    "The Retreat",
    "Sub Club",
    "Miscellania",
    "Melbourne Recital Centre",
    "280 Sydney Rd"
]


def get_events_moshtix():
    '''
        Gets events from moshtix.com
    '''
    driver = webdriver.Chrome(
        executable_path="C:\\Users\\callanroff\\Desktop\\learnings\\Web Scraping/chromedriver_mac64\\chromedriver",
        chrome_options=options
    )
    driver.get("https://www.moshtix.com.au/v2/")
    time.sleep(2)
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
        time.sleep(2)
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
        time.sleep(2)
    return(df_final[df_final["Title"] != ""].reset_index(drop=True))


def get_events_oztix():
    '''
        Gets events from oztix.com.au
    '''
    driver = webdriver.Chrome(
        executable_path="C:\\Users\\callanroff\\Desktop\\learnings\\Web Scraping/chromedriver_mac64\\chromedriver",
        chrome_options=options
    )
    driver.get("https://www.oztix.com.au/")
    time.sleep(2)
    df_final = pd.DataFrame({
        "Title": [""],
        "Date": [""],
        "Venue": [""],
        "Venue1": [""],
        "Link": [""]
    })
    for venue in venues:
        search = venue
        time.sleep(2)
        search_box = driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/header/div[3]/div/form/label/input'
        )
        search_box.send_keys(search)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
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
        time.sleep(2)
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


def get_events_eventbrite():
    '''
        Gets events from eventbrite.com.au
    '''
    driver = webdriver.Chrome(
        executable_path="C:\\Users\\callanroff\\Desktop\\learnings\\Web Scraping/chromedriver_mac64\\chromedriver",
        chrome_options=options
    )
    driver.get("https://www.eventbrite.com.au/")
    time.sleep(2)
    df_final = pd.DataFrame({
        "Title": [""],
        "Date": [""],
        "Venue": [""],
        "Venue1": [""],
        "Link": [""]
    })
    for venue in venues:
        try:
            search = venue
            driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div/div[1]/div/div/header/div/div[1]/div[1]/button/div/div/div/div'
            ).click()
            time.sleep(2)
            search_box = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[2]/div/div/div/div/div[1]/div/div/main/div/div/div/main/header/div/form/div/div/div/div/input'
            )
            search_box.send_keys(search)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2)
            soup = BeautifulSoup(
                driver.page_source, "html"
            )
            postings = soup.find_all(
                "div", {"class": "search-event-card-wrapper"})
            df = pd.DataFrame({
                "Title": [""],
                "Date": [""],
                "Venue": [""],
                "Venue1": [""],
                "Link": [""]
            })
            for post in postings:
                title = post.find(
                    "div", {"class": "eds-event-card__formatted-name--is-clamped eds-event-card__formatted-name--is-clamped-three eds-text-weight--heavy"}).text.strip()
                date = post.find(
                    "div", {"class": "eds-event-card-content__sub-title eds-text-color--primary-brand eds-l-pad-bot-1 eds-l-pad-top-2 eds-text-weight--heavy eds-text-bm"}).text.strip()
                ven = venue.split(",", 1)[0]
                ven1 = post.find(
                    "div", {"data-subcontent-key": "location"}).text.strip()
                link = post.find(
                    "a", {"tabindex": "0"}).get("href")
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
                '/html/body/div[2]/div/div[1]/header/div/div[1]/a/i'
            ).click()
            time.sleep(2)
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


def get_all_events():
    '''
        Concatenates results across various sources, and performs some additional cleaning
    '''
    df_moshtix = get_events_moshtix()
    df_oztix = get_events_oztix()
    df_eventbrite = get_events_eventbrite()
    month_mapping = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }
    df_moshtix["Day Number"] = df_moshtix["Date"].apply(
        lambda x: x[4:6] if len(x) == np.max(
            df_moshtix["Date"].str.len()) else "0" + x[4]
    )
    df_moshtix["Month Number"] = df_moshtix["Date"].apply(
        lambda x: month_mapping[x[-8:-5]]
    )
    df_moshtix["Date (New)"] = "2023-" + \
        df_moshtix["Month Number"] + "-" + df_moshtix["Day Number"]
    df_oztix["Day Number"] = df_oztix["Date"].apply(
        lambda x: x[4:6] if len(x.split(" ")[1]) == 2 else "0" + x[4]
    )
    df_oztix["Month Number"] = [
        month_mapping[x] for x in [
            string[:3] for string in [
                item[2] for item in df_oztix["Date"].str.split(" ")
            ]
        ]
    ]
    df_oztix["Date (New)"] = "2023-" + \
        df_oztix["Month Number"] + "-" + df_oztix["Day Number"]
    df_eventbrite["Day Number"] = str(np.zeros(df_eventbrite.shape[0]))
    df_eventbrite["Month Number"] = str(np.zeros(df_eventbrite.shape[0]))
    for i in range(df_eventbrite.shape[0]):
        if df_eventbrite["Date"][i][-7] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            df_eventbrite["Day Number"][i] = df_eventbrite["Date"][i][-7:-
                                                                      5].replace(" ", "")
            df_eventbrite["Month Number"][i] = month_mapping[df_eventbrite["Date"][i][0:3]]
        elif df_eventbrite["Date"][i][0] == "y":
            df_eventbrite["Day Number"][i] = str(datetime.today().day)
            df_eventbrite["Month Number"][i] = str(datetime.today().month)
        elif df_eventbrite["Date"][i][0] == "r":
            df_eventbrite["Day Number"][i] = str(datetime.date(
                pd.to_datetime(datetime.today() + timedelta(days=1))).day)
            df_eventbrite["Month Number"][i] = str(datetime.date(
                pd.to_datetime(datetime.today() + timedelta(days=1))).month)
    df_eventbrite["Day Number"] = df_eventbrite["Day Number"].apply(
        lambda x: "0" +
        x.replace(" ", "") if len(x.replace(" ", "")) == 1 else x
    )
    df_eventbrite["Month Number"] = df_eventbrite["Month Number"].apply(
        lambda x: "0" +
        x.replace(" ", "") if len(x.replace(" ", "")) == 1 else x
    )
    df_eventbrite["Date (New)"] = "2023-" + \
        df_eventbrite["Month Number"] + "-" + df_eventbrite["Day Number"]
    df = pd.concat([df_moshtix, df_oztix, df_eventbrite],
                   axis=0).reset_index(drop=True)
    df["Date"] = pd.to_datetime(df["Date (New)"], format='%Y-%m-%d')
    df["Date"] = df["Date"].apply(
        lambda x:
            x if x >= datetime.today() + timedelta(days=-1)
            else
        pd.to_datetime(datetime(
            datetime.date(x).year + 1,
            datetime.date(x).month,
            datetime.date(x).day
        ))
    )
    df_out = df[[
        "Title",
        "Date",
        "Venue",
        "Link"
    ]].sort_values("Date", ascending=True).reset_index(drop=True)
    df_out = df_out.drop_duplicates(
        subset=["Date", "Venue"], keep="first").reset_index(drop=True)
    return(df_out)


def export_events():
    '''
        Export output to CSV format
    '''
    df = get_all_events()
    df.to_csv("music_events.csv")
