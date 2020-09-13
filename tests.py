import os
import photobot as pb
import unittest
from dotenv import load_dotenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

class EnvironmentVariableTest(unittest.TestCase):
    def test_text_file(self):
        self.assertIsNotNone(os.getenv('TEXT_FILE'))

    def test_image_dir(self):
        self.assertIsNotNone(os.getenv('IMAGE_DIR'))

    def test_font_file(self):
        self.assertIsNotNone(os.getenv('FONT_FILE'))

    def test_repost_channel(self):
        self.assertIsNotNone(os.getenv('REPOST_CHANNEL'))

    def test_tokent(self):
        self.assertIsNotNone(os.getenv('TOKEN'))


class DataExistTest(unittest.TestCase):
    def test_font_file_exist(self):
        self.assertTrue(os.path.isfile(os.getenv('FONT_FILE')))

    def test_text_file_exist(self):
        self.assertTrue(os.path.isfile(os.getenv('TEXT_FILE')))

    def test_requirements_file_exist(self):
        self.assertTrue(os.path.isfile('requirements.txt'))

    def test_images_dir_exist(self):
        self.assertTrue(os.path.isdir(os.getenv('IMAGE_DIR')))

class BotFuncTest(unittest.TestCase):
    def test_get_text(self):
        self.assertIsInstance(pb.get_text(os.getenv('TEXT_FILE')),str)

    def test_gen_markup(self):
        self.assertIsInstance(pb.gen_markup(),InlineKeyboardMarkup)  


if __name__ == '__main__':
    unittest.main()
