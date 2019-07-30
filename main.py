from dotenv import load_dotenv
load_dotenv()
import os
import requests
import random
import csv
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal

# column names for csv records file
column_names = ['id','date','bond','charges','county','gender','race']

def check_for_updates(latest_record):
    last_date = latest_record.split(',')[1]
    last_id = latest_record.split(',')[0]
    mdy = last_date.split('/')

    then = datetime(int(mdy[2]), int(mdy[0]), int(mdy[1]))
    now = datetime.now()

    print(str(now-then))
    if (now - then).days > 2:
        return True
    return False
    
latest_index = 0

def get_next_latest():
    global latest_index
    # get last ID number as a start
    index_page = requests.get(os.getenv("HOST_SERVER"))
    raw_html = BeautifulSoup(index_page.text,'html.parser')
    latest_mugs = raw_html.find_all(id='mugs')
    picture_links = latest_mugs[0].find_all('a');
    return int(picture_links[1].get('href').split('=')[1])

def get_mugshots(amount):
    updated = False
    mugs = []
    offset = 1
    records = []
    if amount > 64:
        amount = 64

    while len(mugs) < amount:
        if updated == False:
            records_file = open("records.csv","r")
            records = records_file.readlines()
            records_file.close()
            if len(records) == 0:
                update_records()
            else:
                last = records[len(records) - 1]
                if check_for_updates(last):
                    update_records(last.split(',')[0])
            records_file = open("records.csv","r")
            records = records_file.readlines()
            records_file.close()
            if len(records) < amount:
                amount = len(records)
            updated = True

        rec = records[len(records) - offset]
        mugs.append(rec)
        offset += 1
    return mugs

def get_record(id):
    record = {}
    # get the page html
    get_page = requests.post(os.getenv("MUG_ROUTE_PREFIX")+str(id))
    
    # parse html into soup
    soup = BeautifulSoup(get_page.text, 'html.parser')

    # get the details section
    details = soup.find_all("div","mugshotsNameDetail")
    if len(details) == 0:
        return False
    details = details[0]

    # check if has name
    name = details.find_all("h2")[0].text
    if name:
        record['id'] = id

    # grab info
    other = details.find_all("b");
    for info in other:
        if info.text == "Booking on:":
            record["date"] = info.next_sibling.string.rstrip()
        elif info.text == "County:":
            record["county"] = info.next_sibling.string.rstrip()
        elif info.text == "Gender:":
            record["gender"] = info.next_sibling.string.rstrip()
        elif info.text == "Race:":
            record["race"] = info.next_sibling.string.rstrip()

    image = requests.get("http://mugshots.starnewsonline.com/Content/Images/WM/"+ str(id) + ".jpg", stream=True)
    if image.status_code == 200:
        file = open("mugs/" + str(id) + ".jpg", "wb")
        for chunk in image:
            file.write(chunk)
        file.close()

    details = soup.find_all("div","mugshotsArrestInfoDetail")
    # get charges
    if len(details) > 0:
        charges = []
        bond = 0
        for charge in details[0].find_all("ul")[0].find_all("li"):
            violations = charge.find_all("b")
            if len(violations) > 0:
                charges.append(violations[0].next_sibling.string)
                # get bond next to violation
                if len(violations) > 1:
                    bond_string = violations[1].next_sibling.string
                    bond += Decimal(sub(r'[^\d.]', '', bond_string))
        record['bond'] = bond
        record['charges'] = charges
    return record

def increment_total():
    count_file = open("./count.txt","r")
    count = int(count_file.read()) + 1
    count_file.close()
    count_file = open("./count.txt","w")
    count_file.write(str(count))
    count_file.close()

def update_records(last_id=False):
    global column_names, latest_index
    fields= {"_EVENTTARGET": "ctl00$ContentPlaceHolder1$lbtnNext"}
    with open('records.csv','a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        records_received = 0
        if last_id == False:
            last_id = get_next_latest() 
            i = last_id
            while i > last_id - 32:
                record = get_record(i)
                if record == False:
                    i -= 1
                    continue
                else:
                    records_received += 1
                i -= 1
                print(str(i) + " - ADDING")
                increment_total()
                writer.writerow(record)
        else:
            i = int(last_id) + 1
            while i < int(last_id):
                record = get_record(i)
                if record == False:
                    i += 1
                    continue
                else:
                    records_received += 1
                print(str(i) + " - ADDING")
                increment_total()
                writer.writerow(record)
            i += 1
