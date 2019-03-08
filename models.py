import pandas as pd


class Rock:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Sensor:
    def __init__(self, id, abbreviation):
        self.id = id
        self.abbreviation = abbreviation



class Experiment:
    def __init__(self, dataset):
        self.dataset = dataset
        self.rock_id = None
        self.description = None
        self.start_time = None
        self.frequency=None

    # def calculate_frequency(self):
    #     nrows = 10000
    #     df = pd.read_csv(self.dataset.filepath, nrows=nrows, usecols=["time"])


    # def read_chunk()
