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
from social_media_statics.aparat_ir.options import script_name as sn
from time import sleep
aparat_root_url = "https://www.aparat.com/"

opts = Options()
opts.set_headless(True)
assert opts.headless
aparat_browser = Chrome(options=opts, executable_path='C:/Users/Soroush/PycharmProjects/ip-tools/dependencies/chromedriver.exe')

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
        log.log(sn, "Loading login page.")
        aparat_browser.get("https://www.aparat.com/login")
    except:
        log.log(sn,"Couldn't get into login page.")
        return False

    sleep(2)

    #find username field
    #checks for 5 times, with 3 seconds wait.
    for i in range(5):
        #find username field and fill it.
        try:
            log.log(sn, "Finding username input.")
            username_field = aparat_browser.find_element_by_id("username")
        except Exception as msg:
            log.log(sn,"Couldn't find username field."+str(msg))
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
        log.log(sn,"Clicking on first stage login button.")
        login_first_stage_button = aparat_browser.find_elements_by_class_name("btn")[1]
        assert "ورود" in login_first_stage_button.text,"login first stage button list index is wrong, please check."
    except:
        log.log(sn,"Couldn't find first stage login submit button")
        return False
    else:
        login_first_stage_button.click()

    #check if it worked.
    log.log(sn,"Check if username has found.")
    assert "کاربر پیدا نشد!" not in [element.text for element in aparat_browser.find_elements_by_class_name("text-error")],"Error message in login page,It seems username is incorrect."
    log.log(sn,"Username has found.")
    #find password field
    #checks for 5 times, with 3 seconds wait.
    sleep(2)
    for i in range(5):
        try:
            log.log(sn,"Finding password input.")
            password_field = aparat_browser.find_element_by_id("password")
        except:
            log.log(sn,"Couldn't find username field.")
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
        log.log(sn,"find login second stage button.")
        login_final_stage_button = aparat_browser.find_elements_by_class_name("btn")[0]
        assert "ادامه" in login_final_stage_button.text,"login final stage button list index is wrong, please check."
    except:
        log.log(sn,"Couldn't find final stage login submit button")
        return False
    else:
        login_final_stage_button.click()


    sleep(5)

    for i in range(5):
        try:
            log.log(sn,"Checking if logging in was successfull.")
            assert "https://www.aparat.com/" == aparat_browser.current_url,"Login failed, didn't load first page."
        except Exception as msg:
            log.log(sn,str(msg))
            if i<4:
                sleep(1)
                continue
            else:
                assert "https://www.aparat.com/" == aparat_browser.current_url, "Login failed, didn't load first page."
        else:
            break


    has_logged_in = True

    return True



def get_channel_name(channel_id):
    """
    This function returns title of the channel.
    :param channel_id: ID of channel
    :return: string
    """
    if not has_logged_in:
        log.log(sn,"Please first login into website.")
        return False

    try:
        aparat_browser.get(aparat_root_url + str(channel_id) if '@' not in channel_id else channel_id[1::])
    except Exception as msg:
        log.log(sn,"Error in connecting to server ->" + str(msg))
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
        log.log(sn,"Please first login into website.")
        return "!LOGIN"

    try:
        aparat_browser.get(aparat_root_url + "statistics")
    except Exception as msg:
        log.log(sn,"Error in connecting to server ->" + str(msg))
        return

    try:
        members = aparat_browser.find_elements_by_class_name("stat-box")[0].find_elements_by_class_name("number")[0].text
    except:
        log.log(sn,"error in finding stat-box number members text")
        return
    else:
        if members:
            try:
                num = str(members).strip()
            except:
                log.log(sn,"couldn't connect.")
                return 0
            else:
                log.log(sn,"successful connect.")
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
        log.log(sn, "Please first login into website.")
        return "!LOGIN"

    try:
        aparat_browser.get(aparat_root_url + "statistics")
    except Exception as msg:
        log.log(sn, "Error in connecting to server ->" + str(msg))
        return

    try:
        total_views = aparat_browser.find_elements_by_class_name("stat-box")[1].find_elements_by_class_name("number")[0].text
    except:
        log.log(sn, "error in finding stat-box number total views text")
        return
    else:
        if total_views:
            try:
                num = str(total_views).strip()
            except:
                log.log(sn, "couldn't connect.")
                return 0
            else:
                log.log(sn, "successful connect.")
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
        log.log(sn, "Please first login into website.")
        return "!LOGIN"

    try:
        aparat_browser.get(aparat_root_url + "statistics")
    except Exception as msg:
        log.log(sn, "Error in connecting to server ->" + str(msg))
        return

    try:
        total_minute_views = aparat_browser.find_elements_by_class_name("stat-box")[2].find_elements_by_class_name("number")[0].text
    except:
        log.log(sn, "error in finding stat-box number total minute views text")
        return
    else:
        if total_minute_views:
            try:
                num = str(total_minute_views).strip()
            except:
                log.log(sn, "couldn't connect.")
                return 0
            else:
                log.log(sn, "successful connect.")
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
        log.log(sn, "Please first login into website.")
        return "!LOGIN"

    try:
        aparat_browser.get(aparat_root_url + "statistics")
    except Exception as msg:
        log.log(sn, "Error in connecting to server ->" + str(msg))
        return

    try:
        today_views = aparat_browser.find_elements_by_class_name("stat-box")[3].find_elements_by_class_name("number")[0].text
    except:
        log.log(sn, "error in finding stat-box number today views text")
        return
    else:
        if today_views:
            try:
                num = str(today_views).strip()
            except:
                log.log(sn, "couldn't connect.")
                return 0
            else:
                log.log(sn, "successful connect.")
                return str(num.replace(" ", "")) if string else int(num.replace(" ", ""))

        else:
            return 0

def get_cover_image_url(channel_id):
    if not has_logged_in:
        log.log(sn, "Please first login into website.")
        return "!LOGIN"

    try:
        aparat_browser.get(aparat_root_url + "dashboard")
    except Exception as msg:
        log.log(sn,"Error in connecting to server ->"+str(msg))
    else:
        return aparat_browser.find_elements_by_class_name("top")[0].find_elements_by_class_name("avatar")[0].find_elements_by_class_name("avatar-img")[0].get_attribute("src")


def get_count_videos(channel_id):

    if not has_logged_in:
        log.log(sn, "Please first login into website.")
        return "!LOGIN"


    try:
        aparat_browser.get(aparat_root_url + "dashboard")
    except Exception as msg:
        log.log(sn,"Error in connecting to server ->"+str(msg))
    else:
        return aparat_browser.find_elements_by_class_name("dashboard-stats")[0].find_elements_by_class_name("number")[0].text