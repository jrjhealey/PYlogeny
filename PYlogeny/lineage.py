import logging
logger = logging.getLogger('__main__')
NO_COLOR = "\33[m"
RED, GREEN, ORANGE, BLUE, PURPLE, LBLUE, GREY = map("\33[%dm".__mod__, range(31, 38))
def add_color(logger_method, color):
    def wrapper(message, *args, **kwargs):
        return logger_method(color+message+NO_COLOR, *args, **kwargs)
    return wrapper

for level, color in zip(("info", "warning", "error", "debug"), (GREEN, ORANGE, RED, BLUE)):
    setattr(logger, level, add_color(getattr(logger, level), color))


class Lineage(object):
    """A class to hold the methods and info associated with returning lineages from TaxIDs.

    :taxid - the taxid worked out by Eutils
    :ncbi - the NCBITaxa instance. Passed in from parent script so its not invoked inside the loop that calls this
            class (would lead to multiple unnecessary invocations)
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
            logger.warning(f"No lineage returned for taxid {self.taxid}. You may need to update the database.")
            return ['Not_found']
        names = self.ncbi.get_taxid_translator(lineage)
        ordered = [names[tid] for tid in lineage]
        return ordered[2:]


