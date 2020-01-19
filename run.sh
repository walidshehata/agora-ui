#!/bin/bash

pyenv virtualenv agora-ui
pyenv local agora-ui
pip install --upgrade pip
pip install -r requirements.txt

export FLASK_APP=agora-ui.py
flask run -p 5000
