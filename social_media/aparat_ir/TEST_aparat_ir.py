import unittest


from social_media.aparat_ir import garson,prosumer

class AparatTest(unittest.TestCase):

    def test_login(self):
        self.assertEqual(prosumer.login_into_profile('worldisblue','soroush1378'),True)
        pass

    def test_get_statics(self):
        self.assertNotEqual(garson.get_todays_data('worldisblue','worldisblue','soroush1378'),None)

    def test_publish_video(self):
        self.assertEqual(garson.publish_new_video('worldisblue','worldisblue','soroush1378','Test Video','something for test, '*20,['test video','videoa','testa'],1,False),True)