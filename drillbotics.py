import pandas as pd
import requests, json, time
from api_handler import api_handler
from dataset import Dataset
from user import User
from models import Experiment
from tqdm import tqdm
from logger import logger

def main():
    user = User()
    datasets = []
    experiments = []
    invalid_sensors_error = False
    file_paths = user.choose_files()

    ###Dataset Creation
    for i, path in enumerate(file_paths):
        dataset = Dataset(path)

        if(len(dataset.invalid_sensors())==0):
            datasets.append(dataset)
            logger.info("All sensors OK in file {}".format(i))
        else:
            dataset.report_invalid_sensors()
            invalid_sensors_error = True
    if invalid_sensors_error:
        print("Please check if the column names of the CSV files are spelled correctly! If they are correct, please add the new sensors in the database!")
        return


    logger.print_chosen_files(file_paths)
    logger.print_available_rocks(api_handler.rocks)


    for i, dataset in enumerate(datasets):
        experiment = Experiment(dataset)
        experiment.rock_id = user.choose_rock(dataset.filepath)
        experiment.description = user.write_description()
        experiment.start_time = user.set_date()

        dataset.calculate_checksum()
        experiments.append(experiment)



    chunk_size = 500000
    while True:
        experiment_addded = False
        continue_with_upload = user.continue_with_upload()
        if continue_with_upload:
            try:
                for experiment in experiments:
                    logger.success("\n\nUploading file {}.".format(experiment.dataset.filepath))

                    nr_of_chunks = experiment.dataset.file_length // chunk_size if experiment.dataset.file_length % chunk_size == 0 else experiment.dataset.file_length // chunk_size+1
                    with open(experiment.dataset.filepath) as f:
                        for i in tqdm(range(nr_of_chunks)):
                            chunk_response = api_handler.send_file_chunk(experiment, f, chunk_size=chunk_size)
                            if chunk_response.text=='DATASET_ALREADY_IN_DB':
                                logger.error("\n\nThis dataset is already stored in database! Stopping upload!")
                                break
                    if chunk_response.text=='DATASET_ALREADY_IN_DB':
                        continue
                    metadata_response = api_handler.send_metadata(experiment)

                    if metadata_response.text=="METADATA_RECEIVED":
                        logger.success("File {} uploaded!".format(experiment.dataset.filepath))
                        add_experiment_response = api_handler.add_experiment(experiment)

                        if add_experiment_response.text=='EXPERIMENT_BEING_ADDED_TO_THE_DB':
                            logger.success("The uploaded dataset is being written in the database. It may take some time. You can check its progress in the web application!")
                        else:
                            print("An error occred while inserting the dataset in the database!")

            except Exception as exc:
                logger.error("ERROR:  "+str(exc))
            logger.input("Press Enter to continue!")

            break
        elif continue_with_upload==False:
            exit()





if __name__=='__main__':
    while True:
        main()
