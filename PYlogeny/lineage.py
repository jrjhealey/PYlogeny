
class Lineage(object):
    """A class to hold the methods and info associated with returning lineages from TaxIDs.

    :taxid - the taxid worked out by Eutils
    :ncbi - the NCBITaxa instance. Passed in from parent script so its not invoked inside the loop that calls this
            class (would lead to multiple unecessary invocations)
    :ordered - The taxon hierarchy names, correctly ordered as per the lineage
    :lineage_string - a pre-formatted (comma separated) string for printing/writing

    """

    def __init__(self, taxid, ncbi):
        self.taxid = taxid
        self.ncbi = ncbi
        self.ordered = self.taxid2lineage()
        self.lineage_string = ','.join(self.ordered)

    def taxid2lineage(self):
        try:
            lineage = self.ncbi.get_lineage(self.taxid)
        except ValueError:
            return ['Not_found']
        names = self.ncbi.get_taxid_translator(lineage)
        ordered = [names[tid] for tid in lineage]
        return ordered[2:]


