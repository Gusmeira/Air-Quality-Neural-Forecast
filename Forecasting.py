import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px

import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA

from arch.unitroot import ADF, KPSS, PhillipsPerron









class Forecast:
    def __init__(self, series:pd.Series,
                 train_test_split:int,
                 horizon:int, seasonal_period:int,
                 plot:bool=False) -> None:

        self.series = series
        self.train_test_split = train_test_split
        self.horizon = horizon-1
        self.seasonal_period = seasonal_period
        self.plot = plot

        if (self.train_test_split < self.horizon) and (self.train_test_split != 0):
            raise ValueError('train_test_split must be at least equal to horizon!')

        if self.train_test_split > 0:
            self.train = self.series.iloc[:-train_test_split].rename('Train')
            self.test = self.series.iloc[-train_test_split:].rename('Test')
            self.ligant = pd.concat([self.train[-1:], self.test[0:1]])
        else:
            self.train = self.series.rename('Train')
            self.test = self.series.iloc[-1:].rename('Test')

        self.stationarity = self.stationarity_type()

# ==============================================================================

    def plot_time_series(self):
        '''Internal Function.\n
        Plot the main time series with it's train and test properties'''
        self.fig, self.ax = plt.subplots(figsize=(7, 3.5))
        self.train.plot(ax=self.ax, legend=True, lw=3, color='k')
        if self.train_test_split > 0:
            self.test.plot(ax=self.ax, legend=False, lw=3, color='k')
            self.ax.axvline(x=self.train.index[-1], color='grey', linestyle='--', lw=1)
            self.ligant.plot(ax=self.ax, legend=False, lw=1.5, color='k', linestyle='--')
            self.ax.grid(True)

# ==============================================================================

    def stationarity_type(self, printing:bool=False, diff:int=0) -> None:
        '''Internal and External Function.\n
        It is used to determinate if train series is stationary or not.
        The parameter `printing` allows you to visualize results if set to True.
        Statistical methos used are:
        - ADF (Augmented Duck-Fuller)
        - KPSS (Kwiatkowski-Phillips-Schmidt-Shin)
        - PP (Pjillips-Perron)'''

        if diff > 0:
            self.train = self.train.diff(diff).dropna()

        try:
            method_stationary = ''
            method_non_stationary = ''
            stationarity_points = 0

            # Used for major
            result_adf = ADF(self.train)
            result_adf = result_adf.pvalue
            # Used for trends
            result_kpss = KPSS(self.train)
            result_kpss = result_kpss.pvalue
            # Used for autocerrelation
            result_pp = PhillipsPerron(self.train)
            result_pp = result_pp.pvalue

            if result_adf < 0.05:
                stationarity_points += 1
                method_stationary += 'ADF '
            else:
                method_non_stationary += 'ADF '

            if result_kpss > 0.05:
                stationarity_points += 1
                method_stationary += 'KPSS '
            else:
                method_non_stationary += 'KPSS '

            if result_pp < 0.05:
                stationarity_points += 1
                method_stationary += 'PP '
            else:
                method_non_stationary += 'PP '

            if stationarity_points >= 2:
                self.stationarity = 'stationary'
                self.stationarity_method = method_stationary.strip()
            else:
                self.stationarity = 'non-stationary'
                self.stationarity_method = method_non_stationary.strip()

            # Printing == True
            if printing:
                print(f'===== Stacionarity Test in {diff} diff =====')
                print('ADF p-value:', np.round(result_adf,4))
                print('KPSS p-value:', np.round(result_kpss,4))
                print('PP p-value:', np.round(result_pp,4))
                print(f'Result: {self.stationarity} ({self.stationarity_method})')

        except:
            self.stationarity = 'stationary'
            self.stationarity_method = 'inconclusive'

        return self.stationarity

# ==============================================================================

    def model_errors(self, prediction:pd.Series):
        '''Internal Function.\n
        It allows all train_test() methods to calculate errors.
        - Absolute errors:
            - Difference
            - MAE
            - RMSE
        - Percentage errors:
            - MAPE'''
        error = np.round(self.test[self.horizon]-prediction[-1],2)
        mae = np.round(np.abs(self.test[self.horizon]-prediction[-1]),2)
        rmse = np.round(np.sqrt((self.test[self.horizon]-prediction[-1])**2),2)
        mape = np.round(100*np.abs(self.test[self.horizon]-prediction[-1])/self.test[self.horizon],2)

        errors = {'error': error,
                  'mae': mae,
                  'rmse': rmse,
                  'mape': mape}

        return errors

# ==============================================================================

    def time_indexes(self, values:list, create_df:bool = True):
        '''Internal Function.\n
        It allows some methods to access the dates that will be predicted.'''
        self.time_index = pd.date_range(start=self.train.index[-1].to_timestamp(), periods=self.horizon+2, freq='MS')[1:]

        if create_df == True:
            df = pd.Series(values, index=self.time_index)
            return df

        return self.time_index

# ==============================================================================

    def acf_pacf(self):
        '''External Function.\n
        Plot Auto Correlation Function and Partial Auto Correlation Function'''
        fig, ax = plt.subplots(1,2, figsize=(10,3))
        sm.graphics.tsa.plot_acf(self.train, lags=self.seasonal_period, ax=ax[0])
        sm.graphics.tsa.plot_pacf(self.train, lags=self.seasonal_period, ax=ax[1])
        plt.show()

# ==============================================================================

    def plot_seasonal_decompose(self):
        '''External Function.\n
        Plot Seasonal Decomposition'''
        decomposition = seasonal_decompose(self.train, model='additive', period=self.seasonal_period)

        plt.subplots(4,1,figsize=(8.5,7))
        plt.subplot(4,1,1)
        decomposition.observed.dropna().plot(title='Observed');
        plt.subplot(4,1,2)
        decomposition.trend.dropna().plot(title='Trend');
        plt.subplot(4,1,3)
        decomposition.seasonal.dropna().plot(title='Seasonal');
        plt.subplot(4,1,4)
        decomposition.resid.dropna().plot(title='Residual');
        plt.tight_layout()