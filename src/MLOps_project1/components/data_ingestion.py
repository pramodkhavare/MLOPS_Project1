
from src.MLOps_project1.config.configuration import Configuration
from src.MLOps_project1.entity.config_entity import DataIngestionConfig 
from src.MLOps_project1.entity.artifacts_entity import DataIngestionArtifacts
from src.MLOps_project1.logger import logging
from src.MLOps_project1.exception import CustomException
import os ,sys 
import tarfile 
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit 
import shutil  
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.MLOps_project1.config.configuration import Configuration

class DataIngestion():
    def __init__(self ,data_ingestion_config :DataIngestionConfig):
        try:
            logging.info(f"{'*'*20}Data Ingestion Step Started{'*'*20}")
            self.config = data_ingestion_config  
            # print(self.config)
        except Exception as e:
            raise CustomException(e ,sys) from e
        
        
    def download_and_extract_data_file(self):
        try:
            pass 
        except Exception as e:
            raise CustomException(e ,sys) from e
    
    def initiate_data_ingestion(self):
        logging.info("data ingestion started")
        
        try:
            data=pd.read_csv(r"D:\Data Science\MachineLearning\Project\UnderProcessProject\MLOPS_Project1\experiments\data\train.csv")
            logging.info(" i have read dataset as a df")
            
            
            os.makedirs(self.config.raw_data_path,exist_ok=True)
            data.to_csv(os.path.join(self.config.raw_data_path, "raw_data.csv",),index=False)
            logging.info(" i have saved the raw dataset in artifact folder")
            
            logging.info("here i have performed train test split")
            
            train_data,test_data=train_test_split(data,test_size=0.25)
            logging.info("train test split completed")
            
            
            
            os.makedirs(self.config.train_data_path ,exist_ok=True)
            train_data.to_csv(os.path.join(self.config.train_data_path ,"train_data.csv"),index=False)
            
            os.makedirs(self.config.test_data_path ,exist_ok=True)
            test_data.to_csv(os.path.join(self.config.test_data_path ,"test_data.csv"),index=False)
            
            logging.info("data ingestion part completed")
            
            
            
            
            
            data_ingestion_artifacts = DataIngestionArtifacts(
                test_file_path= os.path.join(self.config.test_data_path ,"test_data.csv"),
                train_file_path=os.path.join(self.config.train_data_path ,"train_data.csv")
            )
            print(data_ingestion_artifacts)
            return (
                 data_ingestion_artifacts
            )
            
            
        except Exception as e:
           logging.info("exception during occured at data ingestion stage")
           raise CustomException(e,sys) 
       
       
