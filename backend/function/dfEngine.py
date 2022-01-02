#!/usr/bin/env python3
import pandas as pd

o = pd.read_csv('../magnet2.csv', index_col=0)

dataset = o.loc[["x"], ["time", "magnet"]]
magnet = dataset["magnet"]

start_time=int(dataset["time"][1])
end_time=int(dataset["time"][-1])

getSetBySecond = lambda second: dataset[(dataset["time"] > second) & (dataset["time"] < second + 1)]
secondLength = end_time - start_time