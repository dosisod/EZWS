from typing import Optional, List, Any, Dict, Union, TypeVar, cast
from reppy.cache import ReraiseExceptionPolicy, RobotsCache # type: ignore
from reppy.exceptions import ConnectionException # type: ignore
from lxml import html as lxmlhtml # type: ignore
from bs4 import BeautifulSoup # type: ignore
from itertools import chain
import requests
import json
import os

from ezws.simplecsv import simplecsv
from ezws.links import explode

import reppy # type: ignore
reppy.logger.setLevel("CRITICAL")

class EZWS:
	robo=RobotsCache(capacity=100, cache_policy=ReraiseExceptionPolicy(0))
	data: List[str]=[]

	"""
	SELF:

	config json config file
	ua     user agent
	robo   robotcache obj
	soup   current html page soup obj
	raw    raw html from req.get()
	check  check for robot files, keep true
	output name of output csv file
	"""
	def __init__(self, file: Union[str, Dict], ua: str="", check: bool=True, output: str="output.csv") -> None:
		self.ua=ua

		self.check=check

		#setting output to false disables file output
		self.output=output

		self.configarr=_listify(file)

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

	def download(self, url: str) -> Optional[Any]:
		if not self.allowed(url):
			return None

		self.raw=requests.get(url).content

		return BeautifulSoup(self.raw, "html.parser")

	def xpath(self, html: str, xp: str) -> List[Any]:
		return cast(List[Any], lxmlhtml.fromstring(html).xpath(xp))

	def select(self, html: Any, json: Dict) -> List[str]:
		xpath=json.get("xpath", "")
		css=json.get("css", "")

		if xpath:
			found=self.xpath(html.getText(), xpath)

			return [found[0]] if self.config["header"] else found

		#assume css was passed
		found=html.select(css)
		if self.config["header"]:
			found=[found[0]]

		completed=[]
		for item in found:
			output=[]

			contents=_listify(json["contents"])

			for content in contents:
				if content and item.has_attr(content):
					output.append(item[content])

				else:
					output.append(item.text)

			completed+=output

		return completed

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
			for link in chain(*[ explode(link) for link in _listify(json["urls"]) ]):
				if not self.allowed(link):
					return None

				soup=self.download(link)
				if not soup:
					print("could not download file")
					return None

				for divs in soup.select(json["container"]):
					data=[]
					for grab in json["grab"]:
						data+=self.select(divs, grab)

					self.data+=data
					if self.output:
						sc.writerow(data)

		if self.output:
			sc.close()

T=TypeVar("T")
def _listify(obj: T) -> List[T]:
	if isinstance(obj, List):
		return obj

	return [obj]