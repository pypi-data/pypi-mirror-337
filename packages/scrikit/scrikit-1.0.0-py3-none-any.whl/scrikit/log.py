# Custom logging handler for colorized output

import logging
import time
from . import theme

# Custom formatter for log messages with colorized output
class Formatter(logging.Formatter):
	COLORS = {
		logging.DEBUG: theme.log_debug,
		logging.INFO: theme.log_info,
		logging.WARNING: theme.log_warning,
		logging.ERROR: theme.log_error,
		logging.CRITICAL: theme.log_critical,
	}

	def formatTime(self, record, datefmt=None):
		ct = self.converter(record.created)
		if datefmt:
			t = time.strftime(datefmt, ct)
		else:
			t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
		s = f"{t}.{int(record.msecs):03d}"
		return s

	def format(self, record: logging.LogRecord) -> str:
		color = self.COLORS.get(record.levelno, theme.reset)
		new_fmt = (
			f"[{theme.log_timestamp}%(asctime)s{theme.reset}] "
			f"[{color}%(levelname)s{theme.reset}] "
			f"%(message)s{theme.reset}"
		)
		self._style._fmt = new_fmt  # update the internal format
		return super().format(record)

# Apply the custom formatter to the root logger
handler = logging.StreamHandler()     # create a new handler
handler.setFormatter(Formatter())     # Add our custom formatter to the handler
logging.root.handlers = []            # remove any existing handlers from root logger
logging.root.addHandler(handler)      # add our custom handler
logging.root.setLevel(logging.DEBUG)  # Default to DEBUG level