import shalib
import sys

outval = shalib.CRShift(15, 2)
print "15 >> 2 = {}; {}".format(hex(outval), sys.getsizeof(outval))

outval = shalib.CRShift(1, 1)
print "1 >> 1 = {}".format(hex(outval))

outval = shalib.CRShift(0, 5)
print "0 >> 5 = {}".format(hex(outval))

outval = shalib.CRShift(15, 24)
print "15 >> 24 = {}".format(hex(outval))

shalib.aes("Thats my Kung Fu", "Two One Nine Two")
