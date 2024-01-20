#!/usr/bin/env python

# sys imports

import sys
import argparse
import tempfile

# user imports
from lib import *

def cmdline_args():
    # Make parser object
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter, prog="studip-cli")

    p.add_argument("--session", action="store_true",
                   help="creates a user session for great performance improvements") 

    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("list-courses", action="store_true",
                       help="list your courses")
    group.add_argument("view-course", type=str,
                       help="retrieves course info (list)",
                       nargs="+",
                       default=sys.stdin)
    group.add_agrument("list-files", type=str,
                       help="lists files in a list of folders (list)",
                       nargs="+",
                       default=sys.stdin)
    group.add_argument("download", type=str,
                       help="downloads files (list)",
                       nargs="+",
                       default=sys.stdin)
    return(p.parse_args())

def main():
    """ Main program """
    # Code goes over here.


if __name__ == "__main__":
    main():
