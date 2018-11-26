# Filename: shalib.py

# Description: SHA-256 Library Functions

# Date: 20181123 -- ZDH

import sys
import binascii
import math

sbox_vals = [["63","7c","77","7b","f2","6b","6f","c5","30","01","67","2b","fe","d7","ab","76"],
	["ca","82","c9","7d","fa","59","47","f0","ad","d4","a2","af","9c","a4","72","c0"],
	["b7","fd","93","26","36","3f","f7","cc","34","a5","e5","f1","71","d8","31","15"],
	["04","c7","23","c3","18","96","05","9a","07","12","80","e2","eb","27","b2","75"],
	["09","83","2c","1a","1b","6e","5a","a0","52","3b","d6","b3","29","e3","2f","84"],
	["53","d1","00","ed","20","fc","b1","5b","6a","cb","be","39","4a","4c","58","cf"],
	["d0","ef","aa","fb","43","4d","33","85","45","f9","02","7f","50","3c","9f","a8"],
	["51","a3","40","8f","92","9d","38","f5","bc","b6","da","21","10","ff","f3","d2"],
	["cd","0c","13","ec","5f","97","44","17","c4","a7","7e","3d","64","5d","19","73"],
	["60","81","4f","dc","22","2a","90","88","46","ee","b8","14","de","5e","0b","db"],
	["e0","32","3a","0a","49","06","24","5c","c2","d3","ac","62","91","95","e4","79"],
	["e7","c8","37","6d","8d","d5","4e","a9","6c","56","f4","ea","65","7a","ae","08"],
	["ba","78","25","2e","1c","a6","b4","c6","e8","dd","74","1f","4b","bd","8b","8a"],
	["70","3e","b5","66","48","03","f6","0e","61","35","57","b9","86","c1","1d","9e"],
	["e1","f8","98","11","69","d9","8e","94","9b","1e","87","e9","ce","55","28","df"],
	["8c","a1","89","0d","bf","e6","42","68","41","99","2d","0f","b0","54","bb","16"]]

mixCol_vals = [[2,3,1,1], [1,2,3,1], [1,1,2,3], [3,1,1,2]]
invMixCol_vals = [[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]

def CRShift(inval, bits, width=32):
	mask = 0xFFFFFFFF
	newval = ((inval >> bits) | (inval << (width - bits))) & mask
	return newval

def CLShift(inval, bits, width=32):
	mask = 0xFFFFFFFF
	newval = ((inval << bits) | (inval >> (width - bits))) & mask
	return newval

def str2hex (txt):
	hextext = []
	for i in range(len(txt)):
		hextext.append(binascii.hexlify(txt[i]))
	return hextext

def hex2str (hexlist):
	s = ""

	#2D List
	if checkDimension(hexlist) > 1:
		hexlist = Delete_0x(hexlist)
		for i in range(len(hexlist)):
			for j in range(len(hexlist[0])):
				temp  = str(hexlist[i][j])
				temp = temp[0:].zfill(2)
				s+=temp
	else:
		for i in range(len(hexlist)):
			temp  = str(hexlist[i])
			temp = temp[0:].zfill(2)
			s+=temp
			
	return s

def hex2ascii (txt):
	outstr = ""
	for i in range(len(txt)):
		for j in range(len(txt[0])):
			outstr+=binascii.unhexlify(txt[i][j])
	return outstr

def XORmat(m1,m2):
	outmat = []
	
	m1 = Delete_0x(m1)
	m2 = Delete_0x(m2)

	if checkDimension(m1) > 1:
		for i in range(len(m1)):
			temp = []
			for j in range(len(m2[0])):
				temp.append(str(hex(int(m1[i][j], 16) ^ int(m2[i][j], 16))))
			outmat.append(temp)
	else:
		for i in range(len(m1)):
			outmat.append(str(hex(int(m1[i], 16) ^ int(m2[i], 16))))
	return outmat

def sbox(m):
	outmat = []

	# 2D List
	if checkDimension(m) > 1:
		m = Delete_0x(m)

		for i in range(len(m)):
			temp = []
			for j in range(len(m[0])):
				temp.append(sbox_vals[int((int(m[i][j], 16) >> 4) & 0x0f)][int(m[i][j], 16) & 0x0f])
			outmat.append(temp)
	# 1D List
	else:
		m = Delete_0x(m)
		for i in range(len(m)):
			outmat.append(sbox_vals[int((int(m[i], 16) >> 4) & 0x0f)][int(m[i], 16) & 0x0f])
	return outmat

def inv_sbox(l):
	outmat = []

	print "In: {}".format(l)
	l = Delete_0x(l)

	if checkDimension(l) == 1:
		temp = [('0'*(2-len(x))) + x for x in l]
		for i in range(len(temp)):
			outmat.append(ind2hex([(index, row.index(temp[i])) for index, row in enumerate(sbox_vals) if temp[i] in row]))
	else:
		for i in range(len(l)):
			mattemp = []
			temp = [('0'*(2-len(x))) + x for x in l[i]]
			print "Temp: {}".format(temp)
			for j in range(len(temp)):
				mattemp.append(ind2hex([(index, row.index(temp[j])) for index, row in enumerate(sbox_vals) if temp[j] in row]))
			outmat.append(mattemp)

	print "Out: {}".format(outmat)
	return outmat

def Delete_0x(m):
	outmat = []

	# 1D
	if checkDimension(m) == 1:
		if m[0].find("0x") < 0:
			return m
		for i in range(len(m)):
			m[i] = m[i].replace("0x","")
		return m
	# 2D
	else:
		if m[0][0].find("0x") < 0:
			return m
		for i in range(len(m)):
			temp = []
			for j in range(len(m[0])):
				temp.append(m[i][j].replace("0x",""))
			outmat.append(temp)
	return outmat

def ShiftRow_L(m):

	print "ShiftRow_L: {}".format(m)

	if checkDimension(m) > 1:
		for i in range(1, len(m)):
			for j in range(0, i):
				m[i] = ShiftRow_L(m[i])
	else:
		m = [m[1], m[2], m[3], m[0]]
	return m

def ShiftRow_R(m):

	print "ShiftRow_R: {}".format(m)

	if checkDimension(m) > 1:
		for i in range(1, len(m)):
			for j in range(0, i):
				m[i] = ShiftRow_R(m[i])
	else:
		m = [m[3], m[0], m[1], m[2]]
	return m

def mixCol(m):
	outmat = [[0 for col in range(len(m[0]))] for row in range(len(m))]
	for i in range(len(m)):
		for j in range(len(m[0])):
			tempval = 0
			for k in range(len(m)):
				if mixCol_vals[i][k] == 1:
					temp = int(m[k][j], 16)
				elif mixCol_vals[i][k] == 2:
					temp = int(m[k][j], 16) << 1
					if int(m[k][j], 16) >= 0x80:
						temp = temp ^ 0x1B
				elif mixCol_vals[i][k] == 3:
					temp = (int(m[k][j], 16) << 1) ^ int(m[k][j], 16)
					if int(m[k][j], 16) >= 0x80:
						temp = temp ^ 0x1B
				else:
					print ("Lookup Error")
				tempval = tempval ^ (temp & 0xFF)
			outmat[i][j] = str(hex(tempval))
	return outmat

def invMixCol (m):
	outmat = [[0 for col in range(len(m[0]))] for row in range(len(m))]
	for i in range(len(m)):
		for j in range(len(m[0])):
			tempval = 0
			for k in range(len(m)):
				if invMixCol_vals[i][k] == 9:
					temp = (int(m[k][j], 16) << 3) ^ int(m[k][j], 16)
				elif invMixCol_vals[i][k] == 11:
					temp = (((int(m[k][j], 16) << 2) ^ int(m[k][j], 16)) << 1) ^ int(m[k][j], 16)
				elif invMixCol_vals[i][k] == 13:
					temp = ((int(m[k][j], 16) << 1) ^ int(m[k][j], 16) << 2) ^ int(m[k][j], 16)
				elif invMixCol_vals[i][k] == 14:
					temp = ((((int(m[k][j], 16) << 1) ^ int(m[k][j], 16)) << 1) ^ int(m[k][j], 16)) << 1
				else:
					print "Lookup Error"
				tempval = tempval ^ (temp & 0xff)
			outmat[i][j] = str(hex(tempval))
	return outmat

def transposeList(l):

	outmat = [[0 for col in range(len(l[0]))] for row in range(len(l))]
	for i in range(len(l)):
		for j in range(len(l[0])):
			outmat[j][i] = l[i][j]
	return outmat

def checkDimension(l):

	if isinstance(l[0], list):
		return 2
	else:
		return 1

def calcRCon(rcon):
	if rcon < 0x80:
		rcon = rcon << 1
	else:
		rcon = ((rcon << 1) ^ 0x1B) & 0xFF	
	return rcon

def str2list(s):
	outlist = []
	print "String: {}".format(s)
	for i in range(0, len(s), 2):
		outlist.append(s[i:i+2])
	print "Outlist: {}".format(outlist)
	return outlist

def ind2hex(ind):
	s = ""
	print "Ind: {}".format(ind)
	s+=str(hex(ind[0][0]))
	s+=str(hex(ind[0][1]))
	s = s.replace("0x","")
	return s

def keyExpansion (keytext, rounds):
	keymat = []
	keymat.append(keytext)
	round_const = 1
	for i in range(rounds):
		w = transposeList(keytext)
		gw3 = sbox(ShiftRow_L(w[3]))
		gw3[0] = str(hex((int(gw3[0], 16) ^ round_const) & 0xFF))
		gw3 = Delete_0x(gw3)
		w4 = Delete_0x(XORmat(w[0], gw3))
		w5 = Delete_0x(XORmat(w[1], w4))
		w6 = Delete_0x(XORmat(w[2], w5))
		w7 = Delete_0x(XORmat(w[3], w6))
		round_const = calcRCon(round_const)
		keytext = [w4, w5,  w6, w7]
		keymat.append(keytext)
	print "KeyExpansion:\n{}".format(keymat)
	return keymat	

def aes_round(roundkey, statematrix, round_num, round_const, width=16):
	w = transposeList(roundkey)
	statematrix = sbox(statematrix)
	statematrix = ShiftRow_L(statematrix)
	if round_num < 10:
		statematrix = mixCol(statematrix)
	gw3 = sbox(ShiftRow_L(w[3]))
	gw3[0] = str(hex((int(gw3[0], 16) ^ round_const) & 0xFF))
	gw3 = Delete_0x(gw3)
	w4 = Delete_0x(XORmat(w[0], gw3))
	w5 = Delete_0x(XORmat(w[1], w4))
	w6 = Delete_0x(XORmat(w[2], w5))
	w7 = Delete_0x(XORmat(w[3], w6))
	round_const = calcRCon(round_const)
	roundkey = [w4, w5,  w6, w7]
	statematrix = XORmat(transposeList(roundkey), statematrix)
	return transposeList(roundkey), statematrix, round_const

def aes_d_round(roundkey, statematrix, round_num, round_const):
	print "StateMatS: {}".format(statematrix)
	w = transposeList(roundkey)
	print "W: {}".format(w)
	print "W[3]: {}".format(w[3])
	gw3 = ShiftRow_L(w[3])
	print "W[3]: {}".format(gw3)
	gw3 = inv_sbox(gw3)
	print "W[3]: {}".format(gw3)
	gw3[0] = str(hex((int(gw3[0], 16) ^ round_const) & 0xFF))
	gw3 = Delete_0x(gw3)
	w4 = Delete_0x(XORmat(w[0], gw3))
	print "W4: {}".format(w4)
	w5 = Delete_0x(XORmat(w[1], w4))
	print "W5: {}".format(w5)
	w6 = Delete_0x(XORmat(w[2], w5))
	print "W6: {}".format(w6)
	w7 = Delete_0x(XORmat(w[3], w6))
	print "W7: {}".format(w7)
	round_const = calcRCon(round_const)
	roundkey = [w4, w5, w6, w7]
	print "RKey: {}".format(roundkey)
	print "StateMatF: {}".format(statematrix)
	#statematrix = XORmat(transposeList(roundkey), statematrix)
	statematrix = ShiftRow_R(statematrix)
	statematrix = inv_sbox(statematrix)
	if round_num < 10:
		statematrix = invMixCol(statematrix)
	statematrix = XORmat(transposeList(roundkey), statematrix)
	return transposeList(roundkey), statematrix, round_const

def aes(keytext, statetext, mode="E"):
	round_const = 1
	print "Key: {}".format(keytext)
	mykeys = keyExpansion(keytext, 10)
	if mode == "E":
		statetext = XORmat(statetext, keytext)
		for i in range(10):
			print "Round: {}\n".format(i)
			keytext, statetext, round_const = aes_round(keytext, statetext, i+1, round_const)
		return transposeList(statetext)
	elif mode == "D":
		print "SText: {}".format(statetext)
		statetext = XORmat(statetext, keytext)
		print "SText_AK: {}".format(statetext)
		for i in range(10):
			keytext, statetext, round_const = aes_d_round(keytext, statetext, i+1, round_const)
		return transposeList(statetext)
	else:
		print "Error: Invalid Mode"
