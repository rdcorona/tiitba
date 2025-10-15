#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: rdcorona
# @Date:   2020-01-15 16:56:16
# @Last Modified by:   rdcorona
# @Last Modified time: 2021-12-14 10:20:58

"""
GUI to vectorize seismogramas on raster images of historic seismograms and apply main corrections.
The code requires PyQt5, OpenCV, Obspy and Matplotlib dependencies to run properly,
it is suggest to install it previously on python environment.
Or execute the install.sh file

"""
import os
import sys
from MainModules import CentralWidget
import matplotlib.pyplot as plt
try:
	from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QDesktopWidget
	from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QStackedLayout
	from PyQt5.QtGui import QIcon
	import cv2
except ImportError as lib:
	from tkinter import messagebox
	messagebox.showinfo(message='{:} {:}'.format(lib,
						'\nNecessary dependencies to run TIITBA\n' +
						'PyQt5, OpenCV, Obspy, Matplotlib'))
	sys.exit(1)
################################################################################
nap = QApplication(sys.argv)
screen = nap.primaryScreen()
size = screen.availableGeometry()
width, height = size.width(), size.height()
Guiwidth = int(width * 0.7)
guiheigth = int(height * 0.85)
path = os.getcwd()
#########################################################################################
############################ M A I N  I N T E R F A C E #################################
# Define main interface

class InterfazMain(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setFixedSize(Guiwidth, guiheigth)
		self.inicioIG()
		pass

	def inicioIG(self):
		global name, img
		os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
	# Sets Main Window
		DSpath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
					os.pardir))
		self.setWindowTitle('TIITBA V1.2.0')
		self.setWindowIcon(QIcon(f"{DSpath}/Images/logo.png"))
		self.statusBar().showMessage('TIITBA V1.0.2')
	# Central Widget from Class QWidget
		self.cWidget = CentralWidget()
		self.cWidget.move(0,int(height*0.01))
		self.layoutWidgets = QStackedLayout()
		self.setCentralWidget(self.cWidget)
		self.layoutWidgets.addWidget(self.cWidget)

	#####################################################################################
	#  Menu bar
		menubar = QMenuBar(self)
		menubar.setNativeMenuBar(False)
	## Menu file
		# Menu actions
		exitAct = QAction('Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Close Main interface')
		exitAct.triggered.connect(self.close)

		imagee = QAction('Load HR &Seismogram.',self)
		imagee.setShortcut('Ctrl+S')
		imagee.setStatusTip('Load HR seismogram')
		imagee.triggered.connect(self.cWidget.load_image)

		archivo = QAction('Load &Data file',self)
		archivo.setShortcut('Ctrl+D')
		archivo.setStatusTip('Load Data file')
		archivo.triggered.connect(self.cWidget.getdatafile)

		restart = QAction('&Restart Interface', self)
		restart.setShortcut('Ctrl+R')
		restart.setStatusTip('Restart Interface')
		restart.triggered.connect(self.cWidget.setRestart)

		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(imagee)
		fileMenu.addAction(archivo)
		fileMenu.addAction(restart)
		fileMenu.addSeparator()
		fileMenu.addAction(exitAct)
	##### Save menu
		saveImg = QAction('Save &Image', self)
		saveImg.setShortcut('Ctrl+I')
		saveImg.setStatusTip('Save a digital processed image')
		saveImg.triggered.connect(self.cWidget.setSaveImg)

		saveDigi = QAction(' Save vectorized Data', self)
		saveDigi.triggered.connect(self.cWidget.saveData)

		saveCorrected = QAction('Save Corrected data', self)
		saveCorrected.triggered.connect(self.cWidget.saveCorrectedData)

		saveInfo = QAction('Save Information Panel text', self)
		saveInfo.setStatusTip('Save all panel information in a plain text file')
		saveInfo.triggered.connect(self.saveInfoText)

		fileMenu1 = menubar.addMenu('&Save')
		fileMenu1.addAction(saveImg)
		fileMenu1.addAction(saveDigi)
		fileMenu1.addAction(saveCorrected)
		fileMenu1.addAction(saveInfo)
	##### Menu Information
		infoBox = QAction('Information and Contact', self)
		infoBox.setStatusTip('GUI information')
		infoBox.triggered.connect(self.setInformation)
		fileMenu2 = menubar.addMenu('&Information')
		fileMenu2.addAction(infoBox)
		self.setMenuBar(menubar)
		self.show()
#########################################################################################

	def setInformation(self):
		QMessageBox.information(self,'TIITBA',
		f"Tiitba it's a graphical user interface (GUI) developed to ,\nvectorize, analyses and correct old analog seismograms on raster images.\nAlso, this GUI applies basic corrections to the vectorized raw data.\n\nThe use of this GUI it's under the user risk.\nPlease cite Tiitba if it is used to obtain timeseries or any result for your work as: \n Corona- Fernández, R.D. & Santoyo, M.Á. (2022) Re- examination of the 1928 Parral, Mexico earthquake (M6.3) using a new multiplatform graphical vectorization and correction software for legacy seismic data. Geoscience Data Journal, 00, 1-15. Available from: https://doi.org/10.1002/gdj3.159.\nFor more information or software issues with Tiitba contact the authors by email:\nrdcorona@igeofisica.unam.mx / santoyo@igeofisica.unam.mx")

	def saveInfoText(self):
		outname, _ = QFileDialog.getSaveFileName(self, 'Save ASCII file',
							'RecordInformationText.txt',
							"Text Files (*.txt *.dat);; All Files (*)")
		try:
			with open(outname,'w') as f:
				f.write(str(self.cWidget.text.toPlainText()))
		except:
			pass
# Center main window

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topCenter())

	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'TIITBA V1.2.0',
							'Close Tiitba-GUI?',
					QMessageBox.No | QMessageBox.Yes)
		if reply == QMessageBox.Yes:
			event.accept()
			cv2.destroyAllWindows()
			plt.close('all')
		else:
			event.ignore()

	# def quitApp(self):
	# 	QCoreApplication.instance().quit()
#########################################################################################


if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	ex = InterfazMain()
	ex.show()
	sys.exit(app.exec_())
