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
	"""
	def __init__(self, file, ua, check=True):
		if check: #only setup robot checker if robot checking is enabled
			self.ua=ua #user agent
			self.robo=RobotsCache(capacity=0)

		#check disables or enables robots.txt checking
		#recommended to keep default True value
		self.check=check
		self.req=requests

		if os.path.exists(file):
			with open(file) as f:
				self.config=json.load(f) #opens and parses json file

	def allowed(self, url): #checks if url is ok to download
		if self.check:
			return self.robo.allowed(url, self.ua)
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
			self.soup=BeautifulSoup(self.raw, "html.parser")
			return True
		else:
			print("Skipping: not allowed")
			return False
