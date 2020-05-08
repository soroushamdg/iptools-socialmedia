from pyLog.pylog import log
import timeit
import threading
#getting data

def get_telgram_data():
    from social_media.telegram_org import garson
    garson.get_todays_data("iranpythoneers")
    # try:
    #     log.log(__name__,str(timeit.timeit('garson.get_todays_data("iranpythoneers")','from social_media.telegram_org import garson')))
    #     return
    # except Exception as msg:
    #     print("Error in getting Telegram data.")
    #     log.log(__name__,f"Error in getting Telegram Today's data. -> {msg}")
    #     return

def get_aparat_data():
    from social_media.aparat_ir import garson
    garson.get_todays_data("iranpythoneers","iranpythoneers","Not@Work78!")
    try:
        log.log(__name__,str(timeit.timeit('garson.get_todays_data("iranpythoneers","iranpythoneers","Not@Work78!")','from social_media.aparat_ir import garson')))
        return
    except Exception as msg:
        print("Error in getting Aparat data.")
        log.log(__name__,f"Error in getting Aparat Today's data. -> {msg}")
        return


if __name__ == "__main__":

    get_telgram_data()
    get_aparat_data()

    # threads = []
    #
    # #defining threads
    # tele_thread = threading.Thread(target=get_telgram_data,args=())
    # aparat_thread = threading.Thread(target=get_aparat_data,args=())
    #
    #
    # #adding threads
    # threads.append(tele_thread)
    # threads.append(aparat_thread)
    #
    #
    # #starting threads
    # for thread in threads:
    #     thread.start()
    #
    # #waiting for threads to finish
    # for thread in threads:
    #     thread.join()

    print("script end.")