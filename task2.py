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
# from tasks import BrowserManager as br

class DataRetriever:
    def __init__(self):
        self.data = []

    # def retrieve_data(self, search_results, time_frame):
    #     pass
    def __init__(self, browser_manager):
        
        self.browser_manager = browser_manager

    def retrive_data(self, num_months_ago, search_phrase):
        
        browser = self.browser_manager.browser
        # Declearing varibale to return the date
        # data =[]
        counter = 1
        # Handling the possible inputs
        if num_months_ago == 0:
            num_months_ago =1
        # To compare the date
        current_date = datetime.now()
        target_date = current_date - timedelta(days=num_months_ago * 30)  # Assuming each month has 30 days)
    
        # to store articles for extraction
        articles_titiles = []    
        try:
            browser.wait_until_element_is_visible("xpath://*[@id='main-content-area']/div[2]/div[2]", timeout=10)
        except Exception as e:
            print(e, "NOOOOOO")
    
            # to handle paggination
        is_there_ShowMore = True
            
        while is_there_ShowMore:

            # Search result section
            search_list_selector = browser.find_element("xpath=//*[@id='main-content-area']/div[2]/div[2]")
            articles = browser.find_elements("tag:article", parent=search_list_selector)

            # the show more button
            button_locator = browser.find_elements("tag:button", parent=search_list_selector)

            # for each articles 
            for article in articles:
                
                # getting excert section
                excert = browser.find_element("tag:p",parent=article)

                # getting time and description of the post from excert
                time_of_post, description  = extract_before_ellipsis(excert.text)
                article_date = formated_article_date(time_of_post)

                # check if the artices does contains date
                if(article_date == None):
                    continue
                try:

                    # checking the article date is in the time period of the input
                    if is_within_time_frame(article_date, target_date):
                        title= browser.find_element("tag:h3", parent=article)
                        if title.text not in articles_titiles:
                            articles_titiles.append(title.text)
                            
                            # does the title or description contains money
                            # checking how many times the search keyword apears in title and description
                            no_of_search_phrase, contains = no_of_topic_and_money_amount(title.text, 
                                                                                          description, 
                                                                                          search_phrase)
                            # finding the imgae of each article
                            image = browser.find_element(locator="tag:img", parent=article)
                            image_url = image.get_attribute('src')
    
                            picture_name = image_url.split("/")[-1]  # Extracting picture name from URL
                            output_path = Path(get_output_dir()) / picture_name
    
                            ready_article = {"No":counter, "Title": title.text, "Date": article_date, 
                                             "Description": description, "Picture Filename": picture_name, 
                                             "Count": no_of_search_phrase, "Contains Money": contains
                                                }
    
                            # Making work items to be saved on file
                            for article in articles:
                                workitems.outputs.create(payload=ready_article)
    
    
                            # data.append([counter,title.text, article_date, description, 
                            #                     picture_name, no_of_search_phrase, contains])
                            #update counter
                            counter+=1
    
                except Exception as e:
                    print(e)
    
            # try to locate and close the ads section
            try:
                ads_locator = browser.find_element("xpath=//button[@aria-label='Close Ad']")
                browser.click_button(ads_locator) 
    
            except Exception as e:
                pass
            
            # Trying to find if there is more article
            try: 
                # Scroll the element into view the show more button
                browser.scroll_element_into_view(button_locator)
                browser.wait_until_element_is_enabled(button_locator, timeout=10)
    
    
                browser.click_button(button_locator)
                time.sleep(5)
                print("Botton Clicked")
        
            except Exception as e: 
                is_there_ShowMore = False
                pass
    def save_data_to_Excel(workbook, sheet_name):
    
        worksheet = workbook.worksheet(sheet_name)
    
        headers = ["No", "Title", "Date", "Description", "Picture Filename", "Count", "Contains Money"]
    
        try:
            # Fetch the created work items and write them to the Excel file
            for item in workitems.inputs:
                row = [item.payload[header] for header in headers]
                worksheet.append_rows_to_worksheet([row], name=sheet_name)
            print("workitems finished successfully")
        except Exception as e:
            print(e)
            pass

####################################
    # getting the date and description from the excert of the article
    def extract_before_ellipsis(text):
        
        # checking if the text contains the excert
        if len(text) <=0:
            return 
    
        # Split the text at '...'
        date_part = ""
        description_part = ""
        try:
            parts = text.split(" ...")
            # Take the first part, before the '...'
            date_part = parts[0]
            description_part=parts[1]
        except:
            pass
        description_part.replace("Â","")
    
        return date_part, description_part
    
    # formating the article's date
    def formated_article_date(date_extracted):
    
        # cleaning the date part
        date_extracted = date_extracted.strip()
    
        # Defining possible hours, minutes and seconds 
        possible_hms = ["second", "seconds","min\xadutes", 
                            "minute", "minutes", "hour","hours"]
    
        possible_days = ["day", "days"]
    
        possible_months_format_One =["January", "Feburary", "March", "April", 
                                        "May", "June", "July", "August", "September", 
                                        "October", "November", "December"]
    
        possible_months_format_Two =["Jan", "Feb", "Mar", "Apr",
                                        "May", "Jun", "Jul", "Aug", 
                                        "Sep", "Oct", "Nov", "Dec"]
       
        current_date = datetime.now()
       
        # Formatting the date to make it more easy to compare and returning the article times
        try:   
            if(date_extracted.split(" ")[1]) in possible_hms:
                date_object = current_date
                formatted_date = date_object.strftime("%Y%m%d")
                return formatted_date
            elif date_extracted.split(" ")[1] in possible_days:
                # Split the expression to extract the number of days
                num_days = int(date_extracted.split()[0])
                # Calculate the target date by subtracting the number of days from the current date
                date_object = current_date - timedelta(days=num_days)
                formatted_date = date_object.strftime("%Y%m%d")
    
                return formatted_date
    
            elif date_extracted.split(" ")[0] in possible_months_format_One:
                # Convert the date string to a datetime object
                date_object = datetime.strptime(date_extracted, "%B %d, %Y")
        
                # Format the datetime object to the desired format
                formatted_date = date_object.strftime("%Y%m%d")
        
                return formatted_date
    
            elif date_extracted.split(" ")[0] in possible_months_format_Two:
                # Convert the date string to a datetime object
                date_object = datetime.strptime(date_extracted, "%b %d, %Y")
                formatted_date= date_object.strftime("%Y%m%d")
    
                return formatted_date
    
        except Exception as e:
                return e, None
    
    # comparing if the article time is with in the date of given period of time
    def is_within_time_frame(article_date, target_date):
    
        # Convert article date string to a datetime object
        try:
            article_datetime = datetime.strptime(article_date, "%Y%m%d")
        except Exception as e:
            return e, False
        
        # Check if the article date is within the time frame (since the target date)
        return article_datetime  >= target_date
    
    # checking if the topics and description contains money 
    # and how many times the title and description contains the search phrase
    def no_of_topic_and_money_amount(title, description, search_phrase):
    
        # Trying to find the number of times the title and description contains
        countT = title.split(" ").count(search_phrase)
        countD = description.split(" ").count(search_phrase)
    
        # Regex pattern to match various money formats
        pattern = r"\$\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|\d+\s(?:dollars|USD)"
        
        # Find all matches in the text
        matchesT = re.findall(pattern, title)
        matchesD = re.findall(pattern, description)
    
        # returning the number of times money appears and if there is search phrase in both
        return countT + countD,  bool(matchesT + matchesD)

##################################3




@task
def main():
     # Define the path for the new Excel file in the output directory
    output_dir = Path(get_output_dir())
    excel_file_path = output_dir / "Articles.xlsx"
    
    # Create a new Excel workbook and add a worksheet with the name 'Sheet1'
    workbook = excel.create_workbook(fmt="xlsx", sheet_name="Sheet1")
    
    
    # Append a row with column headers
    sheet_name = "Sheet1"
    worksheet = workbook.worksheet(sheet_name)
    row_to_append = [
        ["No", "Title", "Date", "Description", "Picture Filename", "Count", "Contains Money"]
    ]
    # Append the row to the worksheet
    worksheet.append_rows_to_worksheet(row_to_append, header=False)
    
    bm = br()
    url = "https://www.aljazeera.com/"
    bm.opening_the_news_Site(url)
    bm.search_the_phrase("Business")
    rd = retriveData(bm)
    rd.retrive_data(2, "Business")
    save_data_to_Excel(workbook, sheet_name)
    workbook.save(excel_file_path)

    # Saving the workbook
    workbook.save(excel_file_path)
    
    # Close the browser
    browser_instance.close_all_browsers()
    
