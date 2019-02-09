from Bio import Entrez

class Query(object):
    """Given an accession, return the database which should be queried in accordance and run the query.

    :accession - the input query accession number
    :database - an internal variable which holds either a specified database or guesses from the accession
    :taxid - The thing we came here for; the converted TaxID which corresponds to the Accession
    """

    def __init__(self, accession, database=None):
        self.accession = accession
        self.database = self.guess_database() if not database else database
        self.taxid = self.query()


    def __repr__(self):
        return str(self.__class__.__name__ + "<" + self.accession + ">")

    def _is_refseq(self):
        return True if self.accession[2] == "_" else False

    def guess_database(self):
        """Guess the correct database for querying based off the format of the accession"""
        database_mappings_refseq = {'AC_': 'nuccore', 'NC_': 'nuccore', 'NG_': 'nuccore',
                                    'NT_': 'nuccore', 'NW_': 'nuccore', 'NZ_': 'nuccore',
                                    'AP_': 'protein', 'NP_': 'protein', 'YP_': 'protein',
                                    'XP_': 'protein', 'WP_': 'protein'}
        # I THINK! based on:
        # https://www.ncbi.nlm.nih.gov/books/NBK21091/table/ch18.T.refseq_accession_numbers_and_mole/?report=objectonly
        # RefSeq identifiers have a _ at the third position. Non RefSeq ID's are horror show
        # so I'm ignoring them for the time being.
        if not self._is_refseq():
            sys.stderr.write("RefSeq accessions only at present")
            return

        return database_mappings_refseq[self.accession[0:3]]

    def query(self):
        """Query Entrez databases to return the TaxID for the accession"""
        return str(Entrez.read(Entrez.esummary(db=self.database, id=self.accession))[0]['TaxId'])
