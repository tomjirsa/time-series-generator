import sys
from pathlib import Path

path = Path("../generator")

sys.path.insert(0, path.as_posix())

pwd = path.parent

import json

from generator.generator import TimeSeriesGenerator


dirname = Path(__file__)
dirname = dirname.parent

# Load config
config_file = dirname / "config.json"

with open(config_file) as file:
    configuration = json.load(file)

# Generate time series
for time_serie_config in configuration["time_series"]:
    generator = TimeSeriesGenerator(time_serie_config["meta"])
    generator.generate(time_serie_config)
    generator.save(time_serie_config)

