@echo off
pip install virtualenv

virtualenv venv

call venv\Scripts\activate

pip install -r requirements.txt

pip install --upgrade setuptools

echo Packages installed successfully

exit
