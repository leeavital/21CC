
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

	net = buildNetwork(6, 10, 1, bias = True, learningrate=0.03, lrdecay = .99)


	ds = SupervisedDataSet(6, 1)

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
		scores = [recipe['Salty'], recipe['Meaty'], recipe['Piquant'] , recipe['Bitter'], recipe['Sour'], recipe['Sweet']]
		ds.addSample(scores, rating)

	print ds
	
	trainer = BackpropTrainer(net, ds)

	print trainer.trainUntilConvergence(maxEpochs = 1000)

	x = net.activate([7,2,1,3,3])
	y = net.activate([6,2,10,3,1])

	print str(x)
	return str(x > y)