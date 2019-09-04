from reppy.cache import RobotsCache #caching robots.txt files
from urllib.parse import urlparse #parsing local href
from lxml import html as lxmlhtml #converts html to xpath-able tree
from simplecsv import simplecsv #for exporting data
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
			self.robo=RobotsCache(capacity=100)

		#check var disables or enables robots.txt checking
		#recommended to keep default True value
		self.check=check
		self.req=requests #request obj for parsing url

		self.output=output #where to output file

		self.data=[] #init array of grabbed sites

		self.configarr=[] #empty array of all configs
		
		if type(file) is list:
			self.configarr=file
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

	def xpath(self, html, xp): #takes html and returns data from xpath
		tree=lxmlhtml.fromstring(html) #generates tree
		return tree.xpath(xp) #returns data from tree

	def select(self, html, obj): #determines whether to grab using css or xpath
		if "xpath" in obj: #if xpath
			items=self.xpath(html.getText(), obj["xpath"]) #return xpath selector arr
		else: #css
			items=html.select(obj["css"]) #return a css selector arr
			
		if self.config["header"]: #if theres a header keep data to one column
			items=items[:1]

		if "css" in obj: #if data is css attribute(s) from element
			row=[]
			for item in items:
				cont=[] #arr for storing attribs from each css selected element
				if type(obj["contents"]) is str: #if contents is a string, put it into an array
					obj["contents"]=[obj["contents"]]
					
				for content in obj["contents"]:
					if content and item.has_attr(content): #if not empty and valid, get the element from tag
						cont.append(item[content])
					else: #if empty, get the text from tag
						cont.append(item.text)
				row+=cont #append attribs to attrib array
			return row #return all the attribs (css)
		else:
			return items #return xpath

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
	
			for link in self.config["links"]: #loop through links
				samelinks=[] #empty list of links for now
				if type(link["url"]) is str:
					samelinks.append(link["url"]) #if url is a single str not array append it to an array
				else: #assume it is an array
					samelinks=link["url"]
	
				for samelink in samelinks: #passing "url" an array of urls will do the same params on all the links
					if self.allowed(samelink): #check if url is allowed
						self.download(samelink) #if so download it
						for divs in self.soup.select(link["container"]):
							add=[]
							for get in link["grab"]: #grabs each element from inside each div
								add+=self.select(divs, get)
		
							self.data+=add #update internal data
							if self.output:
								sc.writerow(add) #only write to disk if file output is on
			if self.output:
				sc.close() #only close "sc" if file output is on