# Based on testing harness dated 2017-06-02.

# STUDENTS: TO USE:
# 
# The following command will test all test cases on your file:
# 
#   python3 <thisfile.py> <your_one_file.py>
# 
# 
# You can also limit the tester to only the functions you want tested.
# Just add as many functions as you want tested on to the command line at the end.
# Example: to only run tests associated with func1 and func2, run this command:
# 
#   python3 <thisfile.py> <your_one_file.py> func1 func2
# 
# You really don't need to read the file any further, except that when
# a specific test fails, you'll get a line number - and it's certainly
# worth looking at those areas for details on what's being checked. This would
# all be the indented block of code starting with "class AllTests".


# INSTRUCTOR: TO PREPARE:
#  - add test cases to class AllTests. The test case functions' names must
# be precise - to test a function named foobar, the test must be named "test_foobar_#"
# where # may be any digits at the end, such as "test_foobar_13".
# - any extra-credit tests must be named "test_extra_credit_foobar_#"
# 
# - name all required definitions in REQUIRED_DEFNS, and all extra credit functions
#   in EXTRA_CREDIT_DEFNS. Do not include any unofficial helper functions. If you want
#   to make helper definitions to use while testing, those can also be added there for
#   clarity.
# 
# - to run on either a single file or all .py files in a folder (recursively):
#   python3 <thisfile.py> <your_one_file.py>
#   python3 <thisfile.py> <dir_of_files>
#   python3 <thisfile.py> .                    # current directory
# 
# A work in progress by Mark Snyder, Oct. 2015.
#  Edited by Yutao Zhong, Spring 2016.
#  Edited by Raven Russell, Spring 2017.
#  Edited by Mark Snyder, June 2017.


import unittest
import shutil
import sys
import os
import time

#import subprocess

import importlib

############################################################################
############################################################################
# BEGIN SPECIALIZATION SECTION (the only part you need to modify beyond 
# adding new test cases).

# name all expected definitions; if present, their definition (with correct
# number of arguments) will be used; if not, a decoy complainer function
# will be used, and all tests on that function should fail.
	
REQUIRED_DEFNS = [ 	"init_board",
					"get_size",
					"show_board",
					"is_valid_coord",
					"get_coords_by_color",
					"get_colors",
					"count_pieces_by_color",
					"any_floating",
					"is_column_full",
					"place_one",
					"pop_out",
					"check_horizontal",
					"read_board",
					"check_vertical",
					"check_major_diagonal",
					"check_minor_diagonal",
					"check_winner",
					]

# for method names in classes that will be tested
SUB_DEFNS = [ ]

# definitions that are used for extra credit
EXTRA_CREDIT_DEFNS = [ "winning_move" ]

# how many points are test cases worth?
weight_required = 1
weight_extra_credit = 1

# don't count extra credit; usually 100% if this is graded entirely by tests.
# it's up to you the instructor to do the math and add this up!
# TODO: auto-calculate this based on all possible tests.
total_points_from_tests = 90

# how many seconds to wait between batch-mode gradings? 
# ideally we could enforce python to wait to open or import
# files when the system is ready but we've got a communication
# gap going on.
DELAY_OF_SHAME = 1


# set it to true when you run batch mode... 
CURRENTLY_GRADING = False



# what temporary file name should be used for the student?
# This can't be changed without hardcoding imports below, sorry.
# That's kind of the whole gimmick here that lets us import from
# the command-line argument without having to qualify the names.
RENAMED_FILE = "student"


# sample boards

board1str="""\
.......
...R...
...Y...
.YYR...
YRRR...
RYYRY..
"""

def board1():
	return [['.','.','.','.','.','.','.'],
			['.','.','.','R','.','.','.'],
			['.','.','.','Y','.','.','.'],
			['.','Y','Y','R','.','.','.'],
			['Y','R','R','R','.','.','.'],
			['R','Y','Y','R','Y','.','.']]

board11str="""\
.......
...R...
...Y...
.YYR...
YRRRR..
RYYRY..
"""

def board11(): #one move from board1, four in a row
	return [['.','.','.','.','.','.','.'],
			['.','.','.','R','.','.','.'],
			['.','.','.','Y','.','.','.'],
			['.','Y','Y','R','.','.','.'],
			['Y','R','R','R','R','.','.'],
			['R','Y','Y','R','Y','.','.']]


def board12(): # two moves from board1
	return [['.','.','.','.','.','.','.'],
			['.','.','.','R','.','.','.'],
			['.','.','Y','Y','.','.','.'],
			['.','Y','Y','R','.','.','.'],
			['Y','R','R','R','.','.','.'],
			['R','Y','Y','R','Y','.','R']]


def board13(): #after popup 
	return [['.','.','.','.','.','.','.'],
			['.','.','.','R','.','.','.'],
			['.','.','.','Y','.','.','.'],
			['.','Y','Y','R','.','.','.'],
			['Y','R','R','R','.','.','.'],
			['R','Y','Y','R','.','.','.']]


def board14(): #after popup 
	return [['.','.','.','.','.','.','.'],
			['.','.','.','.','.','.','.'],
			['.','.','.','R','.','.','.'],
			['.','.','.','Y','.','.','.'],
			['Y','Y','.','R','.','.','.'],
			['R','R','Y','R','.','.','.']]


def board15():
	return [['.','.','.','.','.','.','.'],
			['.','.','.','R','.','.','.'],
			['.','.','.','Y','.','.','.'],
			['.','.','Y','R','.','.','.'],
			['.','Y','R','R','.','.','.'],
			['.','R','Y','R','Y','.','.']]


board2str="""\
.......
....BB.
..BGGG.
..GGGB.
.GBBGB.
.BBGBGG
"""

def board2():
	return [['.','.','.','.','.','.','.'],
			['.','.','.','.','B','B','.'],
			['.','.','B','G','G','G','.'],
			['.','.','G','G','G','B','.'],
			['.','G','B','B','G','B','.'],
			['.','B','B','G','B','G','B']]


def board21(): # one move for 'G', four in a diagonal
	return [['.','.','.','.','.','.','.'],
			['.','.','.','.','B','B','.'],
			['.','.','B','G','G','G','.'],
			['.','.','G','G','G','B','.'],
			['.','G','B','B','G','B','.'],
			['G','B','B','G','B','G','B']]

def board22(): 
	return [['.','.','.','G','.','.','.'],
			['.','.','G','B','B','B','.'],
			['.','.','B','G','G','G','.'],
			['.','.','G','G','G','B','.'],
			['.','G','B','B','G','B','.'],
			['G','B','B','G','B','G','B']]


board3str="""\
....B..
....BB.
...GGG.
...GGB.
.G.GBB.
.B.GBGB
"""

def board3(): # four in a column
	return [['.','.','.','.','B','.','.'],
			['.','.','.','.','B','B','.'],
			['.','.','.','G','G','G','.'],
			['.','.','.','G','G','B','.'],
			['.','G','.','G','B','B','.'],
			['.','B','.','G','B','G','B']]

def board31(): 
	return [['.','.','.','.','B','.','.'],
			['.','.','.','.','B','B','.'],
			['.','.','.','.','G','G','.'],
			['.','.','.','G','G','B','.'],
			['.','G','.','G','B','B','.'],
			['.','B','.','G','B','G','B']]



# floating pieces
board4str="""\
...BB.
.BGGG.
..GGB.
G.BGB.
B.GBGB
"""

def board4(): #floating piece, three colors
	return [['.','.','.','B','B','.'],
			['.','B','G','G','G','.'],
			['.','.','G','G','B','.'],
			['G','.','B','G','B','.'],
			['B','.','G','B','G','B']]

# floating pieces

def board5():
	return [['.','.','.','.','.','.','.'],
			['.','.','.','.','B','B','.'],
			['.','.','B','G','G','G','.'],
			['.','.','.','G','G','B','.'],
			['.','G','G','B','G','B','.'],
			['.','B','.','G','B','G','B']]



def board6():
	return [['.','.','.','.','.'],
			['.','.','.','Y','.'],	
			['R','R','Y','Y','.'],
			['Y','Y','R','Y','.'],
			['R','R','Y','R','R']]		


def board61():
	return [['.','.','.','.','.'],
			['Y','.','.','Y','.'],	
			['Y','Y','R','R','.'],
			['R','R','Y','R','.'],
			['R','Y','R','Y','Y']]		


def board62():
	return [['.','.','.','.','.'],
			['Y','.','.','R','.'],	
			['Y','Y','R','R','.'],
			['R','R','Y','R','.'],
			['R','Y','R','Y','Y']]		

def board63():
	return [['.','.','.','.','.'],
			['.','.','.','Y','.'],	
			['R','R','Y','Y','.'],
			['R','Y','R','Y','.'],
			['R','R','Y','R','Y']]		
			

board7str="""\
MOMOM
OMOMM
MMOOO
OOMOM
OMOMM
"""

def board7():
	return [['M', 'O', 'M', 'O', 'M'],
			['O', 'M', 'O', 'M', 'M'],
			['M', 'M', 'O', 'O', 'O'],
			['O', 'O', 'M', 'O', 'M'],
			['O', 'M', 'O', 'M', 'M']]
			

# examples from spec
ex1str = '...R...\n..YRR..\n.RYRYR.\nYYYRYYR'
ex2str = '.......\n...Y...\n..YBY..\n.YBBBY.\nYBBBYBY'
ex3str = '....\n....\n.BB.\n.BS.\nSSBS\n'
ex4str = '...\n.A.\n...\nBAB\n'
ex5str = '....\nXO..\nOOXO\nXXOX\nXOXO\n'
ex6str = '.........\n....OX...\n...OOX...\nO.OOXX.X.\n'

def ex2():
	return [['.', '.', '.', '.', '.', '.', '.'],
       		['.', '.', '.', 'Y', '.', '.', '.'],
       		['.', '.', 'Y', 'B', 'Y', '.', '.'],
       		['.', 'Y', 'B', 'B', 'B', 'Y', '.'],
       		['Y', 'B', 'B', 'B', 'Y', 'B', 'Y']]

def ex6():
	return  [['.', '.', '.', '.', '.', '.', '.', '.', '.'],
       		['.', '.', '.', '.', 'O', 'X', '.', '.', '.'],
       		['.', '.', '.', 'O', 'O', 'X', '.', '.', '.'],
       		['O', '.', 'O', 'O', 'X', 'X', '.', 'X', '.']]


# END SPECIALIZATION SECTION
############################################################################
############################################################################


# enter batch mode by giving a directory to work on as the only argument.
BATCH_MODE = len(sys.argv)==2 and (sys.argv[1] in ["."] or os.path.isdir(sys.argv[1]))

# This class contains multiple "unit tests" that each check
# various inputs to specific functions, checking that we get
# the correct behavior (output value) from completing the call.
class AllTests (unittest.TestCase):
		
	############################################################################
		
	def test_init_board_1  (self): self.assertEqual (init_board(1,1),[['.']])
	def test_init_board_2  (self): self.assertEqual (init_board(1,6),[['.','.','.','.','.','.']])
	def test_init_board_3  (self): self.assertEqual (init_board(7,1),[['.'],['.'],['.'],['.'],['.'],['.'],['.']])
	def test_init_board_4  (self): 
		board = init_board(2,3)
		self.assertEqual(board,[['.','.','.'],['.','.','.']])
		self.assertTrue(id(board[0])!=id(board[1]))		# the two rows should not be aliases

	def test_init_board_5  (self): 
		board = init_board(6,7)
		self.assertEqual(board,[['.','.','.','.','.','.','.'],
								['.','.','.','.','.','.','.'],
								['.','.','.','.','.','.','.'],
								['.','.','.','.','.','.','.'],
								['.','.','.','.','.','.','.'],
								['.','.','.','.','.','.','.']])
		for i in range(6):
			for j in range(i+1,6):
				self.assertTrue(id(board[i])!=id(board[j]))		# any two rows should not be aliases
		
	############################################################

	def test_get_size_1	 (self): self.assertEqual (get_size([['.']]), (1,1))
	def test_get_size_2	 (self): self.assertEqual (get_size([['R','.','.']]), (1,3))
	def test_get_size_3	 (self): self.assertEqual (get_size([['.'],['.'],['.']]), (3,1))
	def test_get_size_4	 (self): self.assertEqual (get_size([['.','A','.'],['.','A','B']]), (2,3))
	def test_get_size_5	 (self): self.assertEqual (get_size(board1()), (6,7))
		
	############################################################

	def test_show_board_1	 (self): self.assertEqual (show_board(board1()), board1str)
	def test_show_board_2	 (self): self.assertEqual (show_board([['.']]), '.\n')
	def test_show_board_3	 (self): self.assertEqual (show_board([['.', '.', '.'] ,['A', 'B', 'A']]), "...\nABA\n")
	def test_show_board_4	 (self): self.assertEqual (show_board(board3()), board3str)
	def test_show_board_5	 (self): self.assertEqual (show_board(board4()), board4str)
		
	############################################################

	def test_read_board_1 	(self): self.assertEqual (read_board(board1str), board1())
	def test_read_board_2 	(self): self.assertEqual (read_board(board3str), board3())
	def test_read_board_3 	(self): self.assertEqual (read_board("...\n\n\nABA\n"), [['.', '.', '.'] ,['A', 'B', 'A']]) #blank line ignored
	def test_read_board_4 	(self): self.assertEqual (read_board(".....\n..\nABAAB\n"), None) #not rectangular board
	def test_read_board_5 	(self): self.assertEqual (read_board("....\nABAA\nBB.@"), None) #invalid symbol
	
	############################################################

	def test_is_valid_coord_1	 (self): self.assertEqual (is_valid_coord(board1(), 0, 0), True)
	def test_is_valid_coord_2	 (self): self.assertEqual (is_valid_coord(board1(), -1, -2), False) #negative indexes not allowed
	def test_is_valid_coord_3	 (self): self.assertEqual (is_valid_coord(board1(), 4, 6), True)
	def test_is_valid_coord_4	 (self): self.assertEqual (is_valid_coord(board1(), 10, 0), False)
	def test_is_valid_coord_5	 (self): self.assertEqual (is_valid_coord(board1(), 2, 7), False)

	############################################################

	def test_get_coords_by_color_1	 (self): self.assertEqual (get_coords_by_color(board1(), 'G'), [])
	def test_get_coords_by_color_2	 (self): self.assertEqual (get_coords_by_color([['G','.'],['Y','Y']],'Y'), [(1,0),(1,1)])
	def test_get_coords_by_color_3	 (self): self.assertEqual (get_coords_by_color([['G','Y','.'],['Y','G','Y']],'Y'), [(0,1),(1,0),(1,2)])
	def test_get_coords_by_color_4	 (self): self.assertEqual (get_coords_by_color(board1(),'R'), [(1,3),(3,3),(4,1),(4,2),(4,3),(5,0),(5,3)])
	def test_get_coords_by_color_5	 (self): self.assertEqual (get_coords_by_color(board1(),'Y'), [(2,3),(3,1),(3,2),(4,0),(5,1),(5,2),(5,4)])

	############################################################

	def test_get_colors_1	 (self): self.assertEqual (get_colors(init_board(2,3)),[])
	def test_get_colors_2	 (self): self.assertEqual (get_colors([['.','G','.'],['.','G','.']]),['G'])
	def test_get_colors_3	 (self): self.assertEqual (get_colors([['.','G','.'],['Y','G','R']]),['G','Y','R'])
	def test_get_colors_4	 (self): self.assertEqual (get_colors(board1()),['R','Y'])
	def test_get_colors_5	 (self): self.assertEqual (get_colors([['A'],['B','C'],['.','D','E','F'],['G','.','.','H','I','J']]),['A','B','C','D','E','F','G','H','I','J']) #invalid board
	
	############################################################

	def test_count_pieces_by_color_1	 (self): self.assertEqual (count_pieces_by_color(board1(), 'G'), 0)
	def test_count_pieces_by_color_2	 (self): self.assertEqual (count_pieces_by_color([['.','Y'],['Y','X']], 'X'), 1)
	def test_count_pieces_by_color_3	 (self): self.assertEqual (count_pieces_by_color(board1(), 'R'), 7)
	def test_count_pieces_by_color_4	 (self): self.assertEqual (count_pieces_by_color(board1(), 'Y'), 7)
	def test_count_pieces_by_color_5	 (self): self.assertEqual (count_pieces_by_color(board6(), '.'), 11)
	
	############################################################

	def test_any_floating_1	 (self): self.assertEqual (any_floating(init_board(6,4)), False)
	def test_any_floating_2	 (self): self.assertEqual (any_floating(board1()), False)
	def test_any_floating_3	 (self): self.assertEqual (any_floating(board3()), False)
	def test_any_floating_4	 (self): self.assertEqual (any_floating(board4()), True)
	def test_any_floating_5	 (self): self.assertEqual (any_floating(board5()), True)

	############################################################

	def test_is_column_full_1	 (self): self.assertEqual (is_column_full([['G','Y','.'],['Y','G','Y']],0), True)
	def test_is_column_full_2	 (self): self.assertEqual (is_column_full([['G','Y','.'],['Y','G','Y']],2), False)
	def test_is_column_full_3	 (self): self.assertEqual (is_column_full(board3(),4), True)
	def test_is_column_full_4	 (self): self.assertEqual (is_column_full(board3(),5), False)
	def test_is_column_full_5	 (self): self.assertEqual (is_column_full(board3(),7), False) # not a valid column
	#def test_is_column_full_6	 (self): self.assertEqual (is_column_full(board3(),-2), False) # not a valid column

	############################################################

	def test_place_one_1	 (self): 
		board = init_board(4,4)
		self.assertEqual (place_one(board,1,'M'), True)	# allowed move, return True
		self.assertEqual (board, [['.','.','.','.'],['.','.','.','.'],['.','.','.','.'],['.','M','.','.']]) # board updated after move

	def test_place_one_2	 (self): 
		board = board3()
		self.assertEqual (place_one(board,4,'M'), False)	# move not allowed, return False
		self.assertEqual (board, board3()) # board not updated after move
		
	def test_place_one_3	 (self): 
		board = board3()
		self.assertEqual (place_one(board,9,'M'), False)	# move not allowed, return False
		self.assertEqual (board, board3()) # board not updated after move

	def test_place_one_4	 (self): 
		board = board1()
		self.assertEqual (place_one(board,4,'R'), True)	# allowed move, return True
		self.assertEqual (board, board11()) # board updated after move

	def test_place_one_5	 (self): 
		board = board1()
		self.assertEqual (place_one(board,6,'R'), True)	# allowed move, return True
		self.assertEqual (place_one(board,2,'Y'), True)	# allowed move, return True
		self.assertEqual (board, board12()) # board updated after two moves

	def test_place_one_6	 (self): 
		board = board21()
		self.assertEqual (place_one(board,3,'B'), True)	# allowed move, return True
		self.assertEqual (place_one(board,3,'G'), True)	# allowed move, return True
		self.assertEqual (place_one(board,3,'B'), False) # cannot add more
		self.assertEqual (place_one(board,2,'G'), True)	# allowed move, return True
		self.assertEqual (board, board22()) # board updated after moves

	############################################################

	def test_pop_out_1	 (self): 
		board = board1()
		self.assertEqual (pop_out(board,5,'M'), False)	# no piece in column 5, return False
		self.assertEqual (board, board1()) # board not updated after move

	def test_pop_out_2	 (self): 
		board = board1()
		self.assertEqual (pop_out(board,3,'Y'), False)	# bottom piece not 'Y', return False
		self.assertEqual (board, board1()) # board not updated after move

	def test_pop_out_3	 (self): 
		board = board1()
		self.assertEqual (pop_out(board,8,'R'), False)	# invalid column, return False
		self.assertEqual (board, board1()) # board not updated after move

	def test_pop_out_4	 (self): 
		board = board1()
		self.assertEqual (pop_out(board,4,'Y'), True)	# valid pop up, return True
		self.assertEqual (board, board13()) # board updated after move

	def test_pop_out_5	 (self): 
		board = board13()
		self.assertEqual (pop_out(board,2,'Y'), True)	# valid pop up, return True
		self.assertEqual (pop_out(board,2,'R'), True)	# valid pop up, return True
		self.assertEqual (pop_out(board,1,'Y'), True)	# valid pop up, return True
		self.assertEqual (pop_out(board,3,'R'), True)	# valid pop up, return True
		self.assertEqual (board, board14()) # board updated after moves

	def test_pop_out_6	 (self): 
		board = board1()
		self.assertEqual (pop_out(board,0,'R'), True)	# valid pop up, return True
		self.assertEqual (pop_out(board,0,'Y'), True)	# valid pop up, return True
		self.assertEqual (pop_out(board,0,'R'), False)	# nothing to pop up
		self.assertEqual (pop_out(board,1,'Y'), True)	# valid pop up, return True
		self.assertEqual (board, board15()) # board updated after moves
		
	############################################################

	def test_check_horizontal_1	 (self): self.assertEqual (check_horizontal(init_board(6,7),1,1), False)
	def test_check_horizontal_2	 (self): self.assertEqual (check_horizontal([['A','A','A','A','B','B','B']], 0, 0), True)
	def test_check_horizontal_3	 (self): self.assertEqual (check_horizontal(board11(), 4, 1), True)
	def test_check_horizontal_4	 (self): self.assertEqual (check_horizontal(board11(), 4, 3), False)
	def test_check_horizontal_5	 (self): self.assertEqual (check_horizontal(board11(), 9, 1), False) #invalid location

	############################################################

	def test_check_vertical_1	 (self): self.assertEqual (check_vertical(init_board(6,7),2,3), False)
	def test_check_vertical_2	 (self): self.assertEqual (check_vertical([['A'], ['A'], ['A'], ['A'], ['A']], 0, 0), True)
	def test_check_vertical_3	 (self): self.assertEqual (check_vertical(board3(),2,3), True)
	def test_check_vertical_4	 (self): self.assertEqual (check_vertical(board3(),4,3), False)
	def test_check_vertical_5	 (self): self.assertEqual (check_vertical(board3(),-4,3), False) #invalid location

	############################################################

	def test_check_major_diagonal_1	 (self): self.assertEqual (check_major_diagonal(init_board(6,7),0,1), False)
	def test_check_major_diagonal_2	 (self): self.assertEqual (check_major_diagonal(board61(),1,0), True)
	def test_check_major_diagonal_3	 (self): self.assertEqual (check_major_diagonal(board61(),2,3), False)
	def test_check_major_diagonal_4	 (self): self.assertEqual (check_major_diagonal(ex2(),1,3), True)
	def test_check_major_diagonal_5	 (self): self.assertEqual (check_major_diagonal(board61(),5,0), False) #invalid location

	############################################################

	def test_check_minor_diagonal_1	 (self): self.assertEqual (check_minor_diagonal(init_board(6,7),5,1), False)
	def test_check_minor_diagonal_2	 (self): self.assertEqual (check_minor_diagonal(board21(),5,0), True)
	def test_check_minor_diagonal_3	 (self): self.assertEqual (check_minor_diagonal(ex2(),4,0), True)
	def test_check_minor_diagonal_4	 (self): self.assertEqual (check_minor_diagonal(board21(),3,2), False)
	def test_check_minor_diagonal_5	 (self): self.assertEqual (check_minor_diagonal(board21(),-1,-7), False) #invalid location

	############################################################

	def test_check_winner_1	 (self): self.assertEqual (check_winner(init_board(6,7)), "pending")
	def test_check_winner_2	 (self): self.assertEqual (check_winner(board1()), "pending")
	def test_check_winner_3	 (self): self.assertEqual (check_winner(board11()), "R") #horizontal
	def test_check_winner_4	 (self): self.assertEqual (check_winner(board21()), "G") #minor diagonal
	def test_check_winner_5	 (self): self.assertEqual (check_winner(board3()), "G") #vertical
	def test_check_winner_6	 (self): self.assertEqual (check_winner(board61()), "Y") #major diagonal
	def test_check_winner_7	 (self): self.assertEqual (check_winner(board7()), "draw") 
	def test_check_winner_8	 (self): self.assertEqual (check_winner(board62()), "tie!") #should not happen

	############################################################


	def test_extra_credit_winning_move_1 (self): 
		self.assertEqual (winning_move(board1(),'R'),4) # horizontal
		self.assertEqual (winning_move(board6(),'Y'),3) # vertical

	def test_extra_credit_winning_move_2 (self): 
		self.assertEqual (winning_move(board2(),'G'),0) # minor diagonal
		self.assertEqual (winning_move(board31(),'G'),2) # minor diagonal

	def test_extra_credit_winning_move_3 (self): 
		self.assertEqual (winning_move(board6(),'R'),0) # major diagonal
		self.assertEqual (winning_move(board63(),'Y'),1) # major diagonal

	def test_extra_credit_winning_move_4 (self): 
		self.assertEqual (winning_move(ex6(),'O'),1) #left most column 
		self.assertEqual (winning_move(ex6(),'X'),5) #left most column
	
	def test_extra_credit_winning_move_5 (self): 
			self.assertEqual (winning_move(board1(),'K'),None) # no such color
			self.assertEqual (winning_move(board1(),'Y'),None) # no winning move for that color
			self.assertEqual (winning_move(board22(),'G'),None) # no winning move for that color			
			self.assertEqual (winning_move(board3(),'G'),None) # already wins
	
	
	############################################################################
	
# This class digs through AllTests, counts and builds all the tests,
# so that we have an entire test suite that can be run as a group.
class TheTestSuite (unittest.TestSuite):
	# constructor.
	def __init__(self,wants):
		self.num_req = 0
		self.num_ec = 0
		# find all methods that begin with "test".
		fs = []
		for w in wants:
			for func in AllTests.__dict__:
				# append regular tests
				# drop any digits from the end of str(func).
				dropnum = str(func)
				while dropnum[-1] in "1234567890":
					dropnum = dropnum[:-1]
				
				if dropnum==("test_"+w+"_") and (not (dropnum==("test_extra_credit_"+w+"_"))):
					fs.append(AllTests(str(func)))
				if dropnum==("test_extra_credit_"+w+"_") and not BATCH_MODE:
					fs.append(AllTests(str(func)))
		
#		print("TTS ====> ",list(map(lambda f: (f,id(f)),fs)))
		# call parent class's constructor.
		unittest.TestSuite.__init__(self,fs)

class TheExtraCreditTestSuite (unittest.TestSuite):
		# constructor.
		def __init__(self,wants):
			# find all methods that begin with "test_extra_credit_".
			fs = []
			for w in wants:
				for func in AllTests.__dict__:
					if str(func).startswith("test_extra_credit_"+w):
						fs.append(AllTests(str(func)))
		
#			print("TTS ====> ",list(map(lambda f: (f,id(f)),fs)))
			# call parent class's constructor.
			unittest.TestSuite.__init__(self,fs)

# all (non-directory) file names, regardless of folder depth,
# under the given directory 'dir'.
def files_list(dir):
	this_file = __file__
	if dir==".":
		dir = os.getcwd()
	info = os.walk(dir)
	filenames = []
	for (dirpath,dirnames,filez) in info:
#		print(dirpath,dirnames,filez)
		if dirpath==".":
			continue
		for file in filez:
			if file==this_file:
				continue
			filenames.append(os.path.join(dirpath,file))
#		print(dirpath,dirnames,filez,"\n")
	return filenames

def main():
	if len(sys.argv)<2:
		raise Exception("needed student's file name as command-line argument:"\
			+"\n\t\"python3 testerX.py gmason76_2xx_Px.py\"")
	
	if BATCH_MODE:
		print("BATCH MODE.\n")
		run_all()
		return
		
	else:
		want_all = len(sys.argv) <=2
		wants = []
		# remove batch_mode signifiers from want-candidates.
		want_candidates = sys.argv[2:]
		for i in range(len(want_candidates)-1,-1,-1):
			if want_candidates[i] in ['.'] or os.path.isdir(want_candidates[i]):
				del want_candidates[i]
	
		# set wants and extra_credits to either be the lists of things they want, or all of them when unspecified.
		wants = []
		extra_credits = []
		if not want_all:
			for w in want_candidates:
				if w in REQUIRED_DEFNS:
					wants.append(w)
				elif w in SUB_DEFNS:
					wants.append(w)
				elif w in EXTRA_CREDIT_DEFNS:
					extra_credits.append(w)
				else:
					raise Exception("asked to limit testing to unknown function '%s'."%w)
		else:
			wants = REQUIRED_DEFNS + SUB_DEFNS
			extra_credits = EXTRA_CREDIT_DEFNS
		
		# now that we have parsed the function names to test, run this one file.	
		run_one(wants,extra_credits)	
		return
	return # should be unreachable!	

# only used for non-batch mode, since it does the printing.
# it nicely prints less info when no extra credit was attempted.
def run_one(wants, extra_credits):
	
	has_reqs = len(wants)>0
	has_ec   = len(extra_credits)>0
	
	# make sure they exist.
	passed1 = 0
	passed2 = 0
	tried1 = 0
	tried2 = 0
	
	# only run tests if needed.
	if has_reqs:
		print("\nRunning required definitions:")
		(tag, passed1,tried1) = run_file(sys.argv[1],wants,False)
	if has_ec:
		print("\nRunning extra credit definitions:")
		(tag, passed2,tried2) = run_file(sys.argv[1],extra_credits,True)
	
	# print output based on what we ran.
	if has_reqs and not has_ec:
		print("\n%d/%d Required test cases passed (worth %d each)" % (passed1,tried1,weight_required) )
		print("\nScore based on test cases: %.2f/%d (%.2f*%d) " % (
																passed1*weight_required, 
																total_points_from_tests,
																passed1,
																weight_required
															 ))
	elif has_ec and not has_reqs:
		print("%d/%d Extra credit test cases passed (worth %d each)" % (passed2, tried2, weight_extra_credit))
	else: # has both, we assume.
		print("\n%d / %d Required test cases passed (worth %d each)" % (passed1,tried1,weight_required) )
		print("%d / %d Extra credit test cases passed (worth %d each)" % (passed2, tried2, weight_extra_credit))
		print("\nScore based on test cases: %.2f / %d ( %d * %d + %d * %d) " % (
																passed1*weight_required+passed2*weight_extra_credit, 
																total_points_from_tests,
																passed1,
																weight_required,
																passed2,
																weight_extra_credit
															 ))
	if CURRENTLY_GRADING:
		print("( %d %d %d %d )\n%s" % (passed1,tried1,passed2,tried2,tag))

# only used for batch mode.
def run_all():
		filenames = files_list(sys.argv[1])
		#print(filenames)
		
		wants = REQUIRED_DEFNS + SUB_DEFNS
		extra_credits = EXTRA_CREDIT_DEFNS
		
		results = []
		for filename in filenames:
			print(" Batching on : " +filename)
			# I'd like to use subprocess here, but I can't get it to give me the output when there's an error code returned... TODO for sure.
			lines = os.popen("python3 tester1p.py \""+filename+"\"").readlines()
			
			# delay of shame...
			time.sleep(DELAY_OF_SHAME)
			
			name = os.path.basename(lines[-1])
			stuff =lines[-2].split(" ")[1:-1]
			print("STUFF: ",stuff, "LINES: ", lines)
			(passed_req, tried_req, passed_ec, tried_ec) = stuff
			results.append((lines[-1],int(passed_req), int(tried_req), int(passed_ec), int(tried_ec)))
			continue
		
		print("\n\n\nGRAND RESULTS:\n")
		
			
		for (tag_req, passed_req, tried_req, passed_ec, tried_ec) in results:
			name = os.path.basename(tag_req).strip()
			earned   = passed_req*weight_required + passed_ec*weight_extra_credit
			possible = tried_req *weight_required # + tried_ec *weight_extra_credit
			print("%10s : %3d / %3d = %5.2d %% (%d/%d*%d + %d/%d*%d)" % (
															name,
															earned,
															possible, 
															(earned/possible)*100,
															passed_req,tried_req,weight_required,
															passed_ec,tried_ec,weight_extra_credit
														  ))
# only used for batch mode.
def run_all_orig():
		filenames = files_list(sys.argv[1])
		#print(filenames)
		
		wants = REQUIRED_DEFNS + SUB_DEFNS
		extra_credits = EXTRA_CREDIT_DEFNS
		
		results = []
		for filename in filenames:
			# wipe out all definitions between users.
			for fn in REQUIRED_DEFNS+EXTRA_CREDIT_DEFNS	:
				globals()[fn] = decoy(fn)
				fn = decoy(fn)
			try:
				name = os.path.basename(filename)
				print("\n\n\nRUNNING: "+name)
				(tag_req, passed_req, tried_req) = run_file(filename,wants,False)
				(tag_ec,  passed_ec,  tried_ec ) = run_file(filename,extra_credits,True)
				results.append((tag_req,passed_req,tried_req,tag_ec,passed_ec,tried_ec))
				print(" ###### ", results)
			except SyntaxError as e:
				tag = filename+"_SYNTAX_ERROR"
				results.append((tag,0,len(wants),tag,0,len(extra_credits)))
			except NameError as e:
				tag =filename+"_Name_ERROR"
				results.append((tag,0,len(wants),tag,0,len(extra_credits)))
			except ValueError as e:
				tag = filename+"_VALUE_ERROR"
				results.append((tag,0,len(wants),tag,0,len(extra_credits)))
			except TypeError as e:
				tag = filename+"_TYPE_ERROR"
				results.append((tag,0,len(wants),tag,0,len(extra_credits)))
			except ImportError as e:
				tag = filename+"_IMPORT_ERROR_TRY_AGAIN"
				results.append((tag,0,len(wants),tag,0,len(extra_credits)))
			except Exception as e:
				tag = filename+str(e.__reduce__()[0])
				results.append((tag,0,len(wants),tag,0,len(extra_credits)))
		
# 			try:
# 				print("\n |||||||||| scrupe: "+str(scruples))
# 			except Exception as e:
# 				print("NO SCRUPE.",e)
# 			scruples = None
		
		print("\n\n\nGRAND RESULTS:\n")
		for (tag_req, passed_req, tried_req, tag_ec, passed_ec, tried_ec) in results:
			name = os.path.basename(tag_req)
			earned   = passed_req*weight_required + passed_ec*weight_extra_credit
			possible = tried_req *weight_required # + tried_ec *weight_extra_credit
			print("%10s : %3d / %3d = %5.2d %% (%d/%d*%d + %d/%d*%d)" % (
															name,
															earned,
															possible, 
															(earned/possible)*100,
															passed_req,tried_req,weight_required,
															passed_ec,tried_ec,weight_extra_credit
														  ))

def try_copy(filename1, filename2, numTries):
	have_copy = False
	i = 0
	while (not have_copy) and (i < numTries):
		try:
			# move the student's code to a valid file.
			shutil.copy(filename1,filename2)
			
			# wait for file I/O to catch up...
			if(not wait_for_access(filename2, numTries)):
				return False
				
			have_copy = True
		except PermissionError:
			print("Trying to copy "+filename1+", may be locked...")
			i += 1
			time.sleep(1)
		except BaseException as e:
			print("\n\n\n\n\n\ntry-copy saw: "+e)
	
	if(i == numTries):
		return False
	return True

def try_remove(filename, numTries):
	removed = False
	i = 0
	while os.path.exists(filename) and (not removed) and (i < numTries):
		try:
			os.remove(filename)
			removed = True
		except OSError:
			print("Trying to remove "+filename+", may be locked...")
			i += 1
			time.sleep(1)
	if(i == numTries):
		return False
	return True

def wait_for_access(filename, numTries):
	i = 0
	while (not os.path.exists(filename) or not os.access(filename, os.R_OK)) and i < numTries:
		print("Waiting for access to "+filename+", may be locked...")
		time.sleep(1)
		i += 1
	if(i == numTries):
		return False
	return True

# this will group all the tests together, prepare them as 
# a test suite, and run them.
def run_file(filename,wants=None,checking_ec = False):
	if wants==None:
		wants = []
	
	# move the student's code to a valid file.
	if(not try_copy(filename,"student.py", 5)):
		print("Failed to copy " + filename + " to student.py.")
		quit()
		
	# import student's code, and *only* copy over the expected functions
	# for later use.
	import importlib
	count = 0
	while True:
		try:
# 			print("\n\n\nbegin attempt:")
			while True:
				try:
					f = open("student.py","a")
					f.close()
					break
				except:
					pass
# 			print ("\n\nSUCCESS!")
				
			import student
			importlib.reload(student)
			break
		except ImportError as e:
			print("import error getting student... trying again. "+os.getcwd(), os.path.exists("student.py"),e)
			time.sleep(0.5)
			while not os.path.exists("student.py"):
				time.sleep(0.5)
			count+=1
			if count>3:
				raise ImportError("too many attempts at importing!")
		except SyntaxError as e:
			print("SyntaxError in "+filename+":\n"+str(e))
			print("Run your file without the tester to see the details")
			return(filename+"_SYNTAX_ERROR",None, None, None)
		except NameError as e:
			print("NameError in "+filename+":\n"+str(e))
			print("Run your file without the tester to see the details")
			return((filename+"_Name_ERROR",0,1))	
		except ValueError as e:
			print("ValueError in "+filename+":\n"+str(e))
			print("Run your file without the tester to see the details")
			return(filename+"_VALUE_ERROR",0,1)
		except TypeError as e:
			print("TypeError in "+filename+":\n"+str(e))
			print("Run your file without the tester to see the details")
			return(filename+"_TYPE_ERROR",0,1)
		except ImportError as e:			
			print("ImportError in "+filename+":\n"+str(e))
			print("Run your file without the tester to see the details or try again")
			return((filename+"_IMPORT_ERROR_TRY_AGAIN	",0,1))	
		except Exception as e:
			print("Exception in loading"+filename+":\n"+str(e))
			print("Run your file without the tester to see the details")
			return(filename+str(e.__reduce__()[0]),0,1)
	
	# make a global for each expected definition.
	for fn in REQUIRED_DEFNS+EXTRA_CREDIT_DEFNS	:
		globals()[fn] = decoy(fn)
		try:
			globals()[fn] = getattr(student,fn)
		except:
			if fn in wants:
				print("\nNO DEFINITION FOR '%s'." % fn)	
	
	if not checking_ec:
		# create an object that can run tests.
		runner = unittest.TextTestRunner()
	
		# define the suite of tests that should be run.
		suite = TheTestSuite(wants)
	
	
		# let the runner run the suite of tests.
		ans = runner.run(suite)
		num_errors   = len(ans.__dict__['errors'])
		num_failures = len(ans.__dict__['failures'])
		num_tests    = ans.__dict__['testsRun']
		num_passed   = num_tests - num_errors - num_failures
		# print(ans)
	
	else:
		# do the same for the extra credit.
		runner = unittest.TextTestRunner()
		suite = TheExtraCreditTestSuite(wants)
		ans = runner.run(suite)
		num_errors   = len(ans.__dict__['errors'])
		num_failures = len(ans.__dict__['failures'])
		num_tests    = ans.__dict__['testsRun']
		num_passed   = num_tests - num_errors - num_failures
		#print(ans)
	
	# remove our temporary file.
	os.remove("student.py")
	if os.path.exists("__pycache__"):
		shutil.rmtree("__pycache__")
	if(not try_remove("student.py", 5)):
		print("Failed to remove " + filename + " to student.py.")
	
	tag = ".".join(filename.split(".")[:-1])
	
	
	return (tag, num_passed, num_tests)


# make a global for each expected definition.
def decoy(name):
		# this can accept any kind/amount of args, and will print a helpful message.
		def failyfail(*args, **kwargs):
			return ("<no '%s' definition was found - missing, or typo perhaps?>" % name)
		return failyfail

# this determines if we were imported (not __main__) or not;
# when we are the one file being run, perform the tests! :)
if __name__ == "__main__":
	main()
