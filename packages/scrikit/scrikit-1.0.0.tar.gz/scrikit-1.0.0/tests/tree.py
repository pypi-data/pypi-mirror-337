#!/usr/bin/env python3

# Imports
import scrikit

def main():
	tree = scrikit.Tree()
	tree.print_title("Example Tree")
	tree.print_header(1, "Section (Left-aligned)", "Right-aligned text")
	tree.print_row("Row 1", "Metadata")
	tree.print_row("Row 2", "Metadata")
	tree.print_row("Row 3", "Metadata")
	tree.print_header(2, "Subsection (Left-aligned)", "Right-aligned text")
	tree.print_row("Row 1", "Metadata")
	tree.print_row("Row 2", "Metadata")
	tree.print_header(1, "Section (Left-aligned)", "Right-aligned text")
	tree.print_row("Row 1", "Metadata")
	tree.print_row("Row 2", "Metadata")
	tree.print_row("Row 3", "Metadata")
	tree.print_row("Row 4", "Metadata")
	tree.print_row("Row 5", "Metadata")
	tree.print_header(1, "Section (Left-aligned)", "Right-aligned text")
	tree.print_row("Row 1", "Metadata")
	tree.print_row("Row 2", "Metadata")
	

if __name__ == "__main__":
	main()
