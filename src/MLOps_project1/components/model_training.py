
import os
import sys
import pandas as pd
import numpy as np

from dataclasses import dataclass
from src.MLOps_project1.exception import CustomException
from src.MLOps_project1.logger import logging

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler
from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet

from src.MLOps_project1.utils.utils import *
from src.MLOps_project1.entity.config_entity import DataTransformationConfig ,ModelTrainingConfig
from src.MLOps_project1.entity.artifacts_entity import DataTransformationArtifacts ,ModelTrainingArtifacts

@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')
    
    
class ModelTrainer():
    def __init__(self,
                model_training_config :ModelTrainingConfig ,
                data_transformation_artifacts :DataTransformationArtifacts ,
                ):
        try:
            logging.info(f'\n\n{"*" *20} Model Training Started{"*" *20}')
            self.model_training_config =model_training_config
            self.data_transformation_artifacts =data_transformation_artifacts 
        except  Exception as e:
            raise CustomException(e,sys) from e
    
    def initate_model_training(self):
        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')
            train_array_path  =self.data_transformation_artifacts.transformed_train_data_path
            test_arra_path = self.data_transformation_artifacts.transformed_test_data_path
            train_array = load_array(train_array_path)
            test_array = load_array(test_arra_path)
            
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
            'LinearRegression':LinearRegression(),
            'Lasso':Lasso(),
            'Ridge':Ridge(),
            'Elasticnet':ElasticNet()
        }
            
            model_report:dict=evaluate_model(X_train,y_train,X_test,y_test,models)
            print(model_report)
            print('\n====================================================================================\n')
            logging.info(f'Model Report : {model_report}')

            # To get best model score from dictionary 
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]

            print(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')

            save_object(
                 file_path=self.model_training_config.trained_model_file_path,
                 obj=best_model
            )
            model_training_artifacts = ModelTrainingArtifacts(
                trained_model_file_path=self.model_training_config.trained_model_file_path
            )
            
            return model_training_artifacts
          

        except Exception as e:
            logging.info('Exception occured at Model Training')
            raise CustomException(e,sys)