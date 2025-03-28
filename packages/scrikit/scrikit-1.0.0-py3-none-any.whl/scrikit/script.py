import os
import sys
import datetime
import logging
import traceback
import argparse

from scrikit import theme

class Script:

	def __init__(self):
		# Get the main module (the entry-point script)
		main_module = sys.modules["__main__"]

		# Set the name from the main script's file
		caller_file = main_module.__file__
		self.name = os.path.basename(caller_file)

		# Argparse setup
		self.parser = argparse.ArgumentParser()
		self.arguments = {}

	def print_banner(self, logo_path=None, title_path=None, tagline=None):
			# Start with a newline
			sys.stdout.write('\n')

			# Show logo, if applicable
			if logo_path:
				try:
					with open(logo_path, 'r') as f:
						logo_text = f.read()
						print(f"{theme.banner_logo}{logo_text}{theme.reset}")
						sys.stdout.write('\n')
				except FileNotFoundError:
					logging.error(f"Could not find banner logo at {theme.text_file}{logo_path}{theme.reset}")

			# Show title, if applicable
			if title_path:
				try:
					with open(title_path, 'r') as f:
						title_text = f.read()
						print(f"{theme.banner_title}{title_text}{theme.reset}")
						sys.stdout.write('\n')
				except FileNotFoundError:
					logging.error(f"Could not find banner title at {theme.text_file}{title_path}{theme.reset}")

			# Show tagline, if applicable
			if tagline:
				print(f"\t{theme.banner_tagline}{tagline}{theme.reset}")
				sys.stdout.write('\n')

	def print_metadata(self, title=None, author=None, description=None, url=None, version=None, license=None):
		print(f"{title} ({theme.banner_version}v{version}{theme.reset}) - {description}")
		print(f"Made with {theme.banner_love}<3{theme.reset} by {theme.banner_author}{author}{theme.reset}")
		print(f"An open-source tool licensed under {license}")
		print(f"See more details at {theme.text_link}{url}{theme.reset}")
		print(f"Built with scrikit (the Script Kit) - {theme.text_link}https://github.com/coryavra/scrikit{theme.reset}")

	# Decorator function
	def run(self, decorated_main_script_function):
		def wrapper_function():

			# Start with a newline
			sys.stdout.write('\n')

			# Only parse args if they exist. Otherwise, parser fails when scripts are called programmatically
			self.arguments = vars(self.parser.parse_args())

			# Show start time
			script_start_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
			script_start_time_formatted = script_start_time.strftime("%I:%M:%S %p %Z")
			logging.info(f"Starting script at: {theme.log_timestamp}{script_start_time_formatted}")

			# Show Python version and executable
			logging.info(f"Using Python version {theme.text_file}{sys.version.split(' ')[0]}{theme.reset} executing under {theme.text_file}{sys.executable}{theme.reset}")

			try:
				# Run main script function
				decorated_main_script_function()

			# Handle keyboard interrupts (CTRL + C)
			except KeyboardInterrupt:
				sys.stdout.write('\n')
				logging.info("Interrupt - CTRL-C detected")
				logging.warning("Exiting gracefully")
				sys.exit()

			# Handle generic errors
			except Exception as e:
				logging.error("Encounted an error while executing the script")
				logging.error("Traceback:")
				sys.stdout.write('\n')
				sys.stdout.write(traceback.format_exc())
				sys.exit()

			# Show end time with elapsed seconds
			sys.stdout.write('\n')
			script_end_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
			script_end_time_formatted = script_end_time.strftime("%I:%M:%S %p %Z")
			elapsed_time = str(script_end_time - script_start_time).split('.')[0]
			
			logging.info(f"Script completed at: {theme.log_timestamp}{script_end_time_formatted}{theme.reset} ({theme.text_file}{elapsed_time}{theme.reset} elapsed)")

			# Show tips
			if "save" in self.arguments:
				logging.tip(f"You can save this script's results with {theme.text_file}--save")

		return wrapper_function