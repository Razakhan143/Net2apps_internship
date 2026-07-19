class Base_Model:
    """class to define the data model for the rating scale designer"""
    item_id=''
    item_name=''
    item_description=''
    option_score=''
    option_label=''
    option_description=''




class rating_scale_Processing_Model(Base_Model):
    """class to define the data model for the rating scale designer"""
    item_id=''
    processing_status=''
    processing_rating_scale=''

    

class rating_scale_Rating_Scale_Model(Base_Model):
    """class to define the data model for the rating scale designer"""
    rating_scale_name=''
    rating_scale_description=''

    

class rating_scale_Scores_Model(Base_Model):
    """class to define the data model for the rating scale designer"""
    rating_scale=''
    option_score=''
    option_label=''
    option_description=''
