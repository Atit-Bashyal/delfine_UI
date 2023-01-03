from ..machine_learning.long_term_wind import ProphetWind
from ..machine_learning.long_term_solar import ProphetSolar
from ..machine_learning.short_term_solar import DNNSolar
from ..machine_learning.short_term_wind import DNNWind
from django.conf import settings

solar_path = str(settings.BASE_DIR) + '/data/Mehring.csv'

wind_path = str(settings.BASE_DIR) + '/data/merkel1.csv'

train_split = 0.7

val_split = 0.9

out_steps = 12

in_steps = 36

epochs = 20


# we need to use multiprocessing to run models in parallel (Advanced project)


class Trainer:

    @staticmethod
    def wind_train():
        print('starting wind')
        train_model = DNNWind(wind_path,
                              train_split,
                              val_split,
                              out_steps,
                              in_steps,
                              epochs)

        train_model.compile_and_fit()

    @staticmethod
    def solar_train():
        print('starting solar')
        train_model = DNNSolar(solar_path,
                               train_split,
                               val_split,
                               out_steps,
                               in_steps,
                               epochs)

        train_model.compile_and_fit()
