#!/bin/python
import sys

# since this is a proof-of concept, the input is an ascii hex with bytes space
# separated. the output is returned as an ascii bitfield string with '0' and '1'
def decode(msg):
	if type(msg) != str:
		raise "expected input to be a string"
	in_bytes = msg.split(' ')
	in_bytes.reverse()
	out = ''
	
	while len(in_bytes) > 0:
		val = in_bytes.pop()
		b = int(val, 16)
		if b < 0 or b > 255: raise "invalid byte value"

		if (b & 0x80) == 0:
			# fill block

			val = in_bytes.pop()
			b2 = int(val, 16)
			if b < 0 or b > 255: raise "invalid byte value"

			num_bytes = (((b & 0x3f) << 8) + b2) + 1

			if (b & 0x40) == 0:
				# fill zeros
				out += '00000000' * num_bytes
			else:
				# fill ones
				out += '11111111' * num_bytes
		else:
			# verbatim block
			num_bytes = (b & 0x7f) + 1
			for i in range(num_bytes):
				
				val = in_bytes.pop()
				b = int(val, 16)
				if b < 0 or b > 255: raise "invalid byte value"

				out += '{0:08b}'.format(b)
	return out

if __name__ == '__main__':
	if len(sys.argv) > 1:
		print(decode(' '.join(sys.argv[1:])))
	else:
		print('usage: decode.py <hex encoded>')
		sys.exit(1)

