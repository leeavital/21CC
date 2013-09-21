from yummly import Client

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
				print recipe
				process(match)








def process(recipe):
	print 'Recipe ID:', recipe.id
	print 'Recipe:', recipe.name
	print 'Rating:', recipe.rating
	print 'Total Time:', recipe.totalTime
	print 'Yields:', recipe.yields
	print 'Ingredients:'
	for ingred in recipe.ingredientLines:
		print ingred
	for flavor in recipe.flavors:
			print flavor + ": "+str(recipe.flavors[flavor])
	db = MySQLdb.connect(host="ec2-54-219-48-12.us-west-1.compute.amazonaws.com",user="test_user",passwd="mypass",db="prod", cursorclass=MySQLdb.cursors.DictCursor)
	cur = db.cursor()
	#import tammys thing here
	description = get_description(recipe.source['sourceRecipeUrl'])
	cur.execute("INSERT INTO recipes (name,votes,salty,sweet,spicy,savory,bitter,cuisine, meal, sour) VALUES ('{0}','0','{1}','{2}','{3}','{4}','{5}','{6}', 'MAIN', '{7}')".format(recipe.name,recipe.flavors['Salty'],recipe.flavors['Sweet'],recipe.flavors['Piquant'],recipe.flavors['Meaty'],recipe.flavors['Bitter'],recipe.Attributes['Cuisine'][0], recipe.flavors['Sour'] ))
	recipeidnum = cur.execute("SELECT id FROM recipes WHERE name = '{0}'".format(recipe.name))
	for ingred in recipe:
		food = ingred.split(' ')
		ingredeintname = " ".join(food[1::])
		cur.execute("SELECT COUNT FROM ingredients WHERE name = '{0}'".format(ingredientname))
		ispresent = cur.fetchone()
		if(ispresent <= 0):
			cur.execute("INSERT INTO ingredients (name, type) VALUES ('{0}', FOOD)".format(ingredientname))
		ingredidnum = cur.execute("SELECT id FROM ingredients WHERE name = '{0}'".format(ingredientname))
		cur.execute("INSERT INTO recipecombo (recipeid,ingredientid, amount) VALUES ('{0}','{1}','{2}')".format(recipeidnum,ingredidnum,food[0:1]))
   
if __name__ == "__main__":
		main()