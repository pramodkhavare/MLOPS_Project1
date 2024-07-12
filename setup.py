from setuptools import setup, find_packages
from typing import List

PROJECT_NAME = "MLOPS_Project1"
VERSION = "0.0.1"
DESCRIPTION = "This is python package which help you to create ENd to End ML pipeline"
AUTHOR_NAME = "Pramod Khavare"
AUTHOR_EMIL = "pramodkhavare2000@gmail.com"
# REPO_NAME = "github repo name"

REQUIREMENTS_FILE_NAME = "./requirements_dev.txt"

HYPHEN_E_DOT = "-e ."

def get_requirements_list()->List[str]:
    with open(REQUIREMENTS_FILE_NAME) as requriment_file:
        requriment_list = requriment_file.readlines()
        requriment_list = [requriment_name.replace("\n", "") for requriment_name in requriment_list]

        if HYPHEN_E_DOT in requriment_list:
            requriment_list.remove(HYPHEN_E_DOT)

        return requriment_list
    
with open('README.md' ,'r' ,encoding='utf-8') as file:
    long_description = file.read()


LONG_DESCRIPTION = long_description


setup(name=PROJECT_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description= LONG_DESCRIPTION ,
      author=AUTHOR_NAME,
      author_email=AUTHOR_EMIL,
      packages=find_packages(),
      install_requries = get_requirements_list() ,
      url ='github_url'
     )