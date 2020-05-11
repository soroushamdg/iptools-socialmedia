"""
Garson means the script which organizes raw data into readable tables and structure.

Software diagram:
Raw Data on website -> Receiving by Prosumer -> Organizing by Garson -> Cooking into Valuable Data by Chef
"""

import datetime
from social_media.aparat_ir import prosumer
from social_media.aparat_ir.options import script_name as sn,raw_data_file_name,publish_log_file_name
import csv
import os
import pathlib
from options import data_path
import logger_factory
import logging
logging.getLogger(__name__)
#tk imports
import tkinter as tk
from tkinter import filedialog

def init_csv_file(mode='data'):
    """
    This fucntion will create new csv file
    :param mode: mode : 'data','publish_log'
    :return: Boolean
    """
    if mode == 'data':
        try:
            csv_file = open(raw_data_file_name,'r')
        except:
            logging.debug(f"no {raw_data_file_name} file found! We will create new one.")
            try:
                file = open(raw_data_file_name,'a+')
                header_writer = csv.writer(file)
                header_writer.writerow(["file creation date : " + str(datetime.datetime.now().strftime('%d %B %Y %H:%M:%S'))," "," "," "," "])
                header_writer.writerow(["date",
                                        "videos",
                                        "subscribers",
                                        "today views",
                                        "total views",
                                        "total minute views",
                                        "channel name",
                                        "profile cover"])
                file.close()
                return True
            except Exception as msg:
                logging.debug("can't create new csv file. please check administrator access or problems ->" + str(msg))

                return False
        else:
            csv_file.close()
            logging.debug(f"{raw_data_file_name} file found successfully.")
            return True
    if mode == 'publish_log':
        try:
            csv_file = open(publish_log_file_name, 'r')
        except:
            logging.debug(f"no {publish_log_file_name} file found! We will create new one.")
            try:
                file = open(publish_log_file_name, 'a+')
                header_writer = csv.writer(file)
                header_writer.writerow(
                    ["file creation date : " + str(datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')), " ", " ",
                     " ", " "])
                header_writer.writerow(["date",
                                        "title",
                                        "category",
                                        "description",
                                        "filepath",
                                        "size"])
                file.close()
                return True
            except Exception as msg:
                logging.debug("can't create new csv file. please check administrator access or problems ->" + str(
                            msg))

                return False
        else:
            csv_file.close()
            logging.debug(f"{publish_log_file_name} file found successfully.")
            return True

def get_todays_data(channel_id,username,password,save = True,replace_by_old_todays_data = False,custom_timezone = None,get_list = ["get_subscribers","get_count_videos","get_today_views","get_total_views","get_total_minute_views"]):
    #Chaning path to aparat data
    while(True):
        try:
            os.chdir(str(pathlib.Path(data_path).joinpath('aparat_data')))
        except:
            logging.debug("couldn't find "+ str(pathlib.Path(data_path).joinpath('aparat_data')))
            os.chdir(str(pathlib.Path(data_path).joinpath('aparat_data')))
            os.mkdir("aparat_data")
        else:
            break


    #checking if CSV file of data is there or not.
    assert init_csv_file(),"Error in initiating csv file."

    if not prosumer.has_logged_in:
        assert prosumer.login_into_profile(channel_id=username,password=password),"Error in logging in Aparat Profile."

    #Getting todays time.
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    #opening csv file to write in.
    csv_file = open(raw_data_file_name, 'a+')
    data_writer = csv.writer(csv_file)

    data_row = []

    data_row.append(str(now))

    #start getting data.
    if "get_count_videos" in get_list:
        try:
            members = prosumer.get_count_videos(channel_id)
        except:
            logging.debug("Error in running get_subscribers.")
            pass
        else:
            data_row.append(str(members))
    else:
        data_row.append("-")

    if "get_subscribers" in get_list:
        try:
            members = prosumer.get_subscribers(channel_id)
        except:
            logging.debug("Error in running get_subscribers.")
        else:
            data_row.append(str(members))
    else:
        data_row.append("-")

    if "get_today_views" in get_list:
        try:
            members = prosumer.get_today_views(channel_id)
        except:
            logging.debug("Error in running get_subscribers.")
        else:
            data_row.append(str(members))
    else:
        data_row.append("-")

    if "get_total_views" in get_list:
        try:
            members = prosumer.get_total_views(channel_id)
        except:
            logging.debug("Error in running get_subscribers.")
        else:
            data_row.append(str(members))
    else:
        data_row.append("-")

    if "get_total_minute_views" in get_list:
        try:
            members = prosumer.get_total_minute_views(channel_id)
        except:
            logging.debug("Error in running get_subscribers.")
        else:
            data_row.append(str(members))
    else:
        data_row.append("-")


    if "get_channel_name" in get_list:
        try:
            members = prosumer.get_channel_name(channel_id)
        except:
            logging.debug("Error in running get_subscribers.")
        else:
            data_row.append(str(members))
    else:
        data_row.append("-")


    if "get_cover_image_url" in get_list:
        try:
            cover_url = prosumer.get_cover_image_url(channel_id)
        except:
            logging.debug("Error in running get_cover_image_url.")
        else:
            data_row.append(str(cover_url))
    else:
        data_row.append("-")


    #removing duplicated data by same date
    if replace_by_old_todays_data:
        lines = list()
        with open(raw_data_file_name, 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == now.split()[0]:
                        lines.remove(row)

        with open(raw_data_file_name, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)

    data_writer.writerow(data_row)

    csv_file.close()

def get_media_file_url():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

media_file_types = [
    'mp4',
    'mov',
    'mkv',
]

def publish_new_video(channel_id,username,password,title,description,tags,media_url,category_index = 0,publish_now = True):
    # Chaning path to aparat data
    while (True):
        try:
            os.chdir(str(pathlib.Path(data_path).joinpath('aparat_data')))
        except:
            logging.debug("couldn't find " + str(pathlib.Path(data_path).joinpath('aparat_data')))
            os.chdir(str(pathlib.Path(data_path).joinpath('aparat_data')))
            os.mkdir("aparat_data")
        else:
            break

    # checking if CSV file of data is there or not.
    assert init_csv_file(mode='publish_log'), "Error in initiating csv file."

    # get file
    file_path = get_media_file_url()
    assert any([type in file_path for type in media_file_types]), 'INVALID FILE TYPE'
    logging.debug(f'File type is valid. {file_path} -> {os.path.getsize(file_path)}')

    if not prosumer.has_logged_in:
        assert prosumer.login_into_profile(channel_id=username, password=password), "Error in logging in Aparat Profile."

    # Getting todays time.
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # opening csv file to write in.
    csv_file = open(raw_data_file_name, 'a+')
    data_writer = csv.writer(csv_file)

    data_row = []

    data_row.append(str(now))

    upload_status = prosumer.upload_new_media(title,description,tags,media_url,category_index = category_index,publish_now = publish_now)

    if upload_status:
        data_row += [title,
        category_index,
        description,
        file_path,
        str(os.path.getsize(file_path))]
        data_writer.writerow(data_row)
    else:
        data_row += ['FAILED',
                     'FAILED',
                     'FAILED',
                     'FAILED',
                     'FAILED']
        data_writer.writerow(data_row)