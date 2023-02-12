from os import system
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd


## check website error
def checkWebsiteError():
    error_page = driver.find_element(By.XPATH, "//div[@id='h']")
    if error_page != []:
        print(True)
    else:
        print(False)

## locate and click a button
def clickBtn(by, attr):
    btn = driver.find_element(by, attr)
    btn.click()

    time.sleep(1)




## clear terminal
system("cls")

## define website to scrape
website = "https://www.amazon.com/"

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
time.sleep(5)

## locate and click "All" (categories) button
clickBtn(By.XPATH, "//a[@id='nav-hamburger-menu']")

## locate and click "Computers" (category) button
clickBtn(By.XPATH, "//a[@data-menu-id='6']")

## locate and click "Computers & Tablets" (category) button
clickBtn(By.LINK_TEXT, "Computers & Tablets")

## wait until website completely load
time.sleep(5)

## initialize variable for storage of all item links
Link = []

## initialize variables for dataframe
ASIN = []
Title = []
Price = []

system("cls")

page_cntr = 1

while True:
    print("Page", page_cntr)

    ## locate parent tag
    items_box = driver.find_elements(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div')

    ## iterate thru all items in the item box
    ## and extract ASIN, Title, Price, and href
    price_ind = 0
    for ind, div in enumerate(items_box):
        prod_ASIN = div.get_attribute("data-asin")
        if prod_ASIN != '':
            ASIN.append(prod_ASIN)
            prod_Title = div.find_element(By.TAG_NAME, "h2").text
            Title.append(prod_Title)
            prod_Price = div.find_elements(By.XPATH, '//span[@data-a-color="base"]')[price_ind].text
            prod_Price = f"{prod_Price[0:-3]}.{prod_Price[-2:]}"
            Price.append(prod_Price)
            href = div.find_element(By.TAG_NAME, 'a').get_attribute("href")
            Link.append(href)
            price_ind += 1

    ## limit upto 3 pages only for testing purposes
    if page_cntr <= 3:
        ## go to next page
        next_btn = driver.find_element(By.LINK_TEXT, "Next")
        website = next_btn.get_attribute("href")
        driver.get(website)
        page_cntr += 1
        time.sleep(3)
    else:
        break

## close window
# time.sleep(3)
driver.quit()

## save data into a dataframe
data = {
    "ASIN":ASIN,
    "Title":Title,
    "Price":Price,
    "Link":Link
}
df_computers = pd.DataFrame(data)
print(df_computers)

## save data into a CSV file
df_computers.to_csv("computers.csv", index=False)