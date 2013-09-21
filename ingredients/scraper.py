import urllib2
from bs4 import BeautifulSoup
response = urllib2.urlopen('http://allrecipes.com/search/default.aspx?qt=k&wt=cornbread&rt=r&origin=Home%20Page')
html = response.read()
soup = BeautifulSoup(html)
for link in soup.find_all("a"):
	url =link.get('href')
	if(url == None):
		print('none')
	elif (url.find("http")!= -1):
		print(link.get('href'))


