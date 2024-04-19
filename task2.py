from RPA.Browser.Selenium import Selenium 
import re
import time
import requests
import logging
from pathlib import Path
from robocorp import vault
# from robocorp import excel
from robocorp import storage
from datetime import datetime
from robocorp.tasks import task
from datetime import datetime, timedelta
from robocorp.tasks import get_output_dir
from tasks import BrowserManager as br

# logger = logging.getLogger(__name__)


#@task
# secrets =vault.get_secret('alijazeersite') 



#searching for the phrase of the news
# @task

class retriveData:
    def __init__(self, browser_manager):
        self.browser_manager = browser_manager

    def retrive_data(self, num_months_ago):
        browser = self.browser_manager.browser
        try:
    
    
            browser.wait_until_element_is_visible("xpath://*[@id='main-content-area']/div[2]/div[2]", timeout=10)
            print("Sucessull first part")
            # to handle paggination
            is_there_ShowMore = True
                
            # Search result section
            search_list_selector = browser.find_element("xpath=//*[@id='main-content-area']/div[2]/div[2]")
            articles = browser.find_elements("tag:article", parent=search_list_selector)
            print('Sucessull all')
        except Exception as e:
            print(e, "NOOOOOO")
    
@task
def main():
    bm = br()
    url = "https://www.aljazeera.com/"
    bm.opening_the_news_Site(url)
    bm.search_the_phrase("Business")")
    rd = retriveData(bm)
    retrive_data(2)
