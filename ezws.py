from reppy.cache import RobotsCache #caching robots.txt files
from urllib.parse import urlparse #parsing local href
from lxml import html as lxmlhtml #converts html to xpath-able tree
from simplecsv import simplecsv #for exporting data
from reppy import logger as rpl #used to disable traceback in reppy
from bs4 import BeautifulSoup
import requests #grabs pages
import json #loads url info
import os #check for file existence

class EZWS:
	"""
	SELF:

	config json config file
	ua     user agent
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
			rpl.setLevel("CRITICAL")
			self.robo=RobotsCache(capacity=100)

		#check var disables or enables robots.txt checking
		#recommended to keep default True value
		self.check=check
		self.req=requests #request obj for parsing url

		self.output=output #where to output file

		self.data=[] #init array of grabbed sites
		self.link=None #current link to grab

		self.configarr=[] #empty array of all configs
		
		#if file is a list, replace configarr with file
		if type(file) is list:
			self.configarr=file

		#if not append the one object to the configarr
		else:
			self.configarr.append(file)

	def allowed(self, url): #checks if url is ok to download
		if self.check:
			if self.robo.allowed(url, self.ua): #checks robot file
				return True

			else:
				print(url, "is not allowed") #notify user if url isnt allowed
				return False
		else:
			return True #if robot checking is off, return true regardless

	@property #when url is called, return it
	def url(self):
		return self.link

	@url.setter #when url is set, parse it
	def url(self, url):
		self.link=url
		self.urlp=urlparse(url)

	def download(self, url):
		if self.allowed(url):
			self.raw=self.req.get(url).content
			self.soup=BeautifulSoup(self.raw, "html.parser") #loads html into soup obj

	def xpath(self, html, xp): #takes html and returns data from xpath
		tree=lxmlhtml.fromstring(html) #generates tree
		return tree.xpath(xp) #returns data from tree

	def select(self, html, json): #determines whether to grab using css or xpath
		if "xpath" in json: #if xpath
			found=self.xpath(html.getText(), json["xpath"]) #return xpath selector arr

		elif "css" in json: #css
			found=html.select(json["css"]) #return a css selector arr

		if self.config["header"]: #if theres a header keep data to one column
			found=found[:1]

		if "css" in json: #if data is css attribute(s) from element
			completed=[]
			for item in found:
				output=[] #arr for storing attribs from each css selected element
				if type(json["contents"]) is str: #if contents is a string, put it into an array
					json["contents"]=[json["contents"]]

				for content in json["contents"]:
					if content and item.has_attr(content): #if not empty and valid, get the element from tag
						output.append(item[content])

					else: #if empty, get the text from tag
						output.append(item.text)

				completed+=output #append attribs to attrib array

			return completed #return scraped data (css)

		else:
			return found #return scraped data (xpath)

	def clear(self):
		self.data=[]

	def load(self, index):
		tmp=self.configarr[index]

		if type(tmp) is dict: #if file is json obj, load it
			self.config=tmp

		else: #assume it is a file and load it
			if os.path.exists(tmp):
				with open(tmp) as f:
					self.config=json.load(f) #opens and parses json file

	def grab(self, index=None):
		if index==None: #using grab() with no params will grab all configs passed
			for i in range(len(self.configarr)):
				self.grab(i) #grab "i" config file

		else:
			self.load(index) #get current file obj
			if self.output: #only create simplecsv obj if file outputting is on
				sc=simplecsv(self.output, mode="w+") #using w+ mode to remove old output
				if self.config["header"]:
					sc.writerow(self.config["header"]) #add header from config to csv
	
			for json in self.config["links"]: #loop through links
				links=[] #empty list of links for now
				if type(json["url"]) is str:
					links.append(json["url"]) #if url is a single str not array append it to an array

				else: #assume it is an array
					links=json["url"]
	
				for link in links: #passing "url" an array of urls will do the same params on all the links
					if self.allowed(link): #check if url is allowed
						self.download(link) #if so download it

						for divs in self.soup.select(json["container"]):
							data=[]
							for grab in json["grab"]: #grabs each element from inside each div
								data+=self.select(divs, grab)
		
							self.data+=data #update internal data
							if self.output:
								sc.writerow(data) #only write to disk if file output is on
			if self.output:
				sc.close() #only close "sc" if file output is on