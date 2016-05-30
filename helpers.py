
# recursively split the range into a binary tree and return the midpoints.
def gen_scattered_pieces(depth, start_p, end_p):
	if depth == 0: return []
	if start_p >= end_p: return []
	mid = (end_p + start_p) / 2
	if mid == end_p: print('ERROR: ', mid, start_p, end_p)
	depth -= 1
	half = depth / 2
	return [mid] + \
		gen_scattered_pieces(depth - half, start_p, mid) + \
		gen_scattered_pieces(half, mid + 1, end_p)

# generate some contiguous pieces starting at start_p
def gen_contiguous_pieces(n, start_p, cluster_size):
	n = min(n, cluster_size)
	return [x for x in range(start_p, start_p + n)]

def gen_realistic_pieces(n, num_pieces, cluster_size):
	ret = []
	# positions are the start positions of contiguous ranges of max cluster pieces
	positions = gen_scattered_pieces(n, 0, num_pieces / cluster_size)
	positions.reverse()
	
	while len(ret) < n:
		pos = positions.pop()
		ret += gen_contiguous_pieces(n - len(ret), pos * cluster_size, cluster_size)

	return ret

