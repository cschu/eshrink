    #!/usr/bin/env python3

import argparse
import csv
import gzip
import hashlib
import os
import sys


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
        
            yield row[:4] + [row[5], encoded,]

    def process_file(self, fi, fo):
        with gzip.open(fi, "rt") as _in, open(fo, "wt") as _out:
            print(*("\t".join(item) for item in self.encode(_in)), file=_out, sep="\n")

    def dump_hashes(self, fo):
        with open(fo, "wt") as _out:
            for k, v in sorted(self.encoded.items()):
                print(k, *v, file=_out, sep="\t")

        


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir")
    args = ap.parse_args()


    encoder = EmapperEncoder()
    
    w = os.walk(args.input_dir)
    try:
        path, dirs, _ = next(w)
    except StopIteration:
        print(f"Invalid input dir: {args.input_dir}")
        dirs = []

    for i, d in enumerate(dirs):
        if i > 2:
            break
        f = os.path.join(path, d, f"{d}.emapper.annotations.gz")
        if os.path.isfile(f):
            print(f)
            encoder.process_file(f, f"{os.path.basename(f)}.python3.encoded")
    
    encoder.dump_hashes("hashes.txt")



if __name__ == "__main__":
    main()
