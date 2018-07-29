import requests
from bs4 import BeautifulSoup
import csv

# Get the page
resp = requests.get("https://pt.wikipedia.org/wiki/Lista_de_parques_nacionais_do_Brasil")

# Parse data with bs and get all tables in the page
bsoup = BeautifulSoup(resp.content, 'lxml')
# Make sure to select the correct tables by adding the classes
tables = bsoup.findAll("table", {"class": ["sortable", "plainrowheaders"]})

# Set csv file for output
f = open("out.csv", "w")

# Find all rows inside the first table of the page
# [1::1] will skip the first row (the headers of the table)
for row in tables[0].findAll("tr")[1::1]:
    cols = row.findAll(["th", "td"])

    # Make sure that the table is the one that I need (the one with 7 rows)
    if len(cols) == 7:

        # Retrieve NAME and URL
        name = cols[0].find("a")
        # Some of the data maybe empty, check to avoid errors
        if name:
            park_name = name.find(text=True)
            wiki_url = name.get("href")
        else:
            wiki_url = ""
            park_name = ""
        
        # Retrieve IMG URL
        image = cols[1].find("img")
        # Some of the data maybe empty, check to avoid errors
        if image:
            img_url = image.get("src")
        else:
            img_url = ""
        
        # Retrieve GEO LOC
        location = cols[2].find("a", class_="external text")
        geo = location.find(text=True)

        # Retrieve STATE list
        # Before finding the state, we need to remove the geo location info
        for col in cols:
            geotags = col.findAll("small")
            if geotags:
                for geotag in geotags:
                    geotag.extract()
        # Now go ahead and extract only the state name
        state = cols[2].findAll(text=True)
        print(state)
        # Retrieve CREATION
        creation = cols[3].findAll(text=True)

        # Retrieve AREA
        area = cols[4].find(text=True)
        area = area.replace("&", "")

        # Retrieve DESCRIPTION
        desc_text = cols[6].findAll(text=True)
        # This will get the text mixed with a lot of "garbage" like the citation marks
        # Clean everything and combine into one string...
        only_text = [text for text in desc_text if text[0] != '[']
        description = (
            ''.join(only_text)
            .replace('\xa0', ' ') # Replace non-breaking spaces for actual spaces
            .replace('\n', '') # Replace new line markers
            .strip()
        )

        # Write to a csv file
        write_csv = park_name + ";" + wiki_url + ";" + geo + ";" + area + ";" + description + "\n"
        f.write(write_csv)

# Close and save csv file
f.close()