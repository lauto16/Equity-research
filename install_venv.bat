@echo off
python -m venv venv

call venv\Scripts\activate

pip install -r requirements.txt

pip install --upgrade setuptools

echo Packages installed successfully

exit
