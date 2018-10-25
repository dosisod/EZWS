from urllib.parse import urlparse   #parsing local href
from reppy.cache import RobotsCache #caching robots.txt files
from simplecsv import simplecsv     #for exporting data
from bs4 import BeautifulSoup
import requests #grabs pages
import json     #loads url info
import os       #check for file existence

class EZWS:
	"""
	SELF:

	config json config file
	ua     user agent
	txt    path to current robot file
	robo   robotcache obj
	link   current link
	urlp   url parse object for current link
	soup   current html page soup obj
	req    requests obj
	raw    raw html from req.get()
	check  check for robot files, keep true
	output name of output csv file
	"""
	def __init__(self, file, ua, check=True, output="output.csv"): #setting output to false disables file output
		if check: #only setup robot checker if robot checking is enabled
			self.ua=ua #user agent
			self.robo=RobotsCache(capacity=0)

		#check var disables or enables robots.txt checking
		#recommended to keep default True value
		self.check=check
		self.req=requests #request obj for parsing url

		self.output=output #where to output file

		self.data=[] #init array of grabbed sites

		if type(file) is dict: #if file is json obj, load it
			self.config=file

		else: #assume it is a file and load it
			if os.path.exists(file):
				with open(file) as f:
					self.config=json.load(f) #opens and parses json file

	def allowed(self, url): #checks if url is ok to download
		if self.check:
			if self.robo.allowed(url, self.ua): #checks robot file
				return True
			else:
				print(url,"is not allowed") #notify user if url isnt allowed
				return False
		else:
			return True #if robot checking is off, return true regardless

	@property #when url is called, return it
	def url(self):
		if hasattr(self, "link"): #handles whether self has link attribute
			return self.link
		else:
			return "" #if not return empty string

	@url.setter #when url is set, parse it
	def url(self, url):
		self.link=url
		self.urlp=urlparse(url)

	def download(self, url):
		if self.allowed(url):
			self.raw=self.req.get(url).content
			self.soup=BeautifulSoup(self.raw, "html.parser") #loads html into soup obj

	def grab(self):
		if self.output: #only create simplecsv obj if file outputting is on
			sc=simplecsv("output.csv", mode="w+") #using w+ mode to remove old output
			if self.config["header"]:
				sc.writerow(self.config["header"]) #add header from config to csv

		for link in self.config["links"]:     #loop through links
			if self.allowed(link["url"]): #check if url is allowed
				self.download(link["url"]) #if so download it
				for divs in self.soup.select(link["container"]):
					row=[] #reset row
					for get in link["grab"]: #grabs each element from inside each div
						if self.config["header"]: #if theres a header keep data to one column
							items=divs.select(get["css"])[:1]
						else: #else dont care about data being in order
							items=divs.select(get["css"])

						for item in items:
							cont=[] #arr for storing attribs from each css selected element
							for content in get["contents"]:
								if content: #if not empty, get the element from tag
									cont.append(item[content])
								else: #if empty, get the text from tag
									cont.append(item.text)
							row.append(cont)

					self.data+=row
					if self.output:
						sc.writerow(row)
		if self.output:
			sc.close()
