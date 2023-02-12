from os import system
import pandas as pd

## clear terminal
system("cls")

## read csv file from website https://www.football-data.co.uk/englandm.php
df_premier22 = pd.read_csv("https://www.football-data.co.uk/mmz4281/2223/E0.csv")
# print(df_premier22.head())

## rename columns
df_premier22 = df_premier22.rename(columns={"FTHG":"home_goals", "FTAG":"away_goals"})
# print(df_premier22.head())