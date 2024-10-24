# Import required libraries 
import os
from pathlib import Path


# Speicify path defaults
APP_PATH = Path(os.environ["PYTHONPATH"])
OUTPUT_PATH = APP_PATH / "output/"


# Email
SMTP_SERVER = "smtp.gmail.com"
PORT = 465


# Venue-address mapping
venues = [
    "Brunswick Ballroom",
    "The Night Cat",
    "Croxton Bandroom",
    "Corner Hotel",
    "Northcote Theatre",
    "Northcote Social Club",
    "The Workers Club",
    "The Retreat",
    "The Retreat Hotel",
    "Sub Club",
    "Sub Club Melbourne",
    "Miscellania",
    "Melbourne Recital Centre",
    "280 Sydney Rd",
    "Max Watt's Melbourne",
    "Sidney Myer Music Bowl",
    "Forum Melbourne",
    "Howler",
    "The Toff in Town",
    "Kindred Bandroom",
    "Gasometer (Upstairs)",
    "Gasometer Downstairs",
    "170 Russell"
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
    "2/252 Swanston St, VIC, Australia",
    "3 Harris St, VIC, Australia",
    "484 Smith St, VIC, Australia",
    "170 Russell, VIC, Australia"
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
    "2/252 Swanston St, VIC, Australia": "The Toff in Town",
    "3 Harris St, VIC, Australia": "Kindred Bandroom",
    "484 Smith St, VIC, Australia": "Gasometer (Upstairs)",
    "170 Russell, VIC, Australia": "170 Russell"
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
    "The Toff in Town": "2/252 Swanston St, VIC, Australia",
    "Kindred Bandroom": "3 Harris St, VIC, Australia",
    "Gasometer (Upstairs)": "484 Smith St, VIC, Australia",
    "170 Russell": "170 Russell, VIC, Australia"
}