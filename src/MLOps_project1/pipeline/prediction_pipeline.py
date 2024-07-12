
import sys
import os
from src.MLOps_project1.utils.utils import *
import pandas as pd
from src.MLOps_project1.logger import logging
from src.MLOps_project1.exception import CustomException



class CustomData():
    def __init__(self,
                 carat:float,
                 depth:float,
                 table:float,
                 x:float,
                 y:float,
                 z:float,
                 cut:str,
                 color:str,
                 clarity:str )->None:
        
        self.carat=carat
        self.depth=depth
        self.table=table
        self.x=x
        self.y=y
        self.z=z
        self.cut = cut
        self.color = color
        self.clarity = clarity 
    
    
    def get_data_as_dataframe(self):
        try:
            data_dictionary={
                'carat':[self.carat],
                'depth':[self.depth],
                'table':[self.table],
                'x':[self.x],
                'y':[self.y],
                'z':[self.z],
                'cut':[self.cut],
                'color':[self.color],
                'clarity':[self.clarity] 
                
            }
            
            df=pd.DataFrame(data_dictionary)
            logging.info("Dataframe created")
            return df
        
        except Exception as e:
            logging.info("Exception occured in prediction")
            raise CustomException(e,sys)




class PredictPipeline:
    def __init__(self ,model_dir:str ,preprocessor_dir:str):
        try:
            #We will pass saved_models folde path as input 
            self.model_dir = model_dir 
            self.preprocessor_dir = preprocessor_dir

        except Exception as e:
            raise CustomException(e ,sys) from e 
        
    def get_latest_model_path(self):
        try:
            # Get list of folders in the specified directory

            folder_list = os.listdir(self.model_dir)
            # Sort the folders by name (which represents the date)
            sorted_folders = sorted(folder_list, reverse=True)

            # Extract the newest folder (first element after sorting)
            newest_folder = sorted_folders[0] 
            filename = os.listdir(os.path.join(self.model_dir ,newest_folder))[0]
            file_path = os.path.join(self.model_dir ,newest_folder ,filename)

            return file_path
        except Exception as e:
            raise CustomException(e ,sys) from e 
        
    def get_latest_preprocessor_path(self):
        try:
            folder_path =self.preprocessor_dir
            folder_list = os.listdir(folder_path)
            sorted_folders = sorted(folder_list, reverse=True)
            newest_folder = sorted_folders[0] 
            preprocesssor_dir = os.listdir(os.path.join(folder_path,newest_folder))[0]
            preprocessor = os.listdir(os.path.join(folder_path,newest_folder ,preprocesssor_dir))[0]
            preprocessor_path = os.path.join(folder_path ,newest_folder ,preprocesssor_dir,preprocessor)

            return preprocessor_path

        except Exception as e:
            raise CustomException(e, sys) from e 
    
    
    
    def pipeline_config(self,feature):
        
        try:
            # logging.info('Reading preprocessor and model pkl file')
            prerocessor_path=self.get_latest_preprocessor_path()
            mode_path= self.get_latest_model_path()
            
            
            preprocessor=load_object(prerocessor_path)
            model=load_object(mode_path)
            logging.info('.pkl file converted')
            
            scaled_data=preprocessor.transform(feature)
            
            y_prediction=model.predict(scaled_data)
            
            return y_prediction
        
    
        except Exception as e:
            logging.info("Exception occured in prediction")
            raise CustomException(e,sys)
        
        
        
        
if __name__ == "__main__":
    model_dir = r"D:\Data Science\MachineLearning\Project\UnderProcessProject\MLOPS_Project1\artifact\model_training"
    preprocessor_dir = r"D:\Data Science\MachineLearning\Project\UnderProcessProject\MLOPS_Project1\artifact\transformed_data_dir"
    pipeline = PredictPipeline(
        model_dir= model_dir,
        preprocessor_dir= preprocessor_dir
    ) 
    
    
    
# src\MLOps_project1\pipeline\prediction_pipeline.py