import sys
import os
import argparse


def run_deflat(filename, addr, baseaddr=None):
    if baseaddr:
        os.system("python3 deflat.py -f %s --addr %s -b %s" % (filename, addr, baseaddr))
    else:
        os.system("python3 deflat.py -f %s --addr %s" % (filename, addr))


def main():
    description = """
    This is a support script for multiple patches on a single file.
    Please use the main 'deflat.py' script if there is only a single patch to be applied.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-f", "--file", help="binary to analyze")
    parser.add_argument("--addr", nargs='+', help="address of target function in hex format")
    parser.add_argument('-b',"--baseaddr", help="file base address")
    args = parser.parse_args()

    if args.file is None or args.addr is None:
        parser.print_help()
        sys.exit(0)

    filename = args.file
    baseaddr = args.baseaddr

    addr = args.addr
    
    for val in addr:
        run_deflat(filename, val, baseaddr)
        os.system("rm %s" % filename)
        filename += '_recovered'
    
    new_filename = filename.split("_")[0] + "_recovered_multi"

    os.system("mv %s %s" % (filename, new_filename))
    

if __name__ == "__main__":
    main()
