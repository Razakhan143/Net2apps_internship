import time
from TestCases.reverse_rating_scale import rating_scale_reverse
from TestCases.validate_rating_scale import rating_scale_validation
from TestCases.automation_rating_scale import rating_scale_automation
from Controller.controllers_rating_scale import rating_scale_fill_sheet_controller


if __name__ == "__main__":
    start_time = time.time()
    ##=========== Performance Reverse: fetching the data from the website and filling the data model=============

    # Step 1: Extract data from the website
    module_reverse=rating_scale_reverse()
    driver, data_list = module_reverse.rating_scale_reverse()
    
    # Fill the data into the Google Sheet
    fill_module_sheet=rating_scale_fill_sheet_controller()

    # filling the data into the google sheet of Section 1, 2 and 3
    fill_module_sheet.rating_scale_processing_fill_controller(data_list)
    fill_module_sheet.rating_scale_description_fill_controller(data_list)
    fill_module_sheet.rating_scale_scores_fill_controller(data_list)

    #===========all the data has been fetched and filled in to Google Sheet=============



    #===========Performing Validation on the Data(Google Sheet and Web Instances)=============

    val=rating_scale_validation()

    # validation for Section 2 and 3
    val.validate_description_section(data_list)
    val.validate_scores_section(data_list)

    #==========Validation Completed=============



    #===========Perfroming Automation satisfy the changes on web if find any wrong data=============

    automation=rating_scale_automation()
    automation.automate(data_list, driver)

    #===========Automation Completed=============
    end_time = time.time()
    print(f"Total time taken to Run all the processes: {end_time - start_time:.2f} seconds")
