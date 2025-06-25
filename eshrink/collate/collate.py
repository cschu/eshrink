#! /usr/bin/env python3

import argparse
import os
import pathlib

from ..buffered_reader import stream_file


class EmapperRecord:
	def __init__(self, fhash, nproteins, fields):
		self.fhash = fhash
		self.nproteins = nproteins
		self.nsets = 1
		self.fields = fields

	def update(self, other):
		if other.fhash == self.fhash:
			if other.fields != self.fields:
				raise ValueError(f"Fields do not match: \n{self.fields}\n{other.fields}")
		self.nsets += other.nsets
		self.nproteins += other.nproteins


class EmapperCollator:
	def __init__(self):
		self.records = {}
	def process_file(self, f):
		for line in stream_file(f):
			fhash, nproteins, *fields = line.strip().split("\t")
			
			new_rec = EmapperRecord(fhash, nproteins, fields)
			rec = self.records.get(fhash)	
			if rec is None:
				self.records[fhash] = new_rec
			else:
				rec.update(new_rec)





def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("input_dir", type=str)
	args = ap.parse_args()

	try:
		path, dirs, _ in os.walk(args.input_dir)
	except StopIteration:
		print(f"Invalid input dir: {args.input_dir}")
		dirs = []

	collator = EmapperCollator()

	for dir in dirs:
		f = pathlib.Path(path / dir / "hashes.txt")
		if f.is_file():
			collator.process_file(f)

	




	try:
		path, dirs, _ = next(w)
	except StopIteration:
		print(f"Invalid input dir: {args.input_dir}")
		dirs = []






if __name__ == "__main__":
	main()