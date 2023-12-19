
#ENCODING = 'cp1251' # Кодировка импорта и экспорта
ENCODING = 'utf8' # Кодировка импорта и экспорта


#OPEN_FILES_WHEN_DONE = False # Открыть папку в конце
OPEN_FILES_WHEN_DONE = True


from sys import argv
import pandas as pd
import re
from time import sleep
import os
from os.path import exists, realpath
from pathlib import Path
from colorama import Fore, Back, Style
from transliterate import translit, get_available_language_codes
import readchar
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
        REGEXP_PACKAGE = re.compile(r'^[RCLF]-\d{4}|L-LQW\d{2}|L-LQG\d{2}|L-LQW2BHN|F-BLM\d{2}|F-LFCN|F-HFCN|F-NF[EM]\d{2}')
        REGEXP_VALUE_C = re.compile(r'\AC-\d{4}-.{1,}-\d{1,}-\S{1,}')
        REGEXP_VALUE_R = re.compile(r'\AR-\d{4}-\S{1,}-.')
        REGEXP_VALUE_L = re.compile(r'\AL-.{1,}-.{1,}nH|n[^\n]{0,}')
        REGEXP_VALUE_F_LFCN = re.compile(r'\d{2,4}[+]$|\d{2,4}[+]$')
        #REGEXP_IS_ACTIVE = re.compile(r'^[RCLF]-.{1,}')
        REGEXP_IS_ACTIVE = re.compile(r'\A(?![DXTQ])')

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

        packs_l = {'L-0402': '0402_C',
                   'L-LQW15': '0402_C',
                   'L-LQG15': '0402_C',
                   'L-LQW18': '0603_C',
                   'L-LQW21': '0805_C',
                   'L-LQW2BHN': '0805_LQW2BHN'}

        packs_f = {'F-LFCN': '1206_FV',
                   'F-HFCN': '1206_FV',
                   'F-LFCG': '0805_FV',
                   'F-BLM15': '0402_C',
                   'F-BLM18': '0603_C',
                   'F-BLM21': '0805_C'}

        def extract_package(row):
            try:
                comment = row['Comment']
            except KeyError:
                error('Ошибка чтения PNP')
            try:
                pack = REGEXP_PACKAGE.search(comment).group(0)
                #print(pack[:1])
                if pack[:1] == 'R':
                    pack = pack[2:]
                elif pack[:1] == 'C':
                    pack = pack[2:] + '_C'
                elif pack[:1] == 'L':
                    if pack in packs_l:
                        pack = packs_l[pack]
                #print(comment, pack)
                elif pack[:1] == 'F':
                    #print(pack, comment)
                    if pack in packs_f:
                        pack = packs_f[pack]
                else:
                    pack = ''
                #print(comment, pack)
            except Exception as e:
                pack = ''
                #print('Корпус не найден:',comment)
            return pack

        def extract_value(row):
            comment = row['Comment']
            try:
                pack = REGEXP_PACKAGE.search(comment).group(0)
                if pack[:1] == 'R':
                    val = extract_value_R(comment)
                elif pack[:1] == 'C':
                    val = extract_value_C(comment)
                elif pack[:1] == 'L':
                    val = extract_value_L(comment)
                elif pack[:1] == 'F':
                    val = extract_value_F(comment)
                else:
                    val = ''
            except Exception as e:
                val = ''
                #print('Ошибка номинала', e, comment)
            return val


        def extract_value_R(comment):
            try:
                val = REGEXP_VALUE_R.search(comment).group(0)
                val = val.split('-')[2]
                return val
            except:
                return

        def extract_value_F(comment):
            try:
                val = comment[2:]
                try:
                    val = REGEXP_VALUE_F_LFCN.search(val).group(0)
                except:
                    pass
                return val
            except Exception as e:
                print(e)
                return

        def extract_value_C(comment):
            try:
                val = REGEXP_VALUE_C.search(comment).group(0)
                val = val.split('-')[4]
                if not 'uF' in val:
                    val = val.replace('u', 'uF')
                return val
            except:
                return

        def extract_value_L(comment):
            try:
                val = comment       #REGEXP_VALUE_L.search(comment).group(0)
                val = val.split('-')
                val_c = ''
                vals = ['n', 'nH', 'u', 'uH']
                for i in val:
                    for j in vals:
                        if j in i:
                            val_c = i
                if not 'nH' in val_c:
                    val_c = val_c.replace('n', 'nH')
                if not 'uH' in val_c:
                    val_c = val_c.replace('u', 'uH')
                return val_c
            except Exception as e:
                #print(e)
                return

        csv['package'] = csv.apply(extract_package, axis=1)
        csv['value'] = csv.apply(extract_value, axis=1)

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