import time
import os
from Service.DayForce.Utilites.selenium_helper import handywrapper
from Service.DayForce.Utilites.gspread_helper import GspreadSheetHelper
from Service.DayForce.TestCases.Pay_Category_Reverse import  Pay_Category_Reverse
from Service.DayForce.Utilites.Pay_Category_Common_Helper import Pay_Category_Common_Helper
from Service.DayForce.Controllers.Pay_Category_Load_fill_Controller import Pay_Category_loader_controller

class Pay_Category_Automate:
    """this class is responsible for automating the pay category data into the Dayforce application."""
   
    def automate_pay_category(self,driver,web_models,groups):
        """this method automates the pay category data into the Dayforce application."""

        # get the pay category data from the Google Sheet and compare it with the web models
        loader_controller = Pay_Category_loader_controller()
        sheet_models = loader_controller.pay_category_loader_controller()
        wrapper = handywrapper(driver)
        helper = Pay_Category_Common_Helper()
        GSH=GspreadSheetHelper()
        worksheet = GSH.getsheet(os.environ['SHEET_NAME'])

        # get the colors for formatting the cells in the Google Sheet
        client_id=0
        status=[["Processed"]]
        for i in range(len(sheet_models)):
            id = int(sheet_models[i].item_id)-1

            # check if the object name in the web models is same as the object name in the sheet models and update the pay category data accordingly
            if id < len(web_models) and web_models[id].object_name == sheet_models[i].object_name :

                # check if all the other attributes of the pay category are same in the web models and sheet models and update the pay category data accordingly
                similarity=(str(web_models[id].object_description) == helper.maps(sheet_models[i].object_description) and 
                        str(web_models[id].pay_category_group) == sheet_models[i].pay_category_group and 
                        web_models[id].multiplier_rate == float(sheet_models[i].multiplier_rate) and 
                        str(web_models[id].category) == helper.maps(sheet_models[i].category) and 
                        str(web_models[id].show_hours) == helper.maps(sheet_models[i].show_hours.capitalize()) and 
                        str(web_models[id].show_amount) == helper.maps(sheet_models[i].show_amount.capitalize()) and 
                        str(web_models[id].is_irregular_cost) == helper.maps(sheet_models[i].is_irregular_cost.capitalize()) and
                        str(web_models[id].sort_order) == helper.maps(sheet_models[i].sort_order) and 
                        str(web_models[id].code_name) == helper.maps(sheet_models[i].code_name) and 
                        str(web_models[id].reference_code) == helper.maps(sheet_models[i].reference_code) and 
                        str(web_models[id].reference_code_2) == helper.maps(sheet_models[i].reference_code_2) )
            else:
                # if the object name in the web models is not same as the object name in the sheet models, create a new pay category data and update it accordingly
                print("No pay category found for object so, creating new one:", sheet_models[i].object_name)
                client_id+=1
                similarity=False

            if not similarity:
                # if the all pay category data is not similar, update the pay category data in the Dayforce application and update the status in the Google Sheet
                print("Automating for Pay Category Object Name:", sheet_models[i].object_name)
                helper.update_pay_category(sheet_models[i], groups, driver, len(web_models) + client_id)

        # update the status of the pay category data in the Google Sheet
        GSH.update_sheet(worksheet,'B','B',status*(len(web_models) + client_id))
        time.sleep(5)
        wrapper.click_element('XPATH', "//span[@class='dijit dijitReset dijitInline dijitButton' and @widgetid = 'UI_Mixins__TooltipMixin_5']")




if __name__ == "__main__":

    #============== Performing the Reverse test case for Pay Category ==============
    pay_category_reverse = Pay_Category_Reverse()
    web_models, groups, driver = pay_category_reverse.Pay_Category_Reverse()

    #============== Reverse Completed ===================

    #============== Performing the Automate test case for Pay Category ==============
    pay_category_automate = Pay_Category_Automate()
    pay_category_automate.automate_pay_category(driver, web_models, groups)

    # #============== Automation Completed ===================