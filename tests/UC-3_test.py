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

def test_preprocessData(qtbot):
	"""
	UC-3-01

	Melakukan praproses setelah memasukkan berkas yang sesuai
	"""
	testID = "UC-3-01"
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

	preprocessor = Preprocessor()

	assert preprocessor.preprocess(window.data["Review"][0]) == ["ojek", "online", "mudah", "jangkau", "pes", "aplikasi"]
	assert preprocessor.preprocess(window.data["Review"][1]) == ["harga", "sedia", "ojek", "online", "sangat", "jangkau"]
	assert preprocessor.preprocess(window.data["Review"][2]) == ["jasa", "ojek", "online", "langgar", "undang"]
	assert preprocessor.preprocess(window.data["Review"][3]) == ["bisnis", "transportasi", "roda", "ojek", "online", "beberapa", "negara"]

	print(f"{testID} passed")


def test_preprocessInapproriateData(qtbot):
	"""
	UC-3-02

	Melakukan praproses setelah memasukkan berkas yang tidak sesuai
	"""
	testID = "UC-3-02"
	testName = "Melakukan praproses setelah memasukkan berkas yang tidak sesuai"
	print("\n" + testID + "\n" + testName)

	window = AppWindow()
	window.show()
	qtbot.addWidget(window)
	qtbot.waitForWindowShown(window)
	filepath = "G:/Kuliah/Skripsi/Program/data/WordList.txt"
	importer = DataImporter(filepath)
	window.data = importer.get_data()
	window.preprocess_data()
	window.msg.done(1)

	assert window.msg is not None
	assert window.msg.windowTitle() == "Warning"
	assert window.msg.text() == "Anda harus mengimpor data terlebih dahulu"
	assert window.data is None

	print(f"{testID} passed")