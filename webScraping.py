from os import system
from bs4 import BeautifulSoup
import requests
import pandas as pd

## clear terminal
system("cls")

## define website to scrape
website = "https://subslikescript.com/movie/titanic-120338"

## send request to website to get html content
result = requests.get(website)
# print(result)

## extract website's html content and encode it as text
content = result.text
# print(content)

## reformat content as lxml
soup = BeautifulSoup(content, "lxml") # lxml is for processing of XML and HTML file in Python
# print(soup.prettify())

## find the parent tag of desired content
box = soup.find("article", class_="main-article")
# print(box)

## extract title
title = box.find("h1").get_text().strip()
# print(title)

## extract transcript
transcript = box.find("div", class_="full-script").get_text(strip=True, separator=' ')
# print(transcript)

## extract description
description = box.find("p", class_="plot").get_text(strip=True, separator=' ')
# print(description)

## save transcripts into a text file using title as a filename
with open(f"{title}.txt", 'w', encoding="utf-8") as file: # encode transcripts as utf-8 to avoid UnicodeEncodeError
    file.write(transcript)

## create a dataframe
trans_dict = {"title":[title], "transcript":[transcript]}
df_titanic = pd.DataFrame(trans_dict)
print(df_titanic)

## save dataframe into a CSV file
df_titanic.to_csv("movieTranscripts.csv", index=False)