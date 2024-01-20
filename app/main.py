#!/usr/bin/env python

# sys imports

import sys
import argparse

# user imports
from lib import *

def cmdline_args():
    # Make parser object

    default = []

    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter, prog="studip-cli")

    p.add_argument("--session", action="store_true",
                   help="creates a user session for great performance improvements")

    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-courses", action="store_true",
                       help="list your courses")
    group.add_argument("--view-course", type=str,
                       help="retrieves course info (list)",
                       nargs="*",
                       default=default)
    group.add_argument("--list-files", type=str,
                       help="lists files in a list of folders (list)",
                       nargs="*",
                       default=default)
    group.add_argument("--download", type=str,
                       help="downloads files (list)",
                       nargs="*",
                       default=default)
    return(p.parse_args())

def main():
    """ Main program """
    args = cmdline_args()

    # Check if any specified argument is not used
    if not any(vars(args).values()):
        data = sys.stdin.read().replace("\n", " ").rstrip().split(" ")
        print("stdin", data)
    else:
        # Process the arguments after any specified option
        for arg_name, arg_value in vars(args).items():
            if arg_value:
                print(f"{arg_name} args:", arg_value)

if __name__ == "__main__":
    main()
