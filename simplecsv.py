import csv

class simplecsv:
	def __init__(self, file=""):
		self.table=[]
		self.f=open(file, "a+")
		self.csvr=csv.reader(self.f.read())
		self.csvw=csv.writer(self.f)
		for row in self.csvr:
			self.table.append(row)

	def writerow(self, row):
		self.csvw.writerow(row)

	def writerows(self, rows):
		self.csvw.writerows(rows)

	def close(self):
		self.f.close()
