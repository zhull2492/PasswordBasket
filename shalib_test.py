import shalib
import sys

#	statematrix = [plaintexthex[0::4],plaintexthex[1::4],plaintexthex[2::4],plaintexthex[3::4]]
#	roundkey_0 = [hexkey[0::4],hexkey[1::4],hexkey[2::4],hexkey[3::4]]
key = shalib.str2hex("Thats my Kung Fu", 16)
plaintext = shalib.str2hex("Two One Nine Two", 16)
ciphertext = shalib.aes([key[0::4], key[1::4], key[2::4], key[3::4]], [plaintext[0::4], plaintext[1::4], plaintext[2::4], plaintext[3::4]])
print "Cipher: {}".format(ciphertext)
#print "\n\nNext Round\n\n"
#rkey, stmat = shalib.aes(rkey, stmat, 2)

newtext = [['01', '23', '45', '67'], ['89', 'ab', 'cd', 'ef'], ['fe', 'dc', 'ba', '98'], ['76', '54', '32', '10']]
newkey = [['0f', '15', '71', 'c9'], ['47', 'd9', 'e8', '59'], ['0c', 'b7', 'ad', 'd6'], ['af', '7f', '67', '98']]

#ciphertext = shalib.aes(shalib.transposeList(newkey), shalib.transposeList(newtext))
#print "Cipher: {}".format(ciphertext)
#rkey, stmat = shalib.aes(rkey, stmat, 2)

key = shalib.str2hex("hello00000000000", 16)

#ciphertext = shalib.aes([key[0::4], key[1::4], key[2::4], key[3::4]], shalib.transposeList(newtext))
#print "Cipher: {}".format(ciphertext)
