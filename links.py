import itertools
import re

#given a url with {{}} numbering, explode (enumerate) all possible links
def explode(url):
	matches=re.findall(r"\{\{(.[^\{\}]*?\|.*?|[0-9]+\-[0-9]+)\}\}", url)
	splited=re.split(r"\{\{.*?\}\}", url)

	if matches!=[] and len(splited)>len(matches):
		fragments=[] #2d array of each param enumeration
		for param in matches:
			fragments.append(parse(param))

		#create all possible combos from given lists
		combos=list(itertools.product(*fragments))

		done=[]
		for combo in combos:
			tmp=""
			for index, val in enumerate(combo):
				tmp+=splited[index]+str(val)

			tmp+=splited[-1]

			done.append(tmp)

		return done

	else:
		#url is not syntaxed, put it in an arrya then return it
		return [url]

#given a single {{}} expression, auto identify the possible combos
def parse(expr):
	if "|" in expr: #string array representation
		return expr.split("|")

	else: #number range representation
		tmp=expr.split("-")
		start=int(tmp[0])
		end=int(tmp[1])

		current=[]
		for n in range(end-start):
			current.append(start+n) #build out fragments from starting point to end

		return current
