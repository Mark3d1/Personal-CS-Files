"""
Project 4
Mark Foss

"""

def init_board(num_rows, num_cols):
	filler = '.' #initiating variables
	#This one is unnecessary but if wanted it could
	#be used to change the filler to anything
	list2 = [] 
	i = 0 #creating the counter
	while i < num_rows: #repeats loop until however many
	#rows are needed
		list1 = [] # recreates list upon loop
		i2 = 0 #counter within the second while
		while i2 < num_cols:
			list1.append(filler) #adds '.' to list for however
			#many columns are needed within a row
			i2 += 1 
		list2.append(list1) #adds list 1 to list 2
		#where list 1 becomes a row and loops until
		#the desired amount of rows are obtained
		i += 1
	return list2
#returns list of rows

def show_board(board):
	i = 0 #creating initial variables
	i2 = 0
	str1 = ""
	str2 = ""
	list1 = []

	while i < len(board):
		i2 = 0 #setting i2 and str1 to 0 each time the 
		#outerloop loops
		str1 = ""
		while i2 < len(board[i]):
	#sets val as the position in row i and column i2
			val = board[i][i2]
	#adds the value to str1 to store it
			str1 += val
			i2 += 1
	#adds str1 to str2 but on the next line
	#str1 then becomes wiped and the process loops
		str2 += str1 + "\n"
		i += 1
	
#returns str2
	return str2

def read_board(s):
	acceptable = ['A','B','C','D','E','F','G','H','I','J','K','L','M', \
	'N','O','P','Q','R','S','T','U','V','W','X','Y','Z','.']
#creates a list of all values allowed to be on the game board
	list3 = [] #initializes other variables
	list2 = []
	list2 = s.split()
	#splits the string and removes whitespaces then adds it to list2
	for x in list2:
	#sorts through list2
		list1 = []
	#resets list1 every loop
		for xs in x:
	#sorts through the individual values in the 2D list
			if xs in acceptable:
				list1.append(xs)
	#if the xs value is an acceptable value listed earlier
	#then it is added to list1
			else:
				return None
	#otherwise it would be None because its an invalid board
		list3.append(list1)
	#list1 is then added to list3 for storage before its wiped
	i = 0 #initializes i variable for loops
	i2 = 1 
	while i < (len(list3) - 1):
	#loops through the values of the length of list3
		if len(list3[i]) != len(list3[i2]):
	#if the lists are not the same length then the
	#board is invalid and not rectangular
			return None
		i += 1
		i2 += 1

	return list3
	#returns the valid board split up


def get_size(board):
	counter = 0
	#initializes counter
	row = len(board)
	#sets row = to the length of the board
	column = len(board[0])
	#columns = to length of list within row
	list1 = [] #initializes list1
	list1.append(row)
	list1.append(column)
	#adds the row length and column length to list1
	size = tuple(list1)
	#turns list into tuple then returns it as the size
	return size


def is_valid_coord(board,r,c):
	
	if r < len(board) and r >= 0:
		rtest = True
	#verifies if the row coord is within the
	#possible bounds
	else:
		return False
	i=0
	while i < len(board):
		if c < len(board[i]) and c >= 0:
	#if the columns is within the possible columns
	#(length of row) and non negative then it continues
	#otherwise its not possible and returns false
			ctest = True
		else:
			return False
		i += 1
	if rtest == ctest:
		test1 = True
#if the board passed each previous test then the return
#value will be True
	return test1


def get_coords_by_color(board,color):
	i = 0
	list2 = []
	while i < len(board):
		i2 = 0
		tuple1 = ()
	#resets these variables every loop
		while i2 < len(board[i]):
			list1 = []
	#resets list1 in this loop
			if board[i][i2] == color:
				list1.append(i)
				list1.append(i2)
				tuple1 = tuple(list1)
#loops through each value if that value is = to
#the specified color then its coordinates (i,i2)
#are added to a list which is then turned into
#a tuple
				list2.append(tuple1)
#the tuple is then added to the list of coords
			else:
				tuple1 = None
			i2 += 1
		i += 1
	return list2
#returns the list of tuple coordinates

def get_colors(board):
	list1 = []
	colors = ['A','B','C','D','E','F','G','H','I','J','K','L','M', \
	'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
#initializes variables, colors is all possible "colors" 
#and excludes '.'
	for boar in board:
		for boa in boar:
#loops through the 2D list
			if boa in colors:
#verifies that boa is an acceptable color in the list of colors
				if boa not in list1:
					list1.append(boa)
#if the identified color is not already in the list then it is
#added to list1, otherwise it won't be added as it is a
#duplicate
	return list1


def count_pieces_by_color(board,color):
	counter = 0
	for boar in board:
		for boa in boar:
#loops through each value in the 2D list
			if boa == color:
				counter += 1
#if the value is the same as the specified color then
#the counter is increased by 1
	return counter


def any_floating(board):
	colors = ['A','B','C','D','E','F','G','H','I','J','K','L','M', \
	'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	list1 = []
#sets up initial variables and possible colors
	i = 0
	while i < (len(board)-1):
#loops through the 2D list while resetting the value of i2 each
#outerloops
		i2 = 0
		while i2 < len(board[i]):
			if (board[i][i2] in colors):
				if (i+1) >= len(board):
					return False
				if (board[(i+1)][i2] == '.'):
					return True
#if the counter of the outerloop is larger than the length
#of the board then its false as it would create an index
#error and it means that a color is already at the bottom.
#if the bottom is '.' then the board has a floating value
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
#runs through the length of the board
#(amount of rows)
		if c > len(board):
			return False
#if the amount of columns are more than
#the amount of rows then its false
#because its invalid
		else:
			if board[i][c] == '.':
				return False
#if the board has a '.' then it isnt false
		i += 1
	return True
#if it fails all checks then its full and returns
#true


def place_one(board,c,color):
	fullcheck = is_column_full(board,c)
	if fullcheck == True:
		return False
#first it sees if the board is full, if it is then
#it returns False and nothing is placed
	elif c > len(board):
		return False
#if the amount of columns are greater than the
#length then its invalid so it returns False
	else:
		i = 0
		del board[i][c]
		board[i].insert(c,color)
		floatcheck = any_floating(board)
#deletes top value then adds the color to the spot
#identifies if the board now has a float value
		while floatcheck == True:
			del board[i][c]
			board[i].insert(c,'.')
#if the board has a floating color then it replaces the color
#with '.'
			i+=1
			del board[i][c]
			board[i].insert(c,color)
			floatcheck = any_floating(board)
#then it replaces the point below it with the color and
#checks if its floating and it repeats until it no longer
#floats

		return True


def pop_out(board,c,color):
	i = -1
	if c > len(board):
		return False
#if c > length of board then its invalid
	if board[-1][c] == color:
		del board[-1][c]
		board[-1].insert(c,'.')
		floatcheck = any_floating(board)
#deletes item on bottom row then replaces it with '.'
#then checks if a value is floating
		if floatcheck == True:
			while  floatcheck == True:
				prev = board[i][c]
				del board[i][c]
				board[i].insert(c,board[i-1][c])
				i -= 1
				del board[i][c]
				board[i].insert(c,prev)
#if a value is floating then this section of the code
#will store a value then delete the stored value
#it will then insert the stored prev value above where it was before
				floatcheck = any_floating(board)
#it will check if its floating again and continue the loop
		return True
#if the pop was successful then it returns true

	else:
		return False
#otherwise it will be false

	

def check_horizontal(board,r,c):
	i = 0
	list1 = []
	boundcheck = r
	if boundcheck > len(board):
		return False
#checks if the board is within
#valid bounds
	else:
		run = board[r][c]
		if run == '.':
			return False
#run is the starting value. if its not a
#color then its false
		while i < 4:
			if run == board[r][c]:
				list1.append(board[r][c])
				c += 1
			i += 1
#otherwise it runs through the next 4 values in
#the row and adds them to a list

		if len(list1) == 4:
			return True
#if the list has 4 of the same values then it returns
#true
		else:
			return False



def check_vertical(board,r,c):
	i = 0
	list1 = []
	if r > len(board) or r < 0:
		return False
#verifies if the board is valid
	boundcheck = r + 4
	if boundcheck > len(board):
		return False
#verifies if the board is valid in a
#different way
	run = board[r][c]
	if run == '.':
		return False
#ensures that run is a color
	while i < 4:
		if run == board[r][c]:
			list1.append(board[r][c])
			r += 1
		i += 1
#sees if run is the same as the value of
#each of the same value in the column of each row
#for 4 different rows then adds it to the list1
	if len(list1) == 4:
		return True
#if list1 has 4 of the values then its valid
	else:
		return False


def check_major_diagonal(board,r,c):
	i = 0
	list1 = []
	if r > len(board) or r < 0:
		return False
	boardcheck = r + 4
	if boardcheck > len(board):
		return False
	run = board[r][c]
	if run == '.':
		return False
#verifies if the board is valid and that
#the initial value is a color
	while i < 4:
		if run == board[r][c]:
			list1.append(board[r][c])
			r += 1
			c += 1
		i += 1
#sorts through the run in a downward to the
#right pattern by increasing r and c each
#loop. If its the same color as run
#then its added to list1
	if len(list1) == 4:
		return True
#if list1 has 4 values then it
#has connected 4 diagonally
	else:
		return False

def check_minor_diagonal(board,r,c):
	i = 0
	list1 = []
	if r > len(board) or r < 0:
		return False
	boardcheck = r - 4
	if boardcheck > len(board):
		return False
	run = board[r][c]
	if run == '.':
		return False
#verifies if the board is valid and
#that run is a color
	while i < 4:
		if run == board[r][c]:
			list1.append(board[r][c])
			r -= 1
			c += 1
		i += 1
#loops through the board in an upward to the right
#fashion and verifies that the value is the same
#as the one stored in run. If it is then it is
#added to list1
	if len(list1) == 4:
		return True
#if list1 has the same values then the check
#identifies it as true
	else:
		return False


def check_winner(board):
#incomplete code that I couldn't figure out
	size = get_size(board)
	colors = get_colors(board)
	i = 0
	list1 = []
	list2 = []
	area = size[0] * size[1]
	#after initializing some variables it determines the area
	#area will be used to see if the game has drawn
	print(area)
	countcolor1 = count_pieces_by_color(board,colors[0])
	countcolor2 = count_pieces_by_color(board,colors[1])
	countcolor = countcolor1 + countcolor2
	print(countcolor)
	#this initializes some variables
	coord1 = get_coords_by_color(board,colors[0])
	coord2 = get_coords_by_color(board,colors[1])
	while i < len(coord1):
		i2 = 0
		r = i
		c = coord1[i][i2]
#sets row value to i which is the counter throught he loops
#sets c to the coord within the row
		checkh = check_horizontal(board,r,c)
		checkv = check_vertical(board,r,c)
		checkma = check_major_diagonal(board,r,c)
		checkmi = check_minor_diagonal(board,r,c)
#verifies if the coord passes any of the checks
		if checkh == True or checkv == True or checkma == True or checkmi == True:
			listuple = []
			listuple.append(r)
			listuple.append(c)
			listuple = tuple(listuple)
			list1.append(listuple)
#if and check is passed then it stores the coord in list1
		i+= 1
		i2 += 1
	while i < len(coord2):
		i2 = 0
		r = i
		c = coord2[i][i2]
		checkh = check_horizontal(board,r,c)
		checkv = check_vertical(board,r,c)
		checkma = check_major_diagonal(board,r,c)
		checkmi = check_minor_diagonal(board,r,c)
		if checkh == True or checkv == True or checkma == True or checkmi == True:
#verifies if the coord passes any of the checks
			listuple = []
			listuple.append(r)
			listuple.append(c)
			listuple = tuple(listuple)
			list2.append(listuple)
		i+= 1
		i2 += 1
#if and check is passed then it stores the coord in list1	
	if countcolor == area:
		return "draw"
	#incomplete code where if the total color count
	#is the same as the area of the board then it
	#would see if the game has drawn, someone won,
	#or if there is a tie
