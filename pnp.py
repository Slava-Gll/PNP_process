import sys
from pnpproc import PnpConverter
from compgen import GenComp
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QInputDialog, QLineEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSettings, Qt
from main_widget import Ui_Form
import os
from io import StringIO


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
        self.ui.textEdit_output_comp.append('Готов к работе')
        self.ui.pushButton_process.clicked.connect(self.process_files)
        self.ui.pushButton_process.setDisabled(True)
        self.ui.pushButton_generate_components.clicked.connect(self.generate_comp)
        self.ui.pushButton_debug.clicked.connect(self.open_debug)
        self.settings = QSettings("SLG", "PNP")
        # self.dropEvent(True)
        self.load_settings()
        self.ui.tabWidget.setStyleSheet(
            "QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")
        self.ui.tabWidget.setTabEnabled(2, False)
        self.ui.tabWidget.setCurrentIndex(0)
        sys.stdout = self.buf_stdout = StringIO()
        sys.stderr = self.buf_stderr = StringIO()

    def open_debug(self):
        self.ui.tabWidget.setTabEnabled(2, True)
        self.ui.tabWidget.setCurrentIndex(2)

        self.ui.textEdit_stdout.setText(self.buf_stdout.getvalue())
        self.ui.textEdit_stderr.setText(self.buf_stderr.getvalue())
    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)

    def save_settings(self):
        self.settings.setValue("user/open_when_done", self.ui.checkBox_open_folder.checkState())
        self.settings.setValue("user/out_path", self.out_folder)

    def load_settings(self):
        if 'user' in self.settings.childGroups():
            val = self.settings.value('user/open_when_done')
            self.ui.checkBox_open_folder.setCheckState(val)
            self.out_folder = self.settings.value('user/out_path')
        else:
            self.out_folder = '%UserProfile%\\Desktop\\'

    def process_files(self):
        self.ui.textEdit_output.setText('Начало обработки...')
        statuses = []
        for file in self.filenames:
            status = pnp_converter.convert(file, open_when_done=self.ui.checkBox_open_folder.checkState() == Qt.Checked)
            if not status and pnp_converter.last_error_comment:
                text, ok = QInputDialog.getText(self, "Столбец Comment не найден",
                                                f"Переопределить название столбца Comment\nпервая строчка:\n{pnp_converter.first_line}")
                if ok and text:
                    status = pnp_converter.convert(file,
                                                   open_when_done=self.ui.checkBox_open_folder.checkState() == Qt.Checked,
                                                   csv_comment_field=text)
            statuses.append(status)
            self.ui.textEdit_output.append(pnp_converter.out_text)
            if not status:
                self.ui.textEdit_output.append(f'   Ошибка: {pnp_converter.last_error}')

        if all(statuses):
            self.ui.textEdit_output.append('\nГотово')
        else:
            self.ui.textEdit_output.append('\nГотово, есть ошибки')

    def choose_file(self):
        dg = QFileDialog.getOpenFileNames(self,
                                          caption='Выберите файл PnP',
                                          dir=self.out_folder,
                                          filter="Файлы PnP (*.txt *.csv *.tsv);;Любые файлы (*)"
                                          )[0]
        self.ui.listWidget_files.clear()
        if dg:
            self.filenames = dg
            self.out_folder = '\\'.join(dg[0].split('/')[:-1])
            print(self.out_folder)
            names = [x.split('/')[-1] for x in dg]
            self.ui.listWidget_files.addItems(names)
            self.ui.pushButton_process.setDisabled(False)
            return
        self.filenames = None
        self.ui.listWidget_files.addItem('<< Файлы не выбранны >>')
        self.ui.pushButton_process.setDisabled(True)

    def generate_comp(self):
        self.ui.textEdit_output_comp.setText('Начало обработки...')
        status = component_generator.process(open_when_done=self.ui.checkBox_open_folder.checkState() == Qt.Checked)
        self.ui.textEdit_output_comp.append(component_generator.out_text)
        if status:
            self.ui.textEdit_output_comp.append('\nГотово')
        else:
            self.ui.textEdit_output_comp.append(component_generator.last_error)
            self.ui.textEdit_output_comp.append('\nГотово, есть ошибки')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pnp_converter = PnpConverter(out_folder='/ready')
    pnp_converter.update_folder()
    component_generator = GenComp(out_folder='/ready')
    window = MainWindow()
    window.show()

    app.exec()
