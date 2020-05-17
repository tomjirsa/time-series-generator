# Time series generator

The generator of artificial time series for testing purposes. 

## Available features for generating time series

- **Base**: base value of the time series generated from a normal distribution. Available parameters are :
  - `base`: the mean of the normal distribution.
  - `variance`: the variance of the normal distribution.
- **Trend** - linear trend component of the time series. Available parameters are:
  - `slope`: the slope of the trend.
- **Season**: the sinusoid-like seasonal component of the time series. Available parameters are:
  - `period`: the length of a seasonal component.
  - `height`: the amplitude of the seasonal component.
- **Missing Values** - missing observations put into the time series. Available parameters are:
  - `from`: start of the interval with the missing values.
  - `to`: end of the interval with the missing values.
- **Annomalies**: adds anomalies to the time series. Available parameters are:
  - `position`: the index of the observation with an anomaly.
  - `coef`: the multiplier of the original observation to create an anomaly. 
- **Changepoint**: adds a change point (change of level) of the time series. Available parameters are:
  - `from`: start of the interval with the changed level.
  - `to`: end of the interval with the changed level.
  - `value`: absolute value of the level change.

## Installation

For the moment the library is so simple it is enough to get the libraries, no versions fixed. 

Raw usage:
```bash
pip install -r requirements.txt
```

Plotting and else:
```bash
pip install -r requirements-front.txt
```

Adding new features:
```bash
pip install -r requirements-dev.txt
```

All of them:
```bash
pip install -r requirements.txt requirements-dev.txt requirements-front.txt
```

## Usage

See examples in the `examples` folder. 