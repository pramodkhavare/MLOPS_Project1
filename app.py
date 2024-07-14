from flask import Flask ,request 
import os ,sys
import pip 
import json 
from flask import render_template ,abort ,send_file

from src.MLOps_project1.logger import logging
from src.MLOps_project1.exception import CustomException
from src.MLOps_project1.pipeline.prediction_pipeline import PredictPipeline ,CustomData
from src.MLOps_project1.pipeline.training_pipeline import Pipeline
from src.MLOps_project1.constant import CONFIG_DIR
from src.MLOps_project1.logger import get_log_dataframe
from src.MLOps_project1.config.configuration import Configuration
from src.MLOps_project1.utils.utils import read_yaml ,load_object 

ROOT_DIR =os.getcwd()
SAVED_MODEL_DIR = r"D:\Data Science\MachineLearning\Project\UnderProcessProject\MLOPS_Project1\artifact\model_training"
PROCESSOR_DIR = r"D:\Data Science\MachineLearning\Project\UnderProcessProject\MLOPS_Project1\artifact\transformed_data_dir"


app = Flask(__name__)   #app is Flask object

@app.route('/')
def home_page():
    return render_template('index.html')



@app.route('/predict' ,methods=['GET' ,"POST"])
def predict_datapoint():
    if request.method=='GET':
        return render_template('form.html')
    else:
        customize_data_config=CustomData(
                   carat=float(request.form.get('carat')),
                   depth=float(request.form.get('depth')),
                   table=float(request.form.get('table')),
                   x=float(request.form.get('x')),
                   y=float(request.form.get('y')),
                   z=float(request.form.get('z')),
                   cut=(request.form.get('cut')),
                   color=(request.form.get('color')),
                   clarity=(request.form.get('clarity'))
                   )

        final_data=customize_data_config.get_data_as_dataframe()
        pipeline=PredictPipeline(
            model_dir=SAVED_MODEL_DIR,
            preprocessor_dir= PROCESSOR_DIR
        )
        predicted_data=pipeline.pipeline_config(final_data)
        
        results=round(predicted_data[0],2)
        print(results)
        return render_template('form.html',final_result=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
    # from src.MLOps_project1.utils.utils import load_object 

    # model = load_object("D:\\Data Science\\MachineLearning\\Project\\UnderProcessProject\\MLOPS_Project1\\artifact\\model_training\\2024-07-12-22-37-29\\trained_model")
    