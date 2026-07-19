from Models.rating_scale_data_model import rating_scale_Processing_Model, rating_scale_Rating_Scale_Model, rating_scale_Scores_Model
from Utilites.gspread_helper import GspreadSheetHelper
class rating_scale_fill_sheet_controller:
    """class to fill the data into the google sheet"""

    #making object of  GspreadSheetHelper
    GSH=GspreadSheetHelper()
    
    def rating_scale_processing_fill_controller(self,models):
        """function to fill the Rating Scale data into the google sheet of Processing Section"""

        # Clearing the sheet before filling the data to avoid duplication
        self.GSH.clear_sheet('A', 'K')
        rows=[]
        for  model in models:
            rows.append([model[0].item_id,
                        model[0].processing_status,
                        model[0].processing_rating_scale])

        self.GSH.update_sheet('A', 'C', rows)
        
        

    def rating_scale_description_fill_controller(self,models):
        """function to fill the Rating Scale data into the google sheet of Description Section"""

        rows=[]
        for model in models:
            rows.append([model[1].rating_scale_name,
                        model[1].rating_scale_description])

        self.GSH.update_sheet('E', 'F', rows)



    def rating_scale_scores_fill_controller(self,models):
        """function to fill the Rating Scale data into the google sheet of Score Section"""

        rows=[]
        for row in models:
            for model in row[2]:
                rows.append([model.rating_scale,
                            model.option_score,
                            model.option_label,
                            model.option_description])

        self.GSH.update_sheet('H', 'K', rows)




class rating_scale_loader_controller:
    """class to load the data from the google sheet"""

    GSH=GspreadSheetHelper()
    rows=GSH.get_sheet_data('A','K')

    def rating_scale_processing_loader_controller(self):
        """function to load the Rating Scale data from the google sheet of Processing Section"""

        data_list=[]
        for row in self.rows:
            if row[1] == 'Processed':
                continue
            processing_model = rating_scale_Processing_Model()
            processing_model.item_id = row[0]
            processing_model.processing_status = row[1]
            processing_model.processing_rating_scale = row[2]
            data_list.append(processing_model)

        return data_list


    def rating_scale_description_loader_controller(self):
        """function to load the Rating Scale data from the google sheet of Description Section"""

        data_list=[]
        for row in self.rows:
            if row[1] == 'Processed' or not row[4]:
                continue
            rating_scale_model = rating_scale_Rating_Scale_Model()
            rating_scale_model.item_id = row[0]
            rating_scale_model.rating_scale_name = row[4]
            rating_scale_model.rating_scale_description = row[5]
            data_list.append(rating_scale_model)
        return data_list



    def rating_scale_scores_loader_controller(self):
        """function to load the Rating Scale data from the google sheet of Score Section"""

        data_list=[]
        for row in self.rows:
            if row[1] == 'Processed' or not row[4]:
                continue
            row_list=[]
            for i in self.rows:
                if row[4] == i[7]:
                    scores_model = rating_scale_Scores_Model()
                    scores_model.rating_scale = i[7]
                    scores_model.option_score = i[8]
                    scores_model.option_label = i[9]
                    scores_model.option_description = i[10]
                    row_list.append(scores_model)
            data_list.append(row_list)

        return data_list



