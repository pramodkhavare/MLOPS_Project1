
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

from src.MLOps_project1.utils.utils import *
from src.MLOps_project1.entity.config_entity import DataTransformationConfig
from src.MLOps_project1.entity.artifacts_entity import DataTransformationArtifacts


class DataTransformation:
    def __init__(self ,data_transformation_config:DataTransformationConfig ):
        try:
            logging.info(f"{'*'*20}Data Ingestion Step Started{'*'*20}")
            self.config = data_transformation_config  
            # print(self.config) 
        except Exception as e:
            raise CustomException(e,sys)
        
    
    def get_data_transformation(self):
        
        try:
            logging.info('Data Transformation initiated')
            
            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = ['cut', 'color','clarity']
            numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']
            
            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
            
            logging.info('Pipeline Initiated')
            
            ## Numerical Pipeline
            num_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())

                ]

            )
            
            # Categorigal Pipeline
            cat_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('ordinalencoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                ('scaler',StandardScaler())
                ]

            )
            
            preprocessor=ColumnTransformer([
            ('num_pipeline',num_pipeline,numerical_cols),
            ('cat_pipeline',cat_pipeline,categorical_cols)
            ])
            
            return preprocessor
            

            
            
        
        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")
            raise CustomException(e,sys)
            
    
    def initialize_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            
            logging.info("read train and test data complete")
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head : \n{test_df.head().to_string()}')
            
            preprocessing_obj = self.get_data_transformation()
            
            target_column_name = 'price'
            drop_columns = [target_column_name,'id']
            
            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]
            
            
            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]
            
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            
            logging.info("Applying preprocessing object on training and testing datasets.")
            
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            print(train_arr)
            preprocessor_file_path = os.path.join(
                self.config.preprocessor_obj_dir_path ,
                self.config.preprocessor_file_name
            )
            os.makedirs(self.config.transformed_train_dir_path ,exist_ok=True)
            transformed_train_data_path = os.path.join(self.config.transformed_train_dir_path ,'train.npz')

            save_numpy_array(
                file_path=transformed_train_data_path ,
                array= train_arr
            )
            
            os.makedirs(self.config.transformed_test_dir_path ,exist_ok=True)
            transformed_test_data_path = os.path.join(self.config.transformed_test_dir_path ,'test.npz')
            save_numpy_array(
                file_path= transformed_test_data_path ,
                array= test_arr
            )
            
            
            save_object(
                file_path=preprocessor_file_path,
                obj=preprocessing_obj
            )
            
            logging.info("preprocessing pickle file saved")
      
            data_trandformation_artifacts = DataTransformationArtifacts(
                transformed_train_data_path = transformed_train_data_path ,
                transformed_test_data_path = transformed_test_data_path ,
                preprocessor_file_path = preprocessor_file_path
            )
            
            return data_trandformation_artifacts
        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")
            raise CustomException(e,sys)
            


