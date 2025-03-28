from scrikit import ansi

# Reset all color and style
reset = ansi.reset

# Generic text & variables
text_generic = ansi.set_fg_color(250)
text_command = ansi.set_fg_color(219)
text_file = ansi.set_fg_color(208)
text_description = ansi.set_fg_color(33)
text_person = ansi.set_fg_color(197)
text_place = ansi.set_fg_color(208)
text_link = f"{ansi.set_fg_color(33)}{ansi.underline}"

# Banner
banner_logo = ansi.set_fg_color(226)
banner_title = ansi.set_fg_color(124)
banner_tagline = ansi.set_fg_color(201)
banner_author = ansi.set_fg_color(39)
banner_version = ansi.set_fg_color(226)
banner_love = ansi.set_fg_color(196)

# Log messages
log_timestamp = ansi.set_fg_color(117)
log_debug = ansi.set_fg_color(245)
log_info = ansi.set_fg_color(28)
log_warning = ansi.set_fg_color(226)
log_error = ansi.set_fg_color(196)
log_critical = ansi.set_fg_color(201)
log_tip = ansi.set_fg_color(201)
log_input = ansi.set_fg_color(33)

# Tables
table_title = ansi.set_fg_color(255)
table_header = ansi.set_fg_color(250)
table_row_index = ansi.set_fg_color(202)
table_row_right = ansi.set_fg_color(183)

# Trees
tree_title = ansi.set_fg_color(250)
tree_header_left = ansi.set_fg_color(39)
tree_header_right = ansi.set_fg_color(250)
tree_detail_left = ansi.set_fg_color(101)
tree_detail_right = ansi.set_fg_color(183)

# Ratings
rating_critical = ansi.set_fg_color(196)
rating_high = ansi.set_fg_color(208)
rating_medium = ansi.set_fg_color(226)
rating_low = ansi.set_fg_color(33)
rating_informational = ansi.set_fg_color(34)

# Status
status_success = ansi.set_fg_color(43)
status_success_description = ansi.set_fg_color(105)
status_fail = ansi.set_fg_color(124)
status_fail_description = ansi.set_fg_color(208)
