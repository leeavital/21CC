from yummly import Client
import MySQLdb
import MySQLdb.cursors

def main():

	# default option values
	TIMEOUT = 5.0
	RETRIES = 0

	client = Client(api_id="2ecbff5a", api_key="a9e2794b097d6dfc3fef2e3afd81123e", timeout=TIMEOUT, retries=RETRIES)

	keywords = {
		'chicken': 30,
		'eggs': 10,
		'beef': 30,
		'middle eastern': 30,
		'italian': 30,
		'chinese': 30,
		'cookie': 10,
		'cake': 15,
		'pasta': 15,
		'pizza': 10,
		'roasted': 20
		}
	for keyword in keywords.keys():
		print keyword
		results = client.search(keyword, maxResults=keywords[keyword])

		for match in results.matches:
			if match.sourceDisplayName== "AllRecipes":
				recipe = client.recipe(match.id)
				import pprint
				pprint.pformat(recipe, indent = 4)
				process(recipe)








def process(recipe):
	print 'Recipe ID:', recipe.id
	print 'Recipe:', recipe["name"]
	# print 'Rating:', recipe.rating
	# print 'Total Time:', recipe.totalTime
	# print 'Yields:', recipe.yields
	# print 'Ingredients:'
	# for ingred in recipe.ingredientLines:
	# 	print ingred
	# for flavor in recipe.flavors:
	# 		print flavor + ": "+str(recipe.flavors[flavor])
	db = MySQLdb.connect(host="ec2-54-219-48-12.us-west-1.compute.amazonaws.com",user="test_user",passwd="mypass",db="prod", cursorclass=MySQLdb.cursors.DictCursor)
	cur = db.cursor()
	description = "YUM"
	# description = get_description(recipe.source['sourceRecipeUrl'])
	cur.execute("INSERT INTO recipes (name,votes,salty,sweet,spicy,savory,filling,cuisine, meal, sour) VALUES ('{0}','0','{1}','{2}','{3}','{4}','{5}','{6}', 'MAIN', '{7}')".format(recipe.name,recipe.flavors.salty,recipe.flavors.sweet,recipe.flavors.piquant,recipe.flavors.meaty,recipe.flavors.bitter,recipe.attributes['cuisine'][0], recipe.flavors.sour ))
	cur.execute("SELECT id FROM recipes WHERE name = '{0}'".format(recipe.name))
	recipeidnum = cur.fetchone()
	recipeidnum = recipeidnum['id']
	print recipeidnum
	print "RID NUM: "+ str(recipeidnum)
	for ingred in recipe.ingredientLines:
		print ingred
		food = ingred.split(' ')
		ingredientname = " ".join(food[1:])
		print ingredientname
		cur.execute("SELECT COUNT(*) FROM ingredients WHERE name = '{0}'".format(ingredientname))
		ispresent = cur.fetchone()
		print "ISPRESENT: " + str(ispresent)
		if(ispresent['COUNT(*)'] == 0):
			print "ADDING ING"
			cur.execute("INSERT INTO ingredients (name, type) VALUES ('{0}', 'FOOD')".format(ingredientname))
		cur.execute("COMMIT")
		cur.execute("SELECT id FROM ingredients WHERE name = '{0}'".format(ingredientname))
		ingredidnum = cur.fetchone()
		print "ING NUM: " + str(ingredidnum)
		cur.execute("INSERT INTO recipecombo (recipeid,ingredientid, amount) VALUES ('{0}','{1}','{2}')".format(str(recipeidnum),int(ingredidnum['id']),str(food[0])))
		cur.execute("COMMIT")

if __name__ == "__main__":
		main()