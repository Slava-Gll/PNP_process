##################################################################
#################### НАСТРОЙКИ ###################################
##################################################################

MDB_PATH = r"\\smtdev\STC_DB_SMT\CarrierDB.mdb" # путь к MDB
SMB_USERNAME = "Администратор" # логин SMB
SMB_PASSWORD = "R&D_srv" # пароль SMB

#ENCODING = 'cp1251' # Кодировка импорта и экспорта
ENCODING = 'utf8' # Кодировка импорта и экспорта


#OPEN_FILES_WHEN_DONE = False # Открыть папку в конце
OPEN_FILES_WHEN_DONE = True

##################################################################
##################################################################
##################################################################



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

#######LOAD MDB###########
import pyodbc
from smbclient import register_session
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




def ask_mode(modes, question):
        txt = ''
        for key_idx in range(len(modes)):
            txt += f'{key_idx+1} : {modes[key_idx]}\n'
        msg(txt, title=question, color=WHITE, cls=True)
        key = 'abc'
        while not key.isdigit():
            key = readchar.readkey()
            try:
                key = int(key)
                mode = modes[key - 1]
                return key - 1
            except:
                key = 'abc'
                pass
#delete_folder = ask_mode(YESNO, 'Удалить старые файлы?')
include_D = ask_mode(YESNO, 'Включить актив?')
delete_folder = True
if exists('READY/'):
    if delete_folder:
        try:
            shutil.rmtree('READY/')
        except Exception as e:
            error('Ошибка удаления папки', e)

msg('Обработка ...', title='Обработка', color=YELLOW, cls=True)
df_join_good = pd.DataFrame()
df_join_bad = pd.DataFrame()
df_join = pd.DataFrame()





try:
    register_session("smtdev", username=SMB_USERNAME, password=SMB_PASSWORD)
    #shutil.copyfile(MDB_PATH, "CarrierDB.mdb")
    #MDB_FILE = realpath(r'CarrierDB.mdb')
    MDB_FILE = MDB_PATH
    driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
    cnxn = pyodbc.connect(f'Driver={driver};DBQ={MDB_FILE}')
    crsr = cnxn.cursor()
    library = pd.read_sql("SELECT * FROM CarrierTable", cnxn)
    library = library[['CarrierId', 'ComponentName', 'Location']]

except Exception as e:
    error('Не удалось подключиться к БД SMT', e)


try:
    library = library[['CarrierId', 'ComponentName', 'Location']]
    library_filtered = library[library['Location']=='STANOK'].reset_index(drop=True)
    library_filtered['CarrierId'] = library_filtered['CarrierId'].astype('str').str.zfill(6)
    library_filtered.rename(columns={"ComponentName": "Comment"}, inplace=True)
except Exception as e:
    error('файл библиотеки не читается')

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
        OUT_FOLDER = f'READY/{OUT_FILE}/'
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
        
        try:
            csv = pd.merge(csv, library_filtered, on='Comment', how='left', sort=False)
        except KeyError as e:
            error('Ошибка чтения PNP', e, INPUT_FILE)
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
        csv['CarrierId'] = 'R' + csv['CarrierId']
        csv.drop(columns=['Location'], inplace=True)


        ###############################################
        ###############################################
        ###############################################
        csv_pnp = csv.copy()
        csv_comp = csv.copy()

        if not include_D:
            csv_comp = csv_comp[csv_comp.Comment.str.match(REGEXP_IS_ACTIVE)]
        csv_comp.drop_duplicates(subset=['Comment'], keep='first', inplace=True)


        csv_comp = csv_comp[['Comment', 'CarrierId', 'package', 'value', 'Translit']]
        csv_comp['tip_lenty'] = ''
        csv_comp.loc[csv_comp.package.isin(['0603_C', '0603']), 'tip_lenty'] = "Tape08-4 white"
        csv_comp.loc[csv_comp.package.isin(['0402_C', '0402']), 'tip_lenty'] = "Tape08-2 white"
        csv_comp = csv_comp[csv_comp['value']!='NM'].reset_index(drop=True)
        saved = False
        print(f"    Кол-во ПКИ без CARRIER: {csv_comp['CarrierId'].isna().sum()}")
        for comp in csv_comp.loc[csv_comp['CarrierId'].isna(), 'Comment'].to_list():
            print(f"        {comp}")
        csv_exists = csv_comp.dropna(subset=['CarrierId'])
        csv_nonexistent = csv_comp[csv_comp['CarrierId'].isna()]
        df_join_good = pd.concat([df_join_good, csv_exists], ignore_index=True, sort=False)
        df_join_bad = pd.concat([df_join_bad, csv_nonexistent], ignore_index=True, sort=False)
        while not saved:
            try:
                csv_exists.to_csv(OUT_FOLDER+'good_'+OUT_FILE, sep=';', index=False, header=True, encoding=ENCODING)
                csv_nonexistent.to_csv(OUT_FOLDER+'bad_'+OUT_FILE, sep=';', index=False, header=True, encoding=ENCODING)
                saved = True
            except Exception as e:
                print(f'Ошибка сохранения, возможно файл уже открыт:\n{e}')
                sleep(1)
            df_join_good.to_csv('READY/COMP_GOOD.csv', sep=';', index=False, header=True, encoding=ENCODING)
            df_join_bad.to_csv('READY/COMP_BAD.csv', sep=';', index=False, header=True, encoding=ENCODING)


        csv_pnp = csv_pnp.drop('CarrierId', axis=1)
        saved = False
        df_join = pd.concat([df_join, csv_pnp], ignore_index=True, sort=False)
        while not saved:
            try:
                csv_pnp.to_csv(OUT_FOLDER+OUT_FILE, sep=';', index=False, header=True, encoding=ENCODING)
                saved = True
            except Exception as e:
                print(f'Ошибка сохранения, возможно файл уже открыт:\n{e}')
                sleep(1)
            #df_join['Layer'] = '-'
            #df_join.to_csv('READY/PNP_all.csv', sep=';', index=False, header=True)




        ###############################################
        ###############################################
        ###############################################
            
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