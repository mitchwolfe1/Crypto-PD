# Crypto Pump and Dump Predictor

## Setup
1) Install Python@3.8 and symlink it into your path and as python3 (or use an alias)
2) pip3 install pipenv
3) pipenv shell
4) pipenv install

## Structure
- Use the ingestion directory for ingesting data from online datasets
- Use the processing directory for processing the data and writing it to a format that can be used for training
- Use the model directory for doing all the iterative training and model weight adjustments, as well as writing the model structure (layering etc.)
- Use the visualization directory for dashboarding our progress and testing the model (initial thoughts are to use either Flask or Tensorboard)
- Use run.py as an orchestrator (to help call certain methods and pass variables for training/re-training the model)
- Use predictor.py to make predictions once the model is trained (this format will be figured out later)
