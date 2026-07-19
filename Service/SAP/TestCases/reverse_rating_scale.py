import re
import time
from Utilites.login_SAP import login_SAP
from Utilites.selenium_helper import handywrapper
from Controller.controllers_rating_scale import rating_scale_fill_sheet_controller
from Models.rating_scale_data_model import rating_scale_Processing_Model, rating_scale_Rating_Scale_Model, rating_scale_Scores_Model


class rating_scale_reverse:
    """This class is responsible for reversing the data from the SAP website and filling it into the Google Sheet"""
    
    def rating_scale_reverse(self):
        """function to reverse the data from the SAP website and fill it into the Google Sheet"""

        login_instance = login_SAP()
        driver = login_instance.open_and_login_SAP()
        wrapper = handywrapper(driver)

        #redirecting to the rating scale designer page
        url = driver.current_url
        scrub_id = re.search(r'_s\.crb=([^&]+)', url).group(1)
        new_url = f"https://hcm41.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=form_rating_scale&itrModule=talent&_s.crb={scrub_id}"
        driver.get(new_url)
        
        #scrapping all the Scales of rating scale designer
        Scale_name=wrapper.get_elements_text('XPATH',"//a[contains(@id,'link') and @class='fd-link fd-link--compact']")

        data_list=[]
        # iterating through all the Scales and scrapping the data
        for i, Scale in enumerate(Scale_name):
            print(f"============= Scale {i+1}: {Scale} =============")
            #clicking on the Scale
            wrapper.click_element('LINK_TEXT', Scale)
            # apply exception handling to avoid the error if the OK button is not available
            try:
                #fetching the name of the rating scale
                name=wrapper.element_attribute('ID', "48:_txtFld", "value")
            except:
                 # clicking okay if avaialable
                wrapper.click_element('XPATH',"//button[contains(text(),'OK')]")
                #fetching the name of the rating scale
                name=wrapper.element_attribute('ID', "48:_txtFld", "value")

            description=wrapper.element_attribute('ID', "50:_txtArea", "value")

            # all score ,labels and descriptions 
            scores=wrapper.find_elements('XPATH',"//input[@size='7']")
            labels=wrapper.find_elements('XPATH',"//input[@size='34']")
            option_description=wrapper.find_elements('XPATH',"//textarea[@cols='42']")
            
            Data_model_section1=rating_scale_Processing_Model() #Data_model_section1 : Data Model for Processing Section, 
            Data_model_section2=rating_scale_Rating_Scale_Model() #Data_model_section2: Data Model for Rating Scale Section,

            Data_model_section1.item_id=i+1
            Data_model_section1.processing_status="Pending"
            Data_model_section1.processing_rating_scale=name

            Data_model_section2.rating_scale_name=name
            Data_model_section2.rating_scale_description=description
            section3_data=[]
            #fetching the description of the rating scale
            for j in range(len(scores)):
                Data_model_section3=rating_scale_Scores_Model() # Data_model_section3: Data Model for Scores Section
                Data_model_section3.rating_scale = name
                Data_model_section3.option_score = scores[j].get_attribute("value")
                Data_model_section3.option_label = labels[j].get_attribute("value")
                Data_model_section3.option_description = option_description[j].text
                section3_data.append(Data_model_section3)
            
            # refreshing the page to avoid stale element reference error
            data_list.append([Data_model_section1, Data_model_section2, section3_data])
            driver.refresh()

            # returning the all_data list to the calling function
        return driver, data_list





if __name__ == "__main__":

    start_time = time.time()
    ##=========== Performance Reverse: fetching the data from the website and filling the data model=============

    # Step 1: Extract data from the website
    module_reverse=rating_scale_reverse()
    _, data_list = module_reverse.rating_scale_reverse()
    
    # Step 2: Fill the data into the Google Sheet
    fill_module_sheet=rating_scale_fill_sheet_controller()
    
    # filling the data into the google sheet of Section 1, 2 and 3
    fill_module_sheet.rating_scale_processing_fill_controller(data_list)
    fill_module_sheet.rating_scale_description_fill_controller(data_list)
    fill_module_sheet.rating_scale_scores_fill_controller(data_list)


    #===========all the data has been filled into the google sheet, reversed Completed=============
    end_time = time.time()
    print(f"Reverse Completed. Total time taken for the Reverse Process: {end_time - start_time:.2f} seconds")