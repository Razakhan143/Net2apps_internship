class rating_scale_operation_helpers:
    """class to perform the operation for the rating scale designer"""

    same_item_id=''

    def get_scale_if_exists(self, scale_data, models,section_model):
        """function to check if the specific instance is present in the models list from website"""
        for row_no in range(len(models)):
            if row_no < len(section_model) and scale_data == models[row_no][1].rating_scale_name:
                return True, row_no
        return False, 0
    


    def update_scale(self, rating_scale_data, scores_data, wrapper):
        """function to check the condition call the function for create new instance or update the existing instance of the rating scale designer"""
        auto_changes= rating_scale_automation_changes_web()
        
        all_instance=wrapper.find_elements("XPATH","//a[contains(@id,'link') and @class='fd-link fd-link--compact']")
        
        if rating_scale_data.rating_scale_name in [instance.text for instance in all_instance]:
            
            wrapper.click_element("LINK_TEXT", rating_scale_data.rating_scale_name)
            auto_changes.rating_scale_exist(rating_scale_data, scores_data, wrapper)
        else:
            auto_changes.rating_scale_notexist(rating_scale_data, scores_data, wrapper)

    

    

class rating_scale_automation_changes_web:
    """class to perform the automation process for the rating scale designer"""

    def fill_name_disc(self, data, xpath, wrapper, locator):
        """function to fill the name and description of the rating scale designer"""
        wrapper.send_keys_to_element(locator, xpath, data)

    def fill_scores_data(self, data, xpath, wrapper, locator):
        """function to fill the score, label and description of the rating scale designer"""
        elements = wrapper.find_elements(locator, xpath)
        for new_data, element in zip(data, elements):
            element.clear()
            element.send_keys(new_data)

    def rating_scale_exist(self, rating_scale_data, scores_data, wrapper):
        """function to update the existing instance of the rating scale designer"""
        # checking the number of scores in the data list and the web page
        data_list = self.combine_scores_data(rating_scale_data, scores_data)
        scores_sheet = len(data_list[2])
        scores_web = len(wrapper.find_elements("XPATH", "//input[@size='7']"))

        print(f"Number of Scores in the Sheet: {scores_sheet}, Number of Scores in the web page: {scores_web}")

        if scores_sheet > scores_web:
            for _ in range(scores_sheet - scores_web):
                self.create_new_option(wrapper)
        elif scores_sheet < scores_web:
            for _ in range(scores_web - scores_sheet):
                self.delete_option(wrapper)

        self.fill_name_disc(data_list[0], "48:_txtFld", wrapper, "ID")
        self.fill_name_disc(data_list[1], "50:_txtArea", wrapper, "ID")
        self.fill_scores_data(data_list[2], "//input[@size='7']", wrapper, "XPATH")
        self.fill_scores_data(data_list[3], "//input[@size='34']", wrapper, "XPATH")
        self.fill_scores_data(data_list[4], "//textarea[@cols='42']", wrapper, "XPATH")

        wrapper.click_element("ID", "38:_link") # Save the Updated Scale
        wrapper.refresh()

    def rating_scale_notexist(self, rating_scale_data, scores_data, wrapper):
        """function to create a new instance of the rating scale designer"""
        print("creating new instance of the rating scale designer")
        wrapper.click_element("ID", "17:_link")
        wrapper.click_element("XPATH", "//label[contains(text(),'Build your own')]")
        wrapper.click_element("XPATH", "//button[@title='OK']")
        print("Filling the data in the new instance")
        self.rating_scale_exist(rating_scale_data, scores_data, wrapper)

    def create_new_option(self, wrapper):
        """function to create a new option in the rating scale designer"""
        print("Creating a new option in the rating scale designer.")
        wrapper.click_element("XPATH", "//a[contains(text(),'Add New Score')]")

    def delete_option(self, wrapper):
        """function to delete an option in the rating scale designer"""
        print("Deleting an option in the rating scale designer.")
        option = wrapper.find_elements("XPATH", "//a[@class='fd-link fd-link--compact ratingScaleSmallIconPadding deleteIcon']")
        option[0].click()

    def combine_scores_data(self, rating_scale_data, scores_data):
        data_list = []
        data_list.append(rating_scale_data.rating_scale_name)
        data_list.append(rating_scale_data.rating_scale_description)
        data_list.append([row.option_score for row in scores_data])
        data_list.append([row.option_label for row in scores_data])
        data_list.append([row.option_description for row in scores_data])
        return data_list

