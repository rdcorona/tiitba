#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: rdcorona
# @Date:   2021-04-22 17:04:43
# @Last Modified by:   RDCoronaSismo
# @Last Modified time: 2022-02-24 20:54:46
"""
Auxiliary functions for Auxiliary modules of TIITBA GUI.

"""
import numpy as np
import matplotlib.pyplot as plt

def select_mvc(x, y, nitems):
	from matplotlib.widgets import Cursor
	"""
	This function allows to pick on a seismogram image to obtain coordinates

	:type x: array_like
	:param x: time array
	:type y: array_like
	:param y: amplitude array
	:type nitems: int
	:param nitems: number of points to pick on images
	:rtype: list
	:retuns: list of tuples with the coordinates of the picked points
	"""
	fs = 16
	fig, ax = plt.subplots(1, 1, figsize=(10,5))
	ax.set_title('Zoom on the clipped area, \npress space-bar when ready to'
				' select clipped peaks', fontsize=fs)
	ax.plot(x, y, 'k', lw=0.75)
	cursor = Cursor(ax, useblit=True, color='r', linewidth=0.75)
	zoom_ok = False
	while not zoom_ok:
		zoom_ok = plt.waitforbuttonpress()
	plt.title('Click on both sides of clipped peaks\npress enter'
				' when you finish', fontsize=fs)
	val = fig.ginput(nitems, timeout=-1)
	plt.close()
	return val

def find_nearest(array, value):
	"""
	Function for find the nearest index value to a given coordinate
	:type array: array_like
	:param array: time array
	:type value: int
	:param value: time coordinate value
	:rtype: list
	:retuns: list of index
	"""
	array = np.asarray(array)
	idx = (np.abs(array - value)).argmin()
	return idx

def deriviti(prms, directdata, modeldata, vector):
	"""
	Deriviti function

	:type prms: array_like / list
	:param prms: parameters for least squares approximation "m" it could be an array or a list
	:type directdata: array_like
	:param directdata: observed data
	:type modeldata: array_like
	:param modeldata: estimated data
	:type vector: array_like / list
	:param vector: array or list of the observed values that will dampen the solution by least squares
	:retuns: (G, prms, d) G matrix least square like; prms least square parameters; d estimated data by least square

	"""
	aa = len(prms)
	nn = len(directdata)
	delm = prms/1000
	G = np.ones([nn,3])
	for jj in range(aa):
		prms[jj] = prms[jj] + delm[jj]
		d = (prms[0]*vector**0)+(prms[1]*vector)+(prms[2]*vector**2)
		d2 = d
		prms[jj] = prms[jj]-2*delm[jj]
		d = (prms[0]*vector**0)+(prms[1]*vector)+(prms[2]*vector**2)
		d1 = d
		prms[jj] = prms[jj] + delm[jj]
		G[0:nn, jj] = (d2-d1)/(2*delm[jj])
	return G, prms, d


def fixParameters(G, dif, vector, indx, di):
	"""
	Restrict parameters function
	:type G: numpy.array()
	:param G: G matrix for least squares approximation 
	:type dif: array_like
	:param dif: difference between observed and estimated data
	:type vector: array_like / list
	:param vector: array or list of the observed values that will dampen the solution by least squares
	:type indx: list
	:param indx: list of index
	:type di: array_like
	:param di: estimated data
	:rtype: matrix_matrix
	:returns: (GtG, Gd) GtG G transpose x G matrix; G transpose x dif 
	"""
	GtG = np.transpose(G)*G
	Gd = np.transpose(G)*dif
	h = np.array([])
	v = np.array([])
# Solution Restrictions
	h = np.append(h,1)
	h = np.append(h,vector[0])
	h = np.append(h,vector[0]**2)
	v = np.append(v,1)
	v = np.append(v,vector[0])
	v = np.append(v,vector[0]**2)
	v = np.append(v,0)
	s = di[0]
	GtG = np.hstack([GtG, h.reshape(3,1)])
	GtG = np.vstack([GtG,v])
	Gd = np.vstack([Gd,s])
# 2do
	h = np.array([])
	v = np.array([])
	h = np.append(h,1)
	h = np.append(h,vector[-1])
	h = np.append(h,vector[-1]**2)
	h = np.append(h,0)
	v = np.append(v,1)
	v = np.append(v,vector[-1])
	v = np.append(v,vector[-1]**2)
	v = np.append(v,0)
	v = np.append(v,0)
	s = di[-1]
	GtG = np.hstack([GtG, h.reshape(4,1)])
	GtG = np.vstack([GtG,v])
	Gd = np.vstack([Gd,s])
# 3er
	h = np.array([])
	v = np.array([])
	h = np.append(h,1)
	h = np.append(h,vector[1])
	h = np.append(h,vector[1]**2)
	h = np.append(h,0)
	h = np.append(h,0)
	v = np.append(v,1)
	v = np.append(v,vector[1])
	v = np.append(v,vector[1]**2)
	v = np.append(v,0)
	v = np.append(v,0)
	v = np.append(v,0)
	s = di[1]
	GtG = np.hstack([GtG, h.reshape(5,1)])
	GtG = np.vstack([GtG,v])
	Gd = np.vstack([Gd,s])
	return GtG, Gd

