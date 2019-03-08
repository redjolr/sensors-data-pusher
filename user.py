import tkinter as tk
from tkinter import filedialog
from tkcalendar import Calendar, DateEntry
from api_handler import api_handler
import datetime
from logger import logger

class User:
    def choose_files(self):
        print("*********Hey there*********")
        print("The next step is to choose the CSV files you wish to upload to the database. \nCareful! The datasets that you choose, are not checked by the system. This means that it is your responsibility to check that you are not uploading an existing dataset.")
        rsp = input("Press ENTER continue!\n")
        root = tk.Tk()
        root.withdraw()
        file_strings = filedialog.askopenfilenames()
        file_paths = [r'{}'.format(file_str) for file_str in file_strings ]
        return file_paths


    def choose_rock(self, path):
        rocks = api_handler.rocks
        while True:
            rock_input = logger.input("\n\nPlease choose the rock for file {}: ".format(path))
            try:
                chosen_rock = int(rock_input)
                assert chosen_rock>=1 and chosen_rock<=len(rocks)
            except Exception:
                logger.error("The value should be from {} to {}!".format(1,len(rocks)))
                continue
            break
        return chosen_rock

    def write_description(self):
        return logger.input("Please write a description of the experiment that generated this file:   ")

    def set_date(self):
        while True:
            inputDate = logger.input("Please write the date of the experiment (dd/mm/yyyy):   ")
            date_arr = inputDate.split('/')
            if len(date_arr) !=3:
                logger.error("Date format invalid")
                continue
            day,month,year = date_arr[0], date_arr[1], date_arr[2]
            valid_date = True
            try :
                datetime.datetime(int(year),int(month),int(day))
            except ValueError :
                valid_date = False
            if valid_date :
                break
            else:
                logger.error("Input date is not valid!")
        return '{}-{}-{} 00:00:00'.format(year, month, day)

    def continue_with_upload(self):
        resp = logger.input("\n\nContinue with upload? (y/n): ")
        if resp=='y' or resp=='Y' or resp=='yes' or resp=='YES' :
            logger.info("The file is being read! This may take a while, depending on file size.")
            cont = True
        elif resp=='n' or resp=='N' or resp=='no' or resp=='NO' :
            logger.error("Upload cancelled!")
            cont = False
        else:
            logger.error("Invalid response!")
            cont = None
        return cont
