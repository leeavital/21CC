
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
	
	ratedRecipes2 = {}
	for x in ratedRecipes:
		print x
		ratedRecipes2[int(x['recipeid'])] = x['score']/10.0

	recipeQuery = "SELECT * FROM recipes where id in " + str(tuple(ratedRecipes2.keys()))
	print recipeQuery
	cur.execute(recipeQuery)

	recipes = cur.fetchall()


	for recipe in recipes:
		print "RECIPE IS: "+str(recipe)
		rating = ratedRecipes2[recipe['id']]
		print recipe
		scores = [recipe['salty'], recipe['sweet'], recipe['spicy'], recipe['savory'], recipe['filling']]
		ds.addSample(scores, rating)

	print ds
	trainer = BackpropTrainer(net, ds)


	#activate!
	xs = 0
	for x in range(10):
		trainer.trainUntilConvergence(maxEpochs=100)

		x = net.activate([10,3,7,8,10]) #new recipe values
		y = net.activate([0,9,1,2,1]) #new recipe values
		if x > y:
			xs += 1



	return str(xs)
	return Recipe