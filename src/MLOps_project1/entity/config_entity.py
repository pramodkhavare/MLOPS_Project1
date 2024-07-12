
import os ,sys 
from datetime import datetime
#We are going to store information but not in classes but tuple
# We can use other options like list ,dict (dict is mutable)
from collections import namedtuple
from dataclasses import dataclass


def get_time_stamp():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


@dataclass(frozen= True)
class TrainingPipelineConfig():
    artifact_dir :str
    

@dataclass(frozen= True)
class DataIngestionConfig():
    raw_data_path :str 
    train_data_path :str 
    test_data_path :str 
    
@dataclass(frozen=True)
class DataTransformationConfig:
    preprocessor_obj_dir_path :str 
    preprocessor_file_name :str 
    transformed_test_dir_path :str 
    transformed_train_dir_path :str
    
     
@dataclass(frozen=True) 
class ModelTrainingConfig:
    trained_model_file_path :str 
    model_file_name : str  
    base_accuracy :str 