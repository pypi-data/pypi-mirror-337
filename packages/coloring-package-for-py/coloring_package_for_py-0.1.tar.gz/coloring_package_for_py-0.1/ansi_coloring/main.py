class Coloring:
    """ ANSI Color Codes for Text Effects and Colors """
    @staticmethod
    def palette(color):
        colors = {
            # Standard Colors
            "BLACK": "\033[0;30m",
            "RED": "\033[0;31m",
            "GREEN": "\033[0;32m",
            "BROWN": "\033[0;33m",
            "BLUE": "\033[0;34m",
            "PURPLE": "\033[0;35m",
            "CYAN": "\033[0;36m",
            "LIGHT_GRAY": "\033[0;37m",

            # Bright Colors
            "DARK_GRAY": "\033[1;30m",
            "LIGHT_RED": "\033[1;31m",
            "LIGHT_GREEN": "\033[1;32m",
            "YELLOW": "\033[1;33m",
            "LIGHT_BLUE": "\033[1;34m",
            "LIGHT_PURPLE": "\033[1;35m",
            "LIGHT_CYAN": "\033[1;36m",
            "WHITE": "\033[1;37m",

            # Exclusive, Extended Colors
            "ORANGE": "\033[38;5;214m",
            "GOLD": "\033[38;5;220m",
            "TEAL": "\033[38;5;30m",
            "PINK": "\033[38;5;205m",
            "VIOLET": "\033[38;5;129m",
            "INDIGO": "\033[38;5;54m",
            "MAROON": "\033[38;5;88m",
            "OLIVE": "\033[38;5;100m",

            # Text Effects
            "BOLD": "\033[1m",
            "FAINT": "\033[2m",
            "ITALIC": "\033[3m",
            "UNDERLINE": "\033[4m",
            "BLINK": "\033[5m",
            "NEGATIVE": "\033[7m",
            "CROSSED": "\033[9m",

            # Reset Color
            "RESET": "\033[0m",

            # Background Colors
            "BLACK_BG": "\033[40m",
            "RED_BG": "\033[41m",
            "GREEN_BG": "\033[42m",
            "YELLOW_BG": "\033[43m",
            "BLUE_BG": "\033[44m",
            "MAGENTA_BG": "\033[45m",
            "CYAN_BG": "\033[46m",
            "WHITE_BG": "\033[47m",

            # Bright Background Colors
            "BRIGHT_BLACK_BG": "\033[100m",
            "BRIGHT_RED_BG": "\033[101m",
            "BRIGHT_GREEN_BG": "\033[102m",
            "BRIGHT_YELLOW_BG": "\033[103m",
            "BRIGHT_BLUE_BG": "\033[104m",
            "BRIGHT_MAGENTA_BG": "\033[105m",
            "BRIGHT_CYAN_BG": "\033[106m",
            "BRIGHT_WHITE_BG": "\033[107m",
        }
        
        return colors.get(color.upper(), colors["RESET"])
