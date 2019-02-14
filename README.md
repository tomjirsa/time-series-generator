# Time series generator

The generator of artificial time series for testing purposes. 


## Available features for generating time series

- **Base** - the base of the time series generated from normal distribution. Available parameters are :
  - ***base*** - the mean of the normal distribution
  - ***variance*** - the variance of the normal distribution
- **Trend** - linear trend component of the time series. Available parameters are:
  - ***slope*** - the slope of the trend
- **Season** - the sinusoid-like seasonal component of the time series. Available parameters are:
  - ***period*** - the length of a seasonal component
  - ***height*** - the amplitude of the seasonal component
- **Missing Values** - missing observations put into the time series. Available parameters are:
  - ***from*** - Start of the interval with the missing values
  - ***to*** - End of the interval with the missing values
- **Annomalies** - adds anomalies to the time series. Available parameters are:
  - ***position*** - the index of the observation with an anomaly
  - ***coef*** - the multiplier of the original observation to create an anomaly. 
- **Changepoint** - adds a change point (change of level) of the time series. Available parameters are:
  - ***from*** - Start of the interval with the changed level
  - ***to*** - End of the interval with the changed level
  - ***value*** - absolute value of the level change
  
## Requirements

* Python >= 3.6
* Python libraries 
  * numpy, pandas, matplotlib.pyplot

## Usage

1) Configure you time series to generate in `./config.json`
2) Run `python ./time-series-generator.py`
3) The time series data are saved to the folder as provided in `./config.json`. The default folder is `./timeseries/`. 