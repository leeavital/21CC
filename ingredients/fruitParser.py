import re
def main():
	 f = open("fruits")
	 fw = open('fruitsParsed', 'w')
	 r = "<span id=\"(\w*)\""
	 for line in f:
	 	matches = re.search(r, line)
	 	if matches is not None:
	 		fw.write(matches.group(1) + "\n")



if __name__ == '__main__':
	main()