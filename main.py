from pyLog.pylog import log
import timeit
#getting data
# from social_media_statics.telegram_org import garson
# try:
#     log.log(__name__,str(timeit.timeit(garson.get_todays_data("iranpythoneers"))))
# except Exception as msg:
#     print("Error in getting Telegram data.")
#     log.log(__name__,f"Error in getting Telegram Today's data. -> {msg}")


from social_media_statics.aparat_ir import garson
garson.get_todays_data("iranpythoneers","iranpythoneers","Not@Work78!")
# try:
#     log.log(__name__,str(timeit.timeit(garson.get_todays_data("iranpythoneers","iranpythoneers","Not@Work78!"))))
# except Exception as msg:
#     print("Error in getting Aparat data.")
#     log.log(__name__,f"Error in getting Aparat Today's data. -> {msg}")
