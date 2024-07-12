from flask import Flask ,request 
import os ,sys
import pip 
import json 
from flask import render_template ,abort ,send_file

from src.MLOps_project1.logger import logging
from src.MLOps_project1.exception import HousingException
from src.MLOps_project1.pipeline.prediction_pipeline import HousingData ,Prediction
from src.MLOps_project1.pipeline.training_pipeline import Pipeline
from src.MLOps_project1.constant import CONFIG_DIR
from src.MLOps_project1.logger import get_log_dataframe
from src.MLOps_project1.config.configuration import HousingConfiguration
from src.MLOps_project1.utils.utils import write_yaml ,read_yaml ,load_object

ROOT_DIR =os.getcwd()
SAVED_MODEL_DIR = r"D:\Data Science\MachineLearning\Project\UnderProcessProject\MLOPS_Project1\artifact\model_training"
PROCESSOR_DIR = r"D:\Data Science\MachineLearning\Project\UnderProcessProject\MLOPS_Project1\artifact\transformed_data_dir"