	#!/usr/bin/env python3

import csv
import gzip
import hashlib
import sys

from collections import Counter


def main():

    d = {}
    c = Counter()
    with gzip.open(sys.argv[1], "rt") as _in, open(sys.argv[2] + ".encoded", "wt") as _out1:
        for row in csv.reader(_in, delimiter='\t'):
            if row and row[0] and row[0][0] == "#":
                continue
            annotation = "\t".join(row[4:5] + row[6:])
            m = hashlib.sha256()
            m.update(annotation.encode())
            encoded = m.hexdigest()

            print(*row[:4], row[5], encoded, file=_out1, sep="\t")
            d[encoded] = annotation
            c[encoded] += 1

    with open(sys.argv[2] + ".hashes", "wt") as _out2:
        for k, v in d.items():
            print(k, c[k], v, file=_out2, sep="\t")





if __name__ == "__main__":
    main()