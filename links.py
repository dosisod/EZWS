import re

#given a url with {{}} numbering, explode (enumerate) all possible links
def explode(url):
	matches=re.findall(r"\{\{[0-9]+\-[0-9]+\}\}", url)
	splited=re.split(r"\{\{.*?\}\}", url)

	if matches!=[] and len(splited)>len(matches):
		fragments=[] #2d array of each param enumeration
		for param in matches:
			param=param[2:-2] #strip the "{{}}" characters off

			tmp=param.split("-")
			start=int(tmp[0])
			end=int(tmp[1])

			current=[] #current fragments
			for n in range(end-start):
				current.append(start+n) #build out fragments

			fragments.append(current)

		max=1
		for frag in fragments: #find the number of links needed
			max*=len(frag)

		done=[]
		for i in range(max):
			tmp=""
			for j in range(len(fragments)):
				#create the link and all of its needed parts
				tmp=splited[j]+str(fragments[j][i%len(fragments[j])])

			done.append(tmp+splited[-1])

		return done

	else:
		#url is not syntaxed, put it in an arrya then return it
		return [url]
