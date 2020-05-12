import unittest

from social_media.telegram_org import garson

class TelegramTest(unittest.TestCase):

    def test_get_statics(self):
        self.assertNotEqual(garson.get_todays_data("iranpythoneers"),None)
        self.assertEqual(garson.get_todays_data("padokar_ir"), None)
        self.assertEqual(garson.get_todays_data("StupidUsernameee"), None)
        garson.quit_browser()
