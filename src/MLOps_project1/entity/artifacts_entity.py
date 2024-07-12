from dataclasses import dataclass

@dataclass(frozen=True)
class DataIngestionArtifacts:
    train_file_path :str 
    test_file_path :str
    
@dataclass(frozen=True)
class DataTransformationArtifacts:
    transformed_train_data_path : str 
    transformed_test_data_path :str 
    preprocessor_file_path :str
    
@dataclass(frozen=True)
class ModelTrainingArtifacts:
    trained_model_file_path :str 