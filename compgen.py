import os
import re
from os.path import exists, realpath
import json
import pandas as pd
import pyodbc
from smbclient import register_session
from transliterate import translit

packs_l = {'L-0402': '0402_C',
           'L-ATC-0402': '0402_C',
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

REGEXP_PACKAGE = re.compile(r'^[RCLF]-\d{4}|L-LQW\d{2}|L-LQG\d{2}|L-LQW2BHN|F-BLM\d{2}|F-LFCN|F-HFCN|F-NF[EM]\d{2}')
REGEXP_VALUE_C = re.compile(r'\AC-\d{4}-.+-\d+-\S+')
REGEXP_VALUE_R = re.compile(r'\AR-\d{4}-\S+-.')
REGEXP_VALUE_L = re.compile(r'\AL-.+-.+nH|n[^\n]*')
REGEXP_VALUE_F_LFCN = re.compile(r'\d{2,4}[+]$')
REGEXP_IS_ACTIVE = re.compile(r'\A(?![DXTQ])')

json_config_file = 'conf.json'
SOBRANO_LOC_DEFAULT = 'SOBRANO_V_STANOK'

CONF_DICT = {
    "MDB_PATH": r"",
    "SMB_USERNAME": "",
    "SMB_PASSWORD": ""
}


def get_config():
    if not os.path.exists(json_config_file):
        with open(json_config_file, 'w', encoding='utf8') as outfile:
            json.dump(CONF_DICT, outfile, ensure_ascii=False, indent=4)
    with open(json_config_file, 'r', encoding='utf8') as openfile:
        return json.load(openfile)


def extract_package(row):
    comment = row['Comment']
    try:
        pack = REGEXP_PACKAGE.search(comment).group(0)
        if pack[:1] == 'R':
            pack = pack[2:]
        elif pack[:1] == 'C':
            pack = pack[2:] + '_C'
        elif pack[:1] == 'L':
            if pack in packs_l:
                pack = packs_l[pack]
        elif pack[:1] == 'F':
            if pack in packs_f:
                pack = packs_f[pack]
        else:
            pack = ''
    except Exception:
        pack = ''
    return pack


def extract_value(row):
    comment = row['Comment']
    try:
        pack = REGEXP_PACKAGE.search(comment).group(0)
        if pack[:1] == 'R':
            val = extract_value_r(comment)
        elif pack[:1] == 'C':
            val = extract_value_c(comment)
        elif pack[:1] == 'L':
            val = extract_value_l(comment)
        elif pack[:1] == 'F':
            val = extract_value_f(comment)
        else:
            val = ''
    except Exception:
        val = ''
    return val


def extract_value_r(comment):
    try:
        val = REGEXP_VALUE_R.search(comment).group(0)
        val = val.split('-')[2]
        return val
    except Exception:
        return


def extract_value_f(comment):
    try:
        val = comment[2:]
        try:
            val = REGEXP_VALUE_F_LFCN.search(val).group(0)
        except Exception:
            pass
        return val
    except Exception as err:
        print(err)
        return


def extract_value_c(comment):
    try:
        val = REGEXP_VALUE_C.search(comment).group(0)
        val = val.split('-')[4]
        if 'uF' not in val:
            val = val.replace('u', 'uF')
        return val
    except Exception:
        return


def extract_value_l(comment):
    try:
        val = comment
        val = val.split('-')
        val_c = ''
        vals = ['n', 'nH', 'u', 'uH']
        for i in val:
            for j in vals:
                if j in i:
                    val_c = i
        if 'nH' not in val_c:
            val_c = val_c.replace('n', 'nH')
        if 'uH' not in val_c:
            val_c = val_c.replace('u', 'uH')
        return val_c
    except Exception:
        return


def check_trans(txt):
    if not txt.isascii():
        return "!!!"


class GenComp:
    def __init__(self, encoding='utf8',
                 sobrano_loc=SOBRANO_LOC_DEFAULT, include_active=True, out_folder='READY'):
        config = get_config()
        self.mdb_path = config["MDB_PATH"]
        self.smb_username = config['SMB_USERNAME']
        self.smb_password = config['SMB_PASSWORD']
        self.encoding = encoding
        self.sobrano_loc = sobrano_loc
        self.include_active = include_active
        self.translit = []
        self.last_error = None
        self.library = None
        self.library_sobrano = None
        self.out_text = ''
        self.out_folder = out_folder

    def trans(self, txt):
        if not txt.isascii():
            self.translit.append(f'        {txt}')
            return translit(txt, reversed=True)
        else:
            return txt

    def get_library(self):
        try:
            register_session("smtdev", username=self.smb_username, password=self.smb_password)
            driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
            cnxn = pyodbc.connect(f'Driver={driver};DBQ={self.mdb_path}')
            self.library = pd.read_sql("SELECT CarrierId, ComponentName, Location FROM CarrierTable", cnxn)
            self.library = self.library[['CarrierId', 'ComponentName', 'Location']]
            return True
        except Exception as e:
            self.last_error = f'Не удалось подключиться к БД SMT\n{e}'
            print('lol')
            return False

    def filter_library(self):
        library = self.library
        library_sobrano = library[library['Location'] == self.sobrano_loc].reset_index(drop=True)
        library_sobrano['CarrierId'] = library_sobrano['CarrierId'].astype('str').str.zfill(6)
        library_sobrano.rename(columns={"ComponentName": "Comment"}, inplace=True)
        self.library_sobrano = library_sobrano.copy()

    def augment_library(self):
        library_sobrano = self.library_sobrano.copy()
        library_sobrano['Translit'] = library_sobrano['Comment'].apply(check_trans)
        library_sobrano['Comment'] = library_sobrano['Comment'].apply(self.trans)
        self.out_text += '    Содержат не латинские буквы:\n'
        self.out_text += "\n".join(list(set(self.translit)))
        self.translit = ''
        library_sobrano['Comment'] = library_sobrano['Comment'].str.replace(' ', '-')
        library_sobrano['package'] = library_sobrano.apply(extract_package, axis=1)
        library_sobrano['value'] = library_sobrano.apply(extract_value, axis=1)
        library_sobrano['CarrierId'] = 'R' + library_sobrano['CarrierId']
        library_sobrano.drop(columns=['Location'], inplace=True)
        if not self.include_active:
            library_sobrano = library_sobrano[library_sobrano.Comment.str.match(REGEXP_IS_ACTIVE)]
        library_sobrano = library_sobrano[['Comment', 'CarrierId', 'package', 'value', 'Translit']]
        library_sobrano['tip_lenty'] = ''
        library_sobrano.loc[library_sobrano.package.isin(['0603_C', '0603']), 'tip_lenty'] = "Tape08-4 white"
        library_sobrano.loc[library_sobrano.package.isin(['0402_C', '0402']), 'tip_lenty'] = "Tape08-2 white"
        library_sobrano = library_sobrano[library_sobrano['value'] != 'NM'].reset_index(drop=True)
        self.library_sobrano = library_sobrano.copy()

    def export_to_csv(self):
        try:
            if not exists(self.out_folder):
                os.mkdir(realpath(self.out_folder))
            self.library_sobrano.to_csv(f'{self.out_folder}/COMPONENT_BASE.csv', sep=';', index=False, header=True,
                                        encoding=self.encoding)
            return True
        except Exception as e:
            self.last_error = f'Ошибка сохранения\n{e}'
            return False

    def process(self, open_when_done=True):
        self.out_text = ''
        if not self.get_library():
            return False
        self.filter_library()
        self.augment_library()
        if not self.export_to_csv():
            return False
        if open_when_done:
            os.startfile(realpath(self.out_folder))
        return True
