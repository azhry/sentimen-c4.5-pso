# test command $: pytest -s -v

import sys, os
cwd = os.getcwd().split("\\")
sys.path.append(".." if cwd[-1] == "tests" else "tests/..")

from boundaries.AppWindow import AppWindow
from libs.DataImporter import DataImporter
from libs.Preprocessor import Preprocessor
from PyQt5.QtCore import qWarning, Qt
from PyQt5.QtWidgets import QMessageBox
from helpers.Path import relative_path
from core.Connection import Connection

def test_importCorrectExcelFile(qtbot):
	"""
	UC-2-01

	Memasukkan berkas berekstensi .xlsx yang memiliki
	kolom review dan label
	"""
	testID = "UC-2-01"
	testName = "Memasukkan berkas berekstensi .xlsx yang memiliki kolom review dan label"
	print("\n" + testID + "\n" + testName)

	window = AppWindow()
	window.show()
	qtbot.addWidget(window)
	qtbot.waitForWindowShown(window)
	filepath = "G:/Kuliah/Skripsi/Program/data/dummy_test.xlsx"
	importer = DataImporter(filepath)
	window.data = importer.get_data()
	window.renderTable(window.data)

	assert window.tableWidget.rowCount() == 4

	assert window.tableWidget.item(0, 0).text() == "Ojek online mudah dijangkau dan dapat dipesan dengan aplikasi"
	assert window.tableWidget.item(1, 0).text() == "Harga yang disediakan ojek online sangat terjangkau"
	assert window.tableWidget.item(2, 0).text() == "Jasa ojek online tidak boleh melanggar undang-undang"
	assert window.tableWidget.item(3, 0).text() == "Bisnis transportasi roda dua seperti ojek online sudah ada di beberapa negara"

	assert window.tableWidget.item(0, 1).text() == "Berdampak positif"
	assert window.tableWidget.item(1, 1).text() == "Berdampak positif"
	assert window.tableWidget.item(2, 1).text() == "Berdampak negatif"
	assert window.tableWidget.item(3, 1).text() == "Netral"

	print(f"{testID} passed")


def test_importExcelWithoutLabelColumn(qtbot):
	"""
	UC-2-02

	Memasukkan berkas berekstensi .xlsx yang memiliki
	kolom review tapi tidak memiliki kolom label
	"""
	testID = "UC-2-02"
	testName = "Memasukkan berkas berekstensi .xlsx yang memiliki kolom review tapi tidak memiliki kolom label"
	print("\n" + testID + "\n" + testName)

	window = AppWindow()
	window.show()
	qtbot.addWidget(window)
	qtbot.waitForWindowShown(window)
	filepath = "G:/Kuliah/Skripsi/Program/data/dummy_without_label_test.xlsx"
	importer = DataImporter(filepath)
	window.data = importer.get_data()
	window.renderTable(window.data)
	window.msg.done(1)
	assert window.msg is not None
	assert window.msg.windowTitle() == "Warning"
	assert window.msg.text() == "File tidak memiliki kolom Review dan Label"

	print(f"{testID} passed")


def test_importExceptExcelFile(qtbot):
	"""
	UC-2-03

	Memasukkan berkas berekstensi selain .xlsx
	"""
	testID = "UC-2-03"
	testName = "Memasukkan berkas berekstensi selain .xlsx"
	print("\n" + testID + "\n" + testName)

	window = AppWindow()
	window.show()
	qtbot.addWidget(window)
	qtbot.waitForWindowShown(window)
	filepath = "G:/Kuliah/Skripsi/Program/data/WordList.txt"
	importer = DataImporter(filepath)
	window.data = importer.get_data()
	window.renderTable(window.data)
	window.msg.done(1)

	assert window.msg is not None
	assert window.msg.windowTitle() == "Warning"
	assert window.msg.text() == "File tidak memiliki kolom Review dan Label"

	print(f"{testID} passed")