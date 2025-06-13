    #!/usr/bin/env python3

import csv
import gzip
import hashlib
import sys

from collections import Counter


class EmapperEncoder:
    def __init__(self):
        self.encoded = {}

    def encode(self, _in):
        for row in csv.reader(_in, delimiter="\t"):
            if row and row[0] and row[0][0] == "#":
                continue
            annotation = "\t".join(row[4:5] + row[6:])
            encoded = hashlib.sha256(annotation.encode()).hexdigest()

            self.encoded.setdefault(encoded, [0, annotation])[0] += 1
        
            yield row[:4], row[5], encoded

    def process_file(self, fi, fo):
        with gzip.open(fi, "rt") as _in, open(fo, "wt") as _out:
            print(*("\t".join(item) for item in self.encode(_in)), file=_out, delimiter="\n")

    def dump_hashes(self, fo):
        with open(fo, "wt") as _out:
            for k, v in sorted(self.encoded.items()):
                print(k, *v, file=_out, delimiter="\t")

        


def main():

    encoder = EmapperEncoder()
    encoder.process_file(sys.argv[1], sys.argv[2])
    encoder.dump_hashes("hashes.txt")

    # d = {}
    # c = Counter()
    # with gzip.open(sys.argv[1], "rt") as _in, open(sys.argv[2] + ".encoded", "wt") as _out1:
    #     for row in csv.reader(_in, delimiter='\t'):
    #         if row and row[0] and row[0][0] == "#":
    #             continue
    #         annotation = "\t".join(row[4:5] + row[6:])
    #         encoded = hashlib.sha256((annotation.encode())).hexdigest()

    #         print(*row[:4], row[5], encoded, file=_out1, sep="\t")
    #         d[encoded] = annotation
    #         c[encoded] += 1

    # with open(sys.argv[2] + ".hashes", "wt") as _out2:
    #     for k, v in d.items():
    #         print(k, c[k], v, file=_out2, sep="\t")





if __name__ == "__main__":
    main()