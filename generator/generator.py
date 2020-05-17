import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import json


class TimeSeriesGenerator:

    def __init__(self,configuration):
        """
        Creates initial time serie data frame
        """
        self.number_of_observations = configuration["number_of_observations"]

    def add_base(self,configuration):
        """
        Adds base line time series generated from the random distribution
        :param configuration: configuration of base_line, required keys are base, variance
        :return:
        """

        base = configuration["base"]
        variance = configuration["variance"]
        self.time_series["base"] = self.time_series["cnt"].apply(lambda obs: obs + np.random.normal(base, variance, 1)[0])
        self.time_series["cnt"] = self.time_series["cnt"] + self.time_series["base"]
        self.time_series.drop("base", inplace=True, axis=1)

    def add_trend(self,configuration):
        """
        Adds linear trend to time series
        :param configuration: configuration of the trend, required key is "slope"
        :return:
        """
        slope = configuration["slope"]
        # Create trend
        self.time_series["index"] = self.time_series.index
        self.time_series["trend"] = self.time_series["index"].apply(lambda observation: slope*observation)
        # Add trend to time serie
        self.time_series["cnt"] = self.time_series["cnt"] + self.time_series["trend"]

        # Drop dummy columns
        self.time_series.drop("trend", inplace=True, axis=1)
        self.time_series.drop("index", inplace=True, axis=1)


    def add_season(self,configuration):
        """
        Adds sinusoid season to a time series.
        :param configuration: configuration of the season required keys are period and height
        :return:
        """
        period = configuration["period"]
        height = configuration["height"]

        # Create season
        self.time_series["index"] = self.time_series.index
        self.time_series["season"] = self.time_series["index"].apply(lambda obs: height * math.sin(obs * 2 * math.pi / period))

        # Add trend to time serie
        self.time_series["cnt"] = self.time_series["cnt"] + self.time_series["season"]

        # Drop dummy columns
        self.time_series.drop("season", inplace=True, axis=1)
        self.time_series.drop("index", inplace=True, axis=1)

    def add_nan_values(self,configuration):
        """
        Add NA values in the defined interval to a time serie
        :param configuration: configuration of na_values, required keys are ranges. Ranges is an array of dict with "from" and "to" keywords
        :return:
        """
        ranges = configuration["ranges"]
        for range in ranges:
            start = range["from"]
            end = range["to"]
            self.time_series["cnt"].iloc[start:end+1] = np.nan

    def add_outliers(self,configuration):
        """
        Adds anomalies on the specifed location to a time serie
        :param configuration: configuration of annomalies - an array of dicts {"position": <observation number of the anomaly>, "coef": <multiplyer of the original value at the position>}
        :return:
        """
        anomalies = configuration
        for anomaly in anomalies:
            position = anomaly["position"]
            coeficient = anomaly["coef"]
            self.time_series["cnt"].iloc[position] = self.time_series["cnt"].iloc[position] * coeficient

    def add_jumps(self, configuration):
        """
        Adds sudden change to time serie (all values in the range are increased by the given number)
        :param configuration: an array of dicts {"from": <start of the change>, "to": <end of the change>, "value": <value to increase the observations (for decrease use negative value>}
        :return:
        """
        breaks = configuration
        for record in breaks:
            start = record["from"]
            end = record["to"]
            value = record["value"]
            self.time_series["cnt"].iloc[start:end+1]= self.time_series["cnt"]+ value

    def add_timestamp(self, configuration):
        start = configuration["start"]
        step = configuration["step"]
        # Create season
        self.time_series["index"] = self.time_series.index
        self.time_series["timestamp"] = self.time_series["index"].apply(
            lambda obs: start + obs*step )

        self.time_series.set_index("timestamp", inplace=True)


        # Drop dummy columns
        self.time_series.drop("index", inplace=True, axis=1)
        # print(self.time_series.head())


    def plot(self):
        """
        Plot time series using linechart
        :return:
        """
        self.time_series.plot()
        plt.show()

    def to_pdf(self, file_name):
        """
        Save the plot to a pdf file.
        :param file_name: name of the file saved
        :return:
        """
        fig = self.time_series.plot().get_figure()
        fig.savefig(file_name)
        plt.close("all")
        print("Time series plot " + file_name + " saved.")

    def save_meta(self, file_name, configuration):
        """
        Stores configuration of the generator of the time series
        :param file_name: name of the file
        :param configuration: configuration of the time series generatior
        :return:
        """
        file = open(file_name, "w")
        for key,values in configuration.items():
            record = key + " " +  str(values) + "\n"
            file.write(record)
        file.close()
        print("Time series meta " + file_name + " saved.")

    def to_csv(self, file_name):
        """
        Save generated time series to a file. Index of the dataframe is not saved.
        :param file_name: name of the file
        :return:
        """
        self.time_series.to_csv(file_name, sep=',', index=True)
        print(("Time series " + file_name + " saved."))

    def save(self,configuration):
        """
        Saves all the information about time series. The saved information are time series in csv, meta information, and plot of the time series
        :param configuration: the entire configuration of the time series generator
        :return:
        """
        meta = configuration["meta"]
        self.to_pdf(file_name=meta["path"] + meta["time_series_name"] + "-plot.pdf")
        self.save_meta(file_name=meta["path"] + meta["time_series_name"] + "-meta.txt", configuration=configuration)
        self.to_csv(file_name=meta["path"] + meta["time_series_name"] + ".csv")

    def generate(self, configuration):
        """
        Generates the time series according to the configuration.

        :param configuration: dict - configuration of the time series
        :return:
        """
        # Restart time series
        self.time_series = pd.DataFrame({"cnt": np.zeros(self.number_of_observations)})

        for key in configuration:
            if key == "base_line":
                self.add_base(configuration=configuration[key])
            elif key == "trend":
                self.add_trend(configuration=configuration[key])
            elif key == "season":
                self.add_season(configuration=configuration[key])
            elif key == "na_values":
                self.add_nan_values(configuration=configuration[key])
            elif key == "annomalies":
                self.add_outliers(configuration=configuration[key])
            elif key == "breaks":
                self.add_jumps(configuration=configuration[key])
            elif key == "meta":
                pass
                # print("Processing time serie " + configuration[key]["time_series_name"])
            elif key == "timestamps":
                self.add_timestamp(configuration=configuration[key])
            else:
                raise ValueError('A key ' + key + " is not defined!")

        #self.plotTimeSeries()

    def get(self):
        """
        To return the time series
        :return: time series in pd.DataFrame
        """
        return self.time_series

    def get_business_like(self):

        _ts = self.time_series.copy()

        periods = len(_ts.values.flatten())

        calendar = pd.date_range(start = "20000101", freq = "B", periods=periods)

        time_series = pd.Series(data = _ts.values.flatten(), index = calendar)

        return time_series


