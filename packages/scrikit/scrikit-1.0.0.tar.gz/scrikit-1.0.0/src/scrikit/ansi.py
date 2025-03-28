# ANSI Escape Sequences

# https://notes.burke.libbey.me/ansi-escape-codes/
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# https://en.wikipedia.org/wiki/ANSI_escape_code#C0_control_codes

# For the most part, ANSI escape sequences are composed of three parts:
# 1. The escape code, which consists of the escape character and an opening square bracket
# 2. Numbers separated by ';'
# 3. The closing character, which corresponds to a function

# Escape codes for byte 27 (ASCII 'ESC')
escape_decimal = chr(27)
escape_hex = "\x1b"
escape_octal = "\033"
escape_unicode = "\u001b"

# We will default to the hexadecimal escape code
escape = escape_hex

# Sequence prefixes
csi = escape + "[" # Control Sequence Introducer
dcs = escape + "P" # Device Control String
osc = escape + "]" # Operating System Command

# This is the 'm' control function, which has a complex signature and is used to modify text attributes
# For comprehension, we will be defining it here for use below
def SetGraphicsRendition(*args):
	return csi + ";".join(map(str, args)) + "m" 

# Abbreviate to SGR
SGR = SetGraphicsRendition

# Reset all attributes 
reset = SGR(0)                       # Reset all text attributes

# 1-9: Text Effects (Enable)
bold = SGR(1)                        # Bold on
dim = SGR(2)                         # Dim (faint) on
italic = SGR(3)                      # Italic on
underline = SGR(4)                   # Underline on
blink = SGR(5)                       # Slow blink on
blink_fast = SGR(6)                  # Rapid blink on
reverse_video = SGR(7)               # Reverse video on (invert colors)
invisible = SGR(8)                   # Conceal (invisible) on
strikethrough = SGR(9)               # Crossed-out (strikethrough) on

# 10-20: Font presets (rarely used, not supported)
font_primary = SGR(10)               # Select primary font
font_alternate_1 = SGR(11)           # Select first alternate font
font_alternate_2 = SGR(12)           # Select second alternate font
font_alternate_3 = SGR(13)           # Select third alternate font
font_alternate_4 = SGR(14)           # Select fourth alternate font
font_alternate_5 = SGR(15)           # Select fifth alternate font
font_alternate_6 = SGR(16)           # Select sixth alternate font
font_alternate_7 = SGR(17)           # Select seventh alternate font
font_alternate_8 = SGR(18)           # Select eighth alternate font
font_alternate_9 = SGR(19)           # Select ninth alternate font
fraktur = SGR(20)                    # Fraktur (Gothic) on

# 21-29: Text Effects (Disable)
bold_off = SGR(21)                   # Bold off (normal intensity)
italic_off = SGR(23)                 # Italic off
underline_off = SGR(24)              # Underline off
blink_off = SGR(25)                  # Blink off
reverse_video_off = SGR(27)          # Reverse video off
conceal_off = SGR(28)                # Invisible off
crossed_out_off = SGR(29)            # Crossed-out off

# 30-37: Set foreground color
foreground_black = SGR(30)           # Set foreground color to black
foreground_red = SGR(31)             # Set foreground color to red
foreground_green = SGR(32)           # Set foreground color to green
foreground_yellow = SGR(33)          # Set foreground color to yellow
foreground_blue = SGR(34)            # Set foreground color to blue
foreground_magenta = SGR(35)         # Set foreground color to magenta
foreground_cyan = SGR(36)            # Set foreground color to cyan
foreground_white = SGR(37)           # Set foreground color to white

# 38: Set foreground color to an xterm 256 value
set_fg_color = lambda n: SGR(38, 5, n)            # 5 = 256 color mode
set_fg_rgb = lambda r, g, b: SGR(38, 2, r, g, b)  # 2 = RGB color mode

# 39: Reset foreground color to default
reset_fg = SGR(39)

# 40-47: Set background color
background_black = SGR(40)           # Set background color to black
background_red = SGR(41)             # Set background color to red
background_green = SGR(42)           # Set background color to green
background_yellow = SGR(43)          # Set background color to yellow
background_blue = SGR(44)            # Set background color to blue
background_magenta = SGR(45)         # Set background color to magenta
background_cyan = SGR(46)            # Set background color to cyan
background_white = SGR(47)           # Set background color to white

# 48: Set background color to an RGB value
set_bg_color = lambda n: SGR(48, 5, n)            # 5 = 256 color mode
set_bg_rgb = lambda r, g, b: SGR(48, 2, r, g, b)  # 2 = RGB color mode

# 49: Reset background color to default
reset_bg = SGR(49)

# 50-89: Rarely used, not supported

# 90-97: Set bright foreground color
foreground_bright_black = SGR(90)    # Set foreground color to bright black
foreground_bright_red = SGR(91)      # Set foreground color to bright red
foreground_bright_green = SGR(92)    # Set foreground color to bright green
foreground_bright_yellow = SGR(93)   # Set foreground color to bright yellow
foreground_bright_blue = SGR(94)     # Set foreground color to bright blue
foreground_bright_magenta = SGR(95)  # Set foreground color to bright magenta
foreground_bright_cyan = SGR(96)     # Set foreground color to bright cyan
foreground_bright_white = SGR(97)    # Set foreground color to bright white

# 100-107: Set bright background color
background_bright_black = SGR(100)   # Set background color to bright black
background_bright_red = SGR(101)     # Set background color to bright red
background_bright_green = SGR(102)   # Set background color to bright green
background_bright_yellow = SGR(103)  # Set background color to bright yellow
background_bright_blue = SGR(104)    # Set background color to bright blue
background_bright_magenta = SGR(105) # Set background color to bright magenta
background_bright_cyan = SGR(106)    # Set background color to bright cyan
background_bright_white = SGR(107)   # Set background color to bright white

# Miscellaneous
bell = "\a"                          # Trigger the terminal bell
tab = "\t"                           # Horizontal tab
backspace = "\b"                     # Backspace

flash_screen = csi + "?5h" + csi + "?5l"  # Flash the screen

# Cursor Control - A,B,C,D,H
cursor_up = lambda n=1: csi + f"{n}A"               # Move cursor up by n lines
cursor_down = lambda n=1: csi + f"{n}B"             # Move cursor down by n lines
cursor_right = lambda n=1: csi + f"{n}C"            # Move cursor right by n columns
cursor_left = lambda n=1: csi + f"{n}D"             # Move cursor left by n columns
cursor_home = csi + "H"                             # Move cursor to the home position (0,0)
cursor_pos = lambda row, col: csi + f"{row};{col}H" # Move cursor to specific position

# Screen and Cursor Modes
save_cursor = csi + "s"              # Save the cursor position
restore_cursor = csi + "u"           # Restore the saved cursor position
hide_cursor = csi + "?25l"           # Hide the cursor
show_cursor = csi + "?25h"           # Show the cursor
alt_screen = csi + "?1049h"          # Switch to the alternate screen buffer
main_screen = csi + "?1049l"         # Switch back to the main screen buffer

# Erasing and Clearing
clear_screen = csi + "2J"            # Clear the entire screen
clear_line_right = csi + "K"         # Clear from the cursor to the end of the line
clear_line_left = csi + "1K"         # Clear from the cursor to the start of the line
clear_line_all = csi + "2K"          # Clear the entire line

# Text Manipulation
insert_line = csi + "L"              # Insert a blank line at the cursor position
delete_line = csi + "M"              # Delete the line at the cursor position

# Key Mappings (for reference)
key_f1 = csi + "OP"                  # F1 key
key_f2 = csi + "OQ"                  # F2 key
key_f3 = csi + "OR"                  # F3 key
key_f4 = csi + "OS"                  # F4 key
key_f5 = csi + "15~"                 # F5 key
key_f6 = csi + "17~"                 # F6 key
key_f7 = csi + "18~"                 # F7 key
key_f8 = csi + "19~"                 # F8 key
key_f9 = csi + "20~"                 # F9 key
key_f10 = csi + "21~"                # F10 key
key_f11 = csi + "23~"                # F11 key
key_f12 = csi + "24~"                # F12 key
key_insert = csi + "2~"              # Insert key
key_delete = csi + "3~"              # Delete key
key_home = csi + "OH"                # Home key
key_end = csi + "OF"                 # End key
key_page_up = csi + "5~"             # Page Up key
key_page_down = csi + "6~"           # Page Down key