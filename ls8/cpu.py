"""CPU functionality."""

import sys

class CPU:
	"""Main CPU class."""

	def __init__(self):
		"""Construct a new CPU."""
		self.ram = [0] * 256
		self.register = [0] * 8
		self.pc = 0

		#			 |12345678| 
		self.LDI =	0b10000010
		self.PRN =	0b01000111
		self.HLT =	0b00000001
		self.MUL =	0b10100010


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
				
		print (48, self.ram[:8])

	def alu(self, op, reg_a, reg_b):
		"""ALU operations."""

		if op == "ADD":
			self.reg[reg_a] += self.reg[reg_b]
		#elif op == "SUB": etc
		else:
			raise Exception("Unsupported ALU operation")

	def trace(self):
		"""
		Handy function to print out the CPU state. You might want to call this
		from run() if you need help debugging.
		"""

		print(f"TRACE: %02X | %02X %02X %02X |" % (
			self.pc,
			#self.fl,
			#self.ie,
			self.ram_read(self.pc),
			self.ram_read(self.pc + 1),
			self.ram_read(self.pc + 2)
		), end='')

		for i in range(8):
			print(" %02X" % self.reg[i], end='')

		print()

	def run(self):
		"""Run the CPU."""

		running = True

		IR = self.pc
		while running:

			instruction = self.ram[IR]
			print(88, int(instruction))
			
			if instruction == self.LDI:
				self.register[self.ram[IR+1]] = self.ram[IR+2]
				# ram_write(self.register[self.ram[IR+1]],   )
				IR += 3

			elif instruction == self.PRN:
				print(self.register[self.ram[IR+1]])
				IR += 2
			
			elif instruction == self.HLT:
				running = False

			else:
				print("UNK")
				running = False



	def ram_read(self, addr):
		return self.memory[addr]

	def ram_write(self, addr, data):
		self.memory[addr] = data
