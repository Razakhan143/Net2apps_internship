import os
import time
from selenium import webdriver
from dotenv import load_dotenv
from Service.DayForce.Utilites.selenium_helper import handywrapper
load_dotenv()
class login_dayforce:
    """this class is responsible for logging into the Dayforce application."""
    def login(self):
        """this method logs into the Dayforce application and returns the driver object."""

        # get the login credentials from the environment variables
        company_id = os.environ['COMPANY_ID']
        username = os.environ['USER_NAME']
        password = os.environ['PASSWORD']
        host_address = os.environ['HOST_ADDRESS']
        driver=webdriver.Chrome()

        # maximize the browser window and navigate to the Dayforce login page
        driver.get(host_address)
        selenium_helper = handywrapper(driver)
        
        
        # dayforce company id
        selenium_helper.send_keys_to_element("name", 'ctl00$MainContent$loginUI$txtCompanyId', company_id)
        selenium_helper.click_element("xpath", "//input[@value='Continue to username']")

        # dayforce account username
        selenium_helper.send_keys_to_element("name", 'ctl00$MainContent$loginUI$txtNewUserName', username)
        selenium_helper.click_element("xpath", "//input[@value='Continue to password']")

        time.sleep(1)
        # dayforce account password
        selenium_helper.send_keys_to_element("name", 'ctl00$MainContent$loginUI$txtNewUserPass', password)
        selenium_helper.click_element("xpath", "//input[@value='Log in']")


        time.sleep(3)
        # skip account recovery popup
        selenium_helper.click_element("xpath", "//button[@aria-label='Close']")
        selenium_helper.click_element("xpath", "//span[@widgetid='Button_2']")

        # login as status test001
        selenium_helper.click_element("xpath", "//span[contains(text(),'Next')]")
        return driver