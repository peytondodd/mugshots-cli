from bs4 import BeautifulSoup
import json
import requests
import random
import csv
from re import sub
from decimal import Decimal

# get last ID number as a start
index_page = requests.get("http://mugshots.starnewsonline.com")
raw_html = BeautifulSoup(index_page.text,'html.parser')
latest_mugs = raw_html.find_all(id='mugs')
picture_links = latest_mugs[0].find_all('a');
latest_index = 0
def get_next_latest():
    global latest_index, picture_links
    latest_index += 1
    return int(picture_links[latest_index].get('href').split('=')[1])
latest_index = get_next_latest()

# column names for csv records file
column_names = ['id','name','charges','bond','county','date','gender','race']

# not sure what this does, but it's required in post request

# loop through the ids in specified amount
hr = "------------------------------------------------------"
print("")
print(hr)

def get_mugshots(amount):
    fields= {"_EVENTTARGET": "ctl00$ContentPlaceHolder1$lbtnNext"}
    global column_names, latest_index
    output = ""
    with open('records.csv','a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        records_received = 0
        i = latest_index + 1
        while records_received < amount:
            if i > 10:
                i -= 2 
            elif i > 30:
                i = get_next_latest()
                continue
            else:
                i -= 1

            record = {}

            # get the page html
            get_page = requests.post("http://mugshots.starnewsonline.com/Details.aspx?BookingID="+str(i), fields)
            
            # parse html into soup
            soup = BeautifulSoup(get_page.text, 'html.parser')

            # get the details section
            details = soup.find_all("div","mugshotsNameDetail")
            if len(details) == 0:
                continue
            details = details[0]
            name = details.find_all("h2")[0].text
            if name:
                record['id'] = i
                record['name'] = name

            if len(name) == 0:
                continue

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

            image = requests.get("http://mugshots.starnewsonline.com/Content/Images/WM/"+ str(i) + ".jpg", stream=True)
            if image.status_code == 200:
                file = open("mugs/" + str(i) + ".jpg", "wb")
                for chunk in image:
                    file.write(chunk)
                file.close()

            details = soup.find_all("div","mugshotsArrestInfoDetail")
            if len(details) > 0:
                charges = []
                bond = 0
                for charge in details[0].find_all("ul")[0].find_all("li"):
                    violations = charge.find_all("b")
                    if len(violations) > 0:
                        charges.append(violations[0].next_sibling.string)
                        if len(violations) > 1:
                            bond_string = violations[1].next_sibling.string
                            bond += Decimal(sub(r'[^\d.]', '', bond_string))
                record['bond'] = bond
                record['charges'] = charges
            writer.writerow(record)
            records_received += 1
            print(record)
    return json.dumps(record)
