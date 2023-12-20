import sys
import chardet
from pnpproc import PnpConverter
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSettings, Qt
from main_widget import Ui_Form
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.setWindowTitle("My App")
        self.ui.setupUi(self)
        self.ui.pushButton_select_file.clicked.connect(self.choose_file)
        self.filenames = None
        self.setWindowIcon(QIcon(resource_path('icon.ico')))
        self.ui.listWidget_files.addItem('<< Файлы не выбраны >>')
        self.ui.textEdit_output.append('Готов к работе')
        self.ui.pushButton_process.clicked.connect(self.process_files)
        self.ui.pushButton_process.setDisabled(True)
        self.settings = QSettings("SLG", "PNP")
        # self.dropEvent(True)
        self.load_settings()

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)

    def save_settings(self):
        self.settings.setValue("user/open_when_done", self.ui.checkBox_open_folder.checkState())

    def load_settings(self):
        if 'user' in self.settings.childGroups():
            val = self.settings.value('user/open_when_done')
            self.ui.checkBox_open_folder.setCheckState(val)

    def process_files(self):
        self.ui.textEdit_output.setText('Начало обработки...')
        statuses = []
        for file in self.filenames:
            with open(file, "rb") as fi:
                pnp_converter.encoding = chardet.detect(fi.read())['encoding']
            status = pnp_converter.convert(file, open_when_done=self.ui.checkBox_open_folder.checkState() == Qt.Checked)
            statuses.append(status)
            self.ui.textEdit_output.append(pnp_converter.out_text)
            if not status:
                self.ui.textEdit_output.append(f'   Ошибка: {pnp_converter.last_error}')
        if all(statuses):
            self.ui.textEdit_output.append('\nГотово')
        else:
            self.ui.textEdit_output.append('\nГотово, есть ошибки')

    def choose_file(self):
        print('start')
        dg = QFileDialog.getOpenFileNames(self,
                                          caption='Выберите файл PnP',
                                          dir='C:\\',
                                          filter="Файлы PnP (*.txt *.csv *.tsv);;Любые файлы (*)"
                                          )[0]
        self.ui.listWidget_files.clear()
        if dg:
            self.filenames = dg
            names = [x.split('/')[-1] for x in dg]
            self.ui.listWidget_files.addItems(names)
            self.ui.pushButton_process.setDisabled(False)
            return
        self.filenames = None
        self.ui.listWidget_files.addItem('<< Файлы не выбранны >>')
        self.ui.pushButton_process.setDisabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pnp_converter = PnpConverter('/test_ready')
    pnp_converter.update_folder()

    window = MainWindow()
    window.show()

    app.exec()
