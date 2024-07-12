# echo [$(date)]: "START"


# echo [$(date)]: "creating env with python 3.8 version" 


# conda create --prefix ./env python=3.8 -y


# echo [$(date)]: "activating the environment" 

# source activate ./env

# echo [$(date)]: "installing the dev requirements" 

# pip install -r requirements.txt

# echo [$(date)]: "END"  


#run file :- bash init_setup.sh

echo [$(date)] : "START"

echo [$(date)] : "Creating environment with python 3.10 version"
python -m venv venv

echo [$(date)] : "Activating virtual environment"
# For Windows
if [[ "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
# For Unix or MacOS
else
    source venv/bin/activate
fi

echo [$(date)] : "Installing required requirements"
pip install -r requirements_dev.txt

echo [$(date)] : "END"
