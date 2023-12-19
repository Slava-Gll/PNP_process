import pandas as pd
from time import sleep
import os
from os.path import exists, realpath
from pathlib import Path
from transliterate import translit, get_available_language_codes
import shutil

import warnings


# warnings.filterwarnings('ignore')


def check_file(filename):
    """
    Checks that file exists
    :return:
    :param filename:
    """
    if not exists(filename):
        return False
    return True


def check_trans(txt):
    if not txt.isascii():
        return "!!!"


class PnpConverter:
    def __init__(self, out_folder='READY'):
        self.out_folder = out_folder
        self.last_error = ''
        self.csv = None
        self.translit = []
        self.out_text = ''
        self.encoding = 'utf8'

    def pre_check(self, filename):
        """
        Checks for all startup conditions
        returns status
        :return:
        """
        if not check_file(filename):
            self.last_error = 'Ошибка чтения файла'
            return False
        if not self.load_csv(filename, encoding=self.encoding):
            return False
        return True
    def update_folder(self):
        """
        tries to remove target folder and then
        creates it to ensure that it's empty
        :return:
        """

        try:
            if exists(self.out_folder):
                shutil.rmtree(realpath(self.out_folder))
            os.mkdir(realpath(self.out_folder))
            return True
        except Exception:
            return False

    def load_csv(self, filename, encoding='utf8', separator=';', fwf=False):
        try:
            if not fwf:
                self.csv = pd.read_csv(filename, sep=separator, engine='python', encoding=encoding)
            else:
                self.csv = pd.read_fwf(filename)
            self.csv['Comment'] = self.csv['Comment']
            return True
        except Exception as e:
            self.last_error = f'Ошибка чтения PNP\n{e}'
            return False

    def trans(self, txt):
        if not txt.isascii():
            self.translit.append(f'        {txt}')
            return translit(txt, reversed=True)
        else:
            return txt

    def export_csv(self, new_name):
        try:
            new_name = f'{self.out_folder}/{new_name}.csv'
            print(new_name)
            self.csv.to_csv(new_name,
                            sep=';',
                            index=False,
                            header=True,
                            encoding=self.encoding)
            return True
        except Exception as e:
            self.last_error = f'Ошибка сохранения, возможно файл уже открыт:\n{e}'
            return False

    def fix(self):
        self.csv['Comment'] = self.csv['Comment'].str.replace('"', '')
        print('    Содержат не латинские буквы:')
        self.csv['Translit'] = self.csv['Comment'].apply(check_trans)
        self.csv['Comment'] = self.csv['Comment'].apply(self.trans)
        self.out_text += "\n".join(list(set(self.translit)))
        self.csv.drop_duplicates(subset=['Designator'], keep='first', inplace=True)
        self.csv['Comment'] = self.csv['Comment'].str.replace(' ', '-')

    def convert(self, file_path, open_when_done=True):
        """

        :return:
        :param file_path:
        """
        if not self.pre_check(file_path):
            return False
        out_file = Path(file_path).stem
        self.out_text = f'Проект: {out_file}'
        self.fix()
        if not self.export_csv(out_file):
            return False
        if open_when_done:
            os.startfile(realpath(self.out_folder))
        return True