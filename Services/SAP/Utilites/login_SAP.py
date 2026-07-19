import os
import re
from dotenv import load_dotenv
from selenium import webdriver
# from Service.SAP.Utilites.selenium_helper import handywrapper
from Utilites.selenium_helper import handywrapper
load_dotenv()

class login_SAP:
    """class to handle the login process, it takes the driver as input and returns the driver after login"""

    def open_and_login_SAP(self):
        """function to open the website and login to the website, it takes the driver as input and returns the driver after login"""
        # opening the website and logging in to the website
        driver=webdriver.Chrome()
        driver.implicitly_wait(10)
        driver.get(os.getenv("SAP_HOST_ADDRESS"))
        wrapper = handywrapper(driver)

        Company_ID = os.getenv("SAP_COMPANY_ID")
        User_Name = os.getenv("SAP_USER_NAME")
        Password = os.getenv("SAP_PASSWORD")
        #entering company ID
        wrapper.send_keys_to_element("xpath", "//input[@placeholder='Enter Company ID']", Company_ID)

        #press continue button
        wrapper.click_element('XPATH',"//bdi[contains(text(),'Continue')]")

        #entering username and password
        #email
        wrapper.send_keys_to_element('XPATH',"//input[@placeholder='Email or User Name']", User_Name)

        #password
        wrapper.send_keys_to_element('XPATH',"//input[@placeholder='Password']", Password)

        #clicking on continue button
        wrapper.click_element('XPATH',"//div[contains(text(),'Continue')]")

        #accepting the data privacy policy
        wrapper.click_element('XPATH',"//button[contains(text(),'Accept')]")

        #returning driver for further use in other modules
        return driver

