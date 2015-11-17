import random
import datetime
import argparse
import atexit
import sys
from string import ascii_uppercase
from math import fabs
from copy import deepcopy

#TODO use enchant to detect if a word is in the dictionary

# CLASSES
class Coordinate():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return str(self.x+1) + "," + str(self.y+1)
		
	def __repr__(self):
		return "(" + self.__str__() + ")"

	def __eq__(self,other):
		return self.x==other.x and self.y==other.y

	def __ne__(self,other):
		return self.x!=other.x or self.y!=other.y
		
	def isAdjacent(self, coord):
		if fabs(coord.x - self.x) > 1:
			return False
		if fabs(coord.y - self.y) > 1:
			return False
		
		return True

class Board():
	def __init__(self,b=[]):
		self.board = b
		
	def _boggle_init(self):
		cube01 = ['A','S','P','F','K','F']
		cube02 = ['O','C','M','U','I','T']
		cube03 = ['T','W','A','O','T','O']
		cube04 = ['L','Y','E','D','V','R']
		cube05 = ['R','L','I','E','X','D']
		cube06 = ['Y','T','L','E','R','T']
		cube07 = ['O','O','J','B','A','B']
		cube08 = ['H','W','V','E','T','R']
		cube09 = ['N','E','I','U','S','E']
		cube10 = ['G','E','E','N','A','A']
		cube11 = ['T','S','T','I','D','Y']
		cube12 = ['T','O','E','S','S','I']
		cube13 = ['O','A','C','S','P','H']
		cube14 = ['G','E','W','N','H','E']
		cube15 = ['N','L','N','H','Z','R']
		cube16 = ['U','N','H','I','QU','M']

		self.cube_pool = [cube01,cube02,cube03,cube04,
							cube05,cube06,cube07,cube08,
							cube09,cube10,cube11,cube12,
							cube13,cube14,cube15,cube16]
		
	def generateBoard(self,method="boggle"):
		self.board=[]
		if method != "random": #If it equals boggle or any random input, do the boggle method
			self._boggle_init()
			for x in range(4):
				row = []
				for y in range(4):
					cube = random.choice(self.cube_pool)
					letter = random.choice(cube)
					row.append(letter)
					self.cube_pool.pop(self.cube_pool.index(cube))
				self.board.append(row)
		elif method=="random":
			for x in range(4):
				row = []
				for y in range(4):
					letter = random.choice(ascii_uppercase)
					row.append(letter)
				self.board.append(row)

	def printBoard(self):
		for x in range(len(self.board)):
			s = ''
			for y in range(len(self.board[0])):
				s += ' ' + self.board[x][y] + ' '
			print(s)
			
	def getCoordinates(self,letter):
		l = letter.upper()
		coords = []
		for x in [x for x,row in enumerate(self.board) if l in row]:
			for y in [y for y,col in enumerate(self.board[x]) if l in col]:
				coords.append(Coordinate(x,y))
		return coords
		
	def containsWord(self,word,print_history=False):
		w = word.upper()
		history = []
		for c in self.getCoordinates(w[0]):
			history.append([c])
		for letter in [l for j,l in enumerate(w) if j > 0]:
			del_history = []
			add_history = []
			coords = self.getCoordinates(letter)
			if len(history) == 0:
				return False
			for i,line in enumerate(history):
				lines_to_follow = [x for x in coords if x.isAdjacent(line[-1]) and x not in line]
				if lines_to_follow > 0:
					for match in lines_to_follow:
						tmp_line = deepcopy(line)
						tmp_line.append(match)
						add_history.append(tmp_line)
					del_history.append(line)
			for line in del_history:
				history.pop(history.index(line))
			for line in add_history:
				history.append(line)
				
		if len(history) > 0:
			if print_history:
				for line in history:
				      print(line)  
			return True
			
class Options():
	def __init__(self):
		self.found_words = []
	
		parse = argparse.ArgumentParser(description='A Boggle board generator.')
		parse.add_argument('--method', default='boggle', metavar='m',
			help='how Boggle board is generated. "boggle" creates a realistic board. "random" creates a random set of letters.')
		parse.add_argument('--mode', default='', metavar='M',
			help='"play" displays board and you find words. "file" searches how many boards need to generate to contain a word in text file')
			
		args = parse.parse_args()
		self.method = args.method
		self.mode = args.mode
		
	def askUser(self):
		if self.mode == '':
			print("Which mode would you like?")
			print("  A) Play Boggle")
			print("  B) Find words")
			choice = raw_input(": ")
			self.mode = choice.strip().upper()
			
	def genFile(self):
		first_time = datetime.datetime.now()
		words = [line.strip() for line in open('words.txt')]
		b = Board()
		index = 0
		while len(self.found_words) == 0:
				index += 1
				b.generateBoard(self.method)
				for w in words:
						if b.containsWord(w):
								self.found_words.append(w)

		second_time = datetime.datetime.now()
		b.printBoard()
		print "You found " + str(len(self.found_words)) + " words in " + str(index) + " boards in " + str(second_time-first_time)

		for w in self.found_words:
				print(w)
				b.containsWord(w,True)
				
	def genPlay(self):
		b = Board()
		b.generateBoard(self.method)
		b.printBoard()
		
		while True:
			n = raw_input("\n\nWord: ")
			if n == "exit":
				break
			elif b.containsWord(n):
				print "Correct"
				self.found_words.append(n)
				b.printBoard()
			else:
				print "Incorrect"
				b.printBoard()
				
		for w in found_words:
			print(w)
			b.containsWord(w,True)
			
	def boggle(self):
		if self.mode == "B": # Find words in text file
			self.genFile()
		else: # Play boggle and find words (defaults to this option
			self.genPlay()

# USER INPUT
options = Options() # parse arguments
options.askUser()	# prompt for mode if not included in arguments
options.boggle()	# print the board based on mode
