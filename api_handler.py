import requests, json
from models import *
class APIHandler:

    def __init__(self, host):
        self.host = host
        self.rocks_and_sensors = json.loads(requests.get(host+"/api/getrocksandsensors/").text)
        self.rocks = self.get_rocks()
        self.sensors = self.get_sensors()
        self.sens_abbrs = [sensor.abbreviation for sensor in self.sensors]
        self.sensor_ids = {sensor.abbreviation:sensor.id for  sensor in self.sensors }


    def get_rocks(self):
        rocks = []
        for rock in self.rocks_and_sensors['rocks']:
            rocks.append(Rock(rock["id"], rock["name"]))
        return rocks

    def get_sensors(self):
        sensors = []
        for sensor in self.rocks_and_sensors['sensors']:
            sensors.append(Sensor(sensor["id"], sensor["abbreviation"]))
        return sensors

    def send_file_chunk(self, experiment, file_handler, chunk_size=100000):
        url = self.host+"/api/upload_chunk/{}/".format(experiment.dataset.checksum)
        file_chunk = file_handler.read(chunk_size)
        response = requests.post(url, data={'chunk':file_chunk})

        return response


    def send_metadata(self, experiment):
        url = self.host+"/api/upload_chunk/{}/".format(experiment.dataset.checksum)
        metadata = {"rock_id": experiment.rock_id,
                    "description": experiment.description,
                    "start_time": experiment.start_time,
                    "checksum": experiment.dataset.checksum}

        response = requests.post(url, data={'metadata':json.dumps(metadata)})
        return response

    def add_experiment(self, experiment):
        url = host+"/api/addexperiment/{}/".format(experiment.dataset.checksum)
        response = requests.post(url)
        return response

# host = "http://localhost:8000"
host = "http://188.166.60.216"
api_handler = APIHandler(host)
