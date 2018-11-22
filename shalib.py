# Filename: shalib.py

# Description: SHA-256 Library Functions

# Date: 20181121 -- ZDH

import sys
import binascii
import math

def CRShift(inval, bits, width=32):
	if __debug__:
		print "Shifting {} by {}".format(hex(inval), bits)
		print "First: {}".format(hex(inval >> bits))
		print "Second: {}".format(hex(inval << (width-bits)))
		print "Width: {}".format(width)
	mask = 0xFFFFFFFF
	newval = ((inval >> bits) | (inval << (width - bits))) & mask
	return newval

def CLShift(inval, bits, width=32):
	mask = 0xFFFFFFFF
	newval = ((inval << bits) | (inval >> (width - bits))) & mask
	return newval

def str2hex (txt, width):
	hextext = []
	for i in range(width):
		if __debug__:
			print i
			print txt[i]
		hextext.append(binascii.hexlify(txt[i]))
		if __debug__:
			print hextext[i]
	return hextext

def aes(key, plaintext, width=16):
	sbox = [["63","7c","77","7b","f2","6b","6f","c5","30","01","67","2b","fe","d7","ab","76"],
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
	hexkey = str2hex(key, width)
	plaintexthex = binascii.hexlify(plaintext)
	if __debug__:
		print "Key: {}".format(hexkey)
		print "PlainText: {}".format(plaintexthex)
	w = [hexkey[0:4], hexkey[4:8], hexkey[8:12], hexkey[12:16]]
	if __debug__:
		print "W {}".format(w)
		print "W0: {}".format(w[0])
		print "W1: {}".format(w[1])
		print "W2: {}".format(w[2])
		print "W3: {}".format(w[3])
	gw3 = [w[3][1], w[3][2], w[3][3], w[3][0]]
	if __debug__:
		print "GW3: {}".format(gw3)
		print "GW3,0: {}".format(int(gw3[0]))
		print ((int(w[3][0]) >> 4) & 0x0F)
	gw3[0] = (sbox[int(int(gw3[0]) / 10)][int(gw3[0]) % 10])
	gw3[1] = (sbox[int(int(gw3[1]) / 10)][int(gw3[1]) % 10])
	gw3[2] = (sbox[int(int(gw3[2]) / 10)][int(gw3[2]) % 10])
	gw3[3] = (sbox[int(int(gw3[3]) / 10)][int(gw3[3]) % 10])
	if __debug__:
		print "GW3: {}".format(gw3)
	round_const = [1,0,0,0]
	print (int(w[3][0], 16))
	print (int(round_const[0]))
	print (hex(int(w[3][0], 16) + int(round_const[0])))
	hextest = str(hex(int(w[3][0], 16) + int(round_const[0])))
	print (hextest.replace("0x",""))
	gw3 = [str(hex(int(gw3[0], 16) - round_const[0])), str(hex(int(gw3[1], 16) - round_const[1])), str(hex(int(gw3[2], 16) - round_const[2])), str(hex(int(gw3[3], 16) - round_const[3]))]
	gw3[0] = gw3[0].replace("0x","")
	gw3[1] = gw3[1].replace("0x","")
	gw3[2] = gw3[2].replace("0x","")
	gw3[3] = gw3[3].replace("0x","")
	if __debug__:
		print "GW3: {}".format(gw3)
	w4 = [str(hex(int(w[0][0], 16) ^ int(gw3[0], 16))), str(hex(int(w[0][1], 16) ^ int(gw3[1], 16))), str(hex(int(w[0][2], 16) ^ int(gw3[2], 16))), str(hex(int(w[0][3], 16) ^ int(gw3[3], 16)))]
	w4[0] = w4[0].replace("0x","")
	w4[1] = w4[1].replace("0x","")
	w4[2] = w4[2].replace("0x","")
	w4[3] = w4[3].replace("0x","")
	if __debug__:
		print "W4: {}".format(w4)
	w5 = [str(hex(int(w[1][0], 16) ^ int(w4[0], 16))), str(hex(int(w[1][1], 16) ^ int(w4[1], 16))), str(hex(int(w[1][2], 16) ^ int(w4[2], 16))), str(hex(int(w[1][3], 16) ^ int(w4[3], 16)))]
	w5[0] = w5[0].replace("0x","")
	w5[1] = w5[1].replace("0x","")
	w5[2] = w5[2].replace("0x","")
	w5[3] = w5[3].replace("0x","")
	if __debug__:
		print "W5: {}".format(w5)
	w6 = [str(hex(int(w[2][0], 16) ^ int(w5[0], 16))), str(hex(int(w[2][1], 16) ^ int(w5[1], 16))), str(hex(int(w[2][2], 16) ^ int(w5[2], 16))), str(hex(int(w[2][3], 16) ^ int(w5[3], 16)))]
	w6[0] = w6[0].replace("0x","")
	w6[1] = w6[1].replace("0x","")
	w6[2] = w6[2].replace("0x","")
	w6[3] = w6[3].replace("0x","")
	if __debug__:
		print "W6: {}".format(w6)
	w7 = [str(hex(int(w[3][0], 16) ^ int(w6[0], 16))), str(hex(int(w[3][1], 16) ^ int(w6[1], 16))), str(hex(int(w[3][2], 16) ^ int(w6[2], 16))), str(hex(int(w[3][3], 16) ^ int(w6[3], 16)))]
	w7[0] = w7[0].replace("0x","")
	w7[1] = w7[1].replace("0x","")
	w7[2] = w7[2].replace("0x","")
	w7[3] = w7[3].replace("0x","")
	if __debug__:
		print "W7: {}".format(w7)
	roundkey_1 = w4 + w5 + w6 + w7
	if __debug__:
		print "RoundKey_1: {}".format(roundkey_1)
