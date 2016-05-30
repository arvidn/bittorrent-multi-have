#!/bin/python
import sys

# since this is a proof-of concept, the input is an ascii-digit bitfield. i.e.
# a string of '0' and '1'.
# the output is returned in HEX as a string
def encode(bitfield):
	if type(bitfield) != str:
		raise "expected bitfield to be a string"

	# remove trailing zeros, we don't encode those, they are implied
	while len(bitfield) > 0 and bitfield[-1] == '0':
		bitfield = bitfield[:-1]

	# first pad the bitfield to be divisible by 8
	remainder = len(bitfield) % 8
	if remainder > 0:
		bitfield += '0' * (8 - remainder)

	output = "";

	while len(bitfield) > 0:

		if bitfield[:24] == '000000000000000000000000':
			# we should encode a fill-zero
			length = 2
			bitfield = bitfield[16:]
			while bitfield[:8] == '00000000' and length < 0x4000:
				length += 1
				bitfield = bitfield[8:]

			length -= 1
			output += '%02x %02x ' % (0x00 | (length >> 8), length & 0xff)
			continue

		if bitfield[:24] == '111111111111111111111111':
			# we should encode a fill-ones
			length = 2
			bitfield = bitfield[16:]
			while bitfield[:8] == '11111111' and length < 0x4000:
				length += 1
				bitfield = bitfield[8:]

			length -= 1
			output += '%02x %02x ' % (0x40 | (length >> 8), length & 0xff)
			continue

		verbatim = ''
		length = 0
		while len(bitfield) > 0 \
			and bitfield[:24] != '111111111111111111111111' \
			and bitfield[:24] != '000000000000000000000000' \
			and length < 128:

			val = 0
			for i in range(8):
				val <<= 1
				if bitfield[0] == '1': val |= 1
				bitfield = bitfield[1:]

			length += 1
			verbatim += '%02x ' % val

		length -= 1
		output += '%02x ' % (0x80 | length)
		output += verbatim

	return output

def encode_pieces(pieces):
	pieces = sorted(pieces)

	bitfield = ''
	for p in pieces:
		bitfield += '0' * (p - len(bitfield))
		bitfield += '1'

#	print('bitfield: ', bitfield)
	return encode(bitfield)

if __name__ == '__main__':
	if len(sys.argv) > 2 and sys.argv[1] == '--bitfield':
		print(encode(sys.argv[2]))
	elif len(sys.argv) > 2 and sys.argv[1] == '--pieces':
		pieces = []
		for p in sys.argv[2:]:
			pieces.append(int(p))

		print(encode_pieces(pieces))
	else:
		print('usage: encode.py --bitfield <string of ones and zeros>')
		print('       encode.py --pieces <piece-idx>...')
		sys.exit(1)

