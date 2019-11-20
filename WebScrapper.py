import pandas as pd
import requests
from bs4 import BeautifulSoup

page = requests.get("https://forecast.weather.gov/MapClick.php?lat=34.05349000000007&lon=-118.24531999999999#.XdVbrVczbIU")
soup = BeautifulSoup(page.content, 'html.parser')
week = soup.find(id="seven-day-forecast-body")
items = week.find_all(class_='tombstone-container')

periodNames = []
shortDescription = []
temperature = ["Low: 66 °F"]

counter = 0

for x in items:
    periodNames.append(items[counter].find(class_="period-name").get_text())
    shortDescription.append(items[counter].find(class_="short-desc").get_text())
    if counter >= 1:
        temperature.append(items[counter].find(class_="temp").get_text())
    counter = counter+1

dataCompiled = pd.DataFrame({
"Period Name": periodNames,
"Description": shortDescription,
"Temperature": temperature,
})
print(dataCompiled)

dataCompiled.to_csv('Text.csv')