import os
import os.path

class ImportSolid(object):
    """Import solid seqencing related data"""
    def check_solid(self):
        """check whether it has the valid instance data for solid seq qa"""
        if not os.path.isdir(data):
            raise RuntimeError
        r_rs = r_qs = []
        for entry in os.listdir(data_dir):
            if os.path.isfile(entry):
                if entry.endswith(".csfasta"):
                    r_rs.append(entry)
                elif entry.endswith(".qual"):
                    r_qs.append(entry)
        if r_rs and r_qs:
            self.raw_reads = r_rs
            self.raw_q = r_qs
        else:
            raise RuntimeError

    def analysis_solid(self):
        """docstring for reading_solid"""


class Import(object):
    """Import seqencing related data"""
    def __init__(self, seq_type, data_dir):
        """
        seq_type: "solid", "illumina"
        """
        self.data_dir = data_dir
        self.seq_type = seq_type
