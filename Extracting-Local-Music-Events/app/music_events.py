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


def get_events_moshtix():
    '''
        Gets events from moshtix.com
    '''
    try:
        driver = webdriver.Chrome()
    except:
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
            df = pd.concat(
                [df, pd.DataFrame({
                    "Title": title,
                    "Date": date,
                    "Venue": ven,
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
        df_final = pd.concat([df_final, df], axis = 0).reset_index(drop = True)
        #df_final = df_final.append(df, ignore_index=True)
        driver.find_element(
            By.XPATH,
            '//*[@id="header"]/nav/ul/li[1]/a'
        ).click()
        time.sleep(1)
    return(df_final[df_final["Title"] != ""].reset_index(drop=True))


def get_events_oztix():
    '''
        Gets events from oztix.com.au
    '''
    try:
        driver = webdriver.Chrome()
    except:
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
            #df = df.append({
            #   "Title": title,
            #    "Date": date,
            #    "Venue": ven,
            #    "Venue1": ven1,
            #    "Link": link
            #}, ignore_index=True)
            df = df.reset_index(drop=True)
        df_final = pd.concat([df_final, df], axis = 0).reset_index(drop = True)
        #df_final = df_final.append(df, ignore_index=True)
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


def get_events_eventbrite():
    '''
        Gets events from eventbrite.com.au
    '''
    try:
        driver = webdriver.Chrome()
    except:
        driver = webdriver.Chrome(
            executable_path="C:\\Users\\callanroff\\Desktop\\learnings\\Web Scraping/chromedriver_mac64\\chromedriver",
            chrome_options=options
        )
    time.sleep(1)
    df_final = pd.DataFrame({
        "Title": [""],
        "Date": [""],
        "Venue": [""],
        "Venue1": [""],
        "Link": [""]
    })
    for venue in venues:
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
                #df = df.append({
                #   "Title": title,
                #    "Date": date,
                #    "Venue": ven,
                #    "Venue1": ven1,
                #    "Link": link
                #}, ignore_index=True)
                df = df.reset_index(drop=True)
            df_final = pd.concat([df_final, df], axis = 0).reset_index(drop = True)
            #df_final = df_final.append(df, ignore_index=True)
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


def get_events_humanitix():
    '''
        Only use for Miscellania (or others which can only be found on humanitix)
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


def get_events_ticketek():
    '''
        Gets events from premier.ticketek.com.au (for the Forum only)
    '''
    try:
        driver = webdriver.Chrome()
    except:
        driver = webdriver.Chrome(
            executable_path="C:\\Users\\callanroff\\Desktop\\learnings\\Web Scraping/chromedriver_mac64\\chromedriver",
            chrome_options=options
        )
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
        #df = df.append({
        #   "Title": title,
        #    "Date": date,
        #    "Venue": ven,
        #    "Venue1": ven1,
        #    "Link": link
        #}, ignore_index=True)
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


def get_all_events():
    '''
        Concatenates results across various sources, and performs some additional cleaning
    '''
    df_moshtix = get_events_moshtix()
    df_oztix = get_events_oztix()
    df_eventbrite = get_events_eventbrite()
    df_humanitix = get_events_humanitix()
    df_ticketek = get_events_ticketek()
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
    if df_moshtix.shape[0] > 0:
        df_moshtix["Day Number"] = df_moshtix["Date"].apply(
            lambda x: x[4:6] if len(x) == np.max(
                df_moshtix["Date"].str.len()) else "0" + x[4]
        )
        df_moshtix["Month Number"] = df_moshtix["Date"].apply(
            lambda x: month_mapping[x[-8:-5]]
        )
        df_moshtix["Date (New)"] = year + "-" + \
            df_moshtix["Month Number"] + "-" + df_moshtix["Day Number"]
    else:
        pass
    if df_oztix.shape[0] > 0:
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
        df_oztix["Date (New)"] = year + "-" + \
            df_oztix["Month Number"] + "-" + df_oztix["Day Number"]
    else:
        pass
    if df_eventbrite.shape[0] > 0:
        df_eventbrite["Day Number"] = np.zeros(len(df_eventbrite)).astype("object")
        df_eventbrite["Month Number"] = np.zeros(len(df_eventbrite)).astype("object")
        for i in range(df_eventbrite.shape[0]):
            if df_eventbrite["Date"][i][0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                df_eventbrite["Day Number"][i] = df_eventbrite["Date"][i][0:2] if df_eventbrite["Date"][i][1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] else "0" + df_eventbrite["Date"][i][0]
                df_eventbrite["Month Number"][i] = month_mapping[
                    df_eventbrite["Date"][i].replace(" ", "")[1:4] if df_eventbrite["Date"][i][1] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] else df_eventbrite["Date"][i].replace(" ", "")[2:5]
                ]
            elif df_eventbrite["Date"][i][0] == "y":
                df_eventbrite["Day Number"][i] = str(datetime.today().day)
                df_eventbrite["Month Number"][i] = str(datetime.today().month)
            elif df_eventbrite["Date"][i][0] == "r":
                df_eventbrite["Day Number"][i] = str(datetime.date(
                    pd.to_datetime(datetime.today() + timedelta(days=1))).day)
                df_eventbrite["Month Number"][i] = str(datetime.date(
                    pd.to_datetime(datetime.today() + timedelta(days=1))).month)
            else:
                df_eventbrite["Day Number"][i] = str(datetime.date(
                    pd.to_datetime(datetime.today() + timedelta(days=2))).day)
                df_eventbrite["Month Number"][i] = str(datetime.date(
                    pd.to_datetime(datetime.today() + timedelta(days=2))).month)
        df_eventbrite["Day Number"] = df_eventbrite["Day Number"].apply(
            lambda x: "0" +
            x.replace(" ", "") if len(x.replace(" ", "")) == 1 else x
        )
        df_eventbrite["Month Number"] = df_eventbrite["Month Number"].apply(
            lambda x: "0" +
            x.replace(" ", "") if len(x.replace(" ", "")) == 1 else x
        )
        df_eventbrite["Date (New)"] = year + "-" + \
            df_eventbrite["Month Number"] + "-" + df_eventbrite["Day Number"]
    else:
        pass
    if df_humanitix.shape[0] > 0:
        df_humanitix["Day Number"] = df_humanitix["Date"].apply(
            lambda x: "0" + x[0] if x[1] in ["s", "n", "r", "t"] else x[:2]
        )
        df_humanitix["Month Number"] = [
            month_mapping[x] for x in [
                string[:3] for string in [
                    item[1] for item in df_humanitix["Date"].str.split(" ")
                ]
            ]
        ]
        df_humanitix["Date (New)"] = year + "-" + \
            df_humanitix["Month Number"] + "-" + df_humanitix["Day Number"]
    else:
        pass
    if df_ticketek.shape[0] > 0:
        df_ticketek["Day Number"] = np.zeros(len(df_ticketek))
        df_ticketek["Month Number"] = np.zeros(len(df_ticketek))
        for i in range(len(df_ticketek)):
            if df_ticketek["Date"][i][5] == " ":
                df_ticketek["Day Number"][i] = "0" + df_ticketek["Date"][i][4]
                df_ticketek["Month Number"][i] = month_mapping[df_ticketek["Date"][i][6:9]]
            else:
                df_ticketek["Day Number"][i] = df_ticketek["Date"][i][4:6]
                df_ticketek["Month Number"][i] = month_mapping[df_ticketek["Date"][i][7:10]]
        df_ticketek["Date (New)"] = year + "-" + df_ticketek["Month Number"] + "-" + df_ticketek["Day Number"]
    else:
        pass
    df = pd.concat([df for df in [df_moshtix, df_oztix, df_eventbrite, df_humanitix, df_ticketek] if df.shape[0] > 0],
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


def export_events(
    venue_list=venues,
    from_date=str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day),
    to_date=str(datetime.today().year + 1) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day),
):
    '''
        Export output to CSV format
    '''
    df = get_all_events()
    df = df[
        (df["Venue"].isin(venue_list)) &
        (pd.to_datetime(df["Date"]) >= pd.to_datetime(from_date, format="%Y-%m-%d")) &
        (pd.to_datetime(df["Date"]) <= pd.to_datetime(to_date, format="%Y-%m-%d"))
    ]
    df.to_csv("./music_events.csv")
    
    
if __name__ == "__main__":
    export_events()
