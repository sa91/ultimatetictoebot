from copy import deepcopy
from math import exp
import sys
import random
import signal


StateVisited={}
POSINF = float('inf')
NEGINF = float('-inf')

DRAW = 876686789789890
two_with_center = 300
two_without_center = 200
for_each_cell = 25
two_with_center_to_fill = 125
win = 2500
lose = -2800
Heuristic_block=[]
## Copied Functions
class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()

def determine_blocks_allowed(old_move, block_stat):
	blocks_allowed = []
	if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
		blocks_allowed = [1,3]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
		blocks_allowed = [1,5]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
		blocks_allowed = [3,7]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
		blocks_allowed = [5,7]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
		blocks_allowed = [0,2]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
		blocks_allowed = [0,6]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
		blocks_allowed = [6,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
		blocks_allowed = [2,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
		blocks_allowed = [4]
	else:
		sys.exit(1)

	final_blocks_allowed = []
	for i in blocks_allowed:
		if block_stat[i] == '-':
			final_blocks_allowed.append(i)
	if len(final_blocks_allowed) == 0 :
		for i in xrange(len(block_stat)) :
			if block_stat[i] == '-':
				final_blocks_allowed.append(i)

	return final_blocks_allowed

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in xrange(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in xrange(id1*3,id1*3+3):
			for j in xrange(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		new_blal = []
		all_blal = [0,1,2,3,4,5,6,7,8]
		for i in all_blal:
			if block_stat[i]=='-':
				new_blal.append(i)

		for idb in new_blal:
			id1 = idb/3
			id2 = idb%3
			for i in xrange(id1*3,id1*3+3):
				for j in xrange(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))
	return cells
		
# Returns True if move is valid
def check_valid_move(game_board, block_stat, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True

	#List of permitted blocks, based on old move.
	blocks_allowed  = determine_blocks_allowed(old_move, block_stat)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
	cells = get_empty_out_of(game_board, blocks_allowed, block_stat)
	#Checks if you made a valid move. 
	if current_move in cells:
		return True
	else:
		return False

def update_lists(game_board, block_stat, move_ret, fl):

	game_board[move_ret[0]][move_ret[1]] = fl

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3	
	id1 = block_no/3
	id2 = block_no%3
	mflg = 0

	flag = 0
	for i in xrange(id1*3,id1*3+3):
		for j in xrange(id2*3,id2*3+3):
			if game_board[i][j] == '-':
				flag = 1


	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if mflg != 1:
                    for i in xrange(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-' and game_board[id1*3][i] != 'D':
                                mflg = 1
                                break
		if mflg != 1:
                    for i in xrange(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-' and game_board[i][id2*3] != 'D':
                                mflg = 1
                                break
	if flag == 0:
		block_stat[block_no] = 'D'
	if mflg == 1:
		block_stat[block_no] = fl
	
	return mflg

#Check win
def terminal_state_reached(game_board, block_stat,point1,point2):
	### we are now concerned only with block_stat
	bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='D') or (bs[3]!='-' and bs[3]!='D' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='D' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		return True, 'W'
	## Col win
	elif (bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-' and bs[0]!='D') or (bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-' and bs[4]!='D') or (bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-' and bs[5]!='D'):
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='D') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='D'):
		return True, 'W'
	else:
		smfl = 0
		for i in xrange(9):
			if block_stat[i] == '-':
				smfl = 1
				break
		if smfl == 1:
			return False, 'Continue'
		
		else:
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
				return True, 'D'	

def print_lists(gb, bs):
	print '=========== Desiered Board ==========='
	for i in xrange(9):
		if i > 0 and i % 3 == 0:
			print
		for j in xrange(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Desiered Block Status ========="
	for i in xrange(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
## INSERT VERIFICATION IF CODE PRODUCES INVALID MOVE
def evaluate_block(block, myflag):
	utility = 0
	if myflag == "x":
		oppflag = "o"
	else:
		oppflag = "x"
	if (block[0][0] == myflag and block[1][1] == myflag and block[2][2] == "-") or (block[0][0] == "-" and block[1][1] == myflag and block[2][2] == myflag):
		utility += two_with_center
	elif block[0][0] == myflag and block[1][1] == "-" and block[2][2] == myflag :
		utility += two_with_center_to_fill
	elif (block[0][0] == oppflag and block[1][1] == oppflag and block[2][2] == "-") or (block[0][0] == "-" and block[1][1] == oppflag and block[2][2] == oppflag):
		utility -= two_with_center
	elif block[0][0] == oppflag and block[1][1] == "-" and block[2][2] == oppflag :
		utility -= two_with_center_to_fill

	if (block[0][2] == myflag and block[1][1] == myflag and block[2][0] == "-") or (block[0][2] == "-" and block[1][1] == myflag and block[2][0] == myflag) :
		utility += two_with_center
	elif block[0][2] == myflag and block[1][1] == "-" and block[2][0] == myflag :
		utility += two_with_center_to_fill
	elif (block[0][2] == oppflag and block[1][1] == oppflag and block[2][0] == "-") or (block[0][2] == "-" and block[1][1] == oppflag and block[2][0] == oppflag) :
		utility -= two_with_center
	elif block[0][2] == oppflag and block[1][1] == "-" and block[2][0] == oppflag :
		utility -= two_with_center_to_fill

	if (block[0][1] == myflag and block[1][1] == myflag and block[2][1] == "-") or (block[0][1] == "-" and block[1][1] == myflag and block[2][1] == myflag) :
		utility += two_with_center
	elif block[0][1] == myflag and block[1][1] == "-" and block[2][1] == myflag :
		utility += two_with_center_to_fill
	elif (block[0][1] == oppflag and block[1][1] == oppflag and block[2][1] == "-") or (block[0][1] == "-" and block[1][1] == oppflag and block[2][1] == oppflag) :
		utility -= two_with_center
	elif block[0][1] == oppflag and block[1][1] == "-" and block[2][1] == oppflag :
		utility -= two_with_center_to_fill

	if (block[1][0] == myflag and block[1][1] == myflag and block[1][2] == "-") or (block[1][0] == "-" and block[1][1] == myflag and block[1][2] == myflag) :
		utility += two_with_center
	elif block[1][0] == myflag and block[1][1] == "-" and block[1][2] == myflag :
		utility += two_with_center_to_fill
	elif (block[1][0] == oppflag and block[1][1] == oppflag and block[1][2] == "-") or (block[1][0] == "-" and block[1][1] == oppflag and block[1][2] == oppflag) :
		utility -= two_with_center
	elif block[1][0] == oppflag and block[1][1] == "-" and block[1][2] == oppflag :
		utility -= two_with_center_to_fill

	if (block[0][0] == myflag and block[0][1] == myflag and block[0][2] == "-") or (block[0][0] == "-" and block[0][1] == myflag and block[0][2] == myflag) or (block[0][0] == myflag and block[0][1] == "-" and block[0][2] == myflag):
		utility += two_without_center
	elif (block[0][0] == oppflag and block[0][1] == oppflag and block[0][2] == "-") or (block[0][0] == "-" and block[0][1] == oppflag and block[0][2] == oppflag) or (block[0][0] == oppflag and block[0][1] == "-" and block[0][2] == oppflag):
		utility -= two_without_center
	if (block[2][0] == myflag and block[2][1] == myflag and block[2][2] == "-") or (block[2][0] == "-" and block[2][1] == myflag and block[2][2] == myflag) or (block[2][0] == myflag and block[2][1] == "-" and block[2][2] == myflag):
		utility += two_without_center
	elif (block[2][0] == oppflag and block[2][1] == oppflag and block[2][2] == "-") or (block[2][0] == "-" and block[2][1] == oppflag and block[2][2] == oppflag) or (block[2][0] == oppflag and block[2][1] == "-" and block[2][2] == oppflag):
		utility -= two_without_center
	if (block[0][0] == myflag and block[1][0] == myflag and block[2][0] == "-") or (block[0][0] == "-" and block[1][0] == myflag and block[2][0] == myflag) or (block[0][0] == myflag and block[1][0] == "-" and block[2][0] == myflag):
		utility += two_without_center
	elif (block[0][0] == oppflag and block[1][0] == oppflag and block[2][0] == "-") or (block[0][0] == "-" and block[1][0] == oppflag and block[2][0] == oppflag) or (block[0][0] == oppflag and block[1][0] == "-" and block[2][0] == oppflag):
		utility -= two_without_center
	if (block[2][0] == myflag and block[2][1] == myflag and block[2][2] == "-") or (block[2][0] == "-" and block[2][1] == myflag and block[2][2] == myflag) or (block[2][0] == myflag and block[2][1] == "-" and block[2][2] == myflag):
		utility += two_without_center
	elif (block[2][0] == oppflag and block[2][1] == oppflag and block[2][2] == "-") or (block[2][0] == "-" and block[2][1] == oppflag and block[2][2] == oppflag) or (block[2][0] == oppflag and block[2][1] == "-" and block[2][2] == oppflag):
		utility -= two_without_center
	for i in xrange(0, 3):
		for j in xrange(0, 3):
			if block[i][j] == "x":
				utility += for_each_cell
			elif block[i][j] == "o":
				utility -= for_each_cell
	return utility

def evaluate_grid(bs):
	ret = 0
	const = win**3/8;
	for i in xrange(0,9,3):
		v=1
		for j in xrange(3) :
			v *= bs[i+j]
		if v < const:
			ret += (v-(const*8))**3
		else :
			ret += v**3
		
	for i in xrange(3):
		v=1
		for i in xrange(0,9,3):
				v *= bs[i+j]
		if v < const:
			ret += (v-(const*8))**3
		else :
			ret += v**3
		
	v=1
	for i in xrange(3):
		v *= bs[i*4]
	if v < const:
			ret += (v-(const*8))**3
	else :
			ret += v**3
	
	v=1
	for i in xrange(3):
		v *= bs[2*(i+1)]
	if v < const:
			ret += (v-(const*8))**3
	else :
			ret += v**3
	
	if bs[4] < win/2 :
			ret += (bs[4]-(win))**3
	else :
			ret += bs[4]**3

	return ret


	

class State(object):
	def __init__ (self, temp_board, temp_block, old_move, flag, oppflag, pt1, pt2):
		self.board = temp_board
		self.block = temp_block
		self.old_move = old_move #opposition move
		self.flag = flag
		self.oppflag = oppflag
		self.pt1 = pt1
		self.pt2 = pt2


## ourflag = 2 Nowassumption x
def initialise():
	uplimit=3**9
	A=[]
	A.append(['-','-','-'])
	for i in xrange(uplimit):
		A=[]
		A.append(['-','-','-'])
		A.append(['-','-','-'])
		A.append(['-','-','-'])
		j=i
		k=0
		while j > 0 :		
			if j%3 == 2 :
				A[k/3][k%3]='x'
			elif j%3 == 1 :
				A[k/3][k%3]='o'
			k+=1
			j/=3
		Heuristic_block.append(evaluate_block(A,'x'))



def Heuristics(state,Playerflag):
	Block_information=[]
	for  i in xrange(len(state.block)) :
		blockno = i
		if state.block[i] == Playerflag :
			Block_information.append(win+3000)
		elif state.block[i] == '-' :
			Topleft = (blockno/3)*3,(blockno%3)*3
			Hash=0 
			v=1
			for i in xrange(3):
				for j in xrange (3):
					if state.board[Topleft[0]+i][Topleft[1]+j] == Playerflag :
						Hash += 2*v
					elif state.board[Topleft[0]+i][Topleft[1]+j] == '-' :
						pass
					else :
						Hash += v
					v *= 3
			Block_information.append(Heuristic_block[Hash]+3000)
		else :
			Block_information.append(lose+3000)
	VALUE = evaluate_grid(Block_information)
	return VALUE



def statekeybase(temp_board):
	coefficient=1 
	ret=0 
	v=1
	for i in xrange(len(temp_board)):
		for j in xrange(len(temp_board[i])):
			if temp_board[i][j] == 'x':
				ret+=(v*2)
			elif temp_board[i][j] == 'o':
				ret+=v
			v*=3
	return ret


def maxvalue(state, alpha, beta, base):
	
	status,mesg = terminal_state_reached(state.board,state.block,state.pt1,state.pt2)
	if status == True:
		#print_lists(state.board,state.block)
		#print state.old_move
		if mesg == 'P2' or mesg == 'W' :
			#print "NEGINF"
			return NEGINF,state.old_move,0
		elif mesg == 'P1':
			#print "POSINF"
			return POSINF,state.old_move,0
		elif mesg == 'D':
			#print "DRAW"
			return DRAW,state.old_move,0	
	v = NEGINF
	#print state.old_move, state.block
	blocks_allowed  = determine_blocks_allowed(state.old_move, state.block)
	#print "Done"
	cells = get_empty_out_of(state.board, blocks_allowed , state.block)
	#print "kyunki saas bhi kabhi bahu thi"
	MOVETAKEN = (-1,-1)
	Gflag = 0
	
	for cell in cells :
		NewKey=base+(3**(cell[0]+cell[1]))
		NewState = deepcopy(state)
		NewState.oldmove = cell
		NewState.pt1 += update_lists(NewState.board, NewState.block,cell,state.flag)
		NewState.flag = state.oppflag
		NewState.oppflag = state.flag		
		if StateVisited.has_key(NewKey) == True :
			VALUE = StateVisited[NewKey]
		else :
			try:
				VALUE,MOVE,Gflag = minvalue(NewState,alpha,beta,NewKey)
				StateVisited[NewKey] = VALUE
			except Exception as e:
				#print e,"hello3"
				#print "GOT it"
				Gflag = 2
		if Gflag == 2:
			VAL=Heuristics(deepcopy(state),state.flag)
			#print VALUE
			return VAL,state.old_move,1
		if v <= VALUE :
			v = VALUE
			MOVETAKEN = NewState.oldmove
		if v >= beta :
			return v,MOVETAKEN,Gflag
		if Gflag == 1:
			return v,MOVETAKEN,1
		alpha = max(v, alpha)
	return v,MOVETAKEN,0
	

 

def minvalue(state, alpha, beta, base):
	#print "min"
	status,mesg = terminal_state_reached(state.board,state.block,state.pt1,state.pt2)
	if status == True:
		#print_lists(state.board,state.block)
		#print state.old_move
		if mesg == 'P1' or mesg == 'W' :
			#print "POSINF"
			return POSINF,state.old_move,0
		elif mesg == 'P2':
			#print "NEGINF"
			return NEGINF,state.old_move,0
		elif mesg == 'D':
			#print "DRAW"
			return DRAW,state.old_move,0
		
	v = POSINF

	
	blocks_allowed  = determine_blocks_allowed(state.old_move, state.block)
	cells = get_empty_out_of(state.board, blocks_allowed , state.block)
	
	MOVETAKEN = (-1,-1)
	Gflag=0
	for cell in cells :
		NewKey=base+(3**(cell[0]+cell[1]))
		NewState = deepcopy(state)
		NewState.oldmove = cell
		NewState.pt2 += update_lists( NewState.board, NewState.block, cell, state.flag)
		NewState.flag = state.oppflag
		NewState.oppflag = state.flag
		if StateVisited.has_key(NewKey) == True :
				VALUE = StateVisited[NewKey]
		else:
			try:
				VALUE,MOVE,Gflag = maxvalue(NewState,alpha,beta,NewKey)
				StateVisited[NewKey] = VALUE
			except Exception as e:
				#print e,"hello2"
				Gflag=2
		if Gflag == 2:
			VAL=Heuristics(deepcopy(state),state.flag)
			#print VALUE
			return VAL,state.old_move,1
		if v >= VALUE :
			v = VALUE
			MOVETAKEN = NewState.oldmove
		if v <= alpha :
			return v,MOVETAKEN,Gflag
		if Gflag == 1:
			return v,MOVETAKEN,Gflag
		beta = min(v, beta)
	return v,MOVETAKEN,0
	


def alphabeta(state):
	#print "alphabeta start"
	StateVisited.clear();
	TIMEALLOWED = 11
	cell = (-1,-1)
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(TIMEALLOWED)
	try:
	#if True:
		v,cell,gflag = maxvalue(state,NEGINF,POSINF,statekeybase(state.board))
	except Exception as e:
		blocks_allowed  = determine_blocks_allowed(state.old_move, state.block)
		cells = get_empty_out_of(state.board, blocks_allowed , state.block)
		return cells[random.randrange(len(cells))]
	signal.alarm(0)
	#print  "alpha beta ends : ",gflag
	return cell

	
 ## initialise dekh ke   
class Player12:
		def __init__(self):
			initialise()
			self.number_of_moves_taken = 0
			self.temporary_board = []
			self.temporary_block_stat = []
			self.old_move=()
			self.opp_flag = ""
			self.pt1=0;
			self.pt2=0;
			self.limit=8

		def registermove(self,flag,move):
			f=0
			if not check_valid_move(self.temporary_board, self.temporary_block_stat , move, self.old_move):
				f=1
			if f == 1:
					blocks_allowed  = determine_blocks_allowed(self.old_move, self.temporary_block_stat)
					cells = get_empty_out_of(self.temporary_board , blocks_allowed , self.temporary_block_stat)
					move=cells[random.randrange(len(cells))]
			self.pt1 += update_lists(self.temporary_board, self.temporary_block_stat, move, flag)
			return move

		def move(self,temp_board,temp_block,old_move,myflag):
			#print "myflag is ",myflag
			#print self.number_of_moves_taken
			if myflag == "x":
				self.opp_flag = "o"
			else:
				self.opp_flag = "x"
			self.old_move=deepcopy(old_move)
			self.temporary_board = deepcopy(temp_board)
			self.temporary_block_stat = deepcopy(temp_block)
			self.pt2+= update_lists(self.temporary_board, self.temporary_block_stat, old_move, self.opp_flag)
			state=State(temp_board,temp_block,old_move,myflag,self.opp_flag,self.pt1,self.pt2)
			blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
			cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
			#print "blocks allowed is ", blocks_allowed
			#print "cells allowed is ", cells
			#return self.registermove(myflag, alphabeta(state))
			if old_move == (-1, -1):
				self.limit -= 1
				self.number_of_moves_taken = 1
				return self.registermove(myflag, (3, 5))
				
			else:
				if 4 in blocks_allowed:
						counter_of_flag = 0
						for i in xrange(3, 6):
							for j in xrange(3, 6):
								if self.temporary_board[i][i] == myflag:
									counter_of_flag += 1
						if counter_of_flag >= 2:
							if self.temporary_board[5][3] == myflag and self.temporary_board[5][5] == myflag and (5, 4) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (5, 4))
								
							elif self.temporary_board[5][4] == myflag and self.temporary_board[5][5] == myflag and (5, 3) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (5, 3))
								
							elif self.temporary_board[5][4] == myflag and self.temporary_board[5][3] == myflag and (5, 5) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (5, 5))
								

							elif self.temporary_board[5][3] == myflag and self.temporary_board[3][5] == myflag and (4, 4) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (4, 4))

							elif self.temporary_board[4][4] == myflag and self.temporary_board[3][5] == myflag and (5, 3) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (5, 3))
								
							elif self.temporary_board[4][4] == myflag and self.temporary_board[5][3] == myflag and (3, 5) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (3, 5))
								

							elif self.temporary_board[5][3] == myflag and self.temporary_board[3][3] == myflag and (4, 3) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (4, 3))
								
							elif self.temporary_board[4][3] == myflag and self.temporary_board[3][3] == myflag and (5, 3) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (5, 3))
								
							elif self.temporary_board[4][3] == myflag and self.temporary_board[5][3] == myflag and (3, 3) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (3, 3))
								

							elif self.temporary_board[3][5] == myflag and self.temporary_board[5][5] == myflag and (4, 5) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (4, 5))
								
							elif self.temporary_board[4][5] == myflag and self.temporary_board[5][5] == myflag and (3, 5) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (3, 5))
								
							elif self.temporary_board[4][5] == myflag and self.temporary_board[3][5] == myflag and (5, 5) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (5, 5))
								

							elif self.temporary_board[3][3] == myflag and self.temporary_board[3][5] == myflag and (3, 4) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (3, 4))
								
							elif self.temporary_board[3][4] == myflag and self.temporary_board[3][5] == myflag and (3, 3) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (3, 3))
								
							elif self.temporary_board[3][4] == myflag and self.temporary_board[3][3] == myflag and (3, 5) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (3, 5))
								

							elif self.temporary_board[3][3] == myflag and self.temporary_board[5][5] == myflag and (4, 4) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (4, 4))
								
							elif self.temporary_board[4][4] == myflag and self.temporary_board[5][5] == myflag and (3, 3) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (3, 3))
								
							elif self.temporary_board[4][4] == myflag and self.temporary_board[3][3] == myflag and (5, 5) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (5, 5))
								

							elif self.temporary_board[4][3] == myflag and self.temporary_board[4][5] == myflag and (4, 4) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (4, 4))
								
							elif self.temporary_board[4][4] == myflag and self.temporary_board[4][5] == myflag and (4, 3) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (4, 3))
								
							elif self.temporary_board[4][4] == myflag and self.temporary_board[4][3] == myflag and (4, 5) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (4, 5))
								

							elif self.temporary_board[3][4] == myflag and self.temporary_board[4][4] == myflag and (5, 4) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (5, 4))
								
							elif self.temporary_board[3][4] == myflag and self.temporary_board[5][4] == myflag and (4, 4) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (4, 4))
								
							elif self.temporary_board[4][4] == myflag and self.temporary_board[5][4] == myflag and (3, 4) in cells:
								self.number_of_moves_taken += 1
								return self.registermove(myflag, (3, 4))
						elif counter_of_flag <= 2:
							for cell in cells:
								search_moves_allowed = determine_blocks_allowed(cell, temp_block)
								if search_moves_allowed == [1, 5] or search_moves_allowed == [5, 7]:
									self.number_of_moves_taken += 1
									return self.registermove(myflag, cell)
							self.number_of_moves_taken += 1
							return self.registermove(myflag, alphabeta(state))
								
				
				if self.number_of_moves_taken <= self.limit:
					for cell in cells:
						search_moves_allowed = determine_blocks_allowed(cell, temp_block)
						#print "search_moves_allowed : ",search_moves_allowed
						if search_moves_allowed == [1, 5] or search_moves_allowed == [5, 7] or search_moves_allowed == [1] or search_moves_allowed == [5] or search_moves_allowed == [7]:
							self.number_of_moves_taken += 1
							return self.registermove(myflag, cell)
					self.number_of_moves_taken += 1
					return self.registermove(myflag, alphabeta(state))
				else:
					return self.registermove(myflag, alphabeta(state))
					