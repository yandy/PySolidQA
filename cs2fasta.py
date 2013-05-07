#!/usr/bin/env python

if __name__ == '__main__':
    from pysolidqa import Translate, SolidError
    import sys
    import argparse
    import os.path

    parser = argparse.ArgumentParser(description="Translate csfasta file to fasta file")
    parser.add_argument("inputs", type = str, metavar='N', nargs='+', help = "The csfasta files")
    parser.add_argument("-f", "--filte", action='store_true', default=False, help = "The csfasta files")
    parser.add_argument("-t", "--cutoff", type= int, default = 12, help = "if option 'filte' is True, set the cutoff for quality")
    parser.add_argument("-m", "--min", type= int, default = 25, help = "if option 'filte' is True, set the min length for quality")
    args = parser.parse_args(sys.argv[1:])
    kwargs = vars(args)
    try:
        for idx in range(len(kwargs['inputs'])):
            (pre, ext) = os.path.splitext(kwargs['inputs'][idx])
            if kwargs['filte']:
                output = "%s.filted.fasta" % pre
                qual = "%s.qual" % pre
                cutoff = kwargs['cutoff']
                min_len = kwargs['min']
                t = Translate(kwargs['inputs'][idx], output, qual, cutoff, min_len)
            else:
                output = "%s.fasta" % pre
                t = Translate(kwargs['inputs'][idx], output)
            t.translate()
    except SolidError, e:
        print e
        sys.exit(1)
