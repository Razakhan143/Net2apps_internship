import os
from dotenv import load_dotenv
from gspread_formatting import format_cell_ranges
from Service.DayForce.Utilites.gspread_helper import GspreadSheetHelper
from Service.DayForce.Models.Pay_Category_Models import Pay_Category_Model
load_dotenv()

class Pay_Category_fill_controller:
    """this class is responsible for filling the pay category data into the Google Sheet."""
    # inittialize the GspreadSheetHelper and get the worksheet


    def pay_category_fill_controller(self, data):
        """this method fills the pay category data into the Google Sheet."""
        GSH=GspreadSheetHelper()

        # get Clearing the sheet before filling the data into the worksheet
        GSH.clear_sheet('A', 'N')

        # create a list of rows from web models to be filled into the worksheet
        rows = []
        for row in data:
            rows.append([
                row.item_id,
                row.processing_status,
                row.object_name,
                row.object_description,
                row.pay_category_group,
                row.multiplier_rate,
                row.category,
                row.show_hours,
                row.show_amount,
                row.is_irregular_cost,
                row.sort_order,
                row.code_name,
                row.reference_code,
                row.reference_code_2
            ])

        # update the worksheet with the new data
        GSH.update_sheet('A', 'N', rows)
        print("Pay Category Fill Completed")
            



class Pay_Category_loader_controller:
    """this class is responsible for loading the pay category data from the Google Sheet."""

    def pay_category_loader_controller(self):
        """this method loads the pay category data from the Google Sheet."""
        GSH=GspreadSheetHelper()

        # get the start and end row of the worksheet and get the data from the worksheet
        data = GSH.get_sheet_data('A', 'N', Pad_values=True)

        # create a list of pay category models from the data loaded from the worksheet and return it
        pay_category_models = []
        row_count = 0
        for row in data:
            if row[1] == 'Processed':
                continue
            row_count += 1
            pay_cat_model=Pay_Category_Model()
            pay_cat_model.item_id=row[0]
            pay_cat_model.object_name=row[2]
            pay_cat_model.object_description=row[3]
            pay_cat_model.pay_category_group=row[4]
            pay_cat_model.multiplier_rate=row[5]
            pay_cat_model.category=row[6]
            pay_cat_model.show_hours=row[7]
            pay_cat_model.show_amount=row[8]
            pay_cat_model.is_irregular_cost=row[9]
            pay_cat_model.sort_order=row[10]
            pay_cat_model.code_name=row[11]
            pay_cat_model.reference_code=row[12]
            pay_cat_model.reference_code_2=row[13]
            
            pay_category_models.append(pay_cat_model)
            
        return pay_category_models