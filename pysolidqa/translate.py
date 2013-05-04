class Translate(object):
    """translate solid csfasta file to fasta file"""
    def __init__(self, csfasta, fasta):
        self.csfasta = csfasta
        self.fasta = fasta
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
        fin = open(self.csfasta, 'r')
        fo = open(self.fasta, 'w')
        for line in fin:
            if line.startswith("#"):
                continue
            elif line.startswith(">"):
                fo.write(line)
            else:
                line = line.strip()
                fo.write(self._translate_read(line))
                fo.write("\n")
        fin.close()
        fo.close()

    def _translate_read(self, read):
        seq = [read[0]]
        for b in read[1:]:
            if b == ".":
                break
            seq.append(self.color_space[seq[-1]][b])
        return "".join(seq[2:])
