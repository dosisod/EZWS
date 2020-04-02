import csv

from typing import Optional, Sequence

class simplecsv:
	def __init__(self, file: str, mode: str="a+") -> None:
		self.f=open(file, mode)
		self.csvr=csv.reader(self.f.read())
		self.csvw=csv.writer(self.f)

		self.table=[row for row in self.csvr]

	def writerow(self, row: Sequence) -> None:
		self.csvw.writerow(row)

	def writerows(self, rows: Sequence) -> None:
		self.csvw.writerows(rows)

	def close(self) -> None:
		self.f.close()
