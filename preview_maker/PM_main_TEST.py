import unittest

from preview_maker.main import mini_clips_times,generate_preview

class PreviewMakerTest(unittest.TestCase):

    def test_mini_clips_times(self):
        self.assertNotEqual(mini_clips_times(3,65,368),[])
        self.assertNotEqual(mini_clips_times(2,86,3652),[])
        self.assertNotEqual(mini_clips_times(10,30,90),[])


    def test_generate_preview(self):
        self.assertEqual(generate_preview(r'preview_maker\test_clips\test.mp4',25,349,(0,12)),True)

