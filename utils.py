import traceback
from PyQt.import_module import *
import os


def dumpException(e):
    print('Exception: %s' % e)
    traceback.print_tb(e.__traceback__)


def loadStylesheets(filename):
    '''
    :param filename:
    :return:
    '''
    file = QFile(filename)
    file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = file.readAll()
    QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
