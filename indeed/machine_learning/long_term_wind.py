import pandas as pd
from prophet import Prophet
from django.conf import settings
import warnings
import json
from prophet.serialize import model_to_json
from .dataset_generators import LongTermDataGenerator

warnings.filterwarnings("ignore")


class ProphetWind(LongTermDataGenerator):

    def __init__(self, *args, **kwargs):
        super(ProphetWind, self).__init__(*args, **kwargs)
        self.input_file = self.create_input_dataframe()

    def create_model(self,interval_width=0.95, is_daily_seasonality=True, is_yearly_seasonality=True, holiday_df=None):
        model = Prophet(interval_width=interval_width, daily_seasonality=is_daily_seasonality,
                        yearly_seasonality=is_yearly_seasonality, holidays=holiday_df)
        # model.add_regressor('wind_output_50')
        model.fit(self.input_file)

        # save the model
        with open(str(settings.BASE_DIR) + '/saved_models/wind_prophet.json', 'w') as fout:
            json.dump(model_to_json(model), fout)

        future = model.make_future_dataframe(periods=365)
        forecast = model.predict(future)
        forcast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']][-300:]
        forcast_data = forcast_data.rename(
            columns={'ds': 'timestamp', 'yhat': 'prediction', 'yhat_lower': 'prediction_lower',
                     'yhat_upper': 'prediction_upper'})
        forcast_data['timestamp'] = pd.to_datetime(forcast_data['timestamp'])
        forcast_data = forcast_data.set_index('timestamp')
        forcast_data.to_csv(str(settings.BASE_DIR) + '/saved_forecasts/wind_forecast.csv')
