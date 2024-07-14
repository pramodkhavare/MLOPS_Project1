
import os
import sys
import mlflow
import mlflow.sklearn
import numpy as np
import pickle
from src.MLOps_project1.utils.utils import *
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from src.MLOps_project1.logger import logging
from src.MLOps_project1.exception import CustomException
from src.MLOps_project1.entity.config_entity import DataTransformationConfig ,ModelTrainingConfig ,ModelEvaluationConfig
from src.MLOps_project1.entity.artifacts_entity import DataIngestionArtifacts ,DataTransformationArtifacts ,ModelTrainingArtifacts
import mlflow
import mlflow.sklearn
from urllib.parse import urlparse


class ModelEvaluation:
    def __init__(self, 
                config:ModelEvaluationConfig ,
                data_ingestion_artifacts : DataIngestionArtifacts ,
                model_training_artifacts : ModelTrainingArtifacts ,
                data_transformation_artifacts : DataTransformationArtifacts):
        try:

            logging.info(f'\n\n{"*" * 20} Model Evaluation Step Started {"*" *20}') 
            self.model_evaluation_config = config
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.model_training_artifacts = model_training_artifacts 
            self.data_transformation_artifacts = data_transformation_artifacts
        except Exception as e:
            raise CustomException(e ,sys) from e

    def eval_metrics(self,actual,pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))# here is RMSE
        mae = mean_absolute_error(actual, pred)# here is MAE
        r2 = r2_score(actual, pred)# here is r3 value
        logging.info("evaluation metrics captured")
        return rmse, mae, r2

    def initiate_model_evaluation(self):
        try:
             test_array = load_array(self.data_transformation_artifacts.transformed_test_data_path)
             print("Test Array")
             print(test_array)
             X_test,y_test=(test_array[:,:-1], test_array[:,-1])

             model_path=self.model_training_artifacts.trained_model_file_path
             model=load_object(model_path)    
             logging.info("model has register")
             
             mlflow.set_registry_uri("")  #You wil pass uri where you want to register your model if yp=ou try to host your model

             tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme
             print("tracking_url_type_store")

             print(tracking_url_type_store)
             print(mlflow.set_registry_uri(""))

             with mlflow.start_run():

                prediction=model.predict(X_test)

                (rmse,mae,r2)=self.eval_metrics(y_test,prediction)

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)

                 # Model registry does not work with file store
                if tracking_url_type_store != "file":
                    print(122222222)

                    # Register the model
                    # There are other ways to use the Model Registry, which depends on the use case,
                    # please refer to the doc for more information:
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_model")
                else:
                    print(33333333333333)
                    mlflow.sklearn.log_model(model, "model")

        except Exception as e:
            raise CustomException(e,sys)
