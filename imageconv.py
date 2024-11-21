#!/usr/bin/env python

from pyimagevideo.convert import png2tiff

if __name__ == "__main__":
    from argparse import ArgumentParser

    p = ArgumentParser(description="takes directory of sequential PNG plots to single multipage TIFF")
    p.add_argument("outfn", help="myfile.tiff name to write (in path of input files")
    p.add_argument("pat", help="globbing pattern", default="*.png")
    P = p.parse_args()

    tlist = png2tiff(P.outfn, P.pat)
