import sys, os
cwd = os.getcwd().split("\\")
sys.path.append(".." if cwd[-1] == "tests" else "tests/..")

from boundaries.AppWindow import AppWindow
from libs.DataImporter import DataImporter
from PyQt5.QtCore import qWarning, Qt
from PyQt5.QtWidgets import QMessageBox

# def test_importCorrectExcelFile(qtbot):
#     """
#     UC-2-01

#     Memasukkan berkas berekstensi .xlsx yang memiliki
#     kolom review dan label
#     """
#     testID = "UC-1-01"
#     testName = "Memasukkan berkas berekstensi .xlsx yang memiliki kolom review dan label"
#     print("\n" + testID + "\n" + testName)



#     print(f"{testID} passed")