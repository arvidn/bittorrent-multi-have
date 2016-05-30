#!/bin/python

import encode
import os
from helpers import gen_scattered_pieces
from helpers import gen_realistic_pieces

# write gnuplot file comparing sizes of BITFIELD messages
# and sending a compressed bitfield message

out = open('bitfield-sizes.dat', 'w+')

num_pieces = 10000
cluster_size = 8

# column 1: number of pieces
# column 2: size of a bitfield message
# column 3: size of compressed bitfield message (worst case)
# column 4: size of compressed bitfield message (realistic)

bitfield = ['0'] * num_pieces
for i in xrange(num_pieces + 1):

	scattered_pieces = gen_scattered_pieces(i, 0, num_pieces)
	for pos in scattered_pieces:
		bitfield[pos] = '1'

	# divide by 3 because each byte is HEX encoded with spaces in between
	scatter_size = len(encode.encode(''.join(bitfield))) / 3
	realistic_size = len(encode.encode_pieces( \
		gen_realistic_pieces(i, num_pieces, cluster_size))) / 3
	out.write('%d\t%d\t%d\t%d\n' % (i, \
		5 + (num_pieces + 7)/8, \
		4 + 2 + scatter_size, \
		4 + 2 + realistic_size))

#	print ''.join(bitfield)

out.close()

f = open('bitfield-sizes.gnuplot', 'w+')
f.write('''
set term png small size 640,480
set output "bitfield-sizes.png"
set grid
set ylabel "Bytes"
set xlabel "number of pieces"
plot "bitfield-sizes.dat" using 1:2 with lines title "BITFIELD message", \\
"bitfield-sizes.dat" using 1:3 with lines title "compressed bitfield (worst case)", \\
"bitfield-sizes.dat" using 1:4 with lines title "compressed bitfield (realistic)"

set term png size 1280,800
set output "bitfield-sizes-full.png"
set ytics 50
set xtics 500
replot
''')
f.close()

os.system('gnuplot bitfield-sizes.gnuplot')

