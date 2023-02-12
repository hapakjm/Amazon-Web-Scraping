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
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("window-size=1024,768")
# options.add_argument("--no-sandbox")

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
    if page_cntr < 3:
        ## go to next page
        next_btn = driver.find_element(By.LINK_TEXT, "Next")
        website = next_btn.get_attribute("href")
        driver.get(website)
        page_cntr += 1
        time.sleep(3)
    else:
        break


### ********************************************************* ###


def addToDict(data_index, key, value):
    if key in data_:
        while len(data_[key]) < data_index-1:
            data_[key].append("N/A")
        data_[key].append(value)
    else:
        data_[key] = []
        for i in range(data_index):
            if i < data_index-1:
                data_[key].append("N/A")
            else:
                data_[key].append(value)


def fetchAllData(data_index, Link):
    ### product name, price
    title = driver.find_element(By.XPATH, "//h1[@id='title']").text
    price = driver.find_element(By.XPATH, "//div[@class='a-section a-spacing-micro']/span").text
    # print(title, f"{price[0:-3]}.{price[-2:]}")
    addToDict(data_index, "Title", title)
    addToDict(data_index, "Price", price)

    ### specifications
    specs_row = driver.find_elements(By.XPATH, "//table[@class='a-normal a-spacing-micro']/tbody/tr")
    for tr in specs_row:
        # print(tr.find_element(By.XPATH, "./td[1]").text, tr.find_element(By.XPATH, "./td[2]").text)
        Spec_temp = tr.find_element(By.XPATH, "./td[1]").text
        Spec_Details_temp = tr.find_element(By.XPATH, "./td[2]").text
        addToDict(data_index, Spec_temp, Spec_Details_temp)
        
        

    ### descriptions
    desc_box = driver.find_element(By.XPATH, "//div[@id='feature-bullets']")
    desc_lbl = desc_box.find_element(By.TAG_NAME, "h1").text
    desc_list = desc_box.find_elements(By.XPATH, "./ul/li")
    Desc_Lbl_temp = desc_lbl
    Desc_Info_temp = ''
    try:
        for li in desc_list:
            # print(li.text)
            Desc_Info_temp += li.text
            Desc_Info_temp += "\n"
    except TypeError:
        Desc_Info_temp = "N/A"
    addToDict(data_index, Desc_Lbl_temp, Desc_Info_temp)
    

    ### product information
    prod_info_box = driver.find_element(By.XPATH, "//div[@class='a-row a-spacing-top-base']")

    #### technical details
    tech_details_box = prod_info_box.find_element(By.XPATH, "//div[@class='a-row a-expander-container a-expander-extend-container']")
    tech_details_summary_row = tech_details_box.find_elements(By.XPATH, "//table[@id='productDetails_techSpec_section_1']/tbody/tr")
    for tr in tech_details_summary_row:
        # print(tr.find_element(By.TAG_NAME, "th").text, tr.find_element(By.TAG_NAME, "td").text)
        Tech_Details_Summary_temp = tr.find_element(By.TAG_NAME, "th").text
        Tech_Details_Summary_Info_temp = tr.find_element(By.TAG_NAME, "td").text
        addToDict(data_index, Tech_Details_Summary_temp, Tech_Details_Summary_Info_temp)

    tech_details_other_row = tech_details_box.find_elements(By.XPATH, "//table[@id='productDetails_techSpec_section_2']/tbody/tr")
    for tr in tech_details_other_row:
        # print(tr.find_element(By.TAG_NAME, "th").text, tr.find_element(By.TAG_NAME, "td").text)
        Tech_Details_Other_temp = tr.find_element(By.TAG_NAME, "th").text
        Tech_Details_Other_Info_temp = tr.find_element(By.TAG_NAME, "td").text
        addToDict(data_index, Tech_Details_Other_temp, Tech_Details_Other_Info_temp)

    #### additional information
    additional_info_box = prod_info_box.find_element(By.XPATH, "//div[@id='productDetails_db_sections']")
    additional_info_row = additional_info_box.find_elements(By.XPATH, "//table[@id='productDetails_detailBullets_sections1']/tbody/tr")
    for tr in additional_info_row:
        # print(tr.find_element(By.TAG_NAME, "th").text, tr.find_element(By.TAG_NAME, "td").text)
        Additional_temp = tr.find_element(By.TAG_NAME, "th").text
        Additional_Info_temp = tr.find_element(By.TAG_NAME, "td").text
        addToDict(data_index, Additional_temp, Additional_Info_temp)

        ##### ASIN #####
        # if tr.find_element(By.TAG_NAME, "th").text == "ASIN":
        #     ASIN_temp = tr.find_element(By.TAG_NAME, "td").text

    #### seller info
    Seller_temp = driver.find_element(By.XPATH, "//a[@id='sellerProfileTriggerId']").text
    addToDict(data_index, "Seller", Seller_temp)
    addToDict(data_index, "Link", Link)

    time.sleep(3)

data_ = {}
data_index = 0

for l in Link:
    driver.get(l)
    time.sleep(3)

    ## extract all data
    variation_box = driver.find_elements(By.XPATH, "//ul[@role='radiogroup']")

    if variation_box != []:
        variation_type = driver.find_element(By.XPATH, "//label[@class='a-form-label']").text
        variations = driver.find_elements(By.XPATH, "//button[@class='a-button-text']")
        system("cls")

        for v in variations:
            ### select variant
            v.click()
            selection = driver.find_element(By.XPATH, "//span[@class='selection']").text
            # print(selection)

            fetchAllData(data_index, l)
            
    else:
        fetchAllData(data_index, l)

    data_index += 1

## close window
# time.sleep(3)
driver.quit()


### ********************************************************* ###


## save data into a dataframe
df_computers_ = pd.DataFrame(data_)
print(df_computers_)

## save data into a CSV file
# df_computers_.to_csv("computers_.csv", index=False)