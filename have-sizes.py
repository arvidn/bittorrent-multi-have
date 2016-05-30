#!/bin/python

import encode
import os
from helpers import gen_scattered_pieces
from helpers import gen_realistic_pieces

# write gnuplot file comparing sizes of sending multiple HAVE messages
# and sending a single coalesced lt_have message

out = open('have-sizes.dat', 'w+')

num_pieces = 10000
cluster_size = 8

# column 1: number of pieces
# column 2: size of multiple HAVE messages
# column 3: size of hypothetical HAVE message with multiple piece indices
# column 4: size of compressed bitfield message (with pieces spaced out)
# column 5: size of compressed bitfield message (with pieces clustered realistically)
# column 6: size of compressed bitfield message (with contiguous pieces)
for i in range(1,64):

	scattered_pieces = gen_scattered_pieces(i, 0, num_pieces)
	contiguous_pieces = range(0,i)
	realistic_pieces = gen_realistic_pieces(i, num_pieces, cluster_size)
	
	# divide by 3 because each byte is HEX encoded with spaces in between
	scatter_size = len(encode.encode_pieces(scattered_pieces)) / 3
	contig_size = len(encode.encode_pieces(contiguous_pieces)) / 3
	realistic_size = len(encode.encode_pieces(realistic_pieces)) / 3
	out.write('%d\t%d\t%d\t%d\t%d\t%d\n' % (i, 9 * i, 5 + i * 4, \
		4 + 2 + scatter_size, \
		4 + 2 + realistic_size, \
		4 + 2 + contig_size))

out.close()

f = open('have-sizes.gnuplot', 'w+')
f.write('''
set term png small size 640,480
set output "have-sizes.png"
set grid
set ylabel "Bytes"
set xlabel "number of pieces"
plot "have-sizes.dat" using 1:2 with lines title "regular HAVE messages", \\
"have-sizes.dat" using 1:3 title "multi-index HAVE" with lines, \\
"have-sizes.dat" using 1:4 with lines title "compressed bitfield (spaced out pieces)", \\
"have-sizes.dat" using 1:5 with lines title "compressed bitfield (realistic pieces)", \\
"have-sizes.dat" using 1:6 with lines title "compressed bitfield (contiguous pieces)"

set term png size 1280,800
set output "have-sizes-full.png"
set ytics 20
set xtics 5
replot
''')
f.close()

os.system('gnuplot have-sizes.gnuplot')

