import os
from pathlib import Path

package_name = "MLOps_project1"

list_of_files = [
   ".github/workflows/ci.yaml",
   "src/__init__.py",
   f"src/{package_name}/__init__.py" ,
    f"src/{package_name}/components/__init__.py",
    f"src/{package_name}/config/__init__.py",
    f"src/{package_name}/logger/__init__.py",
    f"src/{package_name}/exception/__init__.py",
    f"src/{package_name}/pipeline/__init__.py",
    f"src/{package_name}/entity/__init__.py"
   "tests/__init__.py",
   "tests/unit/__init__.py",
   "tests/unit/unit.py",
   "tests/integration/__init__.py",
   "tests/integration/int.py",
   "init_setup.sh",
   "requirements.txt", 
   "requirements_dev.txt",
   "setup.py",
   "setup.cfg",
   "pyproject.toml",
   "tox.ini",
   "experiments/experiments.ipynb", 
   ".gitignore" ,
   "README.md"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass # create an empty file