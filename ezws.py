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
	def __init__(self, file, ua, check=True, output="output.csv"):
		if check: #only setup robot checker if robot checking is enabled
			self.ua=ua #user agent
			self.robo=RobotsCache(capacity=0)

		#check disables or enables robots.txt checking
		#recommended to keep default True value
		self.check=check
		self.req=requests

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
		sc=simplecsv("output.csv", mode="w+") #using w+ mode to remove old output
		sc.writerow(self.config["header"]) #add header from config to csv

		for link in self.config["links"]:     #loop through links
			if self.allowed(link["url"]): #check if url is allowed
				self.download(link["url"]) #if so download it
				for divs in self.soup.select(link["container"]):
					row=[]
					for get in link["grab"]: #grabs each element from inside each div
						item=divs.select(get["css"])[0]
						if get["content"]: #if not empty, get the element from tag
							row.append(item[get["content"]])
						else: #if empty, get the text from tag
							row.append(item.text)
					sc.writerow(row)
		sc.close()
