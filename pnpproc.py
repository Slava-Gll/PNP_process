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
        self.last_error_comment = False
        self.csv_comment_field = ''
        self.first_line = ''
        self.csv = None
        self.translit = []
        self.out_text = ''
        self.encoding = 'utf8'
    def convert_utf8(self, filename):
        try:
            with open(filename, 'r+', encoding='utf8') as f:
                self.first_line = f.readlines()[0]
            return True
        except Exception:
            try:
                with open(filename, 'r', encoding='cp1251') as f:
                    lines = f.readlines()
                with open(filename, 'w', encoding='utf8') as f:
                    f.writelines(lines)
                self.first_line = lines[0]
                return True
            except Exception as e:
                self.last_error = e
                return False
    def pre_check(self, filename):
        """
        Checks for all startup conditions
        returns status
        :return:
        """
        if not check_file(filename):
            self.last_error = 'Ошибка чтения файла'
            return False
        if not self.convert_utf8(filename):
            return False
        if not self.load_csv(filename, encoding='utf8'):
            if not self.load_csv(filename, encoding='cp1251'):
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

    def load_csv(self, filename, encoding='utf8', separator=r';|\t'):
        try:
            self.last_error_comment = False
            try:
                self.csv = pd.read_csv(filename, sep=separator, engine='python', encoding=encoding)
                self.csv.rename(columns={self.csv_comment_field: "Comment"}, inplace=True)
                self.csv['Comment']=self.csv['Comment']
            except Exception as e:
                self.csv = pd.read_fwf(filename)
                self.csv.rename(columns={self.csv_comment_field: "Comment"}, inplace=True)
                self.csv['Comment'] = self.csv['Comment']

            return True
        except Exception as e:
            self.last_error = f'Ошибка чтения PNP\nпроверьте формат файла\n{e}'
            self.last_error_comment = True
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
        self.out_text += '    Содержат не латинские буквы:\n'
        self.csv['Translit'] = self.csv['Comment'].apply(check_trans)
        self.csv['Comment'] = self.csv['Comment'].apply(self.trans)
        self.out_text += "\n".join(list(set(self.translit)))
        self.csv['Comment'] = self.csv['Comment'].str.replace(' ', '-')

    def convert(self, file_path, open_when_done=True, csv_comment_field = 'comment'):
        self.csv_comment_field = csv_comment_field
        """

        :return:
        :param file_path:
        """
        out_file = Path(file_path).stem
        self.out_text = f'\nПроект: {out_file}\n'
        self.translit = []
        if not self.pre_check(file_path):
            return False

        self.fix()
        if not self.export_csv(out_file):
            return False
        if open_when_done:
            os.startfile(realpath(self.out_folder))
        return True