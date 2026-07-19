# importing the required modules for the test cases
from Utilites.gspread_helper import GspreadSheetHelper
from TestCases.Pay_Category_Reverse import  Pay_Category_Reverse
from Utilites.Pay_Category_Common_Helper import Pay_Category_Common_Helper
from Controllers.Pay_Category_Load_fill_Controller import Pay_Category_loader_controller

class Pay_Category_Validation:
    """this class is responsible for validating the pay category data from the Dayforce application."""
    
    def validate_pay_category(self, web_models):
        """this method validates the pay category data from the Dayforce application."""

        # get the pay category data from the Google Sheet and compare it with the web models
        GSH=GspreadSheetHelper()
        loader_controller = Pay_Category_loader_controller()
        sheet_models = loader_controller.pay_category_loader_controller()
        
        # get the colors for formatting the cells in the Google Sheet
        helper=Pay_Category_Common_Helper()
        green ,red ,_ = GSH.colors_r_g_b()

        # create a list of cell ranges and colors for formatting the cells in the Google Sheet
        formate_list=[]
        for i in range(len(sheet_models)):
            id = int(sheet_models[i].item_id)-1

            # if the object name is matching then compare the other fields and format the cells in the Google Sheet
            if id < len(web_models) and web_models[id].object_name == sheet_models[i].object_name :
                color= green
                formate_list.append((f"C{id+4}", color))

                color = green if str(web_models[id].object_description) == helper.maps(sheet_models[i].object_description) else red
                formate_list.append((f"D{id+4}", color))
                
                color = green if str(web_models[id].pay_category_group) == sheet_models[i].pay_category_group else red
                formate_list.append((f"E{id+4}", color))

                color = green if web_models[id].multiplier_rate == float(sheet_models[i].multiplier_rate) else red
                formate_list.append((f"F{id+4}", color))

                color = green if web_models[id].category == helper.maps(sheet_models[i].category) else red
                formate_list.append((f"G{id+4}", color))

                color = green if str(web_models[id].show_hours) == helper.maps(sheet_models[i].show_hours.capitalize()) else red
                formate_list.append((f"H{id+4}", color))

                color = green if str(web_models[id].show_amount) == helper.maps(sheet_models[i].show_amount.capitalize()) else red
                formate_list.append((f"I{id+4}", color))

                color = green if str(web_models[id].is_irregular_cost) == helper.maps(sheet_models[i].is_irregular_cost.capitalize()) else red
                formate_list.append((f"J{id+4}", color))

                color = green if str(web_models[id].sort_order) == helper.maps(sheet_models[i].sort_order) else red
                formate_list.append((f"K{id+4}", color))

                color = green if str(web_models[id].code_name) == helper.maps(sheet_models[i].code_name) else red
                formate_list.append((f"L{id+4}", color))

                color = green if str(web_models[id].reference_code) == helper.maps(sheet_models[i].reference_code) else red
                formate_list.append((f"M{id+4}", color))

                color = green if str(web_models[id].reference_code_2) == helper.maps(sheet_models[i].reference_code_2) else red
                formate_list.append((f"N{id+4}", color))
            else:
                # if the object name is not matching then mark all the cells in that row as red as the object not exist
                color = red
                formate_list.append((f"C{id+4}", color))
                formate_list.append((f"D{id+4}", color))
                formate_list.append((f"E{id+4}", color))
                formate_list.append((f"F{id+4}", color))
                formate_list.append((f"G{id+4}", color))
                formate_list.append((f"H{id+4}", color))
                formate_list.append((f"I{id+4}", color))
                formate_list.append((f"J{id+4}", color))
                formate_list.append((f"K{id+4}", color))
                formate_list.append((f"L{id+4}", color))
                formate_list.append((f"M{id+4}", color))
                formate_list.append((f"N{id+4}", color))


        # split the list of cell ranges and colors into two halves and format the cells in the Google Sheet so limit not exceed
        length = len(formate_list)//2
        print("Validating first half")
        GSH.batch_formate_sheet(formate_list[:length])
        print("Validating second half")
        GSH.batch_formate_sheet(formate_list[length:])
        # GSH.batch_formate_sheet(formate_list[:100])
        print("Validation Completed")
        




if __name__ == "__main__":

    #============== Performing the Reverse test case for Pay Category ==============
    pay_category_reverse = Pay_Category_Reverse()
    web_models, groups, driver = pay_category_reverse.Pay_Category_Reverse()

    #============== Reverse Completed ===================

    # #============== Performing the Validation test case for Pay Category ==============
    pay_category_validation = Pay_Category_Validation()
    pay_category_validation.validate_pay_category(web_models)

    #============== Validation Completed ===================