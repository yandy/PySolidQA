import os
import os.path

class Parser(object):

    def __init__(self, fn):
        self.reads_fn = "%s.csfasta" % fn
        self.qual_fn = "%s.qual" % fn

    def parse(self):
        """parse seq and qual file"""
        read_counts  = 0
        valid_len = []

        valid_length_list = {}
        valid_length_dist = {}
        read_q_list = {}
        read_q_dist = {}
        try:
            r_fh = open(self.reads_fn, 'r')
            read_counts[r] = 0
            valid_length_list[r] = []
            valid_length_dist[r] = {}
            for line in r_fh:
                if line.startswith(">") or line.startswith("#"):
                    continue
                read_counts[r] = read_counts[r] + 1
                length = 0
                for bs in line:
                    if bs != ".":
                        length = length + 1
                    else:
                        break
                valid_length_list[r].append(length)
                if length in valid_length_dist[r]:
                    valid_length_dist[r][length] = valid_length_dist[r][length] + 1
                else:
                    valid_length_dist[r][length] = 1
        finally:
            r_fh.close()

        for q in self.raw_q:
            try:
                q_fh = open(q, 'r')
                read_q_list[q] = []
                read_q_dist[q] = {}
                for line in q_fh:
                    if line.startswith(">") or line.startswith("#"):
                        continue
                    qlist = [int(qv) for qv in line.split()]
                    sumq = 0
                    lenq = 0
                    for qv in qlist:
                        if qv <= 0:
                            break
                        else:
                            sumq += qv
                            lenq += 1
                    if lenq > 0:
                        qvs = sumq/lenq
                    else:
                        qvs = 0
                    read_q_list[q].append(qvs)
                    if qvs in read_q_dist[q]:
                        read_q_dist[q][qvs] = read_q_dist[q][qvs] + 1
                    else:
                        read_q_dist[q][qvs] = 1
            finally:
                q_fh.close()
        return {
                "read_counts": read_counts,
                "valid_length_list": valid_length_list,
                "read_average_quality_list": read_q_list,
                "valid_length_distribution": valid_length_dist,
                "read_average_quality_distribution": read_q_dist
                }


class Importer(SolidImporter):
    """Import seqencing related data"""
    def __init__(self, seq_type, data_dir):
        """
        seq_type: "solid", "illumina"
        """
        self.data_dir = data_dir
        self.seq_type = seq_type

    def check(self):
        """docstring for check"""
        ck = getattr(self, "check_%s" % self.seq_type)
        ck()

    def analysis(self):
        """invoke related "analysis" method due to the type of data"""
        am = getattr(self, "analysis_%s" % self.seq_type)
        return am()

    def _full_process(self):
        """the process of workflow"""
        checker = self.check()
        return self.analysis()

    report = property(_full_process, "Get the report")
