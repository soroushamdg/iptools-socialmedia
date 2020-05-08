import unittest
from social_media.telegram_org import garson

class TelegramTest(unittest.TestCase):

    def test_get_statics(self):
        self.assertEqual(garson.get_todays_data("iranpythoneers"),True)
        self.assertEqual(garson.get_todays_data("padokar_ir"), True)
        self.assertEqual(garson.get_todays_data("StupidUsernameee"), True)
