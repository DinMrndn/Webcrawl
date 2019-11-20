import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

title = []
game = []
views = []
comments = []
links = []

def crawl():
    fromPage = int(input("From Page: "))
    toPage = int(input("To Page: "))
    while fromPage < toPage:
        page = requests.get("https://www.gta-multiplayer.cz/en/videos/?page="+ str(fromPage))
        soup = BeautifulSoup(page.content, 'html.parser')
        posts = soup.find_all(class_="Movie MovieDelimiter")
        stats = soup.find_all(class_ = "Stats")

        counter = 0
        for x in stats:
            splitted = stats[counter].get_text().split("\n")
            views.append(splitted[1])
            comments.append(splitted[2])
            title.append(posts[counter].find(class_="Link").get_text())
            game.append(posts[counter].find(class_="UserLink").get_text())
            counter = counter + 1

        for link in soup.findAll(class_="Link"):
            links.append(link.get('href'))

        print("Page " + str(fromPage) + " Completed!")
        fromPage = fromPage + 1

    dataCompiled = pd.DataFrame({
    "Title": title,
    "Game": game,
    "View Count": views,
    "Comment Count": comments,
    "Links": links,
    })
    print("Process Complete")
    dataCompiled.to_csv('GTAwebsite.csv')

user_choice = ""
#main
while user_choice.lower() != "3":
    user_choice = input("Choose:\n"
                        "1. Crawl a GTA Forum Website.\n"
                        "2. Delete CSV File\n"
                        "3. Quit\n: ")
    if user_choice == "1":
        crawl()
    elif user_choice == "2":
        try:
            os.remove("GTAwebsite.csv")
        except(FileNotFoundError):
            print("File does not exist anymore.")
        except(PermissionError):
            print("File is opened and cannot be deleted.")
    elif user_choice == "3":
        print("Goodbye!")
        exit()