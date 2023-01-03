from django.shortcuts import render
import os
from django.http import HttpResponse , JsonResponse
from django.conf import settings
from django.views.generic import TemplateView
from configparser import ConfigParser
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import json
from prophet.serialize import model_from_json

class Forecast(TemplateView):

    def get(self, request, *args, **kwargs):
        type = self.kwargs['type']
        location = self.kwargs['location']
        horizon = self.kwargs['horizon']


        if type == 'wind':

            #with open(str(settings.BASE_DIR) + '/saved_models/wind_prophet.json', 'r') as fin:
                #m2 = model_from_json(json.load(fin))

            future_df = pd.read_csv(str(settings.BASE_DIR) + '/saved_forecasts/wind_forecast.csv',
                                    index_col='timestamp')

            future_df.index = pd.to_datetime(future_df.index)
            unique_dates = [str(x) for x in list(future_df.index.map(pd.Timestamp.date).unique())]

            if horizon in unique_dates:
                future_df['date'] = [str(x) for x in list(future_df.index.map(pd.Timestamp.date))]
                future_df = future_df.loc[future_df['date'] == horizon]
                future_df.drop('date', inplace=True, axis=1)
                ret = future_df.to_json(orient='index', date_format='epoch')

            else:
                val = future_df[-97:].values
                dti = pd.date_range(horizon, periods=97, freq="15T")
                new_df = pd.DataFrame(val, index=dti, columns=future_df.columns)
                ret = new_df.to_json(orient='index', date_format='epoch')

            return JsonResponse({'forecast': [ret],
                                 'location': location})

        if type == 'solar':
            #with open(str(settings.BASE_DIR) + '/saved_models/solar_prophet.json', 'r') as fin:
                #m2 = model_from_json(json.load(fin))

            future_df = pd.read_csv(str(settings.BASE_DIR) + '/saved_forecasts/solar_forecast.csv',
                                    index_col='timestamp')
            future_df.index = pd.to_datetime(future_df.index)
            unique_dates = [str(x) for x in list(future_df.index.map(pd.Timestamp.date).unique())]

            if horizon in unique_dates:
                future_df['date'] = [str(x) for x in list(future_df.index.map(pd.Timestamp.date))]
                future_df = future_df.loc[future_df['date'] == horizon ]
                future_df.drop('date',inplace=True,axis=1)
                ret = future_df.to_json(orient='index', date_format='epoch')

            else:
                val = future_df[-97:].values
                dti = pd.date_range(horizon, periods=97, freq="15T")
                new_df = pd.DataFrame(val,index=dti,columns=future_df.columns)
                ret = new_df.to_json(orient='index', date_format='epoch')

            return JsonResponse({'forecast': [ret],
                                 'location': location })









