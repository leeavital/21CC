from yummly import Client

def main():
	
	# default option values
	TIMEOUT = 5.0
	RETRIES = 0

	client = Client(api_id="2ecbff5a", api_key="a9e2794b097d6dfc3fef2e3afd81123e", timeout=TIMEOUT, retries=RETRIES)





	search = client.search('eggs')
	match = search.matches[0]

	recipe = client.recipe(match.id)

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

if __name__ == "__main__":
	main()