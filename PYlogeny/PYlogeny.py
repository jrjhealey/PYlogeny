#!/usr/bin/env python3

"""
Create a taxonomic breakdown of a list of accessions. Similar to the taxonomy browser
provided by BLAST (which for some reason is not downloadable). Built around the ETE3
taxonomy browsing toolkit and Eutils.
"""

import sys
import argparse
from .query import Query

def get_args():
    """Parse command line arguments"""
    desc="Create a taxonomic breakdown for a list of accession numbers."
    epi=("Given an input list of accession numbers, create a table describing the\n"
         "taxonomic memberships of those accession numbers.\n")

    try:
        parser = argparse.ArgumentParser(description=desc, epilog=epi, prog='PYlogeny.py',
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-i','--infile', action='store',
                            help='A one-per-line file of accession numbers.')
        parser.add_argument('-a', '--accession', action='store',
                            help='A string of one or more (comma separated) accession numbers.')
        parser.add_argument('-o', '--outfile', action='store',
                            help='Output tabular file.')
        parser.add_argument('-e', '--email', action='store', required=True,
                            help='Email to use with Eutils/Entrez.')

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

    except NameError:
        sys.stderr.write("An exception occurred with argument parsing. Check your provided options.")
        sys.exit(1)

def main():
    """Given a list of accessions, return TaxIDs and taxonomic information."""

    args = get_args()



if __name__ == "__main__":
    main()
