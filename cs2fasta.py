#!/usr/bin/env python

if __name__ == '__main__':
    from pysolidqa import Translate, SolidError
    import sys
    import argparse
    import os.path

    parser = argparse.ArgumentParser(description="Translate csfasta file to fasta file")
    parser.add_argument("inputs", type = str, metavar='N', nargs='+', help = "The csfasta files")
    args = parser.parse_args(sys.argv[1:])
    kwargs = vars(args)
    try:
        for idx in range(len(kwargs['inputs'])):
            (pre, ext) = os.path.splitext(kwargs['inputs'][idx])
            output = "%s.fasta" % pre
            t = Translate(kwargs['inputs'][idx], output)
            t.translate()
    except SolidError, e:
        print e
        sys.exit(1)
