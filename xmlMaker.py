#!/usr/bin/python
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import urllib
import csv
import re

#start the xml
listings = ET.Element("listings")

#load and open the csv
f = open('urls.csv')
csv_f = csv.reader(f)

# parsing for each url in csv
for row in csv_f:

    #find our base and region
    rex = re.compile(ur'(.*org)', re.MULTILINE)
    pex = re.compile(ur'http://(.*).craigslist.org', re.MULTILINE)
    base = rex.search(row[0]).groups()[0]
    region = pex.search(row[0]).groups()[0]

    #load the html parser
    html = urllib.urlopen(row[0]).read()
    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all("a", {"id": "replylink"}):
        r = link.get('href') # get reply link
        reply = base + r # build it

        # open and load our new reply url
        replyhtml = urllib.urlopen(reply).read()
        soupre = BeautifulSoup(replyhtml, "html.parser")

        for e in soupre.find_all("a", {"class": "mailapp"}):
            email = e.get_text() #email address

    listing = ET.SubElement(listings, "listing")

    #title
    titleTag = soup.html.head.title.get_text()
    ET.SubElement(listing, "title", lang="en_US").text = titleTag

    #content
    for con in soup.find_all("section", {"id": "postingbody"}):
        content = con.get_text()
    if len(row) > 5:
        ET.SubElement(listing, "content", lang="en_US").text = content + '\n\n' +row[0] + '\n\n' +row[5]
    else:
        ET.SubElement(listing, "content", lang="en_US").text = content + '\n\n' +row[0]
    # category
    if len(row) > 1:
        ET.SubElement(listing, "category", lang="en_US").text = row[1]
    else:
        ET.SubElement(listing, "category", lang="en_US").text = "other"

    # email and name
    ET.SubElement(listing, "contactemail").text = email
    ET.SubElement(listing, "contactname").text = "Craigslist Ad"

    # price
    for p in soup.find_all("span", {"class": "price"}):
        price = p.get_text().strip('$')
    ET.SubElement(listing, "price").text = price
    ET.SubElement(listing, "currency").text = "USD"
    ET.SubElement(listing, "city_area").text = ""

    # city and state use columns C and D if present
    if len(row) > 2:
        ET.SubElement(listing, "city").text = row[2]
    else:
        ET.SubElement(listing, "city").text = region
    if len(row) > 3:
        ET.SubElement(listing, "region").text = row[3]
    else:
        ET.SubElement(listing, "region").text = ""

    ET.SubElement(listing, "countryId").text = "US"
    ET.SubElement(listing, "country").text = ""

    # Custom fields
    if len(row) > 4:
        ET.SubElement(listing, "custom", name="new-custom-field").text = row[4]

    # Images
    img = soup.find_all("img")[0].get('src') #if only one image
    imgs = soup.find_all("a", {"class": "thumb"}) #multiple images
    if len(imgs) > 1:
        for pi in imgs:
            pic = pi.get('href')
            ET.SubElement(listing, "image").text = pic
    elif len(img) > 0:
        ET.SubElement(listing, "image").text = img


    # time
    time = soup.find_all("time")[0].get('datetime')
    ET.SubElement(listing, "datetime").text = time

tree = ET.ElementTree(listings)
tree.write("criagslist.xml", encoding='utf-8', xml_declaration=True)
