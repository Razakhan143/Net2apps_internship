from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
class handywrapper:
        """this class is responsible for wrapping the selenium webdriver methods and providing a convenient interface for interacting with web elements."""
        def __init__(self, driver):
            self.driver = driver

        def create_locator(self, locator_type, locator_value):
            """this method creates a locator tuple based on the locator type and value."""
            locator_type = locator_type.lower()
            if locator_type == "id":
                return (By.ID, locator_value)
            elif locator_type == "name":
                return (By.NAME, locator_value)
            elif locator_type == "xpath":
                return (By.XPATH, locator_value)
            elif locator_type == "tag":
                return (By.TAG_NAME, locator_value)
            elif locator_type == "link_text":
                return (By.LINK_TEXT, locator_value)
            else:
                raise ValueError(f"Unsupported locator type: {locator_type}")
            

        def find_element(self, locator_type, locator_value):
            """this method finds a web element based on the locator type and value."""
            try:
                locator = self.create_locator(locator_type, locator_value)
                element=self.driver.find_element(*locator)
                return element
            except Exception as e:
                print(f"An error occurred with find element: {e}")
                return " "
        

        def find_elements(self, locator_type, locator_value):
            """this method finds a list of web elements based on the locator type and value."""
            try:
                locator = self.create_locator(locator_type, locator_value)
                element=self.driver.find_elements(*locator)
                return element
            except Exception as e:
                print(f"An error occurred with find elements: {e}")
                return " "
        

        def click_element(self, locator_type, locator_value):
            """this method clicks a web element based on the locator type and value."""
            try:
                if self.wait_for_element_clickable(locator_type, locator_value):
                    element = self.find_element(locator_type, locator_value)
                    element.click()
                else:
                    print("Element is not clickable.")
            except Exception as e:
                print(f"An error occurred while clicking the element: {e}")


        def send_keys_to_element(self, locator_type, locator_value, keys):
            """this method sends keys to a web element based on the locator type and value."""
            try:
                element = self.find_element(locator_type, locator_value)
                element.click()  # Click the input field before sending keys
                element.clear()  # Clear the input field before sending keys
                element.send_keys(keys)
            except Exception as e:
                print(f"An error occurred while sending keys to the element: {e}")


        def element_attribute(self, locator_type, locator_value, attribute_name):
            """this method gets the attribute value of a web element based on the locator type and value."""
            try:
                element = self.find_element(locator_type, locator_value)
                return element.get_attribute(attribute_name)
            except Exception as e:
                print(f"An error occurred while getting the attribute: {e}")
                return " "
            
        def get_element_text(self, locator_type, locator_value):
            """this method gets the text of a web element based on the locator type and value."""
            try:
                element = self.find_element(locator_type, locator_value)
                return element.text
            except Exception as e:
                print(f"An error occurred while getting the text of the element: {e}")
                return " "
            
        def get_elements_text(self, locator_type, locator_value):
            """this method gets the text of a list of web elements based on the locator type and value."""
            try:
                elements = self.find_elements(locator_type, locator_value)
                return [element.text for element in elements]
            except Exception as e:
                print(f"An error occurred while getting the text of the elements: {e}")
                return []
            
        def refresh(self):
            """this method refreshes the current page."""
            try:
                self.driver.refresh()
            except Exception as e:
                print(f"An error occurred while refreshing the page: {e}")
            

            # add explicit wait for element to be clickable
        def wait_for_element_clickable(self, locator_type, locator_value, timeout=50):
            """this method waits for a web element to be clickable based on the locator type and value."""
            try:
                locator = self.create_locator(locator_type, locator_value)
                WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                return True
            except TimeoutException:
                print(f"Element with locator ({locator_type}, {locator_value}) is not clickable after {timeout} seconds.")
                return False

