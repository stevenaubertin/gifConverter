# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import getopt


def convert(input, output, fmt='rgb24'):
    #ffmpeg -i input.webm -pix_fmt rgb24 output.gif
    proc = subprocess.Popen([
            'ffmpeg',
            '-i', input,
            '-pix_fmt',fmt,
            output
        ])
    try:
        proc.wait()
    except:
        pass


def print_help():
    print '-i input file'
    print "-o output file or directory"
    print "-d directory (can't use -i then)"
    print "-h to to display this help message"


def main(argv):
    i = None
    o = None
    d = None

    try:
        opts, args = getopt.getopt(
            argv,
            "i:o:d:h"
        )
    except getopt.GetoptError:
        print_help()
        return 2

    if len(argv) == 0:
        print_help()
        return 0

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            return 0
        elif opt == '-i':
            i = [arg]
        elif opt == '-o':
            o = arg
        elif opt == '-d':
            d = arg

    if d:
        if not os.path.isdir(d):
            print 'Error : Invalid directory',d
            return 2
        i = [j for j in os.listdir(d)]

    for input in i:
        convert(input, o if o else ''.join([os.path.splitext(input)[0],'.gif']))

    return 0


if __name__=="__main__":
    sys.exit(main(sys.argv[1:]))