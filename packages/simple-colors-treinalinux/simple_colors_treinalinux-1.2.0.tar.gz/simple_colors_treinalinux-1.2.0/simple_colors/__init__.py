#!/usr/bin/env python3
#
# name.........: simple_colors
# description..: Simple colors to terminal
# author.......: Alan da Silva Alves
# version......: 1.0.0
# date.........: 4/8/2024
# github.......: github.com/treinalinux/my-tools/blob/main/Linux/simple_colors
#
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


def c_success(text):
    """
	The function that displays green on the terminal screen to indicate
	that an action was successfully executed.
    """
    print(f"\033[32m{text}\033[m")


def c_failure(text):
    """
	The function that displays green on the terminal screen to indicate
	that an action was failure executed.
    """
    print(f"\033[1;31m{text}\033[m")


def c_warning(text):
    """
	The function that displays green on the terminal screen to indicate
	that an action was warning  executed.
    """
    print(f"\033[33m{text}\033[m")


def c_info(text):
    """
	The function that displays green on the terminal screen to indicate
	that an action was infomation executed.
    """
    print(f"\033[35m{text}\033[m")

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    c_warning("Import the module 'simple_colors' to use the feature.")
