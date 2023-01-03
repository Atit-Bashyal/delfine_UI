from os import path
import pandas as pd
from pandas import read_csv, read_excel
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np


class LongTermDataGenerator(object):
    def __init__(self, data_path):
        self.file_path = data_path

    def create_daily_dataframe(self):
        df = self.read_data()
        df = df[['datetime', 'power']].dropna()
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        df = df.sort_index()
        daily_df = df.resample('D').sum()
        return daily_df.reset_index().dropna()

    def create_input_dataframe(self):
        df_init = self.create_daily_dataframe()
        input_df = pd.DataFrame()
        input_df['ds'] = df_init['datetime']
        input_df['y'] = df_init['power']
        return input_df

    def read_data(self):
        filename, extension = path.splitext(self.file_path)
        if extension[1:] in ['xlsx', 'xls']:
            file = pd.read_excel(self.file_path)
        elif extension[1:] == 'csv':
            file = pd.read_csv(self.file_path)
        return file


class ShortTermDataGenerator(object):
    def __init__(self, input_width, label_width, shift,
                 data_path, train_ratio, val_ratio=None, label_columns=None):

        # resample raw data
        self.file_path = data_path

        # Store the raw data.

        self.raw = self.read_data

        self.dataframe = self.create_hourly_dataframe()

        # training and validation split

        self.train_split = train_ratio
        self.val_split = val_ratio

        if self.val_split is not None:
            self.train_df, self.val_df, self.test_df = self.df_split()
        else:
            self.train_df, self.test_df = self.df_split()
            self.val_df = pd.DataFrame()

        # Work out the label column indices.
        self.label_columns = label_columns
        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in
                                          enumerate(label_columns)}
        self.column_indices = {name: i for i, name in
                               enumerate(self.dataframe.columns)}

        # Work out the window parameters.
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift
        self.total_window_size = input_width + shift
        self.label_start = self.total_window_size - self.label_width

        # create slice object to find input indices
        self.input_slice = slice(0, input_width)
        # create list of  input indices
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]

        # create slice object to find label indices
        self.labels_slice = slice(self.label_start, None)
        # create list of  label indices
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

    def split_window(self, features):

        """ takes object from tf.data.Dataset instance, and splits
            the sequential data inside object into inputs and labels, according to
            logic for the input and label indices in __init__

            also handles the label_columns so it can be used for both the
            single output and multi-output examples"""

        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]

        if self.label_columns is not None:
            labels = tf.stack(
                [labels[:, :, self.column_indices[name]] for name in self.label_columns],
                axis=-1)

        # Slicing doesn't preserve static shape information, so set the shapes
        # manually. This way the `tf.data.Datasets` are easier to inspect.

        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])

        return inputs, labels

    def make_dataset(self, data):

        """takes pd dataframe with sequential data and returns tf dataset instance
        where each object is a tuple (input,labels)"""

        # convert pd dataframe to np array
        data = np.array(data, dtype=np.float32)

        # convert numpy array of data into tf.data.Dataset instance
        ds = tf.keras.utils.timeseries_dataset_from_array(
            data=data,
            targets=None,
            sequence_length=self.total_window_size,
            sequence_stride=1,
            shuffle=True,
            batch_size=32, )

        # tf.data.Dataset instance :
        # If targets was passed the dataset yields
        # tuple (batch_of_sequences, batch_of_targets).
        # If not, the dataset yields only batch_of_sequences.
        # the ds instance created here contains data.shape/batch_size objects,
        # each object has shape (total_window_size, num_features)"""

        # apply split_window function to each object of ds

        ds = ds.map(self.split_window)

        # applying the function returns a tf  dataset instance with tuple (input,labels)
        # inputs have shape (batch_size,input_width,features)
        # labels have shape (batch_size,label_width,features)

        return ds

    def create_hourly_dataframe(self):
        df = self.raw
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        df = df.sort_index()
        hourly_df = df.resample('H').sum()
        return hourly_df

    def plot(self, model=None, plot_col='power', max_subplots=3):
        inputs, labels = self.example
        plt.figure(figsize=(12, 8))
        plot_col_index = self.column_indices[plot_col]
        max_n = min(max_subplots, len(inputs))
        for n in range(max_n):
            plt.subplot(max_n, 1, n + 1)
            plt.ylabel(f'{plot_col} [normed]')
            plt.plot(self.input_indices, inputs[n, :, plot_col_index],
                     label='Inputs', marker='.', zorder=-10)

            if self.label_columns:
                label_col_index = self.label_columns_indices.get(plot_col, None)
            else:
                label_col_index = plot_col_index

            if label_col_index is None:
                continue

            plt.plot(self.label_indices, labels[n, :, label_col_index],
                     label='Labels', c='#2ca02c', marker='.', zorder=-10)
            if model is not None:
                predictions = model(inputs)
                plt.plot(self.label_indices, predictions[n, :, label_col_index],
                         label='Predictions',
                         c='#ff7f0e', marker='.', zorder=-10)

            if n == 0:
                plt.legend()

        plt.xlabel('Time [h]')

    def df_split(self):

        if self.val_split is not None:
            n = len(self.dataframe)
            train_df = self.dataframe[0:int(n * self.train_split)]
            val_df = self.dataframe[int(n * self.train_split):int(n * self.val_split)]
            test_df = self.dataframe[int(n * self.val_split):]

            train_mean = train_df.mean()
            train_std = train_df.std()

            train_df = (train_df - train_mean) / train_std
            val_df = (val_df - train_mean) / train_std
            test_df = (test_df - train_mean) / train_std

            return train_df, val_df, test_df

        else:
            n = len(self.dataframe)
            train_df = self.dataframe[0:int(n * self.train_split)]
            test_df = self.dataframe[int(n * self.train_split):]

            train_mean = train_df.mean()
            train_std = train_df.std()

            train_df = (train_df - train_mean) / train_std
            test_df = (test_df - train_mean) / train_std

            return train_df, test_df

    @property
    def read_data(self):
        filename, extension = path.splitext(self.file_path)
        if extension[1:] in ['xlsx', 'xls']:
            file = pd.read_excel(self.file_path)
        elif extension[1:] == 'csv':
            file = pd.read_csv(self.file_path)
        return file

    @property
    def train(self):
        return self.make_dataset(self.train_df)

    @property
    def val(self):
        return self.make_dataset(self.val_df)

    @property
    def test(self):
        return self.make_dataset(self.test_df)

    @property
    def example(self):
        """Get and cache an example batch of `inputs, labels` for plotting."""
        result = getattr(self, '_example', None)
        if result is None:
            # No example batch was found, so get one from the `.train` dataset
            result = next(iter(self.train))
            # And cache it for next time
            self._example = result
        return result

    def __repr__(self):
        return '\n'.join([
            f'Total window size: {self.total_window_size}',
            f'Input indices: {self.input_indices}',
            f'Label indices: {self.label_indices}',
            f'Label column name(s): {self.label_columns}'])
