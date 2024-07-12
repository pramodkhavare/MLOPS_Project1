from src.MLOps_project1.components.data_ingestion import DataIngestion
from src.MLOps_project1.components.data_transformation import DataTransformation
from src.MLOps_project1.components.model_training import ModelTrainer
from src.MLOps_project1.exception import CustomException 
from src.MLOps_project1.logger import logging 
from src.MLOps_project1.config.configuration import Configuration
from src.MLOps_project1.entity.artifacts_entity import DataIngestionArtifacts ,DataTransformationArtifacts
import os ,sys
import pandas as pd
import uuid
from threading import Thread
from collections import namedtuple
from datetime import datetime


if __name__ == "__main__":
    configuration = Configuration()
    data_ingestion = DataIngestion(data_ingestion_config=configuration.get_data_ingestion_config())
    data_ingestion.initiate_data_ingestion() 
    
class Pipeline(Thread):
    def __init__(self ,config:Configuration=Configuration()):
        try:
             os.makedirs(config.get_training_pipeline_config().artifact_dir ,exist_ok=True) 
             self.config = config 
        except Exception as e:
            raise CustomException(e ,sys)
        
    def start_data_ingestion(self) ->DataIngestionArtifacts:
        try:
            data_ingestion_config = self.config.get_data_ingestion_config()
        
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_output = data_ingestion.initiate_data_ingestion()

            print('Data Ingestion Completed\n')

            return data_ingestion_output
        
        except Exception as e:
            raise CustomException(e ,sys)
        
    def start_data_transformation(self ,data_ingestion_artifacts:DataIngestionArtifacts ) ->DataTransformationArtifacts:
        try:
            data_transformation_config = self.config.get_data_transformation_config()
            data_ingestion_artifact = data_ingestion_artifacts
            data_transformation_artifacts = DataTransformation(
                data_transformation_config=data_transformation_config
            )
            train_path = data_ingestion_artifact.train_file_path
            test_path = data_ingestion_artifact.test_file_path
            data_transformation_artifacts = data_transformation_artifacts.initialize_data_transformation(
                train_path= train_path,
                test_path= test_path
            )

            print('Data Transformation Completed\n')
            return data_transformation_artifacts
        except Exception as e:
            raise CustomException(e ,sys) 
        
    def start_model_training(self ,data_transformation_artifacts:DataTransformationArtifacts):
        try:
            model_training_config = self.config.get_model_trainer_config()
            
        
            model_trainer = ModelTrainer(
                model_training_config=model_training_config ,
                data_transformation_artifacts= data_transformation_artifacts
            )
            
            
         
            print("Model Training Completed\n")
            return model_trainer.initate_model_training(
          
            )
        except Exception as e:
            raise CustomException(e ,sys) from e  


    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            data_transformation_artifacts = self.start_data_transformation(
                data_ingestion_artifacts=data_ingestion_artifacts 
            )
            model_training_artifacts = self.start_model_training(data_transformation_artifacts=data_transformation_artifacts)
        except Exception as e:
            raise CustomException(e ,sys)
        
        
    def run(self):
        try:
            self.run_pipeline()

        except Exception as e:
            raise CustomException(e ,sys) from e 
        
        
if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run() 
    
# src\MLOps_project1\pipeline\training_pipeline.py