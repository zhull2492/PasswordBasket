import shalib
import sys

#	statematrix = [plaintexthex[0::4],plaintexthex[1::4],plaintexthex[2::4],plaintexthex[3::4]]
#	roundkey_0 = [hexkey[0::4],hexkey[1::4],hexkey[2::4],hexkey[3::4]]
key = shalib.str2hex("Thats my Kung Fu")
plaintext = shalib.str2hex("Two One Nine Two")
ciphertext = shalib.hex2str(shalib.aes([key[0::4], key[1::4], key[2::4], key[3::4]], [plaintext[0::4], plaintext[1::4], plaintext[2::4], plaintext[3::4]]))
print "Plain : {}".format((plaintext))
print "Plain : {}".format(shalib.hex2str(plaintext))
print "Cipher: {}".format(ciphertext)

cipher_b = shalib.str2list(ciphertext)
plaintext = shalib.aes([key[0:4], key[4:8], key[8:12], key[12:16]], [cipher_b[0::4], cipher_b[1::4], cipher_b[2::4], cipher_b[3::4]], "D")
print "Plain: {}".format(plaintext)
print "Plain: {}".format(shalib.hex2ascii(plaintext))
