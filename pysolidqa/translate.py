class Translate(object):
    """translate solid csfasta file to fasta file"""
    def __init__(self, csfasta, fasta, qual = None, cutoff = 12, min_len = 25):
        self.csfasta = csfasta
        self.fasta = fasta
        self.qual = qual
        self.cutoff = cutoff
        self.min_len = min_len
        self.color_space = {
        'A': {
            '0': 'A',
            '1': 'C',
            '2': 'G',
            '3': 'T'
        },
        'G': {
            '0': 'G',
            '1': 'T',
            '2': 'A',
            '3': 'C'
        },
        'C': {
            '0': 'C',
            '1': 'A',
            '2': 'T',
            '3': 'G'
            },
        'T': {
            '0': 'T',
            '1': 'G',
            '2': 'C',
            '3': 'A'
            }
        }

    def translate(self):
        """
        if ft is True, filte low quality base when translate
        """
        fin = open(self.csfasta, 'r')
        fo = open(self.fasta, 'w')
        if self.qual:
            fqual = open(self.qual, 'r')

        for line in fin:
            if self.qual:
                qline = fqual.readline()
            if line.startswith("#"):
                continue
            elif line.startswith(">"):
                fo.write(line)
            else:
                line = line.strip()
                if self.qual:
                    qline = qline.strip()
                    fo.write(self._translate_read(line, qual = qline, cutoff = self.cutoff, min_len = self.min_len))
                else:
                    fo.write(self._translate_read(line))
                fo.write("\n")
        fin.close()
        fo.close()

    def _translate_read(self, read, **filte):
        seq = [read[0]]
        for b in read[1:]:
            if b == ".":
                break
            seq.append(self.color_space[seq[-1]][b])
        end = 1
        if filte:
            qual = filte.get("qual", [])
            cutoff = filte.get("cutoff", 12)
            min_len = filte.get("min_len", 25)
            for q in qual:
                if q < cutoff:
                    break
                end ++ 1
            seq = seq[:end]
            if len(seq) < min_len:
                seq = []
        return "".join(seq)
