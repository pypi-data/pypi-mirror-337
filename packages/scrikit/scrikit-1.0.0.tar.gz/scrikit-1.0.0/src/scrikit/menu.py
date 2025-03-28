import sys
import logging
import datetime

from scrikit import theme

def listen(prompt):
	timestamp = datetime.datetime.now().strftime("%H:%M:%S")
	answer = input(
		f"[{theme.log_timestamp}{timestamp}{theme.reset}] "
		f"[{theme.log_input}INPUT{theme.reset}] "
		f"{str(prompt).strip()} "
		f"{theme.reset}"
	)
	return answer.strip()

def menu(options):
	while True:
		# Display the prompt and available options
		logging.info("Available options:\n")
		for index, option in enumerate(options):
			index_str = f"{index + 1}".rjust(3)  # Right-justify the index
			sys.stdout.write(f"    {index_str}{theme.reset}: {option}\n")
		sys.stdout.write('\n')

		# Get input from the user
		selection = listen("Enter a corresponding number:")

		# Validate and process the input
		if selection.isdigit():
			selection = int(selection)
			if 1 <= selection <= len(options):
				return options[selection - 1]
			else:
				logging.error("Input out of range... try again\n")
		else:
			logging.error("That doesn't look like an integer... try again\n")