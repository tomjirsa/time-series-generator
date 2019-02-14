import os
import time
import json
import numpy as np
import pandas as pd

from generator.generator import TimeSeriesGenerator

start = time.time()

dirname = os.path.dirname(__file__)

# Load config
config_file = dirname + "/config.json"

with open(config_file) as file:
    configuration = json.load(file)

for time_serie_config in configuration["time_series"]:
    generator = TimeSeriesGenerator(time_serie_config["meta"])
    generator.generateTimeSeries(time_serie_config)
    generator.saveTimeSeries(time_serie_config)

