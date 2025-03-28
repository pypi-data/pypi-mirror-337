import os
import sys
import re

from scrikit import ansi
from scrikit import theme

class Tree:

	# Initialize with required attributes
	def __init__(self):
		self.title = ""
		self.width = os.get_terminal_size().columns
		self.current_level = 1
		self.previous_level = 1

	def print_title(self, title):
		self.title = title
		sys.stdout.write("\n")
		sys.stdout.write(f"{theme.table_title}{ansi.underline}{self.title}{theme.reset}\n")

	def print_header(self, level, header_left, header_right = ''):
		# Update table level
		self.current_level = level

		if self.current_level != self.previous_level:
			self.previous_level = level

		# Blank Line
		sys.stdout.write('|' + ('   |' * (level - 1)) + "\n")

		# Header
		line_left = '|' + ('   |' * (level - 1)) + '--' + ' ' + theme.tree_header_left + header_left + theme.reset
		line = self.build_line(line_left, theme.tree_header_right + header_right, ' ')
		sys.stdout.write(line + '\n')

	def print_row(self, row_left, row_right = ''):
		line_left = '|' + ('   |' * self.current_level) + '-- ' + row_left
		line = self.build_line(line_left, row_right)
		sys.stdout.write(line + '\n')

	# Helper functions
	def build_line(self, line_left, line_right, spacer = '.'):
		# First make sure the line won't be longer than the width
		line_left = self.truncate(line_left, self.width - self.get_real_width(line_right) - 3, '-') # Give a 3 char buffer between left and right sides

		line = ""
		spacing = spacer * (self.width - (self.get_real_width(line_left) + (self.get_real_width(line_right))))
		if line_right:
			line += line_left + spacing + theme.table_row_right + line_right + theme.reset
		else:
			line = line_left
		return line

	def get_real_width(self, s):
		# Use regex to remove color codes
		regex = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
		s = regex.sub('', str(s))

		length = len(str(s))
		return length

	def truncate(self, string, length, trailing_char = '.'):
		if self.get_real_width(string) > length:
			invisible_length = len(string) - self.get_real_width(string)
			new_size = length - 3 + invisible_length
			string = string[:new_size].rstrip() + theme.text_file + (trailing_char * 3) + theme.reset

		return string
