import pandas as pd
from joblib import load
import numpy as np  # for mathematical calculation
import seaborn as sns  # for data visualiztion
import pickle
from sklearn.preprocessing import LabelEncoder
import sklearn


def preprocess(processed_data):

   

    return processed_data


def prediction(processed_data):
    # load the model

    with open('./savedModels/model.pkl', 'rb') as file:
        model = pickle.load(file)

   
    ypred = model.predict(processed_data)

    
    return ypred
