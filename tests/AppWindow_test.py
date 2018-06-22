import sys 
sys.path.append('..')

from boundaries.AppWindow import AppWindow
from libs.DataImporter import DataImporter
from PyQt5.QtCore import qWarning, Qt
from PyQt5.QtWidgets import QMessageBox
from time import sleep

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


# def test_importExcelWithNeitherColumn(qtbot):
# 	"""
# 	UC-1-05

# 	Memasukkan berkas berekstensi .xlsx yang tidak memiliki
# 	kolom review maupun label
# 	"""
# 	window = AppWindow()

# def test_importExceptExcelFile(qtbot, monkeypatch):
# 	"""
# 	UC-1-03

# 	Memasukkan berkas berekstensi selain .xlsx
# 	"""
# 	window = AppWindow()
# 	window.show()
# 	qtbot.addWidget(window)
# 	qtbot.waitForWindowShown(window)
# 	filepath = "G:/Kuliah/Skripsi/Program/data/WordList.txt"
# 	importer = DataImporter(filepath)
# 	data = importer.get_data()
# 	window.renderTable(data)
# 	monkeypatch.setattr(QMessageBox, "warning", lambda *args: QMessageBox.Ok)
# 	window.query()
