import time
from Utilites.gspread_helper import GspreadSheetHelper
from TestCases.Rating_Scale_Reverse import rating_scale_reverse
from Controller.controllers_rating_scale import rating_scale_loader_controller
from Utilites.rating_scale_helper import rating_scale_operation_helpers


class rating_scale_validation:
    """class to validate the data in the google sheet with the data fetched from the website"""

    # Selection of color for validation
    GSH=GspreadSheetHelper()
    green, red , _ = GSH.colors_r_g_b()

    # creating object of GspreadSheetHelper, loader_controller and operation_helpers
    loader=rating_scale_loader_controller()
    helper=rating_scale_operation_helpers()

    def validate_description_section(self, web_models):
        """function to validate the data in the google sheet of Section 2"""

        desc_section_data=self.loader.rating_scale_description_loader_controller()
        formate=[]
        for i, row in enumerate(desc_section_data):
            exist, index = self.helper.get_scale_if_exists(row.rating_scale_name, web_models, desc_section_data)
            if exist:
                color = self.green if row.rating_scale_name == web_models[index][1].rating_scale_name else self.red
                formate.append((f"E{i+4}", color))

                color = self.green if row.rating_scale_description == web_models[index][1].rating_scale_description else self.red
                formate.append((f"F{i+4}", color))
            else:
                formate.append((f"E{i+4}", self.red))
                formate.append((f"F{i+4}", self.red))

        self.GSH.batch_formate_sheet(formate)
        print("Validation Completed for Rating Scale Section")


    def validate_scores_section(self,web_models):
        """function to validate the data in the google sheet of Section 3"""

        scores_section_data=self.loader.rating_scale_scores_loader_controller()
        formate=[]
        row_no=4
        for i, row in enumerate(scores_section_data):
            for j, sheet_model in enumerate(row):
                exist, index = self.helper.get_scale_if_exists(sheet_model.rating_scale, web_models, scores_section_data)

                if exist:
                    color = self.green if sheet_model.rating_scale == web_models[index][2][j].rating_scale else self.red
                    formate.append((f"H{row_no}", color))

                    color = self.green if sheet_model.option_score == web_models[index][2][j].option_score else self.red
                    formate.append((f"I{row_no}", color))

                    color = self.green if sheet_model.option_label == web_models[index][2][j].option_label else self.red
                    formate.append((f"J{row_no}", color))

                    color = self.green if sheet_model.option_description == web_models[index][2][j].option_description else self.red
                    formate.append((f"K{row_no}", color))
                else:
                    formate.append((f"H{row_no}", self.red))
                    formate.append((f"I{row_no}", self.red))
                    formate.append((f"J{row_no}", self.red))
                    formate.append((f"K{row_no}", self.red))
                row_no+=1

        self.GSH.batch_formate_sheet(formate)
        print("Validation Completed for Scores Section")






if __name__ == "__main__":

    start_time = time.time()
    #=========== Performance web Scrapping: fetching the data from the website=============

    # Step 1: Extract data from the website
    reverse=rating_scale_reverse()
    _, data_list = reverse.rating_scale_reverse()


    #===========all the data has been fetched=============
    #===========Performing Validation on the Data(Google Sheet and Web Instances)=============
    val=rating_scale_validation()
    # validation controller for Section 2
    val.validate_description_section(data_list)

    # validation controller for Section 3
    val.validate_scores_section(data_list)


    #===========all the validation is completed =============
    end_time = time.time()
    print(f"Total time taken for the Validation process: {end_time - start_time:.2f} seconds")