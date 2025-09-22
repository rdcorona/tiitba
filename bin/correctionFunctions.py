# -*- coding: utf-8 -*-
# @Author: rdcorona
# @Date:   2021-03-09 10:27:51
# @Last Modified by:   rdcorona
# @Last Modified time: 2022-06-30 11:06:13


def detrend(t, a, ntrv=60):
	"""
	De trend time series en overlapped at ntrv time window windows 
	by the first derivative and a second degree polynomial function 

	:type t: array_like()
	:param t: time array
	:type a: array_like()
	:param a: amplitude array
	:type ntrv: int
	:param ntrv: time windows size 

	"""
	from scipy.interpolate import interp1d
	from obspy.signal import detrend
	import numpy as np
	a = a - a[0]
	t = t - t[0]
	dt = np.round(t[1] -t[0], 2)
	ki = 0
	kf = 1
	ke = 0
	ipb = 1
	amp1 = np.array([]) 
	tder = np.array([]) 
	der = np.array([]) 

	while ke < len(a):
		ke = (np.abs(t - ntrv * ipb/2)).argmin()
		tder = np.append(tder, (t[kf]+t[ke])/2) # derivative time
		der = np.append(der, np.mean(a[kf:ke]))
		kf = ki 
		ki = ke
		ipb += 1
		if ke==kf==ki:
			break

	interp = interp1d(np.array(tder), np.array(der), kind='previous', fill_value="extrapolate")
	der = interp(np.sort(t))

	amp1 = a - der
	# for kf in range(int(ntrv/dt), len(a), int(ntrv/dt)):
	# 	if (len(a) - kf) < int(ntrv/dt):
	# 		s2 = polynomial(a[ki:], 2)
	# 		s2 = s2 - s2[0] 
	# 		# s2 = s2 - (s2[0] - s1[-1]) 
	# 		# s2 = s2 + (s1[-1] - s1[-2]) # time series continuity 
	# 		amp1 = np.append(amp1, s2 )
	# 	else:
	# 		s2 = polynomial(a[ki:kf], 2)
	# 		s2 = s2 - s2[0]
	# 		# try:
	# 		# 	s2 = s2 - (s2[0] - s1[-1])
	# 		# 	s2 = s2 + (s1[-1] - s1[-2])
	# 		# except:
	# 		# 	pass
	# 		amp1 = np.append(amp1, s2)
		
	# 	ki = kf
	# 	s1 = s2
	
	# amp1 = amp1 - amp1[0]
	return t, amp1

def GandA94(treg, amp, vr, R, ampinfl):
	"""
	Curvature correction with the Grabrovec and Allegretti (1994) equation. Additionally approximate by leas squares the time series to ensure progressive time

	:type treg: array_like()
	:param treg: sampled time  (evenly sampled or not)
	:type amp: array_like()
	:param amp: amplitudes
	:type vr: float
	:param vr: Paper Drum Speed Rotation in mm/s 
	:type R: float
	:param R: Stylet length in mm
	:type ampinfl: float
	:param ampinfl: Amplitude of inflection point of the curvature in the amplitudes array

	"""
	import numpy as np
# parameters and variables for loop
	sign0 = np.sign(amp[0])
	ki, kf = 0, 1
	tint = [] # np.empty(len(treg), dtype='float')
	while kf < len(treg) - 1:
		if np.sign(amp[kf]) != sign0:
			sign0 = np.sign(amp[kf])
			tint[ki:kf] = (np.linspace(treg[ki], treg[kf], kf-ki + 1))
			ki = kf
		kf = kf + 1
	tint[ki:] = (np.linspace(treg[ki], treg[-1], len(treg)-ki))
	tapr = np.array(tint).T
	del tint
# times by Grabrovec and Allegretti (1994) equation
	X = treg * vr
	amp2 = amp - ampinfl
	ki, kf = 0, 1
	t_ga = np.empty(len(treg), dtype=np.float64)
	sign1 = np.sign(amp2[0])

	# for ii in range(len(treg)):
	# 	t_ga[ii] = (X[ii]-X[0]- (R - np.sqrt(R**2 - (amp[ii]-amp[0])**2))) / vr +treg[ii]

	while kf < len(treg) - 1:
		if np.sign(amp2[kf]) != sign1:
			sign1 = np.sign(amp2[kf])
			t_ga[ki:kf] = (X[ki:kf] - X[ki] - (R - np.sqrt(R**2 - (amp2[ki:kf] - amp2[ki])**2))) / vr + treg[ki]
			ki = kf
		kf = kf + 1
	t_ga[ki:] = (X[ki:] - X[ki] - (R - np.sqrt(R**2 -
					(amp2[ki:])**2))) / vr + treg[ki]
	for i in range(len(t_ga)-1):
		if t_ga[i+1] <= t_ga[i]:
			t_ga[i-1:i+2] = np.sort(t_ga[i-1:i+2])
	t_ga = np.array(t_ga).T
# Linear approximation between re sampled and recovered times by G&A94
# progressive time values
	N = len(treg)
	G = np.transpose(np.matrix([np.ones(N), tapr.T]))
	ssq1 = np.sqrt(np.sum((t_ga - tapr)**2) / np.sum(tapr ** 2))
	ssq = 10000
	damp = np.eye(G.shape[1]) * 0.001
	sign0 = np.sign(amp[0])
	while ssq - ssq1 > 0.001:
		ki = 0
		ssq = ssq1
		for kf in range(1, len(treg)):
			if np.sign(amp[kf])!= sign0:
				mest = np.dot(np.linalg.inv(np.dot(G[ki:kf,0:].T, G[ki:kf,0:])+damp), np.dot(G[ki:kf,0:2].T, t_ga[ki:kf]).T)
				tapr[ki:kf] = (G[ki:kf,0:] * mest).ravel()
				ki = kf
		mest = np.dot(np.linalg.inv(np.dot(G[ki:,0:].T, G[ki:,0:])+damp), np.dot(G[ki:,0:2].T, t_ga[ki:]).T)
		tapr[ki:] = (G[ki:,0:] * mest).ravel()
		ssq1 = np.sqrt(np.sum((t_ga - tapr)**2) / np.sum(tapr ** 2))

	ind = np.argwhere(tapr > 0.0)[0][0]
	tapr[:ind] = np.linspace(0,tapr[ind]-0.001,ind)

	return tapr, t_ga

## Re-sample function

def resample(old_time, data, sps, kind):
	"""
	Time series re-sample spline quadratic interpolation
	:type old_time: array_like()
	:param old_time: sampled time  (evenly sampled or not)
	:type data: array_like
	:param data: Array to interpolate.
	:type sps: float()
	:param sps: Sampling rate
	:type kind: str
	:param kind: spline interpolation order (slinear=1, quadratic=2, cubic=3)

	"""
	import numpy as np
	from scipy.interpolate import InterpolatedUnivariateSpline
	import obspy.signal.interpolation as osi
	from obspy.signal.headers import clibsignal
	
	# old_time = old_time - old_time[0]

	# Ensure consecutive times
	while len(np.unique(old_time)) != len(old_time):
		for t in range(len(old_time) - 2):
			if old_time[t+1] <= old_time[t] and old_time[t+2] > old_time[t]:
				deltat = (old_time[t+2] - old_time[t]) / 2 
				old_time[t+1] = old_time[t] + deltat
			elif old_time[t+1] <= old_time[t]:
				old_time[t+1] = old_time[t] + 0.005

	s_map = {
		"slinear": 1,
		"quadratic": 2,
		"cubic": 3
	}
	if kind in s_map:
		kind = s_map[kind]

	dt = 1/sps
	at = np.arange(old_time.min(), old_time.max() + 0.2, 0.2)
	aa = InterpolatedUnivariateSpline(np.sort(old_time), data, k=kind)(at)
	# new_time = np.arange(old_time.min(), old_time.max() + dt, dt)
	new_time = np.arange(old_time.min(), at.max(), dt)
	old_dt = at[1]-at[0]
	# m = np.diff(data) / old_dt
	# w = np.abs(m)
	# w = 1.0 / np.clip(w, np.spacing(1), w.max())

	# slope = np.empty(len(data), dtype=np.float64)
	# slope[0] = m[0]
	# slope[1:-1] = (w[:-1] * m[:-1] + w[1:] * m[1:]) / (w[:-1] + w[1:])
	# slope[-1] = m[-1]

	# # If m_i and m_{i+1} have opposite signs then set the slope to zero.
	# # This forces the curve to have extrema at the sample points and not
	# # in-between.
	# sign_change = np.diff(np.sign(m)).astype(np.bool)
	# slope[1:-1][sign_change] = 0.0

	# derivatives = np.empty((len(data), 2), dtype=np.float64)
	# derivatives[:, 0] = data
	# derivatives[:, 1] = slope

	# Create interpolated value using hermite interpolation. In this case
	# it is directly applicable as the first derivatives are known.
	# Using scipy.interpolate.piecewise_polynomial_interpolate() is too
	# memory intensive
	# amp_res = np.empty(len(new_time), dtype=np.float64)
	# clibsignal.hermite_interpolation(data, slope, new_time, amp_res,
	# 			len(data), len(amp_res), old_dt, old_time.min())

	# print(old_time.min(), new_time.min(), at.max(), new_time.max())
	amp_res = osi.lanczos_interpolation(aa, at.min(), old_dt, new_time.min(), dt, len(new_time), 20)
	# amp_res = osi.weighted_average_slopes(aa, old_time.min(), old_dt, old_time.min(), dt, len(new_time))

	# amp_res = osi.interpolate_1d(aa, 0.0, at[1]-at[0], 0.0, new_time[1]-new_time[0], int(np.round(at[-1] * sps, 0)), type="cubic")

	# a_rc = interp1d(at, aa, kind='quadratic')
	# amp_res = a_rc(new_time)

	return new_time, amp_res

## Instrumetla Response
def taper(t, a, percent=0.08):
	"""
	Applies a Santoyo-Sesma tapper to the corrected time series signal
	
	:type t: array_like()
	:param t: time array
	:type a: array_like()
	:param a: amplitude array
	:type percent: float
	:param percent: percentage of max time to tapper at the begging an the end 
	"""
	import numpy as np
	N = len(a)
	lim = t.max() * percent
	t1 = t[np.abs((t-lim)).argmin()]
	t2 = t[np.abs(t -(t.max()- t1)).argmin()]
	tapper = np.ones(N)
	for i in range(N):
		if t[i] <= t1:
			tapper[i] = 0.5 * (1+np.cos(np.pi * (1+(t[i]/t1))))
		elif t[i] >= t2:
			tapper[i] = 0.5 * (1+np.cos(np.pi * ((t[i]-t2)/ (t.max()-t2))))

	return tapper * a
	 
def wichertResponse(t, a, T0, epsilon, V0, wat_level, deconv=True):
	import time
	import numpy as np
	N = len(a)
	if N % 2 == 0:
		Nmedios = int(N/2)
	else:
		Nmedios = int((N/2)+1)
	dt = np.round(t[1] - t[0], 3)
	fN = 1/(2*dt)
	df = 1/(N*dt) 
	ff = df*N
	fq = np.fft.fftfreq(N, d=dt)
	fr = np.linspace(0, fN, Nmedios)
	w = fr*2*np.pi
	ini = time.time()
	sis_f = np.fft.fft(a)
	W0 = 2*np.pi/T0  # Angular undamped frequency
# Damping constant based on the rate damping
	ds = np.log(epsilon)/np.sqrt(np.pi**2+np.log(epsilon)**2)
# transfer function
	H_w = V0*(w**2/np.sqrt(((W0**2 - w**2)**2) + (4*ds**2*W0**2*w**2)))
	# water level
	for j in range(0,len(fr)-1):
		if H_w[j] < max(H_w) * wat_level:
			H_w[j] = max(H_w) * wat_level
	HW = np.empty(N)
	HW[0:Nmedios] = H_w
	for j in range(0,int(N/2)):
		HW[Nmedios+j] = H_w[Nmedios-j-1]
# Devonculution or convolution 
	if deconv:
		sis_corr = sis_f / HW
	else:
		sis_corr = sis_f * HW
	amp_correct = np.fft.ifft(sis_corr)
	amp_correct = amp_correct.real
	end = time.time()
	return fq, Nmedios, H_w, sis_f, amp_correct, ini, end

def polesAndZeros(t,a, PolesZeros):
	from obspy.core import Trace, Stats 
	## Creates the PAZ dictionary for the Galitzin instrument

	header = Stats()
	sis = Trace(data=a, header=header)

	paz_vert = { 
		"poles": [-0.524 + 0.00j, -0.524 + 0.00j, -0.524 + 0.00j, -0.524 + 0.00j],
		"zeros": [0.0 +0j, 0.0 + 0j, 0.0 + 0j],
		"gain": 727,
		'sensitivity': 727*1.614}
	 
	paz_hor = { 
		"poles": [-0.257 + 0.00j, -0.257 + 0.00j, -0.257 + 0.00j, -0.257 + 0.00j],
		"zeros": [0.0 +0j, 0.0 + 0j, 0.0 + 0j],
		"gain": 311,
		"sensitivity": 311*0.793}

	
	sis.sismulate(paz_remove=paz_vert)

	return sis.data()
	pass

### Save data 
def saveData(t, a, outname):
	import numpy as np
	data = np.array([t, a])
	data = data.T
	with open(outname, 'w+'):
		np.savetxt(outname, data, fmt=['%e','%e'], delimiter='	')

### Polarity
def chPolarity(a):
	return a * -1
