import glob
import os
import time
import urllib
import urllib.request

import folder as folder
import requests
import wget
from selenium.webdriver.support.select import Select
from seleniumwire import webdriver
# import login and password from from file download for adding proxy
from proxy_auth_data import login, password1
from selenium.webdriver.chrome.options import Options
import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error
import pymysql
from config import host, user, password, db_name
# options
options = webdriver.ChromeOptions()

options.add_experimental_option('prefs', {
    "download.default_directory": "C:\\Users\\Saya\\PycharmProjects\\pythonProject6\\files",
    "download.prompt_for_download": False,  # To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
})
#add proxy
proxy_options = {
    "proxy": {
        "https": f"http://{login}:{password1}@45.155.203.115:8000"
    }
}

# Chrome driver
driver = webdriver.Chrome(executable_path='chromedriver.exe',  options=options)
# open site https://sccourts.org/casesearch/
driver.get("https://sccourts.org/casesearch/")
time.sleep(1)

states = driver.find_elements_by_xpath("//p/a[contains(@class, 'blackLink')]")
print(len(states))
states = [i.get_attribute('href') for i in states]
print(states)
for item in states:

    driver.get("https://www2.greenvillecounty.org/scjd/publicindex/")
    time.sleep(2)

    m1 = driver.find_element_by_id("ContentPlaceHolder1_ButtonAccept").click()
    current_url = driver.current_url

    print(current_url)

    driver.get(current_url)

    select_fr = Select(driver.find_element_by_id("ContentPlaceHolder1_DropDownListCaseTypes"))
    select_fr.select_by_value('SS  ')

    select_fr = Select(driver.find_element_by_id("ContentPlaceHolder1_DropdownlistCaseSubType"))
    select_fr.select_by_value('760   ')

    select_fr = Select(driver.find_element_by_id("ContentPlaceHolder1_DropDownListDateFilter"))
    select_fr.select_by_value('Actions')

    driver.find_element_by_id("ContentPlaceHolder1_TextBoxDateFrom").send_keys("11/01/2021")

    driver.find_element_by_id("ContentPlaceHolder1_TextBoxDateTo").send_keys("11/14/2021")

    driver.find_element_by_id("ContentPlaceHolder1_ButtonSearch").click()
    documents = driver.find_elements_by_xpath("//table[contains(@class, 'searchResultsGrid')]/tbody/tr/td/a")
    print(len(documents))
    documents = [i.get_attribute('href') for i in documents]
    print(documents)

    for item in documents:

        select_fr = Select(driver.find_element_by_id("ContentPlaceHolder1_DropDownListCaseTypes"))
        select_fr.select_by_value('SS  ')

        select_fr = Select(driver.find_element_by_id("ContentPlaceHolder1_DropdownlistCaseSubType"))
        select_fr.select_by_value('760   ')

        select_fr = Select(driver.find_element_by_id("ContentPlaceHolder1_DropDownListDateFilter"))
        select_fr.select_by_value('Actions')

        driver.find_element_by_id("ContentPlaceHolder1_TextBoxDateFrom").send_keys("11/01/2021")

        driver.find_element_by_id("ContentPlaceHolder1_TextBoxDateTo").send_keys("11/14/2021")

        driver.find_element_by_id("ContentPlaceHolder1_ButtonSearch").click()
        documents1 = driver.find_elements_by_xpath("//table[contains(@class, 'searchResultsGrid')]/tbody/tr/td/a")
        print(len(documents1))
        documents1 = [i.get_attribute('href') for i in documents1]
        print(documents1)
        print(item)
        driver.execute_script(item)
        driver.find_element_by_id("__tab_ContentPlaceHolder1_TabContainerCaseDetails_TabPanel5").click()
        time.sleep(2)
        links = driver.find_elements_by_xpath(
            "//span[contains(@id, 'ContentPlaceHolder1_TabContainerCaseDetails_TabPanel5_LabelPanel5Contents')]/table[contains(@class, 'detailsSection')]/tbody/tr/td[contains(@class, 'noWrapCell')]/a")
        print(len(links))
        links = [i.get_attribute('href') for i in links]
        print(links)
        current_url1 = driver.current_url
        # download files
        for item in links:
            driver.get(current_url1)
            print(item)
            driver.get(item)
            # connection with database
            # list_of_files = glob.glob(
            #             'C:/Users/Saya/PycharmProjects/pythonProject6/files/*')  # * means all if need specific format then *.csv

            # try:
            #     connection = pymysql.connect(
            #         host=host,
            #         port=3306,
            #         user=user,
            #         password=password,
            #         database=db_name,
            #
            #     )
            #     print("successfully connected...")
            #     mycursor = connection.cursor()
            #
            #     sql = "SELECT link FROM documents.links WHERE link = %s"
            #
            #     adr = (item)
            #
            #     mycursor.execute(sql, adr)
            #
            #     myresult = mycursor.fetchall()
            #     if len(myresult) == 0:
            #         driver.get(item)
            #         time.sleep(5)
            #         list_of_files = glob.glob(
            #             'C:/Users/Saya/PycharmProjects/pythonProject6/files/*')  # * means all if need specific format then *.csv
            #
            #         latest_file = max(list_of_files, key=os.path.getctime)
            #         _, filename = os.path.split(latest_file)
            #         print(filename)
            #         with connection.cursor() as cursor:
            #             insert_query = "INSERT INTO documents.links (link, name, status) VALUES (%s, %s, '1');"
            #             reviewers_records = [(item, filename)]
            #             cursor.executemany(insert_query, reviewers_records)
            #             connection.commit()
            #             print("successfully recorded in the database")
            #     else:
            #         print("the link already exists")




            # except Exception as ex:
            #     print("Connection refused...")
            #     print(ex)

    # driver.quit()
