from reppy.cache import ReraiseExceptionPolicy, RobotsCache # type: ignore
from reppy.exceptions import ConnectionException # type: ignore
from urllib.parse import urlparse
from lxml import html as lxmlhtml # type: ignore
from bs4 import BeautifulSoup # type: ignore
import requests
import reppy # type: ignore
import json
import os

from ezws.simplecsv import simplecsv
from ezws.links import explode

from typing import Optional, List, Any, Dict, Union, cast

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
	def __init__(self, file: Union[str, Dict], ua: str, check: bool=True, output: str="output.csv") -> None:
		if check:
			self.ua=ua

			reppy.logger.setLevel("CRITICAL")
			self.robo=RobotsCache(capacity=100, cache_policy=ReraiseExceptionPolicy(0))

		self.check=check
		self.req=requests

		#setting output to false disables file output
		self.output=output

		self.data: List[str]=[]
		self.link=""

		self.configarr=file if type(file) is list else [file]

	def allowed(self, url: str) -> bool:
		if not self.check:
			return True

		try:
			if self.robo.allowed(url, self.ua):
				return True
			print(url, "is not allowed")

		except ConnectionException:
			print(url, "seems to be down")

		return False

	@property
	def url(self) -> str:
		return self.link

	@url.setter
	def url(self, url: str) -> None:
		self.link=url
		self.urlp=urlparse(url)

	def download(self, url: str) -> None:
		if self.allowed(url):
			self.raw=self.req.get(url).content
			self.soup=BeautifulSoup(self.raw, "html.parser")

	def xpath(self, html: str, xp: str) -> List[Any]:
		return cast(List[Any], lxmlhtml.fromstring(html).xpath(xp))

	def select(self, html: Any, json: Dict) -> List[str]:
		xpath=json.get("xpath", "")
		css=json.get("css", "")

		if xpath:
			found=self.xpath(html.getText(), xpath)

		elif css:
			found=html.select(css)

		if self.config["header"]:
			found=[found[0]]

		if css:
			completed=[]
			for item in found:
				output=[]

				contents=json["contents"]
				if type(contents) is str:
					contents=[contents]

				for content in contents:
					if content and item.has_attr(content):
						output.append(item[content])

					else:
						output.append(item.text)

				completed+=output

			return completed

		return found

	def clear(self) -> None:
		self.data=[]

	def load(self, index: int) -> None:
		config=self.configarr[index]

		if isinstance(config, Dict):
			self.config=config

		else:
			if os.path.exists(config):
				with open(config) as f:
					self.config=json.load(f)

		return None

	def grab(self, index: Optional[int]=None) -> None:
		if index is None:
			#using grab() with no params will grab all configs passed
			for i in range(len(self.configarr)):
				self.grab(i)

			return None

		self.load(index)
		if self.output:
			sc=simplecsv(self.output, mode="w+")
			if self.config["header"]:
				sc.writerow(self.config["header"])

		for json in self.config["links"]:
			links=[]
			if type(json["url"]) is str:
				links.append(json["url"])

			else:
				links=json["url"]

			done=[]
			for link in links:
				done+=explode(link)

			links=done

			for link in links:
				if not self.allowed(link):
					return None

				self.download(link)

				for divs in self.soup.select(json["container"]):
					data=[]
					for grab in json["grab"]:
						data+=self.select(divs, grab)

					self.data+=data
					if self.output:
						sc.writerow(data)

		if self.output:
			sc.close()