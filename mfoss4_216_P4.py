"""
Project 4
Mark Foss

"""

def init_board(num_rows, num_cols):
	filler = '.'
	list2 = []
	i = 0
	while i < num_rows:
		list1 = []
		i2 = 0
		while i2 < num_cols:
			list1.append(filler)
			i2 += 1
		list2.append(list1)
		i += 1
	return list2


def show_board(board):
	i = 0
	i2 = 0
	str1 = ""
	str2 = ""
	list1 = []

	while i < len(board):
		i2 = 0
		str1 = ""
		while i2 < len(board[i]):
			val = board[i][i2]
			str1 += val
			i2 += 1

		str2 += str1 + "\n"
		i += 1
	
	print(str2)

	return str2

def read_board(s):
	acceptable = ['A','B','C','D','E','F','G','H','I','J','K','L','M', \
	'N','O','P','Q','R','S','T','U','V','W','X','Y','Z','.']
	list3 = []
	list2 = []
	list2 = s.split()
	for x in list2:
		list1 = []
		for xs in x:
			if xs in acceptable:
				list1.append(xs)
			else:
				return None
		list3.append(list1)
	i = 0
	i2 = 1
	while i < (len(list3) - 1):
		if len(list3[i]) != len(list3[i2]):
			return None
		i += 1
		i2 += 1

	return list3


def get_size(board):
	counter = 0
	row = len(board)
	column = len(board[0])
	list1 = []
	list1.append(row)
	list1.append(column)
	size = tuple(list1)
	return size


def is_valid_coord(board,r,c):
	
	if r < len(board) and r >= 0:
		rtest = True
	else:
		return False
	i=0
	while i < len(board):
		if c < len(board[i]) and c >= 0:
			ctest = True
		else:
			return False
		i += 1
	if rtest == ctest:
		test1 = True

	return test1


def get_coords_by_color(board,color):
	i = 0
	list2 = []
	while i < len(board):
		i2 = 0
		list1 = []
		tuple1 = ()
		while i2 < len(board[i]):
			list1 = []
			if board[i][i2] == color:
				list1.append(i)
				list1.append(i2)
				tuple1 = tuple(list1)
				list2.append(tuple1)
				print(list1)
				print(tuple1)
			else:
				tuple1 = None
			i2 += 1
		i += 1
	return list2


def get_colors(board):
	list1 = []
	colors = ['A','B','C','D','E','F','G','H','I','J','K','L','M', \
	'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	for boar in board:
		for boa in boar:
			if boa in colors:
				if boa not in list1:
					list1.append(boa)
	return list1


def count_pieces_by_color(board,color):
	counter = 0
	for boar in board:
		for boa in boar:
			if boa == color:
				counter += 1
	return counter

def any_floating(board):

	colors = ['A','B','C','D','E','F','G','H','I','J','K','L','M', \
	'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	list1 = []
	i = 0
	while i < (len(board)-1):
		i2 = 0
		while i2 < len(board[i]):

			if (board[i][i2] in colors):
				print((i+1), " add")
				print(len(board), " len")
				if (i+1) >= len(board):
					return False
				if (board[(i+1)][i2] == '.'):

					return True
				else:
					check = False
			else:
				check = False
			i2 += 1
		i += 1

	return check


def is_column_full(board,c):

	i = 0
	while i < len(board):
		if c > len(board):
			return False
		else:
			if board[i][c] == '.':
				return False

		i += 1
	return True


def place_one(board,c,color):
	fullcheck = is_column_full(board,c)
	if fullcheck == True:
		return False
	elif c > len(board):
		return False
	else:
		i = 0
		del board[i][c]
		board[i].insert(c,color)
		floatcheck = any_floating(board)
		while floatcheck == True:
			del board[i][c]
			board[i].insert(c,'.')
			i+=1
			del board[i][c]
			board[i].insert(c,color)
			floatcheck = any_floating(board)
		return True


def pop_out(board,c,color):
	i = 0
	if c > len(board):
		return False
	if board[-1][c] == color:
		del board[-1][c]
		board[-1].insert(c,'.')
		floatcheck = any_floating(board)
		if floatcheck == True:
			prev = board[i][c]
			del board[i][c]
			board.insert(c,'.')
			while  floatcheck == True:
				i+= 1
				prev = board[i][c]
				del board[i][c]
				board[i].insert(c,prev)
				floatcheck = any_floating(board)
		return True



		"""while floatcheck == True:
		#	del board[-1][c]
		#	board[i].insert(c,'.')
		#	i += 1
			prev = board[i][c]
			del board[i][c]
			board[i].insert(c,'.')
			i+=1
			del board[i][c]
			board[i].insert(c,prev)
			floatcheck = any_floating(board)
		return True"""
	else:
		return False


	

def check_horizontal(board,r,c):
	i = 0
	list1 = []
	if r > len(board):
		return False
	else:
		run = board[r][c]
		if run == '.':
			return False
		while i < 4:
			
			if run == board[r][c]:
				list1.append(board[r][c])
				print(list1)
				c += 1
			i += 1
			
		if len(list1) == 4:
			return True
		else:
			return False



def check_vertical(board,r,c):
	i = 0
	list1 = []
	if r > len(board) or r < 0:
		return False
	boundcheck = r + 3
	if boundcheck > len(board):
		return False
	run = board[r][c]
	if run == '.':
		return False
	while i < 4:
		if run == board[r][c]:
			list1.append(board[r][c])
			r += 1
		i += 1
	if len(list1) == 4:
		return True
	else:
		return False

def check_major_diagonal(board,r,c):
	i = 0
	list1 = []
	if r > len(board) or r < 0:
		return False
	boardcheck = r + 3
	if boardcheck > len(board):
		return False
	run = board[r][c]
	if run == '.':
		return False
	while i < 4:
		if run == board[r][c]:
			list1.append(board[r][c])
			r += 1
			c += 1
		i += 1
	if len(list1) == 4:
		return True
	else:
		return False

def check_minor_diagonal(board,r,c):
	i = 0
	list1 = []
	if r > len(board) or r < 0:
		return False
	boardcheck = r - 3
	if boardcheck > len(board):
		return False
	run = board[r][c]
	if run == '.':
		return False
	while i < 4:
		if run == board[r][c]:
			list1.append(board[r][c])
			r -= 1
			c += 1
		i += 1
	if len(list1) == 4:
		return True
	else:
		return False

def check_winner(board):
	size = get_size(board)
	colors = get_colors(board)
	i = 0
	area = size[0] * size[1]
	print(area)
	countcolor1 = count_pieces_by_color(board,colors[0])
	countcolor2 = count_pieces_by_color(board,colors[1])
	countcolor = countcolor1 + countcolor2
	print(countcolor)
	coord1 = get_coords_by_color(colors[0])
	coord2 = get_coords_by_color(color[1])
	while i < len(coord1):
		coord1[i]
	""""looping through coordinates 1 each individually checking with all checks to see if the board is full
	then it will also loop through each coordinate for coord2 and see if 4 have been connected
	make sure to split the tuple coords into r and c values"""
		i+= 1
	if countcolor == area:
		return "test"
	#while i < len(board):
