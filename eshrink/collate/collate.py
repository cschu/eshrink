#! /usr/bin/env python3

import argparse
import os
import pathlib
import sys

from ..buffered_reader import stream_file


class EmapperRecord:
	def __init__(self, fhash, nproteins, fields):
		self.fhash = fhash
		self.nsets = 1
		self.nproteins = int(nproteins)
		self.fields = tuple(fields)

	def update(self, fhash, nproteins, fields):
		if fhash == self.fhash:
			if fields != self.fields:
				raise ValueError(f"Fields do not match: \n{self.fields}\n{fields}")
		self.nsets += 1
		self.nproteins += int(nproteins)

	def tostr(self):
		return "\t".join((self.fhash, str(self.nsets), str(self.nproteins),) + self.fields)


class EmapperCollator:
	def __init__(self):
		self.records = {}
	def process_file(self, f):
		for line in stream_file(f):
			fhash, nproteins, *fields = line.strip().split("\t")
			
			rec = self.records.get(fhash)	
			if rec is None:
				self.records[fhash] = EmapperRecord(fhash, nproteins, fields)
			else:
				rec.update(fhash, nproteins, fields)

	def dump(self, out=sys.stdout):
		for record in self.records.values():
			print(record.tostr(), file=out)





def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("input_dir", type=str)
	args = ap.parse_args()

	w = os.walk(args.input_dir)
	try:
		path, dirs, _ = next(w)
	except StopIteration:
		print(f"Invalid input dir: {args.input_dir}")
		dirs = []

	collator = EmapperCollator()

	input_path = pathlib.Path(path)

	for i, dir in enumerate(dirs):
		if i > 10:
			break
		f = pathlib.Path(input_path / dir / "hashes.txt")
		if f.is_file():
			collator.process_file(f)

	collator.dump()

	




	try:
		path, dirs, _ = next(w)
	except StopIteration:
		print(f"Invalid input dir: {args.input_dir}")
		dirs = []






if __name__ == "__main__":
	main()