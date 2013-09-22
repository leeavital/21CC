import MySQLdb
import MySQLdb.cursors
import re
from nltk.corpus import wordnet as wn
import copy
def main():
	db = MySQLdb.connect(host="ec2-54-219-48-12.us-west-1.compute.amazonaws.com",user="test_user",
						 passwd="mypass", cursorclass=MySQLdb.cursors.DictCursor, db = 'prod')
	cur = db.cursor()

	cur.execute("SELECT * FROM ingredients")

	a = cur.fetchall()
	removals = ['cubed', 'chopped', 'diced', '\d*', '\d\\\d', 'diced', 'tablespoons',
				'tablespoon', 'teaspoons', 'teaspoon', 'cups', 'cup', 'cold', 'hot',
				'ground', 'or to taste', 'to taste', 'optional', '(optional)',
				'lbs', 'pound', 'pounds', 'lb', 'large', 'small', 'pinch', 'lean',
				'ounces', 'ounce', ' oz ', 'package', 'trimmed', 'sliced', 'jar', 'shredded',
				'\((\w)*\)',r'/', '\(*','\)*', ' s ', '^ ', 'minced',',', 'bunch', 'cut into wedges',
				'packed', 'rinced', 'torn', 'cans', ' can ', '\.', 'fluid', '^s ','jigger','^ *',
				'cooked', 'uncooked',' raw ', 'inch', 'peeled', 'cored', 'washed', ' and ','beaten',
				'clove',' thin ', ' thick ', '-', 'seeded', 'boiling', ' into ', 'pieces',
				'for decoration', ' bite ','size','wrapped', 'unwrapped',' fine ',' finely',
				'coarse', 'coarsely','fresh', '( )*$', 'slice ', 'thinly', 'thickly', 
				'unflavored', 'flavored','grated','split','heavily', 'lightly','whole',
				'halved']
	es = []
	for elem in a:
		new = elem['name']
		#print elem['name']
		for removal in removals:
			new = re.sub(removal,"",new)
		for removal in removals:
			new = re.sub(removal,"",new)
		

		new = re.sub(' $','', new)

		new= re.sub('( )+','_', new)
		query = "SELECT * from strippedIngredients where name = '{0}'".format(new)
		cur.execute(query)
		row = cur.fetchone()
		if row == None:
			query = "INSERT into strippedIngredients (name, type, unstrippedID) VALUES ('{0}','{1}','{2}')".format(new,'None',elem['id'])
			cur.execute(query)
			cur.execute("COMMIT")
			query = "SELECT id, unstrippedID  from strippedIngredients where name = '{0}'".format(new)
			cur.execute(query)
			c = cur.fetchone()
			u = c['unstrippedID']
			s = c['id']
			query = "UPDATE ingredients SET strippedID = {0} where id = {1}".format(s, u)
			cur.execute(query)	
			cur.execute("COMMIT")
		else:

			query = "SELECT id from strippedIngredients where name = '{0}'".format(new)
			cur.execute(query)
			n = cur.fetchone()['id']	
			query = "UPDATE ingredients SET strippedID = {0} where id = {1}".format(n, elem['id'])
			cur.execute(query)	
			cur.execute("COMMIT")			


		es.append(elem['name'])
		# print  elem['name']

	ingSet = set(es)
	yes = 0.0
	no = 0
	for x in ingSet:
		pass
	# 	try:
	# 		s = wn.synsets(x)[0].hypernyms()[0]
	# 		print x + " -> " + str(s)
	# 		yes += 1
	# 	except:
	# 		no += 1
	# 		# print x + " -> " +"No definition"
	# print yes/(yes + no)



if __name__ == '__main__':
	main()