"""
Garson means the script which organizes raw data into readable tables and structure.

Software diagram:
Raw Data on website -> Receiving by Prosumer -> Organizing by Garson -> Cooking into Valuable Data by Chef
"""

import datetime
from social_media.telegram_org import prosumer
from social_media.telegram_org.options import script_name as sn
import csv
import os
from options import data_path
from pyLog.pylog import log


def init_csv_file():
    try:
        csv_file = open('tlg-raw.iptlg','r')
    except:
        log.log(origin=sn,message="no tlg-raw.iptlg file found! We will create new one.")
        try:
            file = open('tlg-raw.iptlg','a+')
            header_writer = csv.writer(file)
            header_writer.writerow(["file creation date : " + str(datetime.datetime.now().strftime('%d %B %Y %H:%M:%S'))," "," "," "," "])
            header_writer.writerow(["date","members","title","description","profile cover"])
            file.close()
            return True
        except Exception as msg:
            log.log(origin=sn,message="can't create new csv file. please check administrator access or problems ->" + str(msg))

            return False
    else:
        csv_file.close()
        log.log(origin=sn,message="tlg-raw.iptlg file found successfully.")
        return True

def get_todays_data(channel_id,save = True,replace_by_old_todays_data = False,custom_timezone = None,get_list = ["get_subscribers"]):
    #Chaning path to telegram data
    while(True):
        try:
            os.chdir(data_path + r"\telegram_data")
        except:
            log.log(origin=sn,message="couldn't find "+ data_path + r'\telegram_data')
            os.chdir(data_path)
            os.mkdir("telegram_data")
        else:
            break

    #checking if CSV file of data is there or not.
    assert init_csv_file(),"Error in initiating csv file."

    #Getting todays time.
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    #opening csv file to write in.
    csv_file = open('tlg-raw.iptlg', 'a+')
    data_writer = csv.writer(csv_file)

    data_row = []

    data_row.append(str(now))

    #start getting data.
    if "get_subscribers" in get_list:
        try:
            members = prosumer.get_subscribers(channel_id)
        except:
            log.log(origin=sn,message="Error in running get_subscribers.")
        else:
            data_row.append(str(members))
    else:
        data_row.append("-")

    if "get_channel_name" in get_list:
        try:
            channel_name = prosumer.get_channel_name(channel_id)
        except:
            log.log(origin=sn,message="Error in running get_channel_name.")
        else:
            data_row.append(str(channel_name))
    else:
        data_row.append("-")

    if "get_description" in get_list:
        try:
            description = prosumer.get_description(channel_id)
        except:
            log.log(origin=sn,message="Error in running get_description.")
        else:
            data_row.append(str(description))
    else:
        data_row.append("-")

    if "get_cover_image_url" in get_list:
        try:
            cover_url = prosumer.get_cover_image_url(channel_id)
        except:
            log.log(origin=sn,message="Error in running get_cover_image_url.")
        else:
            data_row.append(str(cover_url))
    else:
        data_row.append("-")


    #removing duplicated data by same date
    if replace_by_old_todays_data:
        lines = list()
        with open('tlg-raw.iptlg', 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == now.split()[0]:
                        lines.remove(row)

        with open('tlg-raw.iptlg', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)

    data_writer.writerow(data_row)

    csv_file.close()
    return True