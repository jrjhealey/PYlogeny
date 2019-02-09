#!/usr/bin/env python3

"""
Create a taxonomic breakdown of a list of accessions. Similar to the taxonomy browser
provided by BLAST (which for some reason is not downloadable). Built around the ETE3
taxonomy browsing toolkit and Eutils.
"""

# Standard lib imports
import sys
import logging
import argparse
# Non-standard lib imports (dependencies)
from Bio import Entrez
from ete3 import NCBITaxa
# This package's imports
from .query import Query
from .lineage import Lineage
from .version import __version__

NO_COLOR = "\33[m"
RED, GREEN, ORANGE, BLUE, PURPLE, LBLUE, GREY = map("\33[%dm".__mod__, range(31, 38))

logging.basicConfig(format="[%(asctime)s] %(levelname)-8s->  %(message)s",
                    level=logging.NOTSET, datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)


def add_color(logger_method, color):
    def wrapper(message, *args, **kwargs):
        return logger_method(color+message+NO_COLOR, *args, **kwargs)
    return wrapper


for level, color in zip(("info", "warning", "error", "debug"), (GREEN, ORANGE, RED, BLUE)):
    setattr(logger, level, add_color(getattr(logger, level), color))


def get_args():
    """Parse command line arguments"""
    desc="Create a taxonomic breakdown for a list of accession numbers."
    epi=("Given an input list of accession numbers, create a table describing the \n"
         "taxonomic memberships of those accession numbers. \n")

    try:
        parser = argparse.ArgumentParser(description=desc, epilog=epi, prog="PYlogeny.py")
        parser.add_argument("-i", "--infile", action="store",
                            help="A one-per-line file of accession numbers.")
        parser.add_argument("-o", "--outfile", action="store",
                            help="Output tabular file (default STDOUT).")
        parser.add_argument("-d", "--database", action="store",
                            help="What database to search for the accessions in (if you know it), "
                                 "the script will attempt to use their format to guess otherwise.")
        parser.add_argument("-e", "--email", action="store", required=True,
                            help="Email to use with Eutils/Entrez.")
        parser.add_argument("--version", action="version",
                            version="%(prog)s v{version}".format(version=__version__))
        parser.add_argument("-v", "--verbose", action="count", default=0,
                            help="Increase verbosity/logging.")
        parser.add_argument("-s", "--sql", action="store", default='~/.etetoolkit',
                            help="Location to store the ETE3 database. Default is in ~/.etetoolkit ."
                                 "If you specify a different location to the last instance, a new copy"
                                 "of the database will have to be downloaded regardless.")
        parser.add_argument("-u", "--update", action='store_true',
                            help="Update the local copy of the TaxID database. (False by default, but"
                                 "should be done on a frequent basis).")

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

    except NameError:
        sys.stderr.write("An exception occurred with argument parsing. Check your provided options.")
        sys.exit(1)

    return parser.parse_args()


def main():
    """Given a list of accessions, return TaxIDs and taxonomic information."""
    args = get_args()
    assert args.verbose < 3, f"verbose supports maximum 3 levels at present [0, 1, 2], got: {args.verbose}"
    levels_dict = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}
    logging.getLogger().setLevel(levels_dict[args.verbose])
    logger.info(f"Launching {__file__}")

    logger.debug(f"Contacting NCBI's servers with the email: {args.email}")
    Entrez.email = args.email

    logger.warning(f"Creating the NCBITaxa instance. If this is the first run, this could take some time.")
    logger.warning(f"The database is stored at: {args.sql}")
    ncbi = NCBITaxa(dbfile=args.database)
    if args.update:
        logger.warning(f"Updating the taxa database, this could take some time.")
        ncbi.update_taxonomy_database()

    if args.outfile is None:
        logger.info(f"No output file specified, writing to STDOUT.")
        ofh = sys.stdout
    else:
        ofh = open(args.outfile, 'w')

    with open(args.infile, 'r') as ifh:
        for i, acc in enumerate(ifh):
            logger.info(f"Working on Accession {i}: {acc.strip()}")
            record = Query(acc)
            lineage = Lineage(record.taxid, ncbi).lineage_string
            ofh.write(acc.strip() + ',' + record.taxid + ',' + lineage + '\n')

    ofh.close()


if __name__ == "__main__":
    assert sys.version_info >= (3, 6), "Sorry, this script is absolutely Python3 only."
    main()
