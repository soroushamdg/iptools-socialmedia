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

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from pyLog.pylog import log
from social_media_statics.telegram_org.options import script_name as sn

telegram_root_url = "https://t.me/"

opts = Options()
opts.set_headless(True)
assert opts.headless
tlg_browser = Chrome(options=opts,executable_path='C:/Users/Soroush/PycharmProjects/ip-tools/dependencies/chromedriver.exe')

def get_channel_name(channel_id):
    """
    This function returns title of the channel.
    :param channel_id: ID of channel
    :return: string
    """
    try:
        tlg_browser.get(telegram_root_url + str(channel_id) if '@' not in channel_id else channel_id[1::])
    except Exception as msg:
        log.log(sn,"Error in connecting to server ->" + str(msg))
    else:
        return tlg_browser.find_elements_by_class_name('tgme_page_title')[0].text

def get_subscribers(channel_id,string = True):
    """
    This function returns number of channel subscribers.
    :param channel_id: ID of Channel.
    :param string : if True return String, else return Int
    :return: Str, Number of subscribers.
    :status : COMPLETED
    """
    try:
        tlg_browser.get(telegram_root_url + str(channel_id) if '@' not in channel_id else channel_id[1::])
    except Exception as msg:
        log.log(sn,"Error in connecting to server ->" + str(msg))
        return

    members = [element.text if 'members' in element.text else '' for element in tlg_browser.find_elements_by_class_name('tgme_page_extra')]
    if members:
        try:
            num = str(members[0].split('members')[0]).strip()
        except:
            log.log(sn,"couldn't connect.")
            return 0
        else:
            log.log(sn,"successful connect.")
            return str(num.replace(" ","")) if string else int(num.replace(" ",""))

    else:
        return 0


def get_description(channel_id):
    """
        This function returns description of the channel.
    :param channel_id: ID of channel.
    :return: string
    """
    try:
        tlg_browser.get(telegram_root_url + str(channel_id) if '@' not in channel_id else channel_id[1::])
    except Exception as msg:
        log.log(sn,"Error in connecting to server ->"+str(msg))
    else:
        return tlg_browser.find_elements_by_class_name('tgme_page_description')[0].text

def get_cover_image_url(channel_id):
    try:
        tlg_browser.get(telegram_root_url + str(channel_id) if '@' not in channel_id else channel_id[1::])
    except Exception as msg:
        log.log(sn,"Error in connecting to server ->"+str(msg))
    else:
        return tlg_browser.find_elements_by_class_name('tgme_page_photo_image')[0].get_attribute("src")