#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: rdcorona
# @Date:   2020-02-25 16:56:16
# @Last Modified by:   rdcorona
# @Last Modified time: 2022-06-06 12:53:04

"""
Auxiliary Widget with Functions that
operate for the auxiliary module
 
"""
import sys
import os
import gc
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QTabWidget, QDialog
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QDialogButtonBox, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import cv2
from PIL import Image
import datetime
import re
from obspy.core import UTCDateTime
from obspy import Stream
from obspy.core.trace import Trace, Stats

Image.MAX_IMAGE_PIXELS = 999999999
path = os.getcwd()
nap = QApplication(sys.argv)
screen = nap.primaryScreen()
size = screen.availableGeometry()
width, height = size.width()/3, size.height()/3
ii = 0
data = {}
dicS = {}
gc.set_debug(gc.DEBUG_SAVEALL)
#################################  DIALOG BOX  ##########################################

class tabWindows(QDialog):
	'''
	Tab Window with Auxiliary functions
	'''

	def __init__(self):
		super().__init__()
		self.setFixedSize(int(width), int(height))
		DSpath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
								os.pardir))
		self.setWindowIcon(QIcon(DSpath + '/Images/logo.png'))
		self.setWindowTitle("Auxiliary Modules")

		fftWidget = QTabWidget()
		fftWidget.addTab(imageFunctionsTabe(), "Phase picking on raster image")
		fftWidget.addTab(fileFunctionsTabe(), "Recover clipped amplitudes and save as SAC/MINISEED")
		vbox = QVBoxLayout()
		vbox.addWidget(fftWidget)
		self.setLayout(vbox)
######################################   FIRST TAB   ####################################
 
class fileFunctionsTabe(QWidget):
	def __init__(self):
		super().__init__()
		self.initT1()

	def initT1(self):
		self.makeGroup2()
		self.makeGroup1()
		self.record()
		self.caBtn = QPushButton('Load &File', self)
		self.caBtn.resize(self.caBtn.sizeHint())
		self.caBtn.setStatusTip('Choose Seismogram ASCII File')
		self.caBtn.clicked.connect(self.getDataFile)
		self.mainLayout = QGridLayout()
		self.mainLayout.addWidget(self.caBtn, 0, 0)
		self.mainLayout.addWidget(self.imFilename, 0, 1)
		self.mainLayout.addWidget(self.restorClipped, 1, 0)
		self.mainLayout.addWidget(self.SaveSAC, 1, 1)
		self.setLayout(self.mainLayout)

	def record(self):
		self.imFilename = QLabel()

	def makeGroup1(self):
		self.restorClipped = QGroupBox('Recover Clipped Amplitudes', self)
		self.restorClipped.setStyleSheet('QGroupBox:title {'
					'subcontrol-origin: margin;'
					'subcontrol-position: top right;'
					'padding-left: 5px;'
					'padding-right: 5px; }')
		self.restorClipped.setStyleSheet('QGroupBox {'
					'font: bold;'
					'border: 1px solid silver;'
					'border-radius: 6px;'
					'margin-top: 6px; }')
		self.declabel = QLabel('Decimate Factor')
		self.decFactor = QLineEdit('4')
		self.asBtn = QPushButton('Restore Amplitude', self)
		self.asBtn.resize(self.asBtn.sizeHint())
		self.asBtn.setStatusTip('Help with clipped amplitudes')
		self.asBtn.clicked.connect(self.reduceClippedsignal)
		self.asBtn.setEnabled(False)

		self.gdBtn = QPushButton('Save restored Time Series', self)
		self.gdBtn.resize(self.gdBtn.sizeHint())
		self.gdBtn.setStatusTip('Save unclipped data')
		self.gdBtn.clicked.connect(self.saveData)
		self.gdBtn.setEnabled(False)

		self.fact = QHBoxLayout()
		self.fact.addWidget(self.declabel)
		self.fact.addWidget(self.decFactor)

		self.vbox0 = QVBoxLayout()
		self.vbox0.addLayout(self.fact)
		self.vbox0.addWidget(self.asBtn)
		self.vbox0.addWidget(self.gdBtn)
		self.restorClipped.setLayout(self.vbox0)
		# self.restorClipped.setMinimumSize()

	def makeGroup2(self):
		self.SaveSAC = QGroupBox('Save as SAC/MINISEED', self)
		self.SaveSAC.setStyleSheet('QGroupBox:title {'
					'subcontrol-origin: margin;'
					'subcontrol-position: top right;'
					'padding-left: 5px;'
					'padding-right: 5px; }')
		self.SaveSAC.setStyleSheet('QGroupBox {'
					'font: bold;'
					'border: 1px solid silver;'
					'border-radius: 6px;'
					'margin-top: 6px; }')
		self.dateLbl = QLabel('Eqk Date')
		self.hourLbl = QLabel('Eqk Hour (UTC)')
		self.net_staLbl = QLabel('Net,Sta,Cha')
		self.sdate = QLineEdit('yyyy/mm/dd')
		self.hour = QLineEdit('HH:MM:SS')
		self.net_sta = QLineEdit('NET.STA.HH?')
		self.addBt = QPushButton('Add trace to Stream', self)
		self.addBt.resize(self.addBt.sizeHint())
		self.addBt.clicked.connect(self.sacHeader)
		self.ok_btn = QDialogButtonBox(QDialogButtonBox.Save)
		self.ok_btn.clicked.connect(self.saveStr)
		self.ok_btn.setEnabled(False)

		self.labels = QVBoxLayout()
		self.lineEdit = QVBoxLayout()
		self.labels.addWidget(self.dateLbl)
		self.lineEdit.addWidget(self.sdate)
		self.labels.addWidget(self.hourLbl)
		self.lineEdit.addWidget(self.hour)
		self.labels.addWidget(self.net_staLbl)
		self.lineEdit.addWidget(self.net_sta)

		self.dataBox = QHBoxLayout()
		self.dataBox.addLayout(self.labels)
		self.dataBox.addLayout(self.lineEdit)

		self.concretbox = QVBoxLayout()
		self.concretbox.addLayout(self.dataBox)
		self.concretbox.addWidget(self.addBt)
		self.concretbox.addWidget(self.ok_btn)

		self.SaveSAC.setLayout(self.concretbox)
	################################# Functions #########################################
	# Load datafile and enable buttons

	def getDataFile(self):
		global amp, time, datafile, directory, date, tmp2
		datafile, _ = QFileDialog.getOpenFileName(self, 'Load Data File',
			path, "Text Files (*.txt *.dat);; All Files (*) ")
		if datafile:
			try:
				directory = datafile.split('/')
				date = directory[-1].split('.')
				year, month, day, sta = date[0], date[1], date[2], date[3]
				comp = date[4]
				self.imFilename.setText(f"File from record\n" +
										f"{year}.{month}.{day} {sta} {comp} {weight}")
				self.sdate.clear()
				self.net_sta.clear()
				self.sdate.setText(year+'/'+month+'/'+day)
				try:
					self.net_sta.setText(f"{tmp2[0]}.{sta}.HH{comp[0]}")
				except NameError:
					self.net_sta.setText(f"*net*.{sta}.HH{comp[0]}")
			except NameError:
				directory = datafile.split('/')
				self.imFilename.setText('DataFile: \n' + directory[-1])
			except IndexError:
				directory = datafile.split('/')
				self.imFilename.setText('DataFile: \n' + directory[-1])
			try:
				time, amp = np.loadtxt(datafile, unpack=True, dtype=float)
				# amp = np.genfromtxt(datafile, usecols=1, dtype=float)
				self.asBtn.setEnabled(True)
			except IndexError as e:
				QMessageBox.information(self, 'Error!',
					f'{e}  Incompatible File')
		else:
			QMessageBox.warning(self, 'Error!',
				'No file selected!')
			pass
	#####################################################################################

	def saveStr(self):
		global dicS, st, tmp2
		st = Stream()
		item = ('MINISEED', 'SAC')
		item, okPressed = QInputDialog.getItem(self,'Save Data',
								'AS : ',item, 0, False)
		if okPressed and item == 'MINISEED':
			outname, _ = QFileDialog.getSaveFileName(self, 'Save ASCII File ',
							f"stream.mseed", "Binary Files (*.sac *.mseed);; All files (*)")
			for key in dicS.keys():
				st += Stream(dicS[key])
			st.plot()
			st.write(outname, format='MSEED')
			QMessageBox.information(self, 'File', f"File saved")
			dicS = {}
			self.ok_btn.setEnabled(False)

		elif okPressed and item == 'SAC':
			for key in dicS.keys():
				dicS[key].write(f"{'/'.join(directory[:-1])}/{key[:-4]}.sac", format='SAC')
			QMessageBox.information(self, 'Sac File', 'All traces saved as sac')
			dicS = {}
			self.ok_btn.setEnabled(False)

	def sacHeader(self):
		global amp, time, directory, dicS, header
		header = Stats()
		try:
			self.sdate.text().split('/')
			self.hour.text().split(':')
			self.net_sta.text().split('.')
			try:
				if self.sdate.text() != 'yyyy/mm/dd':
					if self.hour.text() != 'HH:MM:SS':
						header.starttime = UTCDateTime(f"{self.sdate.text()},{self.hour.text()}")
					else:
						QMessageBox.critical(self, 'Error', 'Format error\n' +
							'No Date and Time on SAC file\n')
				else:
					QMessageBox.critical(self, 'Error', 'Format error\n' +
							'No Date and Time on SAC file\n')

			except TypeError as e:
				QMessageBox.critical(self, 'Error',
							'Information Format error '+str(e))
			try:
				tmp2 = self.net_sta.text().split('.')
				header.network = str(tmp2[0])
				header.station = str(tmp2[1])
				header.channel = str(tmp2[2])
			except NameError:
				QMessageBox.critical(self, 'Error', 'Information format error')
			try:
				header.delta = np.round(time[1] - time[0], 4)
				header.npts = int(len(amp))
			except NameError as e:
				QMessageBox.critical(self, 'Error', 'No File selected\n' +
					str(e))
			dicS[f"trace{directory[-1][0:-4]}"] = Trace(data=amp, header=header)

			QMessageBox.information(self, 'Info',
				f"{dicS[f'trace{directory[-1][0:-4]}']} added to stream")
			self.ok_btn.setEnabled(True)
		# 	sism.write(datafile[0:-4]+'.SAC', format='SAC')
		# 	QMessageBox.information(self, 'Sac File', 'SAC file save as\n' +
		# 							directory[-1][0:-4]+'.SAC')
		except IndexError as e:
			QMessageBox.critical(self, 'Error', str(e) +
								'\nwrong data format, try again')
			self.sdate.setText('yyyy/mm/dd')
			self.hour = QLineEdit('HH:MM:SS')
			self.net_sta = QLineEdit('NET.STA.BH*')
		except NameError as e:
			QMessageBox.critical(self, 'Error', str(e) +
							'\nMissing information for header')
	#####################################################################################
	# amplitude recovery

	def reduceClippedsignal(self):
		global nd, amp, time, vectorx, vectory
		import scipy.signal as ss
		from scipy.interpolate import interp1d
		import auxiliaryFunctions as af
		################### Functions #########################################
		nd = np.array(amp, copy=True)
		plt.clf()
		decFactor = int(self.decFactor.text())
		try:
			picclip = 50
			clippedTimes = af.select_mvc(time, amp, picclip*2)
			intervalue = np.array([])

			for i in range(len(clippedTimes)):
				intervalue = np.append(intervalue, clippedTimes[i][0])
			cont = 0
			indx = np.array([], dtype=int)
			for cont in intervalue:
				ind = af.find_nearest(time, cont)
				indx = np.append(indx, ind)
			if len(indx) % 2 == 0:
				for i in range(len(indx)):
					if i % 2 == 0:
						try:
							vectory = amp[indx[i]:indx[i+1]]
							vectorx = time[indx[i]:indx[i+1]]
							plt.figure(i)
							plt.title(f'Mark both the inicial and last sample\nof the clipped signal', fontsize=height*0.05)
							dect = ss.decimate((vectorx), decFactor, 3, zero_phase=True)
							deca = ss.decimate((vectory), decFactor, 3, zero_phase=True)
							plt.plot(dect, deca, 'o-k')
							dat = plt.ginput(2, timeout=-1)
							plt.close()
							inpt = np.array([], dtype=int)
							for x, y in dat:
								ipt = af.find_nearest(dect, x)  # vectorx
								inpt = np.append(inpt,ipt)
							di = deca[inpt[0]:inpt[-1]]
							xt = dect[inpt[0]:inpt[-1]]
							if min(di) > 0:
								m = np.array([max(di)/2, np.mean(di), -1])
							else:
								m = np.array([min(di)/2, np.mean(di),1])
							# vect = np.ones(a+7); fact=1e-3
							d = (m[0]*xt**0)+(m[1]*xt)+(m[2]*xt**2)
							Garr, m, d = af.deriviti(m, di, d, xt)
							dif = di-d
							dif = dif.reshape(len(dif),1)
							G = np.matrix(Garr)
							GtG, Gd = af.fixParameters(G, dif, xt, inpt, di)
							# dm = np.linalg.inv(np.transpose(G)*G) * (np.transpose(G)*dif)
							m = np.linalg.inv(GtG)*Gd
							m = np.array(m)
							m = m.reshape(len(m))
							d = np.array((m[0]*xt**0)+(m[1]*xt)+(m[2]*xt**2))
							d = d.reshape(len(np.transpose(d)))
							dif = di-d
							# ssq = np.sqrt(np.sum(dif*dif)/np.sum(d**2))
							plt.figure((i/2)+1)
							plt.plot(xt,di,xt,d,'r')
							deca[inpt[0]:inpt[-1]] = d
							inta = interp1d(dect, deca, kind='quadratic')(np.linspace(min(dect), max(dect), num=len(vectorx)))
							# Possible Bug
							nvectory = np.copy(inta)
							amp[indx[i]:indx[i+1]] = nvectory
						except ValueError as e:
							QMessageBox.critical(self,'Error',str(e)+'\n'
							'The marks around the saturated peak are close together '
							'or are not on either side of the waveform. You must repeat '
							'the dive for the peak '+str(int(i/2)))
			else:
				QMessageBox.info(message='You must pick on'
									'both sides of each clipped peak\n try again')
			plt.figure(0, figsize=(10,5))
			plt.plot(time,amp,'r')
			plt.plot(time, nd, 'k')
			plt.grid()
			plt.savefig(datafile[0:-4]+'.Recovered.png', dpi=300)
			self.gdBtn.setEnabled(True)
			plt.show()
		except NameError as e:
			QMessageBox.critical(self,'Error', str(e) +
							'\nNo input file')
			pass
	#####################################################################################
	# Save Data in ASCII format

	def saveData(self):
		global time, amp, nd
		try:
			datos = np.array([time, nd])
			datos = datos.T
			item = ('ASCII', 'SAC/MINISEED')
			item, okPressed = QInputDialog.getItem(self,'Save Data',
								'Format : ',item, 0, False)
			if okPressed and item == 'ASCII':
				outname, _ = QFileDialog.getSaveFileName(self, 'Save ASCII File ',
							datafile[0:-4]+'_new.txt', "Text Files (*.txt *.dat);; All files (*)")
				try:
					with open(outname, 'w+'):
						np.savetxt(outname, datos, fmt=['%e','%e'], delimiter='	')
				except FileNotFoundError:
					pass
			elif okPressed and item == 'SAC/MINISEED':
				self.sacHeader()
				self.saveStr()

		except NameError as e:
			QMessageBox.critical(self,'No Data',
								str(e)+'\nNo data found')
#########################################################################################
#################################  TAB 2 ################################################

class imageFunctionsTabe(QWidget):
	def __init__(self):
		super().__init__()
		self.initT2()

	def initT2(self):
		self.makeGroup1()
		self.makeGroup2()
		self.record()
		self.caBtn = QPushButton('Load Raster Image', self)
		self.caBtn.resize(self.caBtn.sizeHint())
		self.caBtn.setStatusTip('Choose Seismogram Raster')
		self.caBtn.clicked.connect(self.load_image)
		self.mainLayout = QGridLayout()
		self.mainLayout.addWidget(self.caBtn, 0,0)
		self.mainLayout.addWidget(self.imFilename, 0,1)
		self.mainLayout.addWidget(self.pickGroup, 1,1)
		self.mainLayout.addWidget(self.inputDataGroup, 1,0)
		self.setLayout(self.mainLayout)

	def record(self):
		self.imFilename = QLabel()

	def makeGroup1(self):
		self.pickGroup = QGroupBox('Phases Picking', self)
		self.pickGroup.setStyleSheet('QGroupBox:title {'
					'subcontrol-origin: margin;'
					'subcontrol-position: top right;'
					'padding-left: 5px;'
					'padding-right: 5px; }')
		self.pickGroup.setStyleSheet('QGroupBox {'
					'font: bold;'
					'border: 1px solid silver;'
					'border-radius: 6px;'
					'margin-top: 6px; }')
		self.seiScale = QPushButton('Seismogram Scale', self)
		self.seiScale.resize(self.seiScale.sizeHint())
		self.seiScale.setStatusTip('Select time marks for Seismogram scale')
		self.seiScale.clicked.connect(self.seismogramScale)
		self.seiScale.setEnabled(False)
		self.quikPick = QPushButton('Quick Pick', self)
		self.quikPick.resize(self.quikPick.sizeHint())
		self.quikPick.setStatusTip('Quick Pick phases per image Seismogram')
		self.quikPick.clicked.connect(self.QuikPick)
		self.quikPick.setEnabled(False)

		self.svBtn = QPushButton('Write S-file', self)
		self.svBtn.resize(self.svBtn.sizeHint())
		self.svBtn.setStatusTip('Save picked phases as S-file')
		self.svBtn.clicked.connect(self.writeSFile)
		self.svBtn.setEnabled(False)
		self.col = QVBoxLayout()
		self.col.addWidget(self.seiScale)
		self.col.addWidget(self.quikPick)
		self.col.addWidget(self.svBtn)
		self.pickGroup.setLayout(self.col)

	def makeGroup2(self):
		self.inputDataGroup = QGroupBox('Input Data For Quick Pick', self)
		self.inputDataGroup.setStyleSheet('QGroupBox:title {'
					'subcontrol-origin: margin;'
					'subcontrol-position: top right;'
					'padding-left: 5px;'
					'padding-right: 5px; }')
		self.inputDataGroup.setStyleSheet('QGroupBox {'
					'font: bold;'
					'border: 1px solid silver;'
					'border-radius: 6px;'
					'margin-top: 0px; }')
		refLab = QLabel('1st Time Mark Date-Time : ')
		self.phaseP = QLabel('P Phase Characteristics')
		self.phaseP.setAlignment(Qt.AlignCenter)
		self.phaseP.setStyleSheet("QLabel {background-self.color: skyblue;}")
		polLabP = QLabel('P polarity :')
		typLabP = QLabel('P arrival Quality : ')
		typLabS = QLabel('S arrival Quality : ')
		self.phaseS = QLabel('S Phase Characteristics')
		self.phaseS.setAlignment(Qt.AlignCenter)
		self.phaseS.setStyleSheet("QLabel {background-self.color: skyblue;}")
		self.rdt = QLabel('Record Date and Time')
		self.rdt.setAlignment(Qt.AlignCenter)
		self.rdt.setStyleSheet("QLabel {background-self.color: skyblue}")

		self.tmmark1 = QLineEdit('YYYY-mm-dd,HH:MM:SS')
		self.tmmark1.setAlignment(Qt.AlignLeft)
		self.tmmark1.setEnabled(False)
		self.tmmark1.setToolTip('Format year-month-day,hour:minute:second')
		stchLab = QLabel('Station and Channel :')
		self.sta_cha = QLineEdit('STA.BH?')
		self.sta_cha.setEnabled(False)
		self.sta_cha.setToolTip('STA=Station Code,  ?=Component')
		self.polarP = QComboBox(self)
		polarity = ['C','D']
		self.polarP.addItems(polarity)
		self.polarP.setEnabled(False)
		self.arrivTypeP = QComboBox(self)
		Quality = ['Impulsive','Emergent']
		self.arrivTypeP.addItems(Quality)
		self.arrivTypeP.setEnabled(False)
		self.arrivTypeS = QComboBox(self)
		self.arrivTypeS.addItems(Quality)
		self.arrivTypeS.setEnabled(False)
		weiLalP = QLabel('Weight for P: ')
		weiLalS = QLabel('Weight for S: ')
		items = ['0','1','2','3','4','9']
		self.weightP = QComboBox(self)
		self.weightP.addItems(items)
		self.weightP.setEnabled(False)
		self.weightS = QComboBox(self)
		self.weightS.addItems(items)
		self.weightS.setEnabled(False)
		##### Reference Time Mark #########
		self.refTimeMark = QGridLayout()
		self.refTimeMark.addWidget(refLab, 0,0)
		self.refTimeMark.addWidget(self.tmmark1, 1,0)
		self.refTimeMark.addWidget(stchLab, 0,1)
		self.refTimeMark.addWidget(self.sta_cha, 1,1)
		#####  P arrival characteristics ##
		self.PData = QGridLayout()
		self.PData.addWidget(polLabP, 0,0)
		self.PData.addWidget(self.polarP, 1,0)
		self.PData.addWidget(typLabP, 0,1)
		self.PData.addWidget(self.arrivTypeP, 1,1)
		self.PData.addWidget(weiLalP, 0,2)
		self.PData.addWidget(self.weightP, 1,2)
		#####  S arrival characteristics ##
		self.SData = QGridLayout()
		self.SData.addWidget(typLabS, 0,1)
		self.SData.addWidget(self.arrivTypeS, 1,1)
		self.SData.addWidget(weiLalS, 0,2)
		self.SData.addWidget(self.weightS, 1,2)
		self.dataBox = QVBoxLayout()
		self.dataBox.addWidget(QLabel(''))
		self.dataBox.addWidget(self.rdt)
		self.dataBox.addLayout(self.refTimeMark)
		self.dataBox.addWidget(self.phaseP)
		self.dataBox.addLayout(self.PData)
		self.dataBox.addWidget(self.phaseS)
		self.dataBox.addLayout(self.SData)
		self.dataBox.setContentsMargins(-1,0,-1,-1)
		self.inputDataGroup.setLayout(self.dataBox)
		# self.inputDataGroup.setFixedSize( width*0.45, height*0.7)
	#####################################################################################
	########################### FUNCTIONS ###############################################

	def load_image(self, event):
		global ii, dpi, img,  year, month, day, est, comp, hour
		global path, imagefile, directory
		imagefile, _ = QFileDialog.getOpenFileName(self, 'Load Seismogram Image',
			path, "Image Files (*.jpg *.png *.jpeg *.tif);; All files (*)")
		ii = ii+1
		path = os.path.split(imagefile)[0]
		if imagefile:
			try:
				# Split Image name separated by dots.
				directory = imagefile.split('/')
				date = directory[-1].split('.')
				year, month, day, est = date[0], date[1], date[2], date[3]
				comp, weight = date[4], date[5]
				self.tmmark1.setEnabled(True)
				self.sta_cha.setEnabled(True)
				self.imFilename.setText('Record Scanning of:\n ' +
					year + '.' + month + '.' + day + '-' + est + ' ' + comp + weight)
				self.sta_cha.clear()
				self.tmmark1.clear()
				self.sta_cha.setText(est+'.BH'+comp[0])
				try:
					self.tmmark1.setText(f"{year}-{month}-{day},{hour[0]}:{hour[1]}:{hour[2]}")
				except NameError:
					self.tmmark1.setText(f"{year}-{month}-{day},HH:MM:SS")
			except IndexError:
				directory = imagefile.split('/')
				self.imFilename.setText(f'Image: \n{directory[-1]}')
				self.tmmark1.setEnabled(True)
				self.sta_cha.setEnabled(True)
			img = cv2.imread(imagefile,0)
			try:
				iimg = Image.open(imagefile)
				dpi = iimg.info['dpi'][0]
				del iimg
				# gc.collect()
			except KeyError:
				(dpi, okPressed) = QInputDialog.getInt(self, 'Image DPI',
								'No DPI on image information. \n'
								'Input Image DPI: ',1200, 0, 3000, 2)
				if okPressed:
					dpi = float(dpi)
			except:
				QMessageBox.Critical(self,'Error!',
					'Without a DPI value, this module can not continue')
				sys.exit(1)
			rows, cols = img.shape[:2]
			# cv2.namedWindow(directory[-1], cv2.WINDOW_NORMAL)
			# cv2.imshow(directory[-1], img)
			# cv2.resizeWindow(directory[-1], (int(width*2),int(width*2*(rows/cols))))
			self.seiScale.setEnabled(True)
			self.quikPick.setEnabled(False)
			self.svBtn.setEnabled(False)
			self.polarP.setEnabled(False)
			self.arrivTypeP.setEnabled(False)
			self.arrivTypeS.setEnabled(False)
			self.weightP.setEnabled(False)
			self.weightS.setEnabled(False)
		else:
			QMessageBox.warning(self, 'Error!',
				'No image file selected!')
			pass
	#########################################################################################
	# Seismogram Scale

	def seismogramScale(self):
		global dot, vr, amp0, img
		img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
		dot = []

		def distance(event, x, y, flags, params):
			global dot
			if event == cv2.EVENT_LBUTTONDBLCLK:
				cv2.circle(img, (x, y), int(dpi*0.005), (0, 255, 0), -1)
				dot.append((x, y))

		QMessageBox.information(self, 'Instructions',
			'<P>DobleClick over at least <b>three continuous time marks</b> <br />'
			'on the same trace of the first arrival <br />'
			'Then press <b>"ESC"</b> to close the image and continue ')
		cv2.namedWindow(f'Pick Time Marks on {directory[-1]}', cv2.WINDOW_NORMAL)
		cv2.resizeWindow(f'Pick Time Marks on {directory[-1]}', (int(width*0.5), int(height*0.48)))
		cv2.setMouseCallback(f'Pick Time Marks on {directory[-1]}', distance)
		while True:
			cv2.imshow(f'Pick Time Marks on {directory[-1]}', img)
			k = cv2.waitKey(1)
			if k == 27 & 0xff:
				break
		cv2.destroyWindow('Pick Time Marks on '+directory[-1])
		try:
			dot = np.array(dot)
			suma = np.array([])
			for i in range(len(dot) - 1):
				suma = np.append(suma,dot[i+1,0]-dot[i,0])
			mean = np.mean(suma)
			vr = ((mean * 25.4) / dpi) / 60
			amp0 = (((dot[0,1] + dot[1,1]) / 2) / dpi) * 25.4
			self.quikPick.setEnabled(True)
		except:
			pass
	# cv2.waitKey(0)
	#####################################################################################
	# Quick phases pick

	def QuikPick(self):
		global phs, data, date, hour, img, xco
		phs = []
		D = {}
		#gc.collect()
		rows, cols = img.shape[:2]
		try:
			if re.match(r'[a-zA-Z]{3}.[bB]{1}[a-zA-Z]{2}$',self.sta_cha.text()):
				D['Sta'] = self.sta_cha.text().split('.')[0]
				D['Chan'] = self.sta_cha.text().split('.')[1]
			elif re.match(r'[a-zA-Z]{4}.[bB]{1}[a-zA-Z]{2}$',self.sta_cha.text()):
				D['Sta'] = self.sta_cha.text().split('.')[0]
				D['Chan'] = self.sta_cha.text().split('.')[1]
			elif re.match(r'[a-zA-Z]{5}.[bB]{1}[a-zA-Z]{2}$',self.sta_cha.text()):
				D['Sta'] = self.sta_cha.text().split('.')[0]
				D['Chan'] = self.sta_cha.text().split('.')[1]
			else:
				QMessageBox.information(self,'',D['Sta']+','+D['Chan'])
			datetime.datetime.strptime(self.tmmark1.text().split(',')[1], '%H:%M:%S')
			datetime.datetime.strptime(self.tmmark1.text().split(',')[0], '%Y-%m-%d')
			self.polarP.setEnabled(True)
			self.arrivTypeP.setEnabled(True)
			self.arrivTypeS.setEnabled(True)
			self.weightP.setEnabled(True)
			self.weightS.setEnabled(True)

			def extracPhasesData(dpi, vr, phs):
				tph = ((phs[:,0]/dpi) * 25.4) / vr
				datetime.datetime.strptime(self.tmmark1.text().split(',')[1], '%H:%M:%S')
				datetime.datetime.strptime(self.tmmark1.text().split(',')[0], '%Y-%m-%d')
				D['1tm_Date'] = self.tmmark1.text().split(',')[0]
				D['1tm_Time'] = datetime.datetime.strptime(self.tmmark1.text().split(',')[1],
									'%H:%M:%S').strftime('%H:%M:%S')
				hour = D['1tm_Time'].split(':')
				date = D['1tm_Date'].split('-')
				D['Ptime'] = (datetime.datetime.strptime(self.tmmark1.text().split(',')[1],
					'%H:%M:%S') + datetime.timedelta(seconds=float(tph[1]-tph[0]))).strftime('%H:%M:%S.%f')
				D['Stime'] = (datetime.datetime.strptime(self.tmmark1.text().split(',')[1],
					'%H:%M:%S') + datetime.timedelta(seconds=float(tph[2]-tph[0]))).strftime('%H:%M:%S.%f')
				D['polarP'] = self.polarP.currentText()
				D['QualityP'] = self.arrivTypeP.currentText()
				D['QualityS'] = self.arrivTypeS.currentText()
				D['weightP'] = int(self.weightP.currentText())
				D['weightS'] = int(self.weightS.currentText())
				if len(tph) > 3:
					D['coda'] = tph[-1]-tph[0]
				return D,date,hour
			#############################################################
			QMessageBox.information(self,'Instructions',
			'<P>The first double click will be on the reference time mark <br />'
			'the following double clicks will be to identify the phases P and S <br />'
			'You can repeat a Phase pick with <b> "z"</b> <br />'
			'Optionally you can pick duration time <b>(coda)</b> <br />'
			'Before close the Raster image <b><FONT COLOR="#FF0000"> define polarity, quality and weight </FONT>'
			'of each picked phases.</b> on the Dialog Frame <br />'
			'"z"   Undo the last marked point <br />'
			'By pressing <b>"Esc"</b>, the process ends and the image closes</P>')

			def getPhases(event,x,y,flags,params):
				global phs, xco
				if event == cv2.EVENT_LBUTTONDBLCLK:
					#cv2.rectangle(clone,(x,y-int(rows/4)),(x,y+int(rows/4)),(0,0,255),int(dpi/500))
					phs.append((x,y))
					if len(phs) == 2:
						(TS, okPressed) = QInputDialog.getDouble(self, 'Image DPI',
							'Did you know approximately how many seconds after P-phase, is S-phase?\n'
							"If you don't know, close this pop-up window\n"
							'Approx S-phase time: ',60, 0, 3000, 2)
						if okPressed:
							xco = int(((TS*vr)/25.4) * dpi)
							# xco = int(((TS * dpi) / 25.4) * vr)
							cv2.rectangle(img,(x+xco,y-int(rows/10)),(x+xco,y+int(rows/10)),(0,255,0),int(dpi/200))
						else:
							pass

			cv2.namedWindow(f'Pick Phases on {directory[-1]}', cv2.WINDOW_NORMAL)
			cv2.resizeWindow(f'Pick Phases on {directory[-1]}', (int(width*0.5), int(height*0.48)))
			cv2.setMouseCallback(f'Pick Phases on {directory[-1]}', getPhases)
			while True:
				for x1,y1 in phs:
					cv2.rectangle(img,(x1,y1-int(rows/4)),(x1,y1+int(rows/4)),(0,0,255),int(dpi/200))

				cv2.imshow(f'Pick Phases on {directory[-1]}',img)
				k = cv2.waitKey(1)
				if k == ord('z'):
					phs = phs[:len(phs) - 1]
				elif k == 27 & 0xff:
					break

			cv2.destroyWindow(f'Pick Phases on {directory[-1]}')
			print(':D')
			#cv2.waitKey(0)
			try:
				phs = np.array(phs)
				data[directory[-1][:-4]], date, hour = extracPhasesData(dpi, vr, phs)
				QMessageBox.information(self,'Saved', 'Information Stored')
			except KeyError as e:
				QMessageBox.information(self,'Try again', str(e) +
					" data missing \n Reference time mark, P and S needed")
			self.polarP.setEnabled(False)
			self.arrivTypeP.setEnabled(False)
			self.arrivTypeS.setEnabled(False)
			self.weightP.setEnabled(False)
			self.weightS.setEnabled(False)
			self.svBtn.setEnabled(True)

		except KeyError as e:
			QMessageBox.warning(self, 'Error!', f'{e} wrong format.\n Correct and try again')
		except ValueError as e:
			QMessageBox.warning(self, 'Error!', str(e))
		except:
			pass
	#####################################################################################

	def writeSFile(self):
		global data, sfileout
		import datetime as dati
		now = str(dati.datetime.now())
		Sf_name = date[2]+'-'+hour[0]+hour[1]+'-'+hour[2]+'R.S'+date[0]+date[1]
		if os.path.exists(path+'/'+Sf_name) and os.stat(path+'/'+Sf_name).st_size > 0:
			f = open(path+'/'+Sf_name,'a')
		else:
			f = open(path+'/'+Sf_name,'w+')
			idd = date[0]+date[1]+date[2]+hour[0]+hour[1]+hour[2]
			f.seek(0)
			f.write(" %4i %2i%2i " % (int(date[0]), int(date[1]), int(date[2])))
			f.write("%2i%2i %4.1f %s %57i\n" % (int(hour[0]),int(hour[1]),float(hour[2]),'R',1))  # line one
			f.write(" %10s %14s %15s%14s %3s%15s%5s\n" % ('ACTION:NEW',now[2:16],'OP:rdcf STATUS:','','ID:',idd +'d','I'))
			f.write(" %-30s %48i\n" % (directory[-1],6))
			f.write(" STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO AIN AR TRES W  DIS CAZ7\n")
		for d_key in data.keys():
			o = data[d_key]
			if 'coda' in o.keys():
				f.write(" %-5s%1s%1s %1s%-4s%1i %1s %2i%2i%6.2f %4i \n" % (o['Sta'],o['Chan'][-2],o['Chan'][-1],
					o['QualityP'][0],'P',o['weightP'],o['polarP'],int(o['Ptime'][0:2]),int(o['Ptime'][3:5]),
					float(o['Ptime'][6:-1]),int(o['coda'])))
				f.write(" %-5s%1s%1s %1s%-4s%1i %1s %2i%2i%6.2f %4i \n" % (o['Sta'],o['Chan'][-2],o['Chan'][-1],
					o['QualityS'][0],'S',o['weightS'],' ',int(o['Stime'][0:2]),int(o['Stime'][3:5]),
					float(o['Stime'][6:-1]),int(o['coda'])))
			else:
				f.write(" %-5s%1s%1s %1s%-4s%1i %1s %2i%2i%6.2f \n" % (o['Sta'],o['Chan'][-2],o['Chan'][-1],
					o['QualityP'][0],'P',o['weightP'],o['polarP'],int(o['Ptime'][0:2]),int(o['Ptime'][3:5]),
					float(o['Ptime'][6:-1])))
				f.write(" %-5s%1s%1s %1s%-4s%1i %1s %2i%2i%6.2f \n" % (o['Sta'],o['Chan'][-2],o['Chan'][-1],
					o['QualityS'][0],'S',o['weightS'],' ',int(o['Stime'][0:2]),int(o['Stime'][3:5]),
					float(o['Stime'][6:-1])))
		f.close()
		QMessageBox.information(self,'Saved','File saved as : ' + Sf_name)
	cv2.destroyAllWindows()
#########################################################################################

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = tabWindows()
	ex.show()
	sys.exit(app.exec_())
