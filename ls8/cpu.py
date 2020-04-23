"""CPU functionality."""

import sys

class CPU:
	"""Main CPU class."""

	def __init__(self):
		"""Construct a new CPU."""
		# operational space
		self.ram = [0] * 256
		self.register = [0] * 8

		# constants
		#			 |12345678| 
		self.LDI =	0b10000010
		self.PRN =	0b01000111
		self.HLT =	0b00000001
		self.MUL =	0b10100010
		self.PUSH =	0b01000101
		self.POP =	0b01000110

		# accounting
		self.pc = 0
		self.sp = len(self.register) -1		# register used for the stack pointer
		self.register[self.sp] = 0xF4		# INIT default stack position to the register
		self.running = True
		self.branchtable = {
			self.HLT: self.halt,
			self.LDI: self.loadimm,
			self.MUL: self.multiply,
			self.PRN: self.output,
			self.PUSH: self.push,
			self.POP: self.pop
		}

	# branchtable defs
	def halt(self):
		self.running = False
	
	def loadimm(self):
		self.register[self.ram[self.pc+1]] = self.ram[self.pc+2]

	def multiply(self):
		self.alu("MULT", self.ram[self.pc+1], self.ram[self.pc+2])

	def output(self):
		print(self.register[self.ram[self.pc+1]])

	def push(self):
		self.register[self.sp] -= 1			# DECK crement to get room for a deeper stack
		regpos = self.ram[self.pc+1]		# get the register to use from the next slot of ram
		val = self.register[regpos]			# get the value from the register
		stackpos = self.register[self.sp]	# where we at in the stack?
		self.ram[stackpos] = val			# put the value on the stack
		self.trace("Push")

	def pop(self):
		stackpos = self.register[self.sp]	# get the current stackpointer 
		val = self.ram[stackpos]			# get the value from ram using stackpointer
		regpos = self.ram[self.pc+1]		# get the register to use from the next slot of ram

		self.register[regpos] = val			# put the value into the register
		self.trace("Pop ")
		self.register[self.sp] += 1			# INN crement for a one shallower stack


	# helper methods
	def load(self, filename):
		"""Load a program into memory."""

		address = 0

		with open(filename) as file:
			for line in file: 
				# break each line on OCTOTHORPE
				line = line.split("#") 
				# clear out leading spaces
				line = line[0].strip()
				# ignore blank lines
				if line == '': continue

					# getting down to business
					# in the
					# 	memory array of
					# 	the same index as
					# 	this line of this file
					# put the 
					# 	value from 
					# 	this line of this file

				self.ram[address] = int(line, 2)

				address += 1
				
		# print (48, self.ram[:8])

	def alu(self, op, reg_a, reg_b):
		"""ALU operations."""

		if op == "ADD":
			self.reg[reg_a] += self.reg[reg_b]
		elif op == "MULT":
			self.register[reg_a] *= self.register[reg_b]
		else:
			raise Exception("Unsupported ALU operation")

	def trace(self, LABEL=str()):
		"""
		Handy function to print out the CPU state. You might want to call this
		from run() if you need help debugging.
		"""

		print(f"{LABEL} TRACE --> PC: %02i | RAM: %03i %03i %03i | Register: " % (
			self.pc,
			#self.fl,
			#self.ie,
			self.ram_read(self.pc),
			self.ram_read(self.pc + 1),
			self.ram_read(self.pc + 2)
		), end='')

		for i in range(8):
			print(" %03i" % self.register[i], end='')

		print(f" | Stack: [{self.register[self.sp]}] ", end='')

		stackpos = 0xF4 - 1
		while self.ram[stackpos] != 0:
			print(" %02i" % self.ram[stackpos], end='')
			stackpos -= 1

		print()

	# RRUUUNNN!!!
	def run(self):
		while self.running:
			IR = self.ram[self.pc]	
			instruction = IR
			
			if self.branchtable.get(IR):
				self.branchtable[IR]()
			else:
				print("unknown instruction")
				self.trace("End")
				self.running = False

			inst_len = ((IR & 0b11000000) >> 6) + 1
			self.pc += inst_len


	def ram_read(self, addr):
		return self.ram[addr]

	def ram_write(self, addr, data):
		self.ram[addr] = data
