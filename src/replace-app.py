#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import re
import codecs
import chardet

from PySide import QtCore, QtGui
from PySide.QtUiTools import QUiLoader

from mainUI import Ui_Form

class mainUI(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        default_dir = os.getcwd()
        self.ui.lineEdit_choose_directory.setText(default_dir)
        self.ui.toolButton_choose_directory.clicked.connect(self.toolButton_choose_directory)
        self.ui.radioButton_search.setChecked(True)
        self.ui.pushButton_execute.clicked.connect(self.pushButton_execute)
        self.ui.listWidget_show_dst_files.setSortingEnabled(True)
        self.ui.label_notification.setStyleSheet("QLabel{color: black;}")

        self.ui.lineEdit_choose_directory.editingFinished.connect(self.handle_lineEdit_choose_directory)
        self.ui.lineEdit_extension.textEdited.connect(self.handle_lineEdit_extension)
        self.ui.lineEdit_suffix.textEdited.connect(self.handle_lineEdit_suffix)
        self.ui.lineEdit_search_word.textEdited.connect(self.handle_lineEdit_search_word)
        self.ui.lineEdit_replace_word.textEdited.connect(self.handle_lineEdit_replace_word)

    def handle_lineEdit_choose_directory(self):
        if self.ui.lineEdit_choose_directory.text() == "":
            self.ui.lineEdit_choose_directory.setStyleSheet("QLineEdit{border: 2px solid #e91e63; border-radius: 4px;}")
        else:
            self.ui.lineEdit_choose_directory.setStyleSheet("QLineEdit{border: 2px solid #8bc34a; border-radius: 4px;}")

    def handle_lineEdit_extension(self):
        if self.ui.lineEdit_extension.text() == "":
            self.ui.lineEdit_extension.setStyleSheet("QLineEdit{border: 2px solid #e91e63; border-radius: 4px;}")
        else:
            self.ui.lineEdit_extension.setStyleSheet("QLineEdit{border: 2px solid #8bc34a; border-radius: 4px;}")

    def handle_lineEdit_suffix(self):
        if self.ui.lineEdit_suffix.text() == "":
            self.ui.lineEdit_suffix.setStyleSheet("QLineEdit{border: 2px solid #e91e63; border-radius: 4px;}")
        else:
            self.ui.lineEdit_suffix.setStyleSheet("QLineEdit{border: 2px solid #8bc34a; border-radius: 4px;}")

    def handle_lineEdit_search_word(self):
        pass
        if self.ui.lineEdit_search_word.text() == "":
            self.ui.lineEdit_search_word.setStyleSheet("QLineEdit{border: 2px solid #e91e63; border-radius: 4px;}")
        else:
            self.ui.lineEdit_search_word.setStyleSheet("QLineEdit{border: 2px solid #8bc34a; border-radius: 4px;}")

    def handle_lineEdit_replace_word(self):
        if self.ui.lineEdit_replace_word.text() == "":
            self.ui.lineEdit_replace_word.setStyleSheet("QLineEdit{border: 2px solid #e91e63; border-radius: 4px;}")
        else:
            self.ui.lineEdit_replace_word.setStyleSheet("QLineEdit{border: 2px solid #8bc34a; border-radius: 4px;}")

    def toolButton_choose_directory(self,*args):
        directory = self.fileDialogMod()
        self.ui.lineEdit_choose_directory.setText(directory)

    def fileDialogMod(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        directory = dialog.getExistingDirectory(self, "対象フォルダを選択", os.path.curdir)
        return directory

    def pushButton_execute(self,*args):
        if self.ui.radioButton_regex.isChecked():
            isRegularExpression = True
        else:
            isRegularExpression = False

        if self.ui.lineEdit_suffix.text() == "":
            self.ui.label_notification.setStyleSheet("QLabel{color: #e91e63;}")
            self.ui.label_notification.setText("接尾辞が入力されていません。")
        else:
            dst_directory_suffix = self.ui.lineEdit_suffix.text()

        if self.ui.lineEdit_extension.text() == "":
            self.ui.label_notification.setStyleSheet("QLabel{color: #e91e63;}")
            self.ui.label_notification.setText("拡張子が入力されていません。")
        else:
            target_extension = self.ui.lineEdit_extension.text()

        if self.ui.lineEdit_replace_word.text() == "":
            self.ui.label_notification.setStyleSheet("QLabel{color: #e91e63;}")
            self.ui.label_notification.setText("置換語句が入力されていません。")
        else:
            replace_word = self.ui.lineEdit_replace_word.text()

        if self.ui.lineEdit_search_word.text() == "":
            self.ui.label_notification.setStyleSheet("QLabel{color: #e91e63;}")
            self.ui.label_notification.setText("検索語句が入力されていません。")
        else:
            search_word = self.ui.lineEdit_search_word.text()

        if self.ui.lineEdit_choose_directory.text() == "":
            self.ui.label_notification.setStyleSheet("QLabel{color: #e91e63;}")
            self.ui.label_notification.setText("対象フォルダが選択されていません。")
        elif not os.path.exists(self.ui.lineEdit_choose_directory.text()):
            self.ui.label_notification.setText("対象フォルダが存在していません。")
        else:
            src_directory = self.ui.lineEdit_choose_directory.text()

        if not self.ui.lineEdit_choose_directory.text() == "" \
        and os.path.exists(self.ui.lineEdit_choose_directory.text()) \
        and not self.ui.lineEdit_extension.text() == "" \
        and not self.ui.lineEdit_suffix.text() == "" \
        and not self.ui.lineEdit_search_word.text() == "" \
        and not self.ui.lineEdit_replace_word.text() == "":
            self.replace_text(src_directory, target_extension, dst_directory_suffix, isRegularExpression, search_word,replace_word)

    def build_dir_list(self, directory):
        dir_list = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if not root in dir_list:
                    dir_list.append(root)
        return dir_list

    def build_file_list(self, directory, extension):
        target_extension = extension
        file_list = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                nam, ext = os.path.splitext(file)
                if ext.lower() == target_extension:
                    file = nam+ext
                    file_list.append(os.path.join(root, file))
        return file_list

    def create_dst_dir_list(self, directory, dir_list, suffix):
        src_directory = directory
        dst_directory_suffix = suffix
        src_dir_list = dir_list
        dst_dir_list = []
        for dir in src_dir_list:
            dir = dir.replace(src_directory, src_directory+dst_directory_suffix)
            dst_dir_list.append(dir)
        return dst_dir_list

    def create_dst_file_list(self, directory, file_list, suffix):
        src_directory = directory
        dst_directory_suffix = suffix
        src_file_list = file_list
        dst_file_list = []
        for file in src_file_list:
            file = file.replace(src_directory, src_directory+dst_directory_suffix)
            dst_file_list.append(file)
        return dst_file_list

    def make_directory_if_not_exists(self, dir_list):
        for dir in dir_list:
            if not os.path.exists(dir):
                os.makedirs(dir)

    def replace_text(self, directory, extension, suffix, regex, str1, str2):
        self.ui.listWidget_show_dst_files.clear()
        src_directory = directory
        target_extension = "."+extension
        dst_directory_suffix = suffix
        isRegularExpression = regex
        search_word = str1
        replace_word = str2
        src_dir_list = self.build_dir_list(src_directory)
        dst_dir_list = self.create_dst_dir_list(src_directory, src_dir_list, dst_directory_suffix)
        self.make_directory_if_not_exists(dst_dir_list)
        src_file_list = self.build_file_list(src_directory, target_extension)
        dst_file_list = self.create_dst_file_list(src_directory, src_file_list, dst_directory_suffix)
        file_dict = dict(zip(src_file_list, dst_file_list))
        progress = 0
        for file in src_file_list:
            encoding = chardet.detect(open(file, "rb").read())["encoding"]
            with codecs.open(file, "r", encoding) as src_file,\
            codecs.open(file_dict[file], "w", encoding) as dst_file:
                src_lines = src_file.readlines()
                dst_lines = []
                for line in src_lines:
                    if isRegularExpression:
                        line = re.sub(search_word, replace_word, line)
                    else:
                        line = line.replace(search_word, replace_word)
                    dst_lines.append(line)
                else:
                    dst_file.write("".join(dst_lines))
            progress += 1
            self.ui.listWidget_show_dst_files.addItem(os.path.basename(file))
            self.ui.progressBar.setValue(round(progress/len(src_file_list)*100))
        self.ui.label_notification.setStyleSheet("QLabel{color: #8bc34a;}")
        self.ui.label_notification.setText("テキスト置換が完了しました！")

def main():

    app = QtGui.QApplication(sys.argv)
    app.setStyle('cleanlooks')
    QtCore.QTextCodec.setCodecForCStrings( QtCore.QTextCodec.codecForLocale() )
    win = mainUI()
    win.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
    win.setFixedSize(600, 260)
    win.show()
    sys.exit(app.exec_())    

if __name__ == '__main__':
    
    main()