# PYlogeny

A simple tool built around ETE3 and BioPython's Eutils to convert from accession numbers to Taxonomy IDs and their
associated lineage information.

## Basics

The only 2 arguments needed are an email address, and a file of accession numbers, one per line, like so:

```
WP_041379885.1
WP_058588699.1
WP_105398703.1
...
```

##### Full usage:
```
usage: PYlogeny.py [-h] [-i INFILE] [-o OUTFILE] [-d DATABASE] -e EMAIL
                   [--version] [-v] [-s SQL] [-u]

Create a taxonomic breakdown for a list of accession numbers.

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        A one-per-line file of accession numbers.
  -o OUTFILE, --outfile OUTFILE
                        Output tabular file (default STDOUT).
  -d DATABASE, --database DATABASE
                        What database to search for the accessions in (if you know it),
                        the script will attempt to use their format to guess otherwise.
  -e EMAIL, --email EMAIL
                        Email to use with Eutils/Entrez.
  --version             show program's version number and exit
  -v, --verbose         Increase verbosity/logging. (-v or -vv)
  -s SQL, --sql SQL     Location to store the ETE3 database. Default is in ~/.etetoolkit/ .
                        If you specify a different location to the last instance, a
                        new copy of the database will have to be downloaded regardless.
  -u, --update          Update the local copy of the TaxID database.
                        (False by default, but should be done on a frequent basis).

Given an input list of accession numbers, create a table describing the taxonomic
memberships of those accession numbers.

The first time you run this program, and any time -u|--update is used, the
taxon dump will be made and an SQL database created. This takes several minutes.
```

## Simple usage

    $ PYlogeny.py -e email@domain.com -i file_of_accessions.txt

## More complicated usage

    $ PYlogeny.py -vvu -e email@domain.com -i file_of_accessions.txt -s /path/to/taxdb -o lineages.csv

## Dependencies
The `ETE3` toolkit, `BioPython`, and _absolutely requires_ `python3` (and no, there is not going to be any `Python2` compatability).
It is advised to use a miniconda/anaconda installation, and install
them via:

    $ conda install -c anaconda biopython

and

    $ conda install -c etetoolkit ete3

The `requirements.txt` file shows the latest versions of these packages, since it was developed with these installed, but will likely work
with somewhat older versions too (untested).
