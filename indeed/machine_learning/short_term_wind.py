import warnings
from .dataset_generators import ShortTermDataGenerator
from .nn_acrhitectures import NNModels
import tensorflow as tf

warnings.filterwarnings("ignore")


class DNNWind(object):

    def __init__(self, path, train_split, val_split, out_steps, in_steps, epochs):
        self.train_split = train_split
        self.val_split = val_split

        self.OUT_STEPS = out_steps
        self.IN_STEPS = in_steps
        self.path = path
        self.MAX_EPOCHS = epochs

        self.window = ShortTermDataGenerator(input_width=self.IN_STEPS,
                                             label_width=self.OUT_STEPS,
                                             shift=self.OUT_STEPS,
                                             data_path=self.path,
                                             train_ratio=self.train_split,
                                             val_ratio=self.val_split,
                                             label_columns=None)

        self.num_features = list(self.window.train.as_numpy_iterator())[0][0].shape[-1]

        self.model = NNModels.multi_linear_model(out_steps=self.OUT_STEPS,
                                                 num_features=self.num_features)

    def compile_and_fit(self, patience=2):
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                          patience=patience,
                                                          mode='min')

        self.model.compile(loss=tf.keras.losses.MeanSquaredError(),
                           optimizer=tf.keras.optimizers.Adam(),
                           metrics=[tf.keras.metrics.MeanAbsoluteError()])

        history = self.model.fit(self.window.train, epochs=self.MAX_EPOCHS,
                                 validation_data=self.window.val,
                                 callbacks=[early_stopping])

