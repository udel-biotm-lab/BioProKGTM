# Knowledge Graph UI

This repository contains code to build a Knowledge Graph User Interface which talks to the KG on neo4j database.

## Download the code

git clone https://github.com/udel-biotm-lab/Waters-Project.git

## Create a python virtual environment (python version 3.12.3)
'path to your python executable' -m venv waters_env

source waters_env/bin/activate

## Install the dependencies
pip install -r requirements.txt

## Update database configuration
cd KG_UI

Update the .env file with your neo4j database properties

## Run the interface
Run the following command

streamlit run interface.py

(or) to host it on a specific port, replace '#port' in the below command with the specific port number

streamlit run interface.py --server.port #port
