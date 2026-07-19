import time
from Utilites.gspread_helper import GspreadSheetHelper
from Utilites.selenium_helper import handywrapper
from Utilites.rating_scale_operation_helper import rating_scale_operation_helpers
from Controller.controllers_rating_scale import rating_scale_loader_controller
from TestCases.reverse_rating_scale import rating_scale_reverse
class rating_scale_automation:
    """class to automate the process of updating the data in the website with the data in the google sheet"""

    def automate(self,models,driver):
        """function to control the automation process for the rating scale designer"""

        # creating object of GspreadSheetHelper, loader_controller, handywrapper and operation_helpers
        loader=rating_scale_loader_controller()
        GSH = GspreadSheetHelper()
        wrapper= handywrapper(driver)
        helper=rating_scale_operation_helpers()

        rating_scale_section_data=loader.rating_scale_description_loader_controller()
        scores_section_data=loader.rating_scale_scores_loader_controller()
        status=[]
        for i in range(len(rating_scale_section_data)):
            all_matched=True

            exist, index = helper.get_scale_if_exists(rating_scale_section_data[i].rating_scale_name, models, rating_scale_section_data)
            if exist:
                # calling the function that checks the condition for validation if true then green else red and the location
                desc_matching_status=(rating_scale_section_data[i].rating_scale_name == models[index][1].rating_scale_name and 
                            rating_scale_section_data[i].rating_scale_description == models[index][1].rating_scale_description
                            )
                
                for j, sheet_model in enumerate(scores_section_data[i]):
                    all_matched=all_matched and desc_matching_status and (
                            sheet_model.rating_scale == models[index][2][j].rating_scale and 
                            sheet_model.option_score == models[index][2][j].option_score and 
                            sheet_model.option_label == models[index][2][j].option_label and 
                            sheet_model.option_description == models[index][2][j].option_description)

            if not all_matched or exist==False:
                helper.update_scale(rating_scale_section_data[i], scores_section_data[i], wrapper)
            status.append(["Processed"])

        GSH.update_sheet('B','B',status)
        print(f"Automation completed.")


if __name__ == "__main__":

    start_time = time.time()
    #=========== Performance web Scrapping: fetching the data from the website=============

    # Step 1: Extract data from the website
    reverse=rating_scale_reverse()
    driver, data_list = reverse.rating_scale_reverse()

    #===========all the data has been fetched=============
    #===========Perfroming Automation satisfy the changes on web if find any wrong data=============

    automation=rating_scale_automation()
    automation.automate(data_list, driver)

    #===========Automation Completed=============
    end_time = time.time()
    print(f"Total time taken for the Automation process: {end_time - start_time:.2f} seconds")
