Made by: Kingbob

Easy to use coloring tool for text.

All the colors:
Coloring is a simple Python class that provides ANSI color codes and text effects for terminal output. It allows you to easily apply colors and text effects to your terminal-based Python programs.

Features
Standard Colors: Apply common colors like black, red, green, blue, and more.

Bright Colors: Apply bright variations of standard colors.

Extended Colors: Access a range of extended colors for more options.

Text Effects: Apply bold, faint, italic, underline, blink, and other text effects.

Background Colors: Set background colors alongside text color.

Easy Reset: Use the RESET code to remove any applied colors or effects.

Installation
You don’t need to install anything from an external source. This class can be directly included into your Python script or packaged into a module.

To use in your project:
Copy the Coloring class to your Python script.

Call the Coloring.palette("color") method to apply colors and text effects.

Alternatively, if you want to package it as a library (as described in the previous response), you can follow the folder structure and package instructions.

Usage
The Coloring class has a single method palette() that accepts a color or effect name as a string argument and returns the corresponding ANSI escape code.

from coloring import Coloring

# Example usage for colored text
print(Coloring.palette("RED") + "This is a red text!" + Coloring.palette("RESET"))
print(Coloring.palette("GREEN") + "This is a green text!" + Coloring.palette("RESET"))

# Example usage for background colors
print(Coloring.palette("BLUE_BG") + "This text has a blue background!" + Coloring.palette("RESET"))

# Example usage for text effects
print(Coloring.palette("BOLD") + "This text is bold!" + Coloring.palette("RESET"))
print(Coloring.palette("UNDERLINE") + "This text is underlined!" + Coloring.palette("RESET"))


Available Colors:
Standard Colors:
BLACK, RED, GREEN, BROWN, BLUE, PURPLE, CYAN, LIGHT_GRAY

Bright Colors:
DARK_GRAY, LIGHT_RED, LIGHT_GREEN, YELLOW, LIGHT_BLUE, LIGHT_PURPLE, LIGHT_CYAN, WHITE

Exclusive/Extended Colors:
ORANGE, GOLD, TEAL, PINK, VIOLET, INDIGO, MAROON, OLIVE

Text Effects:
BOLD, FAINT, ITALIC, UNDERLINE, BLINK, NEGATIVE, CROSSED

Background Colors:
BLACK_BG, RED_BG, GREEN_BG, YELLOW_BG, BLUE_BG, MAGENTA_BG, CYAN_BG, WHITE_BG

Bright Background Colors:
BRIGHT_BLACK_BG, BRIGHT_RED_BG, BRIGHT_GREEN_BG, BRIGHT_YELLOW_BG, BRIGHT_BLUE_BG, BRIGHT_MAGENTA_BG, BRIGHT_CYAN_BG, BRIGHT_WHITE_BG

Reset:
RESET: To reset color back to the default terminal color.   