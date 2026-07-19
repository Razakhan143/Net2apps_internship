import re
import requests
class Pay_Category_Get_Post:
    """this class is responsible for getting and posting the pay category data from the Dayforce application."""
    

    def get_scrub_id(self, driver):
        """this method gets the scrub id from the current url of the driver."""
        
        current_url=driver.current_url
        scrub_id = re.search(r'/u/([^/]+)/', current_url).group(1)
        return scrub_id
    

    def get_session_data(self, driver):
        """this method gets the session data from the driver and returns it as a requests session and csrf token."""
        
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(
                cookie["name"],
                cookie["value"]
            )

        return session
    

    def update_pay_category(self, driver,payload):
        """this method updates the pay category data in the Dayforce application using the API."""
        
        session = self.get_session_data(driver)
        scrub_id = self.get_scrub_id(driver)
        csrf = driver.execute_script("""
        return window.Dayforce?.AppSettingsData?.csrfRequestToken;
        """)

        # create the url and headers for the API call to update the pay category data in the Dayforce application
        url = f"https://usstage261.dayforcehcm.com/MyDayforce/u/{scrub_id}/WFMAdmin/PayCategory/PersistPayCategory"
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "X-CSRF-Token": csrf,
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://usstage261.dayforcehcm.com",
            "Referer": f"https://usstage261.dayforcehcm.com/MyDayforce/u/{scrub_id}/Common/",
        }

        # call the API to update the pay category data in the Dayforce application
        response = session.post(
            url,
            json=payload,
            headers=headers
        )
        if response.status_code == 200:
            print("object updated successfully")
        else:
            print(f"Error: {response.status_code}")


    def post_pay_category(self, api_url, driver):
        """this method posts the pay category data to the Dayforce application using the API."""

        # create a requests session and set the cookies from the driver to the session, then post the pay category data to the Dayforce application using the API and return the response as a json object.
        session = self.get_session_data(driver)
        response = session.post(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None