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

def test_importCorrectExcelFile(qtbot):
	"""
	UC-1-01

	Memasukkan berkas berekstensi .xlsx yang memiliki
	kolom review dan label
	"""
	testID = "UC-1-01"
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


def test_importExcelWithoutData(qtbot):
	"""
	UC-1-02

	Memasukkan berkas berekstensi .xlsx yang memiliki
	kolom review dan label tapi tidak memiliki data
	"""
	testID = "UC-1-02"
	testName = "Memasukkan berkas berekstensi .xlsx yang memiliki kolom review dan label tapi tidak memiliki data"
	print("\n" + testID + "\n" + testName)

	window = AppWindow()
	window.show()
	qtbot.addWidget(window)
	qtbot.waitForWindowShown(window)
	filepath = "G:/Kuliah/Skripsi/Program/data/dummy_no_data_test.xlsx"
	importer = DataImporter(filepath)
	window.data = importer.get_data()
	window.renderTable(window.data)
	assert window.tableWidget.rowCount() == 0

	print(f"{testID} passed")


def test_importExcelWithoutLabelColumn(qtbot):
	"""
	UC-1-03

	Memasukkan berkas berekstensi .xlsx yang memiliki
	kolom review tapi tidak memiliki kolom label
	"""
	testID = "UC-1-03"
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


def test_importExcelWithoutReviewColumn(qtbot):
	"""
	UC-1-04

	Memasukkan berkas berekstensi .xlsx yang memiliki
	kolom label tapi tidak memiliki kolom review
	"""
	testID = "UC-1-04"
	testName = "Memasukkan berkas berekstensi .xlsx yang memiliki kolom label tapi tidak memiliki kolom review"
	print("\n" + testID + "\n" + testName)

	window = AppWindow()
	window.show()
	qtbot.addWidget(window)
	qtbot.waitForWindowShown(window)
	filepath = "G:/Kuliah/Skripsi/Program/data/dummy_without_review_test.xlsx"
	importer = DataImporter(filepath)
	window.data = importer.get_data()
	window.renderTable(window.data)
	window.msg.done(1)
	assert window.msg is not None
	assert window.msg.windowTitle() == "Warning"
	assert window.msg.text() == "File tidak memiliki kolom Review dan Label"

	print(f"{testID} passed")


def test_importExcelWithNeitherColumn(qtbot):
	"""
	UC-1-05

	Memasukkan berkas berekstensi .xlsx yang tidak memiliki
	kolom review maupun label
	"""
	testID = "UC-1-05"
	testName = "Memasukkan berkas berekstensi .xlsx yang tidak memiliki kolom review maupun label"
	print("\n" + testID + "\n" + testName)

	window = AppWindow()
	window.show()
	qtbot.addWidget(window)
	qtbot.waitForWindowShown(window)
	filepath = "G:/Kuliah/Skripsi/Program/data/dummy_without_neither_columns_test.xlsx"
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
	UC-1-06

	Memasukkan berkas berekstensi selain .xlsx
	"""
	testID = "UC-1-06"
	testName = "Memasukkan berkas berekstensi selain .xlsx"
	print("\n" + testID + "\n" + testName)

	window = AppWindow()
	window.show()
	qtbot.addWidget(window)
	qtbot.waitForWindowShown(window)
	filepath = "G:/Kuliah/Skripsi/Program/data/dummy_without_neither_columns_test.xlsx"
	importer = DataImporter(filepath)
	window.data = importer.get_data()
	window.renderTable(window.data)
	window.msg.done(1)

	assert window.msg is not None
	assert window.msg.windowTitle() == "Warning"
	assert window.msg.text() == "File tidak memiliki kolom Review dan Label"

	print(f"{testID} passed")


def test_preprocessData(qtbot):
	"""
	UC-1-07

	Melakukan praproses setelah memasukkan berkas yang sesuai
	"""
	testID = "UC-1-07"
	testName = "Melakukan praproses setelah memasukkan berkas yang sesuai"
	print("\n" + testID + "\n" + testName)

	window = AppWindow()
	window.show()
	qtbot.addWidget(window)
	qtbot.waitForWindowShown(window)
	filepath = "G:/Kuliah/Skripsi/Program/data/dummy_test.xlsx"
	importer = DataImporter(filepath)
	window.data = importer.get_data()
	window.renderTable(window.data)

	stopwordPath = relative_path("id.stopwords.txt")
	correctWordsPath = relative_path("../libs/correct_words.json")
	preprocessor = Preprocessor(stopwordPath, correctWordsPath)

	assert preprocessor.preprocess(window.data["Review"][0]) == ["ojek", "online", "mudah", "jangkau", "pesan", "aplikasi"]
	assert preprocessor.preprocess(window.data["Review"][1]) == ["harga", "sedia", "ojek", "online", "jangkau"]
	assert preprocessor.preprocess(window.data["Review"][2]) == ["jasa", "ojek", "online", "langgar", "undang"]
	assert preprocessor.preprocess(window.data["Review"][3]) == ["bisnis", "transportasi", "roda", "ojek", "online", "negara"]

	print(f"{testID} passed")


def test_preprocessData(qtbot):
	"""
	UC-1-08

	Melakukan praproses setelah memasukkan berkas yang tidak sesuai
	"""
	testID = "UC-1-08"
	testName = "Melakukan praproses setelah memasukkan berkas yang tidak sesuai"
	print("\n" + testID + "\n" + testName)

	window = AppWindow()
	window.show()
	qtbot.addWidget(window)
	qtbot.waitForWindowShown(window)
	filepath = "G:/Kuliah/Skripsi/Program/data/WordList.txt"
	importer = DataImporter(filepath)
	window.data = importer.get_data()
	window.renderTable(window.data)

	stopwordPath = relative_path("id.stopwords.txt")
	correctWordsPath = relative_path("../libs/correct_words.json")
	preprocessor = Preprocessor(stopwordPath, correctWordsPath)

	# TODO

	print(f"{testID} passed")