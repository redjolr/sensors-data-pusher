from api_handler import api_handler
import  hashlib
from logger import logger
class Dataset:
    def __init__(self, filepath):
        self.filepath = filepath
        self.sensors = []
        self.checksum = None
        self.file_length=None #This will be calculated by the calculate_checksum method, for performance reasons
        with open(filepath) as file:
            head_line = file.readline()
            self.sensors =[col.strip() for col in head_line.strip().split(",")]
            self.sensors.remove("time")



    def invalid_sensors(self):
        sensors_in_db = api_handler.sens_abbrs
        invalid_sensors = []
        for abbr in self.sensors:
            if abbr not in sensors_in_db:
                sensors_not_in_db.append(abbr)

        return invalid_sensors

    def report_invalid_sensors(self):
        print("*****************************************************************************************************************")
        print("Sensor name problem in file ", self.filepath)
        print("Sensors with these abbreviations don't exist in the database: ", self.invalid_sensors())
        print("*****************************************************************************************************************\n")

    def calculate_checksum(self):
        with open(self.filepath, 'rb') as file:
            file_content = file.read()
            checksum = hashlib.sha256(file_content).hexdigest()
            self.file_length = len(file_content)
        self.checksum = checksum
        logger.success("Checksum calculated for file {}!".format(self.filepath))
        return checksum
