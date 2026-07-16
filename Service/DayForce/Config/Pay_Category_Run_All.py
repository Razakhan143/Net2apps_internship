# importing the required modules for the test cases
from Service.DayForce.TestCases.Pay_Category_Reverse import  Pay_Category_Reverse
from Service.DayForce.TestCases.Pay_Category_Validate import  Pay_Category_Validation
from Service.DayForce.TestCases.Pay_Category_Automate import  Pay_Category_Automate
from Service.DayForce.Controllers.Pay_Category_Load_fill_Controller import  Pay_Category_fill_controller


if __name__ == "__main__":

    #============== Performing the Reverse test case for Pay Category ==============
    pay_category_reverse = Pay_Category_Reverse()
    web_models, groups, driver = pay_category_reverse.Pay_Category_Reverse()

    #============== Reverse Completed ===================

    #============== Performing the Fill test case for Pay Category ==============
    # pay_category_fill = Pay_Category_fill_controller()
    # pay_category_fill.pay_category_fill_controller(web_models)

    #============== Fill Completed ===================

    # #============== Performing the Validation test case for Pay Category ==============
    pay_category_validation = Pay_Category_Validation()
    pay_category_validation.validate_pay_category(web_models)

    #============== Validation Completed ===================

    #============== Performing the Automate test case for Pay Category ==============
    # pay_category_automate = Pay_Category_Automate()
    # pay_category_automate.automate_pay_category(driver, web_models, groups)

    # #============== Automation Completed ===================