
def build_net_for_user(uID, connection):
	from pybrain.tools.shortcuts import buildNetwork
	from pybrain.supervised.trainers import BackpropTrainer
	from pybrain.datasets import SupervisedDataSet
	cur = connection.cursor()
	query = "SELECT * from users WHERE id = %d"% uID
	print query
	cur.execute(query)
	user = cur.fetchone()
	print user

	net = buildNetwork(5, 10, 1, bias = True)

	ds = SupervisedDataSet(5, 1)

	ratedRecipesQuery  = "SELECT * from userratings where userid = %d" % uID 
	cur.execute(ratedRecipesQuery)
	ratedRecipes = cur.fetchall()
	
	ratedRecipes2 = []
	for x in ratedRecipes:
		ratedRecipes2.append(int(x['recipeid']))


	recipeQuery = "SELECT * FROM recipetocats where idrecipe in " + str(tuple(ratedRecipes2))
	print recipeQuery
	cur.execute(recipeQuery)

	recipes = cur.fetchall()


	for recipe in recipes:
		rating = 1
		print recipe
		scores = [recipe['Tangy'], recipe['Salty'], recipe['MSG'], .5, .5]
		ds.addSample(scores, rating)


	trainer = BackpropTrainer(net, ds)
	trainer.trainUntilConvergence()



	#activate!
	net.activate(None) #new recipe values