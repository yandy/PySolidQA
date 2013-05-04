#!/usr/bin/env python

if __name__ == "__main__":
    from pysolidqa import Parser, SolidError
    import sys
    import argparse
    import os.path

    parser = argparse.ArgumentParser(description="QA script for 2nd sequencing")
    parser.add_argument("inputs", type = str, metavar='N', nargs='+', help = "The files contain reads and quality values")
    parser.add_argument("-d", "--data", type = str, required = False, help = "Data file")
    parser.add_argument("-o", "--output", type = str, required = True, help = "Output file")
    args = parser.parse_args(sys.argv[1:])
    kwargs = vars(args)
    try:
        for idx in range(len(kwargs['inputs'])):
            p = Parser(kwargs['inputs'][idx])
            (pre, ext) = os.path.splitext(kwargs['output'])
            output = "%s-%d%s" % (pre, idx, ext)
            p.report('text', output)
            if 'data' in kwargs:
                (pre, ext) = os.path.splitext(kwargs['data'])
                data = "%s-%d%s" % (pre, idx, ext)
                p.save(data)
    except SolidError, e:
        print e
        sys.exit(1)
