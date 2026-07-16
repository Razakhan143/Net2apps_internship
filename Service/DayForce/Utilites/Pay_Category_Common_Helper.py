from Service.DayForce.Utilites.Get_and_Post.Pay_Category_Get_Post import Pay_Category_Get_Post

class Pay_Category_Common_Helper:
    """this class is responsible for providing common helper methods for pay category validation and update."""

    def maps(self,data):
        """this method maps the data from the Google Sheet to the data from the Dayforce application."""
        return 'None' if data == '' else data
    
    def update_pay_category(self, data_sheet , groups,driver,id):
        """this method updates the pay category data in the Dayforce application using the API."""

        # create a payload for the API call to update the pay category data in the Dayforce application
        rev_groups={k:v for v,k in groups.items()}
        payload=[{"PayCategoryId": id,
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
        "ClientEntityId": "89aa80fb-335d-43a2-87d6-f951531ef970",
        "EntityState": 2,
        "LastModifiedTimestamp": None,
        "OriginalValues": None,
        "ExtendedProperties": []}]

        # call the API to update the pay category data in the Dayforce application
        call_update_api=Pay_Category_Get_Post()
        call_update_api.update_pay_category(driver, payload)
    