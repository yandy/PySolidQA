import os
import os.path

class QAParser(object):

    def __init__(self, fn):
        self.reads_fn = "%s.csfasta" % fn
        self.qual_fn = "%s.qual" % fn
        self.seq_fn = "%s.fasta" % fn

    def parse_reads(self):
        """parse reads file"""
        self.read_counts  = 0
        #record the valid length of every read
        self.valid_len_list = []
        #the distribution of valid length: how many reads of
        #certain valid length
        self.valid_len_dist = {}

        try:
            r_fh = open(self.reads_fn, "r")
            for line in r_fh:
                if line.startswith(">") or line.startswith("#"):
                    continue
                self.read_counts += 1
                length = 0
                for bs in line:
                    if bs!= ".":
                        length += 1
                    else:
                        break
                self.valid_len_list.append(length)
                if length in self.valid_len_dist:
                    self.valid_len_dist[length] += 1
                else:
                    self.valid_len_dist[length] = 1
        except IOError, e:
            raise SolidError("Seqence file not found")
        finally:
            r_fh.close()

    def parse_qual(self):
        """parse quality file"""
        self.base_qual_dist = []
        self.read_qual_dist = {}
        try:
            q_fh = open(self.qual_fn, "r")
            for line in q_fh:
                if line.startswith(">") or line.startswith("#"):
                    continue
                qline = [int(qv) for qv in line.split()]
                q_sum = 0
                q_len = 0
                idx = 0
                for qv in qlist:
                    if qv <= 0:
                        break
                    else:
                        q_sum += qv
                        q_len += 1
                        try:
                            elem = self.base_qual_dist[idx]
                        except IndexError, e:
                            elem = {}
                            self.base_qual_dist << elem
                        finally:
                            if qv in elem:
                                elem[qv] += 1
                            else:
                                elem[qv] = 1
                        idx += 1
                if q_len > 0:
                    q_mean = q_sum/q_len
                else:
                    q_mean = 0
                if q_mean in self.read_qual_dist:
                    self.read_qual_dist[q_mean] += 1
                else:
                    self.read_qual_dist[q_mean] = 1
        except IOError, e:
            raise SolidError("Quality file not found")
        finally:
            q_fh.close()

    def parse_seq(self):
        self.base_type_dist = []
        try:
            seq_fh = open(self.seq_fn, "r")
            for line in seq_fh:
                if line.startswith(">") or line.startswith("#"):
                    continue
                idx = 0
                for b in line:
                    try:
                        elem = self.base_type_dist[idx]
                    except IndexError, e:
                        elem = {}
                        self.base_type_dist << elem
                    finally:
                        if b in elem:
                            elem[b] += 1
                        else:
                            elem[b] = 1
                    idx += 1
        except IOError, e:
            raise SolidError("Seqence file not found")
        finally:
            seq_fh.close()

    def parse(self):
        """parse seq and qual file"""
        self.parse_reads()
        self.parse_qual()
        self.parse_seq()
