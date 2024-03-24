##############################################################################################################
### This program extracts music events from some of my favourite venues across Melbourne. ####################
### The aim is to compile the events into an organised output table, which can be filtered easily by date. ###
### This should save time spent browsing across multiple event webpages. #####################################
##############################################################################################################


# 1. Load required libraries.
from pathlib import Path
import numpy as np
import pandas as pd
import re
import requests
import lxml
import html
import time
from datetime import datetime
from datetime import timedelta
from src.event_extraction.eventbrite import get_events_eventbrite
from src.event_extraction.humanitx import get_events_humanitix
from src.event_extraction.moshtix import get_events_moshtix
from src.event_extraction.oztix import get_events_oztix
from src.event_extraction.ticketek import get_events_ticketek
from src.config import venues, addresses, venue_address_mapping, address_venue_mapping, OUTPUT_PATH


#2. Specify defaults.
year = str(datetime.today().year)


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
    df["Date Aug."] = df["Date (New)"].str[5:10]
    for i in range(len(df)):
        if df["Date Aug."][i] == "02-29":
            df["Date (New)"][i] = df["Date (New)"][i][0:5] + "02-28"
        else:
            pass
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
    df["Date"] = [
        df["Date"][i] if df["Date Aug."][i] != "02-28" else df["Date"][i] + timedelta(days = 1) for i in range(len(df))
    ]
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
    df.to_csv(str(OUTPUT_PATH) + "/music_events.csv", index = False)