#!/usr/bin/env python

# sys imports

import sys
import argparse

# user imports
import studip_cli.browser as browser

def cmdline_args():
    # Make parser object

    default = None

    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter, prog="studip-cli")

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

    # store arg with data from stdin or argument [name, values]
    data = []

    # itererate over args to check if stdin or normal is used
    for arg in vars(args):
        input = getattr(args, arg)
        if isinstance(input, list) and len(input) > 0:
            data.extend([arg, getattr(args, arg)])
        elif isinstance(input, list):
            # Process the arguments after --download
            data.extend([arg, sys.stdin.read().replace("\n", " ").rstrip().split(" ")])

    # if len(data) == 0:
    #     courses.list()
    else:
        match data[0]:
            case "download":
                for item in data[1]:
                    browser.download_file({"file_name": item.split("@@")[0], "file_id": item.split("@@")[1]})
            # TODO
            # case "list-files":
            #     files.list(data[1])
            # case "view-courses":
            #     courses.view(data[1])
if __name__ == "__main__":
    main()
