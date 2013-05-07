#!/usr/bin/env python

if __name__ == "__main__":
    from pysolidqa import Parser, SolidError
    import sys
    import argparse
    import os.path

    parser = argparse.ArgumentParser(description="QA script for 2nd sequencing")
    parser.add_argument("inputs", type = str, metavar='N', nargs='+', help = "The files contain reads and quality values")
    parser.add_argument("-o", "--opath", type = str, required = True, help = "where to restore output files ")
    args = parser.parse_args(sys.argv[1:])
    kwargs = vars(args)
    try:
        for idx in range(len(kwargs['inputs'])):
            fin = kwargs['inputs'][idx]
            p = Parser(fin)
            (name, ext) = os.path.splitext(os.path.basename(fin))
            fout = os.path.join(kwargs['opath'], "%s.md" % name)
            fdata = os.path.join(kwargs['opath'], "%s.data" % name)
            p.save(fdata)
            p.report('text', fout)

    except SolidError, e:
        print e
        sys.exit(1)
