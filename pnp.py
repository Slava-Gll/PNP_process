
#ENCODING = 'cp1251' # Кодировка импорта и экспорта
ENCODING = 'utf8' # Кодировка импорта и экспорта


#OPEN_FILES_WHEN_DONE = False # Открыть папку в конце
OPEN_FILES_WHEN_DONE = True


from sys import argv
import pandas as pd
from time import sleep
import os
from os.path import exists, realpath
from pathlib import Path
from transliterate import translit, get_available_language_codes
import shutil

import warnings
warnings.filterwarnings('ignore')
##########################

###### colors ############
GREEN = '20'
RED = '40'
YELLOW = '60'
WHITE = '70'
##########################

YESNO = ['Нет', 'Да']

def msg(*text, title=None, color=None, cls=False):
        if cls:
            os.system('cls')
        if title:
            os.system(f'title {title}')
        if color:
            os.system(f'color {color}')
        for i in text:
            print(i)  

def error(*e):
    msg(*e, title='ОШИБКА', color=RED, cls=True)
    input('Нажмите ENTER или закройте программу')
    os.system('cls')
    exit()

if len(argv) <=1:
    error('Файлы не выбраны, перетащите PnP на программу')

os.system('cls')

delete_folder = True
if exists('READY/'):
    if delete_folder:
        try:
            shutil.rmtree('READY/')
        except Exception as e:
            error('Ошибка удаления папки', e)

msg('Обработка ...', title='Обработка', color=YELLOW, cls=True)

for i in range(len(argv)):
    if i > 0:
        try:
            INPUT_FILE = argv[i]
        except:
            pass

        if not exists('READY/'):
            os.mkdir('READY/')

        msg(f'Проект: {Path(INPUT_FILE).stem}', cls=False)
        OUT_FILE = Path(INPUT_FILE).stem
        OUT_FOLDER = f'READY/'
        OUT_FILE += '.csv'
        if not exists(OUT_FOLDER):
            os.mkdir(OUT_FOLDER)
        SEP = '\t'

        if exists(INPUT_FILE):
            #print(INPUT_FILE)
            pass
        else:
            error('Отсутствует файл')

    

        try:
            csv = pd.read_csv(INPUT_FILE, sep=SEP, engine='python', encoding=ENCODING)
            try:
                csv['Comment'] = csv['Comment']
            except:
                csv = pd.read_fwf(INPUT_FILE)
        except Exception as e:
            error('pnp не читается', e)

        def check_trans(txt):
            if not txt.isascii():
                return "!!!"

        class store():
            translit = []
        def trans(txt):
            if not txt.isascii():
                store.translit.append(f'        {txt}')
                return translit(txt, reversed=True)
            else:
                return txt
        csv['Comment'] = csv['Comment'].str.replace('"', '')
        print('    Содержат не латинские буквы:')
        csv['Translit'] = csv['Comment'].apply(check_trans)
        csv['Comment'] = csv['Comment'].apply(trans)
        print("\n".join(list(set(store.translit))))
        csv.drop_duplicates(subset=['Designator'], keep='first', inplace=True)
        csv['Comment'] = csv['Comment'].str.replace(' ', '-')

        csv_pnp = csv.copy()
        saved = False
        while not saved:
            try:
                csv_pnp.to_csv(OUT_FOLDER+OUT_FILE, sep=';', index=False, header=True, encoding=ENCODING)
                saved = True
            except Exception as e:
                print(f'Ошибка сохранения, возможно файл уже открыт:\n{e}')
                sleep(1)
        print('\n\n\n-----------------------------------------------')
try:
    pass
except Exception as e:
    print(i)
    input()
msg('Готово', title='Готово', color=GREEN)
if OPEN_FILES_WHEN_DONE:
    os.startfile(realpath('READY/'))
input('Нажмите ENTER чтобы выйти')
exit()