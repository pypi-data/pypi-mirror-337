#!/usr/bin/env python3

# Imports
import scrikit

def main():
	table = scrikit.Table()
	table.set_title("Example Table")
	table.set_header(["Column 1", "Column 2", "Column 3"])
	table.add_row(["Row 1", "Row 1", "Row 1"])
	table.add_row(["Row 2", "Row 2", "Row 2"])
	table.add_row(["Row 3", "Row 3", "Row 3"])
	table.print()

if __name__ == "__main__":
	main()
