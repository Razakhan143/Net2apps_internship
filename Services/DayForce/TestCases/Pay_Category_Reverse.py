import time
from Models.Pay_Category_Models import Pay_Category_Model
from Utilites.Get_and_Post.Pay_Category_Get_Post import Pay_Category_Get_Post
from Utilites.Login import login_dayforce
from Controllers.Pay_Category_Load_fill_Controller import  Pay_Category_fill_controller

class Pay_Category_Reverse:
    """this class is responsible for reversing the pay category data from the Dayforce application."""
    def Pay_Category_Reverse(self):
        """this method reverses the pay category data from the Dayforce application."""

        # get the pay category data from the Dayforce application using the API and return it as a list of web models, group data and driver
        Login = login_dayforce()
        driver = Login.login()
        print("Login Successful")
        pay_category_api = Pay_Category_Get_Post()
        Scrub_id = pay_category_api.get_scrub_id(driver)

        # get the pay category data from the Dayforce application using the API and return it as a list of web models, group data and driver
        url_pay_category = f"https://usstage261.dayforcehcm.com/MyDayforce/u/{Scrub_id}/Common/#SFRNTFBheUNhdGVnb3J5"
        time.sleep(5)
        driver.get(url_pay_category)
        pay_categories_api_url = f"https://usstage261.dayforcehcm.com/MyDayforce/u/{Scrub_id}/WFMAdmin/PayCategory/GetPayCategories"
        pay_categories_group_api_url = f"https://usstage261.dayforcehcm.com/MyDayforce/u/{Scrub_id}/WFMAdmin/PayCategory/GetPayCategoryGroups"

        # get the pay category data from the Dayforce application using the API and return it as a list of web models, group data and driver
        pay_categories_data=pay_category_api.post_pay_category(pay_categories_api_url, driver)['EntityLists'][0]['Entities']
        group_data=pay_category_api.post_pay_category(pay_categories_group_api_url, driver)
        group_id_to_name={group['PayCategoryGroupId'] : group['ShortName'] for group in group_data['Result']}
        
        # create a list of pay category models from the pay category data and return it as a list of web models, group data and driver
        data_list=[]
        for i, pay_category in enumerate(pay_categories_data):
            pay_cat_model=Pay_Category_Model()
            pay_cat_model.item_id = i+1
            pay_cat_model.pay_category_id = pay_category['PayCategoryId']
            pay_cat_model.processing_status = 'Processed'
            pay_cat_model.object_name=pay_category['ShortName']
            pay_cat_model.object_description=pay_category['LongName']
            pay_cat_model.pay_category_group=group_id_to_name.get(pay_category['PayCategoryGroupId'], '')
            pay_cat_model.multiplier_rate=pay_category['DefaultMultiplierRate']
            pay_cat_model.category='System' if pay_category['SystemRequired'] else 'Custom'
            pay_cat_model.show_hours=pay_category['ShowHours']
            pay_cat_model.show_amount=pay_category['ShowDollars']
            pay_cat_model.is_irregular_cost=pay_category['IsIrregularCost']
            pay_cat_model.sort_order=pay_category['SortOrder']
            pay_cat_model.code_name=pay_category['CodeName']
            pay_cat_model.reference_code=pay_category['XRefCode']
            pay_cat_model.reference_code_2=pay_category['XRefCode2']
            pay_cat_model.client_entity_id=pay_category['ClientEntityId']
            data_list.append(pay_cat_model)
        
        print("Pay Category Reverse Completed")
        return data_list, group_id_to_name, driver 







if __name__ == "__main__":

    #============== Performing the Reverse test case for Pay Category ==============
    pay_category_reverse = Pay_Category_Reverse()
    web_models, groups, driver = pay_category_reverse.Pay_Category_Reverse()

    #============== Reverse Completed ===================

    #============== Performing the Fill test case for Pay Category ==============
    pay_category_fill = Pay_Category_fill_controller()
    pay_category_fill.pay_category_fill_controller(web_models)

    #============== Fill Completed ===================