import itertools
import re

from typing import List

#given a url with {{}} numbering, explode (enumerate) all possible links
def explode(url: str) -> List[str]:
	matches=re.findall(r"\{\{(.[^\{\}]*?\|.*?|[0-9]+\-[0-9]+(?:,[0-9]+)?)\}\}", url)
	splited=re.split(r"\{\{.*?\}\}", url)

	if matches!=[] and len(splited) > len(matches):
		done=[]
		for combo in itertools.product(*[parse(p) for p in matches]):
			tmp=""
			for index, val in enumerate(combo):
				tmp+=splited[index] + val

			tmp+=splited[-1]

			done.append(tmp)

		return done

	#url is not syntaxed, put it in an array then return it
	return [url]

def parse(expr: str) -> List[str]:
	if "|" in expr:
		return expr.split("|")

	#parse expr into start, end, step vars
	num=expr.split("-")
	num[1]=num[1].split(",") # type: ignore

	return [str(n) for n in range(
		int(num[0]),
		int(num[1][0]),
		1 if len(num[1])==1 else int(num[1][1])
	)]
