import pandas as pd
from time import sleep
import os
from os.path import exists, realpath
from pathlib import Path
from transliterate import translit, get_available_language_codes
import shutil

import warnings


# warnings.filterwarnings('ignore')


class PnpConverter:
    def __init__(self, out_folder):
        self.out_folder = out_folder
        self.last_error = ''
        self.csv = None

    def pre_check(self):
        """
        Checks for all startup conditions
        returns status
        :return:
        """
        if not self.update_folder():
            self.last_error = 'Ошибка создания папки'
            return False
        return True

    def mid_check(self, filename):
        if not self.check_file(filename):
            self.last_error = 'Ошибка чтения файла'
            return False
        if not self.load_csv(filename):
            return False
        return True

    def update_folder(self):
        """
        tries to remove target folder and then
        creates it to ensure that it's empty
        :return:
        """
        if exists(self.out_folder):
            try:
                shutil.rmtree('READY/')
                os.mkdir(self.out_folder)
                return True
            except Exception:
                return False

    def check_file(self, filename):
        """
        Checks that file exists
        :return:
        :param filename:
        """
        if not exists(filename):
            return False
        return True

    def load_csv(self, filename, encoding='utf8', separator=';', fwf=False):
        try:
            if not fwf:
                self.csv = pd.read_csv(filename, sep=separator, engine='python', encoding=encoding)
            else:
                self.csv = pd.read_fwf(filename)
            csv['Comment'] = csv['Comment']
            return True
        except Exception as e:
            self.last_error = f'Ошибка чтения PNP\n{e}'
            return False

    def convert(self, file_path):
        """

        :return:
        :param file_path:
        """
        if not self.mid_check(file_path):
            return False
        out_file = Path(file_path).stem
        out_text = f'Проект: {out_file}'

        return True, out_text

    @staticmethod
    def final(good_ret, text):
        return good_ret, text
