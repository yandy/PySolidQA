#!/usr/bin/env python

def print_result(result, out):
    """print the result of analysis"""
    #total reads number of each file
    out.write("Result:\nTotal raw reads number:\n\n")
    for k, v in result["read_counts"].items():
        out.write("\nIn file '%s':\t%d reads\n" % (k, v))
    #valid length
    out.write("\n\nValid length of raw reads\n\n")
    #average length
    for k, v in result["valid_length_list"].items():
        out.write("\nIn file '%s':\naverage length:\t%d\n" % (k, sum(v)/len(v)))
    #length distribution
    for k, v in result["valid_length_distribution"].items():
        out.write("\nIn file '%s':\nvalid length distribution:\n" % k)
        for lv, cv in v.items():
            out.write("%d:\t%d\n" % (lv, cv))
    #quality summary
    out.write("\n\nQuality summary of raw reads\n\n")
    #average quality
    for k, v in result["read_average_quality_list"].items():
        out.write("\nIn file %s:\naverage quality:\t%d\n" % (k, sum(v)/len(v)))
    #quality distribution
    for k, v in result["read_average_quality_distribution"].items():
        out.write("\nIn file %s:\naverage quality distribution:\n" % k)
        for lv, cv in v.items():
            out.write("%d:\t%d\n" % (lv, cv))

if __name__ == "__main__":
    from importer import Importer
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="QA script for 2nd sequencing")
    parser.add_argument("-i", "--input", type = str, help = "The directory stored the sequencing data", required = True)
    t_choices = ["solid"]
    parser.add_argument("-t", "--type", type = str,
            choices = t_choices, required = True,
            help = "The sequencing method used to generate the data, currently support only 'solid'")
    parser.add_argument("-o", "--output", type = str, required = True, help = "Output file")
    args = parser.parse_args(sys.argv[1:])
    kwargs = vars(args)
    importer = Importer(kwargs["type"], kwargs["input"])
    ret = ""
    try:
        ret = importer.result
    except RuntimeError:
        print "Reading data file failed!"
    if ret:
        try:
            out = open(kwargs["output"], "w")
            print_result(ret, out)
        finally:
            out.close()
    else:
        print "No result"
