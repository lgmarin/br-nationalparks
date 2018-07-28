import requests
from bs4 import BeautifulSoup

# Get the response page from Wiki and put into
resp = requests.get("https://pt.wikipedia.org/wiki/Lista_de_parques_nacionais_do_Brasil")

# Parse data with bs and get all tables in the page
bsoup = BeautifulSoup(resp.content)
# Make sure to select the correct tables by adding the classes
tables = bsoup.findAll("table", {"class": ["sortable", "plainrowheaders"]})


