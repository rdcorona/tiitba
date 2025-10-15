#!/usr/bin/env python3
# -*- coding: utf-8 -*-# @Author: rdcorona
# @Date:   2020-01-15 16:56:16
# @Last Modified by:   rdcorona
# @Last Modified time: 2022-08-22 10:41:03
"""

Main Widget with Functions that
operate on the Main program of the TIITBA GUI

"""

import sys
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from AuxiliaryModules import tabWindows
try:
	from PyQt5.QtWidgets import QPushButton, QTextEdit,QCheckBox
	from PyQt5.QtWidgets import QVBoxLayout, QLabel, QApplication, QLineEdit
	from PyQt5.QtWidgets import QGroupBox, QFileDialog, QInputDialog
	from PyQt5.QtWidgets import QMessageBox, QGridLayout, QDialog, QSizePolicy
	from PyQt5.QtGui import QPixmap, QFont
	from PyQt5.QtCore import Qt
	from obspy.signal.detrend import polynomial
	from obspy.core import *
	import cv2
	from PIL import Image
	Image.MAX_IMAGE_PIXELS = 999999999
except ImportError as lib:
	from tkinter import messagebox
	messagebox.showinfo(message='{:} {:}'.format(lib,
						'\nNecessary libraries to run TIITBA-GUI:\n' +
						'PyQt5, OpenCV, Obspy, Matplotlib, Pillow'))
	sys.exit(1)
#########################################################################################
nap = QApplication(sys.argv)
screen = nap.primaryScreen()
size = screen.availableGeometry()
width, height = size.width(), size.height()
Guiwidth = int(width * 0.7)
height = height * 0.85
wd_head = size.height() * 0.035
wd_w = int(height - wd_head)
path = os.getcwd()
check = 0
################################  Central Widget  ####################################


class CentralWidget(QDialog):
	def __init__(self, parent=None):
		global Guiwidth, height
		super(CentralWidget, self).__init__(parent)
		self.setFixedSize(Guiwidth, wd_w)
		self.initCW()
		self._want_to_close = False

	def initCW(self):
		# GroupBox start
		self.header()
		self.makeInfoImage()
		self.makeLeftGroupBox()
		self.makeCentralGroupBox()
		self.makeRightGroupBox()
		self.makeDataPlot()
		self.makeDataimagee()
		self.record()
		self.creaExtraGruopBox()
		# Set Layouts
		self.mainLayout = QGridLayout()
		self.mainLayout.addWidget(self.label, 0, 0)
		self.mainLayout.addWidget(self.label1, 0, 3)
		self.mainLayout.addWidget(self.infoimage, 1, 0)
		self.mainLayout.addWidget(self.sisDate, 1, 1)
		self.mainLayout.addWidget(self.text, 1, 3)
		self.mainLayout.addWidget(self.LeftGroupBox, 2, 0)
		self.mainLayout.addWidget(self.CentralGroupBox, 2, 1)
		self.mainLayout.addWidget(self.RightGroupBox, 2, 2)
		self.mainLayout.addWidget(self.canvas, 2, 3)
		self.mainLayout.addWidget(self.toolbar, 3, 3)
		self.mainLayout.addWidget(self.extraGroupBox, 3, 2)
		self.setLayout(self.mainLayout)
		self.show()

	def closeEvent(self, evnt):
		if self._want_to_close:
			super(CentralWidget, self).closeEvent(evnt)
		else:
			evnt.ignore()
			self.setWindowState(Qt.WindowMinimized)
	####################################################################################

	def setRestart(self):
		# Interface reboot
		python = sys.executable
		os.execl(python, python, * sys.argv)

#########################################################################################
#   GUI logos ( Main interface)

	def header(self):
		# UNAM logo on the left
		DSpath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
					os.pardir))
		self.label = QLabel(self)
		self.pix = QPixmap(DSpath + '/Images/logo_unam.png')
		self.pix = self.pix.scaled(int(width * 0.11), int(height * 0.3), Qt.KeepAspectRatio)
		self.label.resize(int(width * 0.11), int(height * 0.377))
		self.label.setPixmap(self.pix)
		self.label.setAlignment(Qt.AlignBottom)
	# geophysics institute  logo at the right
		self.label1 = QLabel(self)
		self.pix1 = QPixmap(DSpath + '/Images/geofisica_logo.png')
		self.pixmap1 = self.pix1.scaled(int(width*0.1177),int(height*0.1),
						Qt.KeepAspectRatio,Qt.FastTransformation)
		self.label1.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
		self.label1.resize(int(width*0.1177), int(height*0.11))
		self.label1.setPixmap(self.pixmap1)
	# GUI Tittle
		self.lab = QLabel('<P> <FONT COLOR="#0D0B55">TIITBA - Historical Seismograms'
			'  Vectorization, Analysis, and Correction</FONT></P>', self)
		self.lab.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		myfont = QFont('Arial',int(width*0.015))
		self.lab.setFont(myfont)
		self.lab.move(int(width*0.20),int(height*0.03))
		self.lab.setWordWrap(True)
		self.lab.resize(int(width*0.3),int(height*0.2))
#########################################################################################
	# Image information group

	def makeInfoImage(self):
		self.infoimage = QGroupBox('', self)
		# group box  Widgets
		self.pixels = QLabel()
		self.pixlab = QLabel(f"Raster Image Pixels Per Inch (PPI):")
		self.pixlab.setWordWrap(True)
		self.pixlab.setFont(QFont('Arial', int(width*0.008)))
		self.pixlab.setAlignment(Qt.AlignVCenter)
		self.pixels.setAlignment(Qt.AlignVCenter)
		self.pixels.setFont(QFont('Arial', int(width*0.008)))
		# Widgets on group box
		self.infbox = QVBoxLayout(self)
		self.infbox.addWidget(self.pixlab)
		self.infbox.addWidget(self.pixels)
		# self.infbox.addWidget(self.okbtn)
		self.infoimage.setLayout(self.infbox)
		self.infoimage.setMaximumSize(int(Guiwidth/6),int(height*0.078))
	#####################################################################################
	# For date of the record. Name of the selected image file or text file

	def record(self):
		self.sisDate = QLabel()
		self.sisDate.setAlignment(Qt.AlignVCenter)
		self.sisDate.setFont(QFont('Arial', int(width*0.008)))
		self.infoimage.setMaximumSize(int(Guiwidth/6), int(height*0.192))
#########################################################################################
# Left GroupBox

	def makeLeftGroupBox(self):
		self.LeftGroupBox = QGroupBox('Digital Image Processing', self)
		self.LeftGroupBox.setStyleSheet('QGroupBox:title {'
					'subcontrol-origin: margin;'
					'subcontrol-position: top right;'
					'padding-left: 5px;'
					'padding-right: 5px; }')
		self.LeftGroupBox.setStyleSheet('QGroupBox {'
					'font: bold;'
					'border: 1px solid silver;'
					'border-radius: 6px;'
					'margin-top: 6px; }')
		# Buttons
		self.btnLoad = QPushButton('Load &Image', self)
		self.btnLoad.resize(self.btnLoad.sizeHint())
		self.btnLoad.setStatusTip('Load Seismogram image')
		self.btnLoad.clicked.connect(self.load_image)

		self.btnRotate = QPushButton('Rotate', self) 
		self.btnRotate.resize(self.btnRotate.sizeHint())
		self.btnRotate.setStatusTip('Rotate Image 90° clockwise')
		self.btnRotate.setEnabled(False)
		self.btnRotate.clicked.connect(self.setRotate)

		self.btnContrast = QPushButton('Increase &Contrast', self)
		self.btnContrast.resize(self.btnContrast.sizeHint())
		self.btnContrast.setStatusTip('Increase the contrast of a grayscale image')
		self.btnContrast.setEnabled(False)
		self.btnContrast.clicked.connect(self.setContrast)

		self.btnBinary = QPushButton('Convert into &Binary', self)
		self.btnBinary.resize(self.btnBinary.sizeHint())
		self.btnBinary.setStatusTip('Convert the image into a binary format')
		self.btnBinary.setEnabled(False)
		self.btnBinary.clicked.connect(self.setBinary)

		self.btnTrim = QPushButton('&Trim Image', self)
		self.btnTrim.resize(self.btnTrim.sizeHint())
		self.btnTrim.setStatusTip('Crops the raster image in a user-defined area')
		self.btnTrim.setEnabled(False)
		self.btnTrim.clicked.connect(self.TrimSeismogram)
	# Vertical Layout for image processing
		self.vbox = QVBoxLayout()
		self.vbox.addWidget(self.btnLoad)
		self.vbox.addWidget(self.btnRotate)
		self.vbox.addWidget(self.btnTrim)
		self.vbox.addWidget(self.btnContrast)
		self.vbox.addWidget(self.btnBinary)

		self.LeftGroupBox.setLayout(self.vbox)
		self.LeftGroupBox.setMaximumSize(int(Guiwidth/6),int(height*0.48))
#########################################################################################
# Central Group Box

	def makeCentralGroupBox(self):
		self.CentralGroupBox = QGroupBox('Seismograms Vectorization', self)
		self.CentralGroupBox.setStyleSheet('QGroupBox:title {'
				'subcontrol-origin: margin;'
				'subcontrol-position: top center;'
				'padding-left: 10px;'
				'padding-right: 10px; }')
		self.CentralGroupBox.setStyleSheet('QGroupBox {'
					'font: bold;'
					'border: 1px solid silver;'
					'border-radius: 10px;'
					'margin-top: 10px; }')
	# Buttons
		self.btnInfo = QPushButton('Raster Size Information', self)
		self.btnInfo.resize(self.btnInfo.sizeHint())
		self.btnInfo.setStatusTip('Raster Size in mm and/or pixels')
		self.btnInfo.setEnabled(False)
		self.btnInfo.clicked.connect(self.getInfo)

		self.btnCoord = QPushButton('&Time and amplitude scale', self)
		self.btnCoord.resize(self.btnCoord.sizeHint())
		self.btnCoord.setStatusTip('Defines the time scale and amplitude scale for the output data')
		self.btnCoord.setEnabled(False)
		self.btnCoord.clicked.connect(self.referenceSystem)

		self.btnDigi = QPushButton('&Vectorize', self)
		self.btnDigi.resize(self.btnDigi.sizeHint())
		self.btnDigi.setStatusTip('Vectorization of traces contained in seismograms')
		self.btnDigi.setEnabled(False)
		self.btnDigi.clicked.connect(self.setVectorize)

		self.btnPrevPlot = QPushButton('&Plot Data', self)
		self.btnPrevPlot.resize(self.btnPrevPlot.sizeHint())
		self.btnPrevPlot.setStatusTip('Plot the progress to verify the seismograms')
		self.btnPrevPlot.setEnabled(False)
		self.btnPrevPlot.clicked.connect(self.prePlot)

		self.btnSave = QPushButton('&Save Data', self)
		self.btnSave.resize(self.btnSave.sizeHint())
		self.btnSave.setStatusTip('Save the time series in a two-column ASCII file')
		self.btnSave.setEnabled(False)
		self.btnSave.clicked.connect(self.saveData)
	# Layout vertical Vectorize
		self.vbox1 = QVBoxLayout()
		self.vbox1.addWidget(self.btnInfo)
		self.vbox1.addWidget(self.btnCoord)
		self.vbox1.addWidget(self.btnDigi)
		self.vbox1.addWidget(self.btnPrevPlot)
		self.vbox1.addWidget(self.btnSave)
		self.CentralGroupBox.setLayout(self.vbox1)
		self.CentralGroupBox.setMaximumSize(int(Guiwidth/6),int(height*0.48))
#########################################################################################
# Right Group Box

	def makeRightGroupBox(self):
		self.RightGroupBox = QGroupBox('Basic Corrections', self)
		self.RightGroupBox.setStyleSheet('QGroupBox:title {'
				'subcontrol-origin: margin;'
				'subcontrol-position: top center;'
				'padding-left: 10px;'
				'padding-right: 10px; }')
		self.RightGroupBox.setStyleSheet('QGroupBox {'
					'font: bold;'
					'border: 1px solid silver;'
					'border-radius: 6px;'
					'margin-top: 6px; }')
	# Buttons
		self.btndatafile = QPushButton('Load ASCII &Data File', self)
		self.btndatafile.resize(self.btndatafile.sizeHint())
		self.btndatafile.setStatusTip('Load a time series in a two-column ASCII file')
		self.btndatafile.clicked.connect(self.getdatafile)

		self.btnchPol = QPushButton("Invert Polarity", self)
		self.btnchPol.resize(self.btnchPol.sizeHint())
		self.btnchPol.setStatusTip('Reverse Seismogram Polarity')
		self.btnchPol.setEnabled(False)
		self.btnchPol.clicked.connect(self.invertPolarity)

		self.btnDtrendBline = QPushButton('De-trend', self)
		self.btnDtrendBline.resize(self.btnDtrendBline.sizeHint())
		self.btnDtrendBline.setStatusTip('shifts and de-trends the seismogram ' +
											' to its baseline')
		self.btnDtrendBline.setEnabled(False)
		self.btnDtrendBline.clicked.connect(self.detrendFunction)

		self.btnCurvaResample = QPushButton('Remove Curvature\n and Resampling', self)
		self.btnCurvaResample.resize(self.btnCurvaResample.sizeHint())
		self.btnCurvaResample.setStatusTip('Remove the curvature of Mechanical instruments and re-sample' +
											' to evenly spaced time series')
		self.btnCurvaResample.setEnabled(False)
		self.btnCurvaResample.clicked.connect(self.curvaResample)

		self.btnResample = QPushButton("Resampling", self)
		self.btnResample.resize(self.btnResample.sizeHint())
		self.btnResample.setStatusTip('resample to evenly spaced time series')
		self.btnResample.setEnabled(False)
		self.btnResample.clicked.connect(self.justResample)

		self.btnResInst = QPushButton('Instrumental &Response', self)
		self.btnResInst.resize(self.btnResInst.sizeHint())
		self.btnResInst.setStatusTip('Remove or Adds the instrumental response for Wiechert instruments')
		self.btnResInst.setEnabled(False)
		self.btnResInst.clicked.connect(self.instrumentalResponse)

		self.btnSaveTimeSeries = QPushButton('&Save Data', self)
		self.btnSaveTimeSeries.resize(self.btnSaveTimeSeries.sizeHint())
		self.btnSaveTimeSeries.setStatusTip('Save time series data in an ASCII and/or sac format')
		self.btnSaveTimeSeries.setEnabled(False)
		self.btnSaveTimeSeries.clicked.connect(self.saveCorrectedData)
	# Corrections Layout vertical
		self.vbox2 = QVBoxLayout()
		self.vbox2.addWidget(self.btndatafile)
		self.vbox2.addWidget(self.btnchPol)
		self.vbox2.addWidget(self.btnDtrendBline)
		self.vbox2.addWidget(self.btnCurvaResample)
		self.vbox2.addWidget(self.btnResample)
		self.vbox2.addWidget(self.btnResInst)
		self.vbox2.addWidget(self.btnSaveTimeSeries)
		self.RightGroupBox.setLayout(self.vbox2)
		self.RightGroupBox.setMaximumSize(int(Guiwidth/6),int(height*0.48))
#########################################################################################
# graphical Pyplot

	def makeDataPlot(self):
		self.fig = matplotlib.figure.Figure()
		self.ax = self.fig.add_subplot(111)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setMaximumSize((int(Guiwidth/2))-10, int(height*0.48))
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.toolbar.setMaximumSize((int(Guiwidth/2))-10, int(height*0.06))
# Image information

	def makeDataimagee(self):
		self.text = QTextEdit()
		self.text.setMaximumSize(int(Guiwidth/2)-10,int(width*0.08))
# Group box extra

	def creaExtraGruopBox(self):
		self.extraGroupBox = QGroupBox('',self)
		self.extraGroupBox.setStyleSheet('QGroupBox:title {'
				'subcontrol-origin: margin;'
				'subcontrol-position: top center;'
				'padding-left: 10px;'
				'padding-right: 10px; }')
		self.extraGroupBox.setStyleSheet('QGroupBox {'
					'font: bold;'
					'border: 1px solid silver;'
					'border-radius: 6px;'
					'margin-top: 6px; }')
		self.btnExtras = QPushButton('Auxiliary Modules', self)
		self.btnExtras.resize(self.btnExtras.sizeHint())
		self.btnExtras.setStatusTip('Open Window of Auxiliary Modules')
		self.btnExtras.clicked.connect(self.extraFunctions)
	# Layout vertical
		self.vbox3 = QVBoxLayout()
		self.vbox3.addWidget(self.btnExtras)
		self.extraGroupBox.setLayout(self.vbox3)

#########################################################################################
############### D I G I T A L  I M A G E  P R O C E S S I N G  M O D U L E  #############
# Define the digital image processing functions
	# Load functions and enable buttons

	def load_image(self, event):
		global ppi, img, directory, imagefile
		global path,clone
		try:
			self.text.append(str(ppi*1))
			sb = QMessageBox()
			sb.setIcon(QMessageBox.Information)
			sb.setWindowTitle('Save Data')
			sb.setText(f'Do you want to save image procesing on {directory[-1]}?')
			sb.setStandardButtons(sb.Yes | sb.No)
			ret = sb.exec_()
			if ret == sb.Yes:
				self.setSaveImg()
				del img
			elif ret ==sb.No:
				del img
				# return
		except:
			pass

		imagefile, _ = QFileDialog.getOpenFileName(self, 'Load Seismogram Raster Image',
		path, "Image Files (*.jpg *.png *.jpeg *.tif);; All files (*)")
		self.pixels.clear()
		path = os.path.split(imagefile)[0]
		cv2.destroyAllWindows()
		if imagefile:
			directory = imagefile.split('/')
			text1 = f"Seismogram: {directory[-1][:-4]}"
			self.sisDate.setText(text1)
			self.sisDate.setWordWrap(True)
			self.sisDate.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
			self.text.append('Image: \n '+directory[-1])
			try:
				ii = Image.open(imagefile)
				ppi = ii.info['dpi'][0]
				self.pixels.setText(str(ppi))
			except KeyError:
				(inp, okPressed) = QInputDialog.getInt(self, 'Raster Image pixels per inch',
							'No PPI on raster information. \n'
							'Input PPI: ',600, 0, 3000, 2)
				if okPressed:
					ppi = float(inp)
					self.pixels.setText(str(ppi))
				else:
					self.pixels.setText('None')
			except NameError:
				QMessageBox.Critical(self,'Error!',
					'Without a PPI value, the usage of some functions will be limited')
			img = cv2.imread(imagefile,0)
			cv2.namedWindow(directory[-1], cv2.WINDOW_NORMAL)
			cv2.imshow(directory[-1], img)
			self.btnRotate.setEnabled(True)
			self.btnTrim.setEnabled(True)
			self.btnContrast.setEnabled(True)
			self.btnBinary.setEnabled(True)
			self.btnInfo.setEnabled(True)
			self.btnDigi.setEnabled(True)
			self.btnCoord.setEnabled(True)
			self.text.clear()
		else:
			QMessageBox.warning(self, 'Warning!',
				'No raster image file loaded!')
			pass
	cv2.waitKey(0)
	#####################################################################################
	# Rotate image 90° clockwise

	def setRotate(self):
		global img
		try:
			img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
			cv2.namedWindow(directory[-1], cv2.WINDOW_NORMAL)
			cv2.imshow(directory[-1], img)
		except NameError as e:
			QMessageBox.warning(self, 'Error!',
				f'{e}\nNo image file found!')
		cv2.waitKey(0)
	#####################################################################################
	# Increase contrast

	def setContrast(self):
		global img
		try:
			clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
			img = clahe.apply(img)
			cv2.namedWindow(directory[-1]+' contrast increase', cv2.WINDOW_NORMAL)
			cv2.imshow(directory[-1]+' contrast increase', img)
		except NameError as e:
			QMessageBox.warning(self, 'Error!',
				f'{e}\nNo image file found!')
		cv2.waitKey(0)
	#####################################################################################
	# Turn image in to binary

	def setBinary(self):
		global img
		try:
			(thersh, img) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY |
											cv2.THRESH_OTSU)
			cv2.namedWindow(directory[-1]+' Binary (B/W)', cv2.WINDOW_NORMAL)
			cv2.imshow(directory[-1]+' Binary (B/W)', img)
		except NameError as e:
			QMessageBox.warning(self, '!Error!',
				f'{e}\nNo image file found!')
		cv2.waitKey(0)
	#####################################################################################
	# Trim Seismogram

	def TrimSeismogram(self):
		# Select ROI
		global img
		try:
			fromCenter = False
			QMessageBox.information(self, 'Select ROI ',
						'Select Region Of Interest and then press SPACE or ENTER key!\n'
						'Cancel the selection process by pressing "c" key! ')

			self.text.append('Select ROI\n' +
						'Select a ROI and then press SPACE or ENTER key!\n' +
						'Cancel the selection process by pressing "c" key! ')

			cv2.namedWindow('Trim in '+directory[-1], cv2.WINDOW_NORMAL)
			cv2.imshow('Trim in '+directory[-1], img)
			r = cv2.selectROI('Trim in '+directory[-1], img, fromCenter)
		# Crop image
			imcp = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
			cv2.destroyWindow('Trim in '+directory[-1])
		# Display cropped image
			img = imcp
			cv2.namedWindow(directory[-1]+' Trimmed', cv2.WINDOW_NORMAL)
			cv2.imshow(directory[-1]+' Trimmed', img)
		except NameError:
			QMessageBox.warning(self, 'Error!',
				'Cannot Trim, no image file found!')
		cv2.waitKey(0)
	#####################################################################################
	# Display image dimensions

	def getInfo(self):
		global ro, co, ppi, ejex, ejey
		try:
			ro, co = img.shape[0:2]
			ejex = (co / ppi) * 25.4  # image width on mm
			ejey = (ro / ppi) * 25.4  # image height on mm
			self.text.append('{:}= {:.4} {:} {:.4} {:}'.format('Raster Image Size', ejex,
							'mm long, by', ejey, 'mm width'))

			self.text.append('{:}={:} {:} {:} {:}'.format('Raster Image Size :', co,
									'pixels long, by ', ro,'pixels width '))
		except NameError:
			self.text.append('{:}={:} {:} {:} {:}'.format('Raster Image Size :', co,
									'pixels long, by ', ro,'pixels width '))

		self.text.append('Image : ' + directory[-1])
	#####################################################################################
	# Save processed image

	def setSaveImg(self):
		global img, imagefile
		try:
			self.text.append(str(ppi*1))
			outnameimg, _ = QFileDialog.getSaveFileName(self, 'Save Digitally Processed Image',
				imagefile[0:-4] + '.processed.jpg',
				"Images Files (*.jpg *.jpg *.tif);; All files (*)")
			PILimg = Image.fromarray(img)
			PILimg.save(outnameimg, dpi=(ppi,ppi))
		except NameError:
			sppi, okPressed = QInputDialog.getInt(self, 'Input Data',
										'Resolution Image in PPI :',600, 0, 2100)
			if okPressed:
				try:
					outnameimg, _ = QFileDialog.getSaveFileName(self, 'Save Digitally Processed Image',
						imagefile[0:-4] + '_processed',
						"Images Files (*.jpg *.jpg *.tif);; All files (*)")
					PILimg = Image.fromarray(img)
					PILimg.save(outnameimg, dpi=(sppi,sppi))
				except:
					pass
		except FileNotFoundError as e:
			pass
			QMessageBox.warning(self,'Warning', str(e))

		except:
			QMessageBox.warning(self, 'Warning!',
				'Image not saved!')
		return outnameimg
#########################################################################################
################  V E C T O R I Z A T I O N   M O D U L E ###############################
# functions for module to vectorize
# Calculates the distance between two time-marks on the  record,
# to obtain amplitude zero value, and paper drums speed rotation

	def referenceSystem(self):
		global X_values, Y_values
		global vr, amp0, clone, imheight
		ro, co = img.shape[:2]

		def timeMarks(heightimg):
			global clone, vr, amp0, dot
			try:
				clone = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
			except:
				clone = img.copy()
			dot = []
			QMessageBox.information(self, 'Instructions',
				'DobleClick over at least three continuous time-marks before\n'
				'the first arrival on the same or earlier trace. \n'
				'By pressing "Esc", the process ends and the image closes')
			self.text.append('Instructions \n' +
				'DobleClick over at least three continuous time-marks before \n' +
				'the first arrival on the same or earlier trace\n' +
				'By pressing "Esc", the process ends and the image closes')

			def distance(event, x, y, flags, params):
				global ppi, dot, vr, amp0, clone, mean
				if event == cv2.EVENT_LBUTTONDBLCLK:
					cv2.circle(clone, (x, y), round(ppi*0.005), (0, 255, 0), -1)
					dot.append((x, y))
			# paper drums speed rotation 'vr' considering the image resolution in (mm/s)
			# To correct the amplitude 'amp0' (amplitude on mm near baseline trace)
			cv2.namedWindow('Define time/amplitude scale', cv2.WINDOW_NORMAL)
			cv2.resizeWindow('Define time/amplitude scale',(int(width*0.5), int(height*0.48)))
			cv2.setMouseCallback('Define time/amplitude scale', distance)
			while True:
				cv2.imshow('Define time/amplitude scale', clone)
				k = cv2.waitKey(1)
				if k == 27 & 0xff:
					break
			cv2.destroyWindow('Define time/amplitude scale')
			if len(dot) > 2:
				dd = np.array(dot)
				suma = np.array([])
				for i in range(len(dd) - 1):
					suma = np.append(suma,dd[i+1,0]-dd[i,0])
				mean = np.mean(suma)
				vr = ((mean * 25.4) / ppi) / 60
				(vr, ok) = QInputDialog.getDouble(self, 'The drum speed rotation ',
				'The computed Drum speed Rotation in mm/s is:',vr, 0, 5, 4)
				amp0 = (((dd[0,1] + dd[1,1]) / 2) / ppi) * 25.4
				amp0 = (-1*amp0 + heightimg)
			return vr, amp0, mean

		def getpoint():
			X_values = np.empty(2)
			Y_values = np.empty(2)
			try:
				(X_values[0], ok) = QInputDialog.getDouble(self, 'Input Values ',
				'Left X value:',0, -10000000000000, 1000000000000, 3)
				(Y_values[0], ok) = QInputDialog.getDouble(self, 'Input Values ',
				'Up Y value:',0, -10000000000000, 1000000000000, 3)
				(X_values[1], ok) = QInputDialog.getDouble(self, 'Input Values ',
				'Right X value :',0, -10000000000000, 1000000000000, 3)
				(Y_values[1], ok) = QInputDialog.getDouble(self, 'Input Values ',
				'Down Y value :',0, -10000000000000, 1000000000000, 3)
			except:
				QMessageBox.critical(self,'Error',
					'Both corners values must be defined')
			return X_values, Y_values

		try:
			imheight = (ro/ppi) * 25.4  # image height on mm
			item = ('Continuous Time-marks','Opposite image corners values')
			item, okPressed = QInputDialog.getItem(self,'Define time/amplitude scale ',
									'How to scale for the output data? : ',item, 0, False)

			if okPressed and item == 'Opposite image corners values':
				X_values, Y_values = getpoint()
				self.text.append('\n{:}={:},{:} '.format('Left Up corner values:  ',
						X_values[0], Y_values[0]))
				self.text.append('{:}={:},{:} '.format('Right Down corner values: ',
						X_values[1],Y_values[1]))

			elif okPressed and item == 'Continuous Time-marks':
				vr, amp0, mean = timeMarks(imheight)

				self.text.append('\n{:}={:.4} {:}'.format('Average distance between' +
														' time-marks',(vr * 60), 'mm'))
				self.text.append('{:}={:.4} {:}'.format('Average distance between' +
														' time-marks',mean, 'pixels'))
				self.text.append('{:}={:.4} {:}'.format('Average paper drums speed rotation' +
													' of the seismograph: ', vr, ' mm/s'))

		except NameError:
			X_values, Y_values = getpoint()
			self.text.append('\n{:}={:},{:} '.format('Left Up corner values:  ',
					X_values[0], Y_values[0]))
			self.text.append('{:}={:},{:} '.format('Right Down corner values: ',
					X_values[1],Y_values[1]))

	#############################################################################################
	# Vectorize

	def setVectorize(self):
		import time
		global points, img, cont, clone, ansd
		ro, co = img.shape[:2]
		check=0
		try:
			color = (255, 0, 225)
			img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
		except:
			# img = clone.copy()
			colors = [(255,0,0),(0,0,255),(0,255,0),(255,255,0),(255,0,255),(0,255,255),(255,136,0)]
			color = colors[np.random.choice(len(colors))]

		# try:
		# 	scf = ppi
		# except NameError:
		# 	scf = 600
		# cb = QCheckBox("Don't show this message again")
		mb = QMessageBox(self)
		mb.setIcon(QMessageBox.Information)
		mb.setWindowTitle('Instructions',)
		mb.setText('"DobleClick"	Mark the coordinate on the seismogram image \n'
			'"z" 	   Undo the last marked point\n'
			'"r" 	   restarts vectorization function \n'
			'"Esc" 	   ends vectorization function')
		# mb.setCheckBox(cb)

		def checkbox_state(cb,mb):
			if cb.isChecked():
				pass
			else:
				mb.exec_()
			return cb.isChecked()
		# ansd = checkbox_state(cb, mb)
		try:
			points = []
			mb.exec_()
			self.text.append('Instructions \n' +
				'"DobleClick"	 Mark the coordinate on the seismogram image \n' +
				'"z" 	   Undo the last marked sample\n' +
				'"r" 	   restarts vectorization function \n' +
				'"Esc" 	   ends vectorization function')

			self.text.append('\n(x,y) Coordinates:')

			def mouseDrawing(event, x, y, flags, params):
				global n_im
				if event == cv2.EVENT_LBUTTONDBLCLK:
					points.append((x, y))
					try:
						if "vr" in globals():		
							self.text.append(f"{(((points[-1][0]/ppi) * 25.4) / vr):.2f},	{(((((points[-1][1]/ppi) * 25.4) * -1) + imheight) - amp0):.2f}")
						elif "Y_values" in globals():
							x = X_values.min() + ((points[-1][0] * (X_values[1] - X_values[0])) / co)   # 
							if Y_values[0] > Y_values[1]:
								yp = (points[-1][1] * -1) + ro
								y = Y_values.min() + ((yp * np.abs(Y_values[1] - Y_values[0])) / ro)  #
							else:
								y = Y_values.min() + ((points[-1][1] * np.abs(Y_values[1] - Y_values[0])) / ro)  #
							self.text.append(f"{x:.2f}, {y:.2f}")
						else:
							self.text.append(f"{(points[-1][0]):.2f}, {((points[-1][1] * - 1) + ro):.2f}")
					except:
						pass

			cv2.namedWindow(f'Vectorize on {directory[-1]}', cv2.WINDOW_NORMAL)
			cv2.resizeWindow(f'Vectorize on {directory[-1]}',(int(width*0.5), int(height*0.48)))
			cv2.setMouseCallback(f'Vectorize on {directory[-1]}', mouseDrawing)
			while True:
				clone = img.copy()
				for cp in points:
					cv2.circle(clone, cp, 3, (0, 0, 255), -1)
					if len(points) > 1:
						self.btnPrevPlot.setEnabled(True)
						self.btnSave.setEnabled(True)
						for i in range(len(points)):
							if i != 0:
								cv2.line(clone, points[i-1], points[i], color, 2)
				cv2.imshow(f'Vectorize on {directory[-1]}',clone)
				# plt.imshow(clone)
				key = cv2.waitKey(delay=1) & 0xff
				if key == ord('z'):
					points = points[:len(points) - 1]
				elif key == ord('r'):
					points = []
					self.text.clear()
					self.text.setText('(x,y) Coordinates : ')
				elif key == 27:
					break
				# 	continue
				# time.sleep(0.05)
			img = clone.copy()
			del clone
			cv2.destroyWindow(f'Vectorize on {directory[-1]}')
			return points, img
		except:
			QMessageBox.warning(self, 'Error!',
				'No Vectorized data')
	#####################################################################################
	# Graphical representation of data

	def prePlot(self):
		global amp0, X_values, Y_values, vr, ppi
		ro, co = img.shape[0:2]
		amp = []
		treg = []
		for i in range(len(points)):
			amp.append(float(points[i][1]))
			treg.append(float(points[i][0]))
		imheight = (ro/ppi) * 25.4  # image height on mm
		self.ax.clear()
		try:
			if "vr" in globals():		
				# plot in canvas figure in the GUI
				self.ax.plot(((np.array(treg)/ppi) * 25.4) / vr,
					((((np.array(amp)/ppi) * 25.4) * -1) + imheight) - amp0, 'k')
				self.ax.set_ylabel('$ Amplitude_{mm} $')
				self.ax.set_xlabel('$ time_{sec} $')
				self.ax.grid()
				self.canvas.draw()
			elif "Y_values" in globals():
				i = 0
				ti_v = np.empty(len(treg))
				amp_v = np.empty(len(amp))
				if Y_values[0] > Y_values[1]:
					amp = (np.array(amp) * -1) + ro
				else:
					amp = np.array(amp)
					self.ax.invert_yaxis()

				for x, y in zip(np.array(treg), np.array(amp)):
					ti_v[i] = X_values.min() + ((x * (X_values[1] - X_values[0])) / co)   # 
					amp_v[i] = Y_values.min() + ((y * np.abs(Y_values[1] - Y_values[0])) / ro)  #
					i += 1
				self.ax.plot(ti_v, amp_v, 'k')
				self.ax.set_ylabel('$ Amplitude [mm] $')
				self.ax.set_xlabel('$ time [sec] $')
				self.ax.grid()
				self.canvas.draw()
			else:
		# except NameError:
				# plot in canvas figure in the GUI
				self.ax.clear()
				self.ax.plot(np.array(treg), (np.array(amp) * -1) + ro, 'k')
				self.ax.set_ylabel('$ Y [pixels] $')
				self.ax.set_xlabel('$ X [pixels] $')
				self.ax.grid()
				self.canvas.draw()
		except:
			pass
	#####################################################################################
	# Save Data in ASCII format

	def saveData(self):
		global points, ampPX, amp_mm, tregPX, treg_s, imagefile
		amp = np.empty(len(points))
		treg = np.empty(len(points))
		ro, co = img.shape[0:2]
		for i in range(len(points)):
			amp[i] = points[i][1]
			treg[i] = points[i][0]
		ampPX = (amp * -1) + ro
		tregPX = treg
	# functions for reference data

		def timeMarks(amp0, imheight, ppi, vr, a, t):
			amp = ((((a/ppi) * 25.4) * -1) + imheight) - amp0
			tr = ((t/ppi) * 25.4) / vr
			return amp, tr

		def pix2coord(a, t, Xpixmax, Ypixmax, x_val, y_val):
			import numpy as np
			X_scale = np.empty(len(t))
			Y_scale = np.empty(len(a))
			if y_val[0] > y_val[1]:
				a = (np.array(a) * -1) + Ypixmax
			else:
				a = np.array(a)
			i = 0
			for x, y in zip(t,a):
				X_scale[i] = x_val.min() + ((x * (x_val[1] - x_val[0])) / Xpixmax)

				Y_scale[i] = y_val.min() + ((y * np.abs(y_val[1] - y_val[0])) / Ypixmax)
				i = i+1
			return Y_scale, X_scale

			# ti_v[i] = X_values.min() + ((x * (X_values[1] - X_values[0])) / co)  # 
			# amp_v[i] = Y_values.min() + ((y * (Y_values[1] - Y_values[0])) / ro)  #
		##################################
		try:
			try:
				global vr, amp0, ppi
				imheight = (ro/ppi) * 25.4  # image height on mm
			# Data array on Pixels	# data array on Define time/amplitude scale
				amp_mm, treg_s = timeMarks(amp0,imheight,ppi,vr,amp,treg)
			except NameError:
				global X_values, Y_values
				amp_mm, treg_s = pix2coord(amp,treg,co,ro,X_values,Y_values)
			outdata = np.array([treg_s, amp_mm])
			outdata = outdata.T
			item = ('Scaled time-series', 'Pixels')
			(item, okPressed) = QInputDialog.getItem(self,'Save Data',
							'          Data : ',item, 0, False)
			if okPressed and item == 'Pixels':
				outdata = np.array([tregPX, ampPX])
				outdata = outdata.T
				outname, _ = QFileDialog.getSaveFileName(self, 'Save as ASCII file ',
							imagefile[0:-4]+'_pixel.txt', "Text files (*.txt *.dat);; All files (*)")
				with open(outname, 'w+'):
					np.savetxt(outname, outdata, fmt=['%e','%e'], delimiter='	')

			elif okPressed and item == "Scaled time-series":
				outname, _ = QFileDialog.getSaveFileName(self, 'Save as ASCII file ',
							imagefile[0:-4]+'_refe.txt', "Text files (*.txt *.dat);; All files (*)")
				with open(outname, 'w+'):
					np.savetxt(outname, outdata, fmt=['%e','%e'], delimiter='	')
			else:
				pass
		except:
			outdata = np.array([tregPX, ampPX])
			outdata = outdata.T
			outname, _ = QFileDialog.getSaveFileName(self, 'Save as ASCII File ',
						imagefile[0:-4]+'_pixel.txt', "Text Files (*.txt *.dat);; All files (*)")
			try:
				with open(outname, 'w+'):
					np.savetxt(outname, outdata, fmt=['%e','%e'], delimiter='	')
			except FileNotFoundError:
				pass
		# except:
		# 	QMessageBox.critical(self,'No Data',
		# 						'There are no data to save')
#########################################################################################
##################  B  A S I C  C O R R E C T I O N S  M O D U L E ###########################
	# Load a data file, and correct them

	def getdatafile(self):
		global path, amp, treg, datafile, directory
		try:
			del amp1, amp
		except:
			pass
			
		datafile, _ = QFileDialog.getOpenFileName(self, 'Load ASCII Data File',
			path, "Text files (*.txt *.dat);; All files (*) ")  # text files formats
		path = os.path.split(datafile)[0]
		if datafile:
			try:
				treg = np.genfromtxt(datafile, usecols=0, dtype=float, comments='#')
				amp = np.genfromtxt(datafile, usecols=1, dtype=float, comments='#')
				self.btnDtrendBline.setEnabled(True)
				self.btnchPol.setEnabled(True)
				self.btnCurvaResample.setEnabled(True)
				self.btnResample.setEnabled(True)
				self.btnResInst.setEnabled(True)
				self.ax.clear()
				self.ax.plot(treg, amp, 'k')
				self.ax.set_ylabel('$ mm $')
				self.ax.set_xlabel('$ sec $')
				self.ax.grid()
				self.canvas.draw()
				directory = datafile.split('/')
				text1 = f"Seismogram: {directory[-1][:-4]}"
				self.sisDate.setText(text1)
				self.sisDate.setWordWrap(True)
				self.sisDate.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
			except IndexError as e:
				QMessageBox.information(self, 'Warning!',
					str(e)+'\nUnsupported file')
		else:
			QMessageBox.warning(self, 'Warning!',
				'No file was loaded!')
			pass
	#####################################################################################
	# Change Polarity
	def invertPolarity(self):
		import correctionFunctions as cf
		"""
		invert seismogram polarity
		"""
		global amp, treg
		self.ax.clear() 
		self.ax.plot(treg, amp,'k', linewidth=0.75, label='Raw data')
		fig, ax = plt.subplots(1,1, figsize=(10,5))
		ax.plot(treg, amp, 'k', linewidth=0.75, label='Raw data')
		amp = cf.chPolarity(amp)
		self.ax.plot(treg, amp,'r', linewidth=0.75)
		self.ax.set_ylabel('$ mm $')
		self.ax.set_xlabel('$ sec $')
		self.ax.grid()
		self.ax.legend(loc='upper right')
		self.canvas.draw()
		ax.plot(treg, amp, 'r', linewidth=0.75,)
		plt.show()
		self.btnSaveTimeSeries.setEnabled(True)
#####################################################################################
	# Corrections to by applied	# by baseline and Slope
	def detrendFunction(self):
		"""
		Detrend function
		"""
		global amp, treg, datafile, amp1
		import correctionFunctions as cf
		
		amp1 = amp.copy()
		try: 
			ntrv, okPressed = QInputDialog.getInt(self, 'Time', 'Window length in seconds: ',
										60, 5, 1000)
			if okPressed:
				treg, amp1 = cf.detrend(treg, amp1, ntrv=ntrv)
				self.ax.clear() 
				self.ax.plot(treg, amp, linewidth=0.75, label='Raw data')
				self.ax.plot(treg, amp1, linewidth=0.75, label='Detrend')
				self.ax.set_ylabel('$ mm $')
				self.ax.set_xlabel('$ sec $')
				self.ax.grid()
				self.ax.legend(loc='upper right')
				self.canvas.draw()
				fig, ax = plt.subplots(1,1, figsize=(10,5))
				fig.suptitle(' Detrend correction ')
				ax.plot(treg, amp, 'gray', linewidth=0.75, label='Raw data')
				ax.plot(treg, amp1, '--k', linewidth=0.75, label='Detrend')
				ax.legend(loc='upper right')
				fig.savefig(datafile[0:-4]+'.detrend.jpg', dpi=300)
				plt.show()
				self.btnSaveTimeSeries.setEnabled(True)
		except:
			QMessageBox.warning(self, 'Warning!',
				'Window duration must be nonzero !')
			pass


	#####################################################################################

	def curvaResample(self):
		"""
		# Calculate the time data to remove curvature effect from  Grabrovec and Allegretti
		# (1994), equation. Additionaly approximate by leas squares the time series to make
		# sure that these are progressive
		"""
		global amp1, amp, treg, vr, R, ampinfl, sps, t_ga, tapr 
		global tapr_res, amp1_res, t_ga_res, amp_res
		import correctionFunctions as cf
	# check on previous corrections data
		try:
			if amp1.any():
				amp = amp1
		except:
			pass
		# Input data by user
		try:
			try:
				(vr, okPressed) = QInputDialog.getDouble(self, 'Input Data',
										'Paper Drum Speed Rotation in mm/s :',vr, 0, 5, 3)
			except:
				(vr, okPressed) = QInputDialog.getDouble(self, 'Input Data',
										'Paper Drum Speed Rotation in mm/s :',0.0, 0, 5, 3)
			if okPressed:
				self.text.append('Input data for curvature correction :')
				self.text.append('Paper Drum Speed Rotation: {0:8.4f} mm/s'.format(vr))
				(R, okPressed) = QInputDialog.getDouble(self, 'Input Data',
								'Stylet length in mm or :',150, 0, 1000, 2)
				if okPressed:
					self.text.append('Stylet length: {0:5f} mm'.format(R))
					ampinfl, okPressed = QInputDialog.getDouble(self,'Input Data',
										'Amplitude of inflection of the curvature\n'
										'[mm or Pixels]:',0.00, min(amp), max(amp), 3)
					if okPressed:
						self.text.append('Inflection amplitude: '
							'{0:} mm\n'.format(ampinfl))
				else:
					pass
			else:
				pass

			tapr, t_ga = cf.GandA94(treg, amp, vr, R, ampinfl)
			t_ga = np.sort(t_ga.ravel())
			tapr = np.sort(np.round(tapr.ravel(),4) - tapr[0])

		# Re sample input 
			sps, okPressed = QInputDialog.getInt(self, 'SPS', 'Sampling rate:',
										20, 5, 100)
			item = ('slinear', 'quadratic', 'cubic')
			kind, okPressed = QInputDialog.getItem(self,'Spline interpolation order',
					'Spline interpolation order\n', item, 0, False)
			if okPressed:
				t_ga_res, amp_res = cf.resample(t_ga, amp, sps, kind)
				tapr_res, amp1_res =cf.resample(tapr, amp, sps, kind)

			self.ax.clear()
			self.ax.plot(treg-treg[0], amp-amp[0], label='Raw data', linewidth=0.75)
			self.ax.plot(tapr_res, amp1_res, label='Re-calculated time by least squares', linewidth=0.75)
			self.ax.plot(t_ga_res, amp_res, label='Calculated time by G&A 94', linewidth=0.75)
			self.ax.set_ylabel('$ mm $')
			self.ax.set_xlabel('$ sec $')
			self.ax.grid()
			self.ax.legend(loc='upper right')
			self.canvas.draw()
			fig, ax = plt.subplots(1,1, figsize=(10,5))
			fig.suptitle('Curvature correction and re-sampled')
			ax.plot(treg, amp, 'k', label='Raw data',linewidth=0.75)
			ax.plot(tapr_res, amp1_res, 'r', label='Re-calculated time by least squares',linewidth=0.75)
			ax.plot(t_ga_res, amp_res, label='Calculated time by G&A 94',linewidth=0.75)
			fig.legend(loc='upper right')
			fig.savefig(datafile[0:-4]+'.time-series.jpg', dpi=300)
			plt.show()
			self.text.append('Correction by Curvature  and Re-sampled done\n')
			self.btnSaveTimeSeries.setEnabled(True)
		except NameError as e:
			QMessageBox.warning(self, 'Name Error', f"{str(e)}\nInput all required data.")
			self.text.clear()
		# except ValueError as e:
		# 	QMessageBox.warning(self, 'Value Error', f"{str(e)}\nInput all required data.")
		# 	self.text.clear()
################################################################
	def justResample(self):
		"""
		Time series resample by lanczos_interpolation 
		"""
		global amp, amp1, treg, sps, tres, amp_res
		import correctionFunctions as cf
	# check on previous corrections data
		try:
			if amp1.any():
				amp = amp1
			elif tres.any():
				amp  = amp_res
				treg = tres
			elif t_ga_res.any():
				amp  = amp_res
				treg = t_ga_res
		except:
			pass
		# Input data by user
		try:
		# Re sample input 
			sps, okPressed = QInputDialog.getInt(self, 'SPS', 'Sampling rate:',
										20, 5, 100)
			item = ('slinear', 'quadratic', 'cubic')
			kind, okPressed = QInputDialog.getItem(self,'Spline interpolation order',
								'Spline interpolation order\n', item, 0, False)
			if okPressed:
				tres, amp_res = cf.resample(treg, amp, sps, kind)
			self.ax.clear()
			self.ax.plot(treg-treg[0], amp-amp[0], label='Raw data', linewidth=0.75)
			self.ax.plot(tres, amp_res, label=f'Resampled at {sps} SPS', linewidth=0.75)
			self.ax.set_ylabel('$ mm $')
			self.ax.set_xlabel('$ sec $')
			self.ax.grid()
			self.ax.legend(loc='upper right')
			self.canvas.draw()
			fig, ax = plt.subplots(1,1, figsize=(10,5))
			fig.suptitle('Resampled')
			ax.plot(treg, amp, 'k', label='Raw data',linewidth=0.75)
			ax.plot(tres, amp_res, label=f'Resampled at {sps} SPS', linewidth=0.75)
			fig.legend(loc='upper right')
			fig.savefig(datafile[0:-4]+'.time-series.jpg', dpi=300)
			plt.show()
			self.btnSaveTimeSeries.setEnabled(True)
		except NameError as e:
			QMessageBox.warning(self, 'Name Error', str(e))
			self.text.clear()
		except ValueError as e:
			QMessageBox.warning(self, 'Value Error', f"{str(e)}asdf")
			self.text.clear()
#########################################################################################
	#  Response correction for Wiechert instruments

	def instrumentalResponse(self):
		import correctionFunctions as cf
		# check on previous corrections data
		global treg, amp, amp_res, amp1_res
		global fr, frec, H_w, sis_f, amp_correct, ini, end
		try:
			amp_res = amp_res - amp_res[0]
			amp1_res = amp1_res - amp1_res[0]
			item = ('G&A94 Data', 'ApLS Data')
			item, okPressed = QInputDialog.getItem(self,'Instrumental Response',
							'Curvature correction data for Instrumental\n'
							'response correction: ', item, 0, False)
			if okPressed and item == 'G&A94 Data':
				amp = amp_res
				treg = t_ga_res
			if okPressed and item == 'ApLS Data':
				amp = amp1_res
				treg = tapr_res
		except:
			pass
		T0, okPressed = QInputDialog.getDouble(self,'T0',
								'Natural undamped period in s :',5, 0, 15,1)
		if okPressed:
			self.text.append('Seismograph constants: ')
			self.text.append('Natural undamped period: {:} s'.format(T0))
			epsilon, okPressed = QInputDialog.getDouble(self, 'Epsilon',
											'Damping rate :', 4, 0, 10,2)
			if okPressed:
				self.text.append('Damping rate {:.2f}'.format(epsilon))
				V0, okPressed = QInputDialog.getInt(self, 'V0',
									'Magnification constant :', 250, 0, 50000)
				if okPressed:
					self.text.append('Static magnification: {:}'.format(V0))

					mssbox = QMessageBox(self)
					mssbox.setIcon(QMessageBox.Question)
					mssbox.setWindowTitle('Wiechert Instrument ',)
					mssbox.setText('Would you like to remove or add Wiechert Instrument to timeseries?')
					btnRemove = mssbox.addButton("Remove", QMessageBox.YesRole)
					btnAdd = mssbox.addButton("Add", QMessageBox.NoRole)
					mssbox.exec_()

		if mssbox.clickedButton() == btnRemove:
			wat_level, okPressed = QInputDialog.getDouble(self, 'Data',
						'Water level in decimal :',0.3, 0.0, 1.0, 3)
			if okPressed:
				deconv = True
				self.text.append('Water level: {:.2}'.format(wat_level))
			else:
				QMessageBox.Warning(self,"Warning",'Water Level needed for Remove Instrumental Response, Try again')
				pass

		elif mssbox.clickedButton() == btnAdd:
			deconv = False
			wat_level = 0.001

		# item = ('Wiechert Instrument Correction', 'Create Poles and Zeros file')
		# item, okPressed = QInputDialog.getItem(self,'Instrumental Response',
							#	'Choose an Option for Instrumental\n'
							#	'response correction', item, 0, False)
		try:
			self.text.append('Calculating ...\nWait')
			fr, Nmedios, H_w, sis_f, amp_correct, ini, end = cf.wichertResponse(treg, amp,T0, epsilon, V0, wat_level, deconv=deconv)
			amp_correct = cf.taper(treg,amp_correct)
			self.text.append('Correction completed after  {:.2} s '.format(end-ini))
			fig, ax = plt.subplots(1, 2, figsize=(10,5))
			ax[0].loglog(fr[:Nmedios], abs(H_w), 'k', linewidth=0.75)
			ax[0].set_ylabel('Amplitude')
			ax[0].set_xlabel('Hz')
			ax[1].loglog(fr[:Nmedios], abs(sis_f[:Nmedios]), 'k', linewidth=0.75)
			ax[1].set_xlabel('Hz')
			ax[1].set_ylabel('Amplitude')
			plt.savefig(f"{datafile[0:-4]}.{wat_level}.f_Response.jpg", dpi=300)

			fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10,5))
			ax[0].plot(treg, amp, 'k', linewidth=0.75)
			ax[1].plot(treg, amp_correct, 'k', linewidth=0.75)
			ax[1].set_xlabel('Time [s]')
			plt.savefig(f"{datafile[0:-4]}.{wat_level}.t_Response.jpg", dpi=300)
			plt.show()
			self.ax.clear()
			self.ax.plot(treg, amp/max(amp), label='Normalized raw data')
			self.ax.plot(treg, amp_correct/max(amp_correct), label='Normalized instrumental Response')
			self.ax.set_ylabel('Normalized Amplitude [mm]')
			self.ax.set_xlabel('$ sec $')
			self.ax.grid()
			self.ax.legend(loc='upper right')
			self.canvas.draw()
			self.btnSaveTimeSeries.setEnabled(True)
		except NameError as error:
			QMessageBox.warning(self,'Error', str(error))
			pass
#########################################################################################
	def saveCorrectedData(self):
		global outname
		import correctionFunctions as cf
		# Functions to save corrected data
		def saveLBase(a, t):
			outname, _ = QFileDialog.getSaveFileName(self, 'Save as ASCII file ',
								f'{datafile[0:-4]}.detrend.txt',
								"Text Files (*.txt *.dat);; All Files (*)")

			cf.saveData(t, a, outname)
			return outname

		def saveCurvature(t, a, t1, a1):
			outname, _ = QFileDialog.getSaveFileName(self, 'Save as ASCII file',
									f'{datafile[0:-4]}.GA94.txt',
									"Text Files (*.txt *.dat);; All Files (*)")
			cf.saveData(t, a, outname)

			outname, _ = QFileDialog.getSaveFileName(self, 'Save ASCII file',
									f'{datafile[0:-4]}.ApLC.txt',
									"Text Files (*.txt *.dat);; All Files (*)")
			cf.saveData(t1, a1, outname)
			return outname

		def saveInstrumento(t, a):
			outname, _ = QFileDialog.getSaveFileName(self, 'Save as ASCII file',
									f'{path}/{datafile[0:-4]}.IR.txt',
									"Text Files (*.txt *.dat);; All Files (*)")
			cf.saveData(t, a, outname)
			return outname

		def saveResampled(t, a):
			outname, _ = QFileDialog.getSaveFileName(self, 'Save as ASCII file',
									f'{path}/{datafile[0:-4]}.resampled.txt',
									"Text Files (*.txt *.dat);; All Files (*)")
			cf.saveData(t, a, outname)
			return outname
		def inputMetadata(a, t, out):
			from obspy.core.utcdatetime import UTCDateTime
			from obspy.core.trace import Trace, Stats
			header = Stats()
			network, okPressed = QInputDialog.getText(self, 'Data for header of sac file',
										'Network name:', QLineEdit.Normal, '')
			if okPressed and network != '':
				header.network = network
				est, okPressed = QInputDialog.getText(self, 'Data for header of sac file',
										'Station name:', QLineEdit.Normal, '')
				if okPressed and est != '':
					header.stattion = est
				header.delta = np.round(t[1]-t[0],3)
				channel, okPressed = QInputDialog.getText(self, 'Data for header of sac file',
											'Channel:', QLineEdit.Normal, 'HH*')
				if okPressed and channel != 'HH*':
					header.channel = channel
				starttime, okPressed = QInputDialog.getText(self, 'Data for header of sac file',
											'Earthquake origin time (UTC):', QLineEdit.Normal,
												'yyyy/mm/dd,hh:mm:ss')
				if okPressed and starttime != 'yyyy/mm/dd,hh:mm:ss':
					header.starttime = UTCDateTime(starttime)
			return header

		def savesac(t, a, datafile, out):
			try:
				directory = datafile.split('/')
				date = directory[-1].split('.')
				year, month, day, est = int(date[0]), date[1], date[2], date[3] #yyy.mm.dd.STA.HH*
				comp = date[4]
				header = Stats()
				network, okPressed = QInputDialog.getText(self, 'Data for header of sac file',
								'Network name:', QLineEdit.Normal, '')
				if okPressed and network != '':
					header.network = network
				header.station = est
				header.delta = np.round(t[1]-t[0],3)
				header.channel = 'HH'+comp[0]
				starttime, okPressed = QInputDialog.getText(self,'Data for header of sac file',
									'Earthquake origin time (UTC):', QLineEdit.Normal, 'hh:mm:ss')
				self.text.append(f'Start time (UTC): {starttime}')
				if okPressed and starttime != 'hh:mm:ss':
					header.starttime = UTCDateTime(f"{year}-{month}-{day},{starttime}")
				else:
					header.starttime = UTCDateTime(f"{year}-{month}-{day},00:00:00")
				sism = Trace(data=a, header=header)
				sism.write(out.split('.')[:-1]+'.sac', format='SAC')
				
			except IndexError as e:
				header = inputMetadata(a, t, out)
				sism = Trace(data=a, header=header)
				sism.write(f"{out.split('.')[:-1]}+.sac", format='SAC')
			except ValueError as e:
				QMessageBox.critical(self,'', str(e))
				pass
			except TypeError as e:
				header = inputMetadata(a, t, out)
				sism = Trace(data=a, header=header)
				sism.write(f"{out.split('.')[:-1]}+.sac", format='SAC')

		#################################################################################
		try:
			# previous directory to save data
			# global route, nom
			# route = str()
			# filename = str()
			# for folder in directory[1:-1]:
			# 	route += str(folder+'/')
			# nom = directory[-1].split('.')
			# for jj in nom[0:-1]:
			# 	filename += str(jj+'.')
			# If cycle to select data
			item = ('Detrend', 'Curvature and resampled',
					'Resampled', 'Instrumental Response')
			item, okPressed = QInputDialog.getItem(self,'Save as ASCII file',
								'Which correction data do you want to save?', item, 0, False)
			if okPressed and item == 'Detrend':
				try:
					outname = saveLBase(amp1, treg)
					QMessageBox.information(self,'Ready','File Saved as'
							' {:}'.format(outname.split('/')[-1]))
				except NameError as e:
					QMessageBox.warning(self,'Error', str(e) +
											'\nNo data for this correction')
					pass
			elif okPressed and item == 'Curvature and resampled':
				try:
					outname = saveCurvature(t_ga_res, amp_res, tapr_res, amp1_res)
					answer = QMessageBox.question(self, 'sac',
											'Save as sac format?',
						QMessageBox.Yes | QMessageBox.No)
					if answer == QMessageBox.Yes:
						savesac(t_ga_res, amp_res, datafile, outname)
						savesac(tapr_res, amp1_res, datafile, outname)
						QMessageBox.information(self,'Ready','File Saved as'
						'{0:} and {1:}'.format(outname.split('/')[-1], outname.split('/')[-1]))
				except FileNotFoundError:
					pass
				except NameError as e:
					QMessageBox.warning(self,'Error', str(e) +
											'\nNo data for this correction')
					pass
			elif okPressed and item == 'Resampled':
				try:
					outname = saveResampled(tres, amp_res)
					QMessageBox.information(self,'Ready','File Saved as'
							' {:}'.format(outname.split('/')[-1]))
				except NameError as e:
					QMessageBox.warning(self,'Error', str(e) +
											'\nNo data for this correction')
					pass
			elif okPressed and item == 'Instrumental Response':
				try:
					outname = saveInstrumento(treg, amp_correct)
					answer = QMessageBox.question(self, 'sac',
											'Save as sac format??',
						QMessageBox.Yes | QMessageBox.No)
					if answer == QMessageBox.Yes:
						savesac(treg, amp_correct, datafile, outname)
						QMessageBox.information(self,'Ready','File Saved as' +
											' {:}'.format(outname.split('/')[-1]))
				except NameError as e:
					QMessageBox.warning(self,'Error', str(e) +
											'\nNo data for this correction')
					pass
		except NameError as e:
			QMessageBox.critical(self,'No Data',str(e)+'\nNo data to save')
	#####################################################################################

	def extraFunctions(self):
		self.nd = tabWindows()
		self.nd.show()

# # grab the dimensions of the image and calculate the center
# # of the image
# (h, w)=image.shape[:2]
# center=(w / 2, h / 2)
# # rotate the image by 180 degrees
# M=cv2.getRotationMatrix2D(center, 180, 1.0)
# rotated=cv2.warpAffine(image, M, (w, h))
# cv2.imshow("rotated", rotated)
# cv2.waitKey(0)
