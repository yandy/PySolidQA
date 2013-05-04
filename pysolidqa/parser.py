import os
import os.path
import json
import cStringIO

from errors import SolidError

class Parser(object):

    def __init__(self, fn):
        self.reads_fn = "%s.csfasta" % fn
        self.qual_fn = "%s.qual" % fn
        self.seq_fn = "%s.fasta" % fn
        self.parsed = False

    def parse_reads(self):
        """parse reads file"""
        self.reads_count  = 0
        #the distribution of valid length: how many reads of
        #certain valid length
        self.valid_len_dist = {}

        try:
            r_fh = open(self.reads_fn, "r")
            for line in r_fh:
                if line.startswith(">") or line.startswith("#"):
                    continue
                line = line.strip()
                self.reads_count += 1
                length = -2
                for bs in line:
                    if bs!= ".":
                        length += 1
                    else:
                        break
                if length <= 0:
                    break
                if length in self.valid_len_dist:
                    self.valid_len_dist[length] += 1
                else:
                    self.valid_len_dist[length] = 1
        except IOError, e:
            raise SolidError("Seqence file not found")
        else:
            r_fh.close()

    def parse_qual(self):
        """parse quality file"""
        # quality distribution based on base position
        self.base_qual_dist = []
        # the mean quality of per reads distribution
        self.read_qual_dist = {}
        try:
            q_fh = open(self.qual_fn, "r")
            for line in q_fh:
                if line.startswith(">") or line.startswith("#"):
                    continue
                line = line.strip()
                qline = [int(qv) for qv in line.split()]
                q_sum = 0
                q_len = 0
                idx = 0
                for qv in qline:
                    if qv <= 0:
                        break
                    else:
                        q_sum += qv
                        q_len += 1
                        try:
                            elem = self.base_qual_dist[idx]
                        except IndexError, e:
                            elem = {}
                            self.base_qual_dist.append(elem)
                        finally:
                            if qv in elem:
                                elem[qv] += 1
                            else:
                                elem[qv] = 1
                        idx += 1
                if q_len > 0:
                    q_mean = float(q_sum/q_len)
                else:
                    q_mean = 0.0
                if q_mean in self.read_qual_dist:
                    self.read_qual_dist[q_mean] += 1
                else:
                    self.read_qual_dist[q_mean] = 1
        except IOError, e:
            raise SolidError("Quality file not found")
        else:
            q_fh.close()

    def parse_seq(self):
        self.base_type_dist = []
        try:
            seq_fh = open(self.seq_fn, "r")
            for line in seq_fh:
                if line.startswith(">") or line.startswith("#"):
                    continue
                line = line.strip()
                idx = 0
                for b in line:
                    try:
                        elem = self.base_type_dist[idx]
                    except IndexError, e:
                        elem = {}
                        self.base_type_dist.append(elem)
                    finally:
                        if b in elem:
                            elem[b] += 1
                        else:
                            elem[b] = 1
                    idx += 1
        except IOError, e:
            raise SolidError("Seqence file not found")
        else:
            seq_fh.close()

    def _full_parse(self):
        """parse seq and qual file"""
        self.parse_reads()
        self.parse_qual()
        self.parse_seq()
        self.parsed = True

    def save(self, filename):
        data_dict = {
        'reads_count': self.reads_count,
        'valid_len_dist': self.valid_len_dist,
        'base_qual_dist': self.base_qual_dist,
        'read_qual_dist': self.read_qual_dist,
        'base_type_dist': self.base_type_dist
        }
        try:
            fh = open(filename, "wb")
        except IOError, e:
            raise e
        json.dump(data_dict, fh)

    def load(self, filename):
        try:
            fh = open(filename, 'r')
        except IOError, e:
            raise e
        data_dict = json.load(fh)
        if not ('reads_count' in data_dict and
                'valid_len_dist' in data_dict and
                'base_qual_dist' in data_dict and
                'read_qual_dist' in data_dict and
                'base_type_dist' in data_dict):
            raise SolidError("format error")
        self.reads_count = data_dict['reads_count']
        self.valid_len_dist = data_dict['valid_len_dist']
        self.base_qual_dist = data_dict['base_qual_dist']
        self.read_qual_dist = data_dict['read_qual_dist']
        self.base_type_dist = data_dict['base_type_dist']

    def report(self, format, filename = None):
        if not self.parsed:
            self._full_parse()
        mth = getattr(self, "report_as_%s" % format, None)
        if mth is None:
            raise SolidError("Report in format '%s' is not supported currently" % format)
        return mth(filename)

    def report_as_html(self, filename):
        raise NotImplementedError

    def report_as_text(self, filename):
        out = cStringIO.StringIO()
        out.write("# Report by PySolidQA\n")
        out.write("## Reads Count:\n%d\n\n" % self.reads_count)
        out.write("## Reads Length Distribution:\n")
        out.write("length\treads\n")
        for k, v in self.valid_len_dist.items():
            out.write("%d:\t%d\n" % (k, v))
        out.write("\n")
        out.write("## Reads Quality Distribution based on base position\n")
        for i in xrange(len(self.base_qual_dist)):
            out.write("#### on position %d:\n" % i)
            out.write("quality\treads\n")
            for k, v in self.base_qual_dist[i].items():
                out.write("%d:\t%d\n" % (k, v))
        out.write("\n")
        out.write("## Reads Mean Quality Distribution\n")
        out.write("quality\treads\n")
        for k, v in self.read_qual_dist.items():
            out.write("%f:\t%d\n" % (k, v))
        out.write("\n")
        out.write("## Base Type Distribution\n")
        for i in xrange(len(self.base_type_dist)):
            out.write("#### on position %d:\n" % i)
            out.write("base\treads\n")
            for k, v in self.base_type_dist[i].items():
                out.write("%s:\t%d\n" % (k, v))
        ret = out.getvalue()
        out.close()
        open(filename, "wb").write(ret)
        return ret
