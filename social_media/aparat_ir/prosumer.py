"""
Prosumer means the script which gets and receives raw data from urls.

pro·sum·er
/prōˈso͞omər/
noun
noun: prosumer; plural noun: prosumers; noun: pro-sumer; plural noun: pro-sumers
an amateur who purchases equipment with quality or features suitable for professional use.

Software diagram:
Raw Data on website -> Receiving by Prosumer -> Organizing by Garson -> Cooking into Valuable Data by Chef
"""


#selenium imports
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
#logging
import logger_factory,logging
logging.getLogger(__name__)
#options imports
from social_media.aparat_ir.options import script_name as sn
#time imports
from time import sleep
#os import
import os
import pathlib
from options import chromdriver_path,test_run

#code seg
aparat_root_url = "https://www.aparat.com/"

opts = Options()
if not test_run:
    opts.set_headless(True)
    assert opts.headless
aparat_browser = Chrome(options=opts, executable_path=chromdriver_path)

has_logged_in = False

def login_into_profile(channel_id, password):
    """
    This function will login into aparat channel profile
    :param channel_id: username
    :param password: password
    :return: True if successful, False if error happens.
    """

    global has_logged_in

    aparat_browser.delete_all_cookies()
    try:
        aparat_browser.get("https://www.aparat.com/signout")
    except:
        pass

    sleep(2)

    #get into login url
    try:
        logging.debug("Loading login page.")
        aparat_browser.get("https://www.aparat.com/login")
    except:
        logging.debug("Couldn't get into login page.")
        return False

    sleep(2)

    #find username field
    #checks for 5 times, with 3 seconds wait.
    for i in range(5):
        #find username field and fill it.
        try:
            logging.debug("Finding username input.")
            username_field = aparat_browser.find_element_by_id("username")
        except Exception as msg:
            logging.debug("Couldn't find username field."+str(msg))
            sleep(3)
            if i < 4:
                continue
            else:
                return False
        else:
            username_field.clear()
            username_field.send_keys(channel_id)
            break


    #find first login stage button
    try:
        logging.debug("Clicking on first stage login button.")
        login_first_stage_button = aparat_browser.find_elements_by_class_name("btn")[1]
        assert "ورود" in login_first_stage_button.text,"login first stage button list index is wrong, please check."
    except:
        logging.debug("Couldn't find first stage login submit button")
        return False
    else:
        login_first_stage_button.click()

    #check if it worked.
    logging.debug("Check if username has found.")
    assert "کاربر پیدا نشد!" not in [element.text for element in aparat_browser.find_elements_by_class_name("text-error")],"Error message in login page,It seems username is incorrect."
    logging.debug("Username has found.")
    #find password field
    #checks for 5 times, with 3 seconds wait.
    sleep(2)
    for i in range(5):
        try:
            logging.debug("Finding password input.")
            password_field = aparat_browser.find_element_by_id("password")
        except:
            logging.debug("Couldn't find username field.")
            if i<4:
                continue
            else:
                return False
        else:
            password_field.clear()
            password_field.send_keys(password)
            break

    sleep(1)

    #find login button and LOGIN
    try:
        logging.debug("find login second stage button.")
        login_final_stage_button = aparat_browser.find_elements_by_class_name("btn")[0]
        assert "ادامه" in login_final_stage_button.text,"login final stage button list index is wrong, please check."
    except:
        logging.debug("Couldn't find final stage login submit button")
        return False
    else:
        login_final_stage_button.click()


    sleep(5)

    for i in range(5):
        try:
            logging.debug("Checking if logging in was successfull.")
            assert "https://www.aparat.com/" == aparat_browser.current_url,"Login failed, didn't load first page."
        except Exception as msg:
            logging.debug(str(msg))
            if i<4:
                sleep(1)
                continue
            else:
                assert "https://www.aparat.com/" == aparat_browser.current_url, "Login failed, didn't load first page."
        else:
            break


    has_logged_in = True

    return True


# GETTINGS STATISTICS
def get_channel_name(channel_id):
    """
    This function returns title of the channel.
    :param channel_id: ID of channel
    :return: string
    """
    if not has_logged_in:
        logging.debug("Please first login into website.")
        return False

    try:
        aparat_browser.get(aparat_root_url + str(channel_id) if '@' not in channel_id else channel_id[1::])
    except Exception as msg:
        logging.debug("Error in connecting to server ->" + str(msg))
    else:
        return aparat_browser.find_element_by_id("channelTitle")[0].text

def get_subscribers(channel_id,string = True):
    """
    This function returns number of channel subscribers.
    :param channel_id: ID of Channel.
    :param string : if True return String, else return Int
    :return: Str, Number of subscribers.
    :status : COMPLETED
    """

    if not has_logged_in:
        logging.debug("Please first login into website.")
        return "!LOGIN"

    try:
        aparat_browser.get(aparat_root_url + "statistics")
    except Exception as msg:
        logging.debug("Error in connecting to server ->" + str(msg))
        return

    try:
        members = aparat_browser.find_elements_by_class_name("stat-box")[0].find_elements_by_class_name("number")[0].text
    except:
        logging.debug("error in finding stat-box number members text")
        return
    else:
        if members:
            try:
                num = str(members).strip()
            except:
                logging.debug("couldn't connect.")
                return 0
            else:
                logging.debug("successful connect.")
                return str(num.replace(" ","")) if string else int(num.replace(" ",""))

        else:
            return 0


def get_total_views(channel_id, string=True):
    """
    This function returns number of channel total video views.
    :param channel_id: ID of Channel.
    :param string : if True return String, else return Int
    :return: Str, Number of subscribers.
    :status : COMPLETED
    """

    if not has_logged_in:
        logging.debug("Please first login into website.")
        return "!LOGIN"

    try:
        aparat_browser.get(aparat_root_url + "statistics")
    except Exception as msg:
        logging.debug("Error in connecting to server ->" + str(msg))
        return

    try:
        total_views = aparat_browser.find_elements_by_class_name("stat-box")[1].find_elements_by_class_name("number")[0].text
    except:
        logging.debug("error in finding stat-box number total views text")
        return
    else:
        if total_views:
            try:
                num = str(total_views).strip()
            except:
                logging.debug("couldn't connect.")
                return 0
            else:
                logging.debug("successful connect.")
                return str(num.replace(" ", "")) if string else int(num.replace(" ", ""))

        else:
            return 0


def get_total_minute_views(channel_id, string=True):
    """
    This function returns number of channel total minute views.
    :param channel_id: ID of Channel.
    :param string : if True return String, else return Int
    :return: Str, Number of subscribers.
    :status : COMPLETED
    """

    if not has_logged_in:
        logging.debug("Please first login into website.")
        return "!LOGIN"

    try:
        aparat_browser.get(aparat_root_url + "statistics")
    except Exception as msg:
        logging.debug("Error in connecting to server ->" + str(msg))
        return

    try:
        total_minute_views = aparat_browser.find_elements_by_class_name("stat-box")[2].find_elements_by_class_name("number")[0].text
    except:
        logging.debug("error in finding stat-box number total minute views text")
        return
    else:
        if total_minute_views:
            try:
                num = str(total_minute_views).strip()
            except:
                logging.debug("couldn't connect.")
                return 0
            else:
                logging.debug("successful connect.")
                return str(num.replace(" ", "")) if string else int(num.replace(" ", ""))

        else:
            return 0


def get_today_views(channel_id, string=True):
    """
    This function returns number of channel today views.
    :param channel_id: ID of Channel.
    :param string : if True return String, else return Int
    :return: Str, Number of subscribers.
    :status : COMPLETED
    """

    if not has_logged_in:
        logging.debug("Please first login into website.")
        return "!LOGIN"

    try:
        aparat_browser.get(aparat_root_url + "statistics")
    except Exception as msg:
        logging.debug("Error in connecting to server ->" + str(msg))
        return

    try:
        today_views = aparat_browser.find_elements_by_class_name("stat-box")[3].find_elements_by_class_name("number")[0].text
    except:
        logging.debug("error in finding stat-box number today views text")
        return
    else:
        if today_views:
            try:
                num = str(today_views).strip()
            except:
                logging.debug("couldn't connect.")
                return 0
            else:
                logging.debug("successful connect.")
                return str(num.replace(" ", "")) if string else int(num.replace(" ", ""))

        else:
            return 0

def get_cover_image_url(channel_id):
    if not has_logged_in:
        logging.debug("Please first login into website.")
        return "!LOGIN"

    try:
        aparat_browser.get(aparat_root_url + "dashboard")
    except Exception as msg:
        logging.debug("Error in connecting to server ->"+str(msg))
    else:
        return aparat_browser.find_elements_by_class_name("top")[0].find_elements_by_class_name("avatar")[0].find_elements_by_class_name("avatar-img")[0].get_attribute("src")


def get_count_videos(channel_id):

    if not has_logged_in:
        logging.debug("Please first login into website.")
        return "!LOGIN"


    try:
        aparat_browser.get(aparat_root_url + "dashboard")
    except Exception as msg:
        logging.debug("Error in connecting to server ->"+str(msg))
    else:
        return aparat_browser.find_elements_by_class_name("dashboard-stats")[0].find_elements_by_class_name("number")[0].text


# UPLOAD NEW STUFF


def upload_new_media(title,description,media_url,tags = [],category_index = 0,publish_now = True):


    if not has_logged_in:
        logging.debug("Please first login into website.")
        return False
    # going to upload page


    try:
        aparat_browser.get(aparat_root_url + 'uploadnew')
    except Exception as msg:
        logging.debug("Error in connecting to server ->" + str(msg))
        return False
    sleep(3)

    #find upload section
    try:
        upload_section = aparat_browser.find_element_by_class_name('react-fine-uploader-file-input')
    except Exception as msg:
        logging.debug("Error in finding upload section ->" + str(msg))
        return False


    #sending file to upload input
    try:
        upload_section.send_keys(media_url)
    except Exception as msg:
        logging.debug("Error in sending file to upload section ->" + str(msg))
        return False

    sleep(1)

    #check if upload started (by checking a text)
    for i in range(3):
        try:
            print(aparat_browser.find_element_by_class_name('sc-gPEVay').text)
            assert 'در حال بارگذاری' in aparat_browser.find_element_by_class_name('sc-gPEVay').text or 'ویدیوی شما با موفقیت بارگذاری شد' in aparat_browser.find_element_by_class_name('sc-gPEVay').text, 'Upload has not started'
        except:
            logging.debug(f'upload has not started -> check {i+1}')
            if i == 2:
                logging.debug('Video upload didn\'t start')
                return False
        else:
            logging.debug(f'upload in progress, check {i+1}')
            break

    #filling in title and description

    #title
    try:
        title_section = aparat_browser.find_element_by_id('title')
    except Exception as msg:
        logging.debug("Error in finding title section ->" + str(msg))
        return False
    else:
        title_section.send_keys(title)

    #description
    try:
        desc_section = aparat_browser.find_element_by_id('descr')
    except Exception as msg:
        logging.debug("Error in finding title section ->" + str(msg))
        return False
    else:
        desc_section.send_keys(description)

    #tags
    try:
        tags_section = aparat_browser.find_element_by_class_name('tags-input--trigger').find_element_by_tag_name('input')
    except Exception as msg:
        logging.debug("Error in finding tags section ->" + str(msg))
        return False
    else:
        for tag in tags:
            tags_section.send_keys(tag)
            sleep(20)
            tags_section.send_keys(Keys.ENTER)
            sleep(5)

    #category
    try:
        #open menu
        aparat_browser.find_element_by_class_name('sc-gGBfsJ').click()
        category_menu = aparat_browser.find_element_by_class_name('sc-fYxtnH').find_element_by_class_name('sc-feJyhm')
        #chose from menu and click
        category_menu.find_elements_by_class_name('sc-hEsumM')[category_index].click()
    except Exception as msg:
        logging.debug("Error in selecting category section ->" + str(msg))
        return False
    else:
        logging.debug("category selected successfully")


    #check if upload has finished
    while True:
        try:
            with aparat_browser.find_element_by_class_name('sc-jDwBTQ').find_element_by_class_name('sc-gPEVay').text as status:
                if  "ویدیوی شما با موفقیت بارگذاری شد" in status:
                    logging.debug('upload has finished')
                    break
                elif "در حال بارگذاری" in status:
                    logging.debug(f'video still uploading. -> {aparat_browser.find_elements_by_class_name("dHqyom")}')
                    continue
        except:
            logging.debug('Error in uploading file, quiting.')
            return False

    # submit video
    if publish_now:
        aparat_browser.find_element_by_class_name('sc-iQKALj').find_element_by_class_name('khoBFo').click()
    else:
        aparat_browser.find_element_by_class_name('sc-iQKALj').find_element_by_class_name('eEsanf').click()

    logging.debug('Video uploaded successfully')
    return True

def quit_browser():
    aparat_browser.quit()