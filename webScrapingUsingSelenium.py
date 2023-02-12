from os import system
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

## clear terminal
system("cls")

## define website to scrape
website = "https://www.adamchoi.co.uk/teamgoals/detailed"

## prevent windows from closing automatically
options = Options()
options.add_experimental_option("detach", True)

## install webdriver manager for chromedriver
driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()), options=options)

## maximize window
# driver.maximize_window()

## open browser
driver.get(website)

## wait until website completely load
time.sleep(15)

## locate and click "All matches" button
all_matches_btn = driver.find_element(By.XPATH, "//label[@analytics-event='All matches']")
all_matches_btn.click()

## locate matches table
matches = driver.find_elements(By.TAG_NAME, "tr")

## initialize variables for each column
dates = []
home_teams = []
scores = []
away_teams = []

## iterate every table row and extract all data
for match in matches:
    date = match.find_element(By.XPATH, "./td[1]").text
    dates.append(date)
    home_team = match.find_element(By.XPATH, "./td[2]").text
    home_teams.append(home_team)
    score = match.find_element(By.XPATH, "./td[3]").text
    scores.append(score)
    away_team = match.find_element(By.XPATH, "./td[4]").text
    away_teams.append(away_team)

## close window
driver.quit()

## create a dataframe
matches_dict = {"dates":dates, "home_teams":home_teams, "scores":scores, "away_teams":away_teams}
df_matches = pd.DataFrame(matches_dict)
print(df_matches)

## save dataframe into a CSV file
df_matches.to_csv("football_data.csv", index=False)