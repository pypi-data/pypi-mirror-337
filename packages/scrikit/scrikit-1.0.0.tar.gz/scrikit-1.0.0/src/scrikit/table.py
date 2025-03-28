import os
import sys
import csv
import re
import logging
import datetime

from scrikit import theme
from scrikit import ansi

class Table:

	# Initialize with required attributes
	def __init__(self):
		# Table data
		self.title = None
		self.header = [] # List of strings, just one header row
		self.rows = [] # List of lists of strings

		# Configurations
		self.max_width = os.get_terminal_size().columns
		self.padding_width = 2
		self.max_rows = None

		# Metadata
		self.column_widths = {} # Dict of ints, specifying char width for each column corresponding to index. Determined by largest string per column
		self.width = 0
		self.height = 0

	def clear(self):
		self.rows.clear()
		self.column_widths = {}
		self.width = 0
		self.height = 0

	def set_title(self, title):
		self.title = title

	def set_header(self, header):
		self.header = header

	def add_row(self, row):
		self.rows.append(row)

	def print(self):
		# Update column widths
		self.calculate_widths()

		# Print title
		if self.title:
			sys.stdout.write("\n")
			sys.stdout.write(f"{theme.table_title}{ansi.underline}{self.title}{theme.reset}\n")
			sys.stdout.write("\n")

		# Print header
		header_string = ''
		for index, string in enumerate(self.header):
			if string:
				header_string += theme.table_header + self.pad(index, str(string)) + theme.reset
		sys.stdout.write(header_string + '\n')

		# Print the rows
		for row in self.rows:
			if self.max_rows:
				if self.rows.index(row) >= self.max_rows:
					break

			row_string = ''
			for index, s in enumerate(row):

				# Build first column
				if index == 0: 
					row_string += theme.table_row_index + self.pad(index, str(s)) + theme.reset

				# Build last column
				elif index == len(row) - 1: 

					# Check if last column needs to be truncated
					if self.width > self.max_width:

						# Get the lenth for all columns except last one
						last_column_index = max(self.column_widths.keys())

						# Sum all values except the one corresponding to the highest index key
						row_length_except_last_column = sum(value for key, value in self.column_widths.items() if key != last_column_index)

						# Add 2 for each column — except the last one — to account for padding 
						row_length_except_last_column += (2 * (len(self.header) - 1))

						# Truncate last column to fit max width
						l = self.max_width - row_length_except_last_column
						row_string += self.truncate(str(s), l)

					# No truncation needed
					else:
						row_string += str(s)

				# Build every other column
				else: 
					row_string += self.pad(index, str(s))

			# Actually print the complete row
			sys.stdout.write(row_string+"\n")

	# My version
	def truncate(self, string, length, trailing_char = '.'):
		if self.get_real_width(string) > length:
			# God, this took a while to figure out
			invisible_length = len(string) - self.get_real_width(string) # Account for length given by invisible chars, such as color codes
			new_size = length - 3 + invisible_length
			string = string[:new_size].rstrip() + theme.text_file + (trailing_char * 3) + theme.reset

		return string

	def save(self, destination_folder=""):
		logging.info('Saving table data to CSV')

		# Sanitize title for file name
		# Remove any character that is not a letter, a number, a space, or an underscore
		sanitized = re.sub(r'[^\w\s]', '', self.title.lower())
		# Replace sequences of spaces with a single space
		sanitized = re.sub(r'\s+', ' ', sanitized)
		# Trim leading and trailing spaces
		sanitized = sanitized.strip()

		timestamp =	datetime.datetime.now().isoformat()
		file_title = "table_" + sanitized + "_" + str(timestamp) + ".csv"

		# Create a new csv file in the current directory
		if not destination_folder:
			destination_folder = os.getcwd()
		
		filepath = os.path.expanduser(os.path.join(destination_folder, file_title.replace(' ', '_')))

		# Write table data to new CSV file
		with open(filepath, 'w+') as f:
			writer = csv.writer(f, escapechar='\\')
			writer.writerow(self.header)
			for row in self.rows:
				writer.writerow(row)

		logging.info("Table data saved to " + theme.text_file + filepath)

	def get_real_width(self, s):
		# Use regex to remove color codes
		# https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
		regex = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
		s = regex.sub('', str(s))

		length = len(str(s))
		return length

	# Get width of table
	def calculate_widths(self):
		# First calculate column widths, starting with header row widths
		for index, s in enumerate(self.header):
			self.column_widths[index] = self.get_real_width(s)

		# Now compare the widths to all rows
		for row in self.rows:
			if self.max_rows:
				if self.rows.index(row) >= self.max_rows:
					break

			for index, s in enumerate(row):

				# Update the column width if necessarys
				if self.get_real_width(s) > self.column_widths[index]:
					self.column_widths[index] = self.get_real_width(s)

		# Update width value
		width = 0
		for key in self.column_widths:
			width += self.column_widths[key]
			width += self.padding_width

		width -= self.padding_width
		self.width = width
		return self.width

	# Get height of table, including title and blank spaces
	def get_height(self):
		# Title
		if self.title:
			self.height += 3 # Blank lines above and below

		# Header
		if self.header:
			self.height += 1

		# Rows
		row_length = len(self.rows)
		if row_length <= self.max_rows:
			self.height += row_length
		else:
			self.height += self.max_rows

		return self.height

	def pad(self, index, s):
		length = 0
		try:
			length = self.column_widths[index] - self.get_real_width(s) + self.padding_width
		except:
			logging.error("Error encountered while calculating padding for columns")
		s = s + (' ' * length)
		return str(s)