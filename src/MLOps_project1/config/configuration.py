from dataclasses import dataclass
import os ,sys 
from src.MLOps_project1.entity.config_entity import DataIngestionConfig ,TrainingPipelineConfig ,\
                                                    DataTransformationConfig,ModelTrainingConfig ,ModelEvaluationConfig

from src.MLOps_project1.utils.utils import read_yaml
from src.MLOps_project1.constant import *
from src.MLOps_project1.exception import CustomException
from src.MLOps_project1.logger import logging


class Configuration():
    def __init__(self , config_file_path = CONFIG_FILE_PATH ,
                 current_time_stamp = CURRENT_TIME_STAMP):
        try:
            # self.config_info = read_yaml(yaml_file_path= config_file_path)
            self.config_info = read_yaml(r'D:\Data Science\MachineLearning\Project\UnderProcessProject\MLOPS_Project1\config\config.yaml')
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp

        except Exception as e:
            raise CustomException (e ,sys) 
        
        
    def get_data_ingestion_config(self) ->DataIngestionConfig:
        try:
            config = self.config_info[DATA_INGESTION_CONFIG_KEY]
            
            
            data_ingestion_dir_key = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[DATA_INGESTION_DIR_KEY] ,
                self.time_stamp
            )
            raw_data_path = os.path.join(
                # self.training_pipeline_config.artifact_dir ,
                data_ingestion_dir_key ,
                config[RAW_DATA_DIR_KEY]

            )
            train_data_path = os.path.join(
                data_ingestion_dir_key ,
                config[INGESTED_DIR_KEY] ,
                config[INGESTED_TRAIN_DIR]
            )
            
            test_data_path = os.path.join(
                data_ingestion_dir_key ,
                config[INGESTED_DIR_KEY] ,
                config[INGESTED_TEST_DIR]
            )
             
            data_ingestion_config = DataIngestionConfig(
                raw_data_path= raw_data_path,
                train_data_path= train_data_path,
                test_data_path= test_data_path
            )
            return data_ingestion_config
        except Exception as e:
            raise CustomException (e ,sys) 
        
    def get_data_transformation_config(self) ->DataTransformationConfig:
        try:
            logging.info("Getting Data Transformation Config Component")
            config = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            transformed_dir = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[TRANSFORMED_DIR_KEY],
                self.time_stamp
            )
            transformed_train_dir = os.path.join(
                transformed_dir ,
                config[TRANSFORMED_TRAIN_DIR_KEY]
            )
            transformed_test_dir = os.path.join(
                transformed_dir ,
                config[TRANSFORMED_TEST_DIR_KEY]
            )
            preprocessed_object_dir = os.path.join(
                transformed_dir ,
                config[PREPROCESSING_DIR_KEY]
            )
            preprocessing_object_file_name = config[PREPROCESSING_OBJECT_FILE_NAME_KEY]

            data_transformation_config = DataTransformationConfig(
                preprocessor_obj_dir_path= preprocessed_object_dir,
                preprocessor_file_name = preprocessing_object_file_name,
                transformed_test_dir_path = transformed_test_dir,
                transformed_train_dir_path = transformed_train_dir
            )
            print(data_transformation_config)

            logging.info(f"Data Transformation Config : [{data_transformation_config}]")
            return data_transformation_config  
        
        except Exception as e:
            raise CustomException (e ,sys)
        
        
    def get_model_trainer_config(self) ->ModelTrainingConfig:

        try:
            config = self.config_info[MODEL_TRAINING_CONFIG_KEY]
            trained_model_file_path = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[TRAINED_MODEL_DIR_NAME_KEY] ,
                self.time_stamp ,
                config[TRAINED_MODEL_ARTIFACTS_KEY] ,
                config[MODEL_FILE_NAME_KEY] 
            )

            model_file_name = config[MODEL_FILE_NAME_KEY] 
            base_accuracy = config[BASE_ACCURACY]

            # model_config_file_path = os.path.join(
            #     ROOT_DIR ,
            #     config[MODEL_CONFIG_DIR] ,
            #     config[MODEL_CONFIG_FILE_NAME_KEY]
            # )
        
            model_training_config = ModelTrainingConfig(
                trained_model_file_path= trained_model_file_path,
                model_file_name = model_file_name,
                base_accuracy= base_accuracy
            )
            

            return model_training_config


        except Exception as e:
            raise CustomException (e ,sys)
        
        
          
        
    def get_training_pipeline_config(self) ->TrainingPipelineConfig:
        try:
            config = self.config_info[TRAINING_PIPELINE_CONFIG]
            artifact_dir  = os.path.join(ROOT_DIR 
                                         ,config[TRAINING_PIPELINE_CONFIG_ARTIFACTS_DIR])
            
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            return training_pipeline_config

        except Exception as e:
            raise CustomException (e ,sys)
        
    def get_model_evalution_config(self) ->ModelEvaluationConfig:
        try:
            model_evaluation_config = ModelEvaluationConfig(
                model_evaluation_file_path= "Pass"
            ) 
            
            return model_evaluation_config
        except Exception as e:
            raise CustomException (e ,sys)


if __name__ == "__main__":
    config =Configuration()
    config.get_model_trainer_config()
    
    
    
# D:\Data Science\MachineLearning\Project\UnderProcessProject\MLOPS_Project1\src\MLOps_project1\config\configuration.py