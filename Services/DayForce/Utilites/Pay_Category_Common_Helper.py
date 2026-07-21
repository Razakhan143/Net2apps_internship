from Utilites.Get_and_Post.Pay_Category_Get_Post import Pay_Category_Get_Post
from Utilites.gspread_helper import GspreadSheetHelper
import uuid
class Pay_Category_Common_Helper:
    """this class is responsible for providing common helper methods for pay category validation and update."""

    def maps(self,data):
        """this method maps the data from the Google Sheet to the data from the Dayforce application."""
        return 'None' if data == '' else data
    
    def update_pay_category(self, data_sheet , groups,driver,status):
        """this method updates the pay category data in the Dayforce application using the API."""

        # create a payload for the API call to update the pay category data in the Dayforce application
        rev_groups={k:v for v,k in groups.items()}
        payload=[{"PayCategoryId": data_sheet.pay_category_id if status == "update" else -1,
        "ShortName": data_sheet.object_name,
        "LongName": data_sheet.object_description,
        "ClientId": 112075,
        "CultureId": None,
        "XRefCode": data_sheet.reference_code,
        "XRefCode2": data_sheet.reference_code_2,
        "PayCategoryGroupId": rev_groups.get(data_sheet.pay_category_group),
        "SortOrder": data_sheet.sort_order,
        "DefaultMultiplierRate": data_sheet.multiplier_rate,
        "SystemRequired": True if data_sheet.category == 'System' else False,
        "CodeName": data_sheet.code_name,
        "ShowHours": True if data_sheet.show_hours == 'TRUE' else False,
        "ShowDollars": True if data_sheet.show_amount == 'TRUE' else False,
        "IsIrregularCost": True if data_sheet.is_irregular_cost == 'TRUE' else False,
        "CollapsableLabel": None,
        "NodeLevel": None,
        "CurrentClientId": None,
        "CurrentClientName": None,
        "NumberOfChild": None,
        "ClientEntityId": str(uuid.uuid4()),
        "EntityState": 2 if status == "update" else 1,
        "LastModifiedTimestamp": None,
        "OriginalValues": None,
        "ExtendedProperties": []}]

        # call the API to update the pay category data in the Dayforce application
        call_update_api=Pay_Category_Get_Post()
        call_update_api.update_pay_category(driver, payload)
        if status=='create':
            self.update_id(driver,data_sheet.object_name, data_sheet.item_id)


    def update_id(self,driver, obj_name,id):
        """to update the paycategoryid in gsheets"""
        call_update_api=Pay_Category_Get_Post()
        GSH=GspreadSheetHelper()
        Scrub_id = call_update_api.get_scrub_id(driver)
        pay_categories_api_url = f"https://usstage261.dayforcehcm.com/MyDayforce/u/{Scrub_id}/WFMAdmin/PayCategory/GetPayCategories"
        pay_categories_data=call_update_api.post_pay_category(pay_categories_api_url, driver)['EntityLists'][0]['Entities']
      
        obj = next(
            (item['PayCategoryId'] for item in pay_categories_data if item['ShortName'] == obj_name),
            None
        )
        GSH.worksheet.update(f"O{int(id) + 3}:O{int(id) + 3}",[[obj]])







    def search_item(self, scale_data, models,section_model):
        """function to check if the specific instance is present in the models list from website"""
        for row_no in range(len(models)):
            if row_no < len(section_model) and scale_data == models[row_no][1].rating_scale_name:
                return True, row_no
        return False, 0
    



    