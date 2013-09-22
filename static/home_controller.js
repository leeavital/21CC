angular.module('deepLinking', ['ngAnimate']);


angular.module( 'deepLinking', [] ).
   config( ['$routeProvider', function( $routeProvider ) {
	  $routeProvider
		 .when( '/welcome', {templateUrl: '/static/welcome.html', controller: WelcomeCntl} )
		 .when( '/recipe/:recipeId', {templateUrl: '/static/recipe.html', controller: RecipeController} )
		 .when( '/recommendations', {templateUrl: '/static/recommendations.html', controller: RecommendationController} )
		 .when( '/users', {templateUrl: '/static/users.html', controller: UsersCntl} )
		 .when( '/training', {templateUrl: '/static/training.html', controller: TrainingCntl} )
		 .when( '/home', {templateUrl: '/static/home.html', controller: HomeCntl} )
		 .when( '/recipes/:recipesIds', {templateUrl: '/static/recipes.html', controller: RecipesController} );
   }]);



// ----------------------------------------------------------------------------
// 
// ----------------------------------------------------------------------------
function WelcomeCntl( $scope, $location  ) {
       
}
WelcomeCntl.$inject = [ '$scope', '$location' ];




// ----------------------------------------------------------------------------
// AppCntl -- main driver for the app. Does nothing so far
// ----------------------------------------------------------------------------
function AppCntl( $scope, $location, $http, $rootScope ){
   
   $http.get( '/current_user' ).success( function( data, status, headers ){
	 
	  $rootScope.current_user = data.username;
	  
	  if( $location.path() == '' ){
		 $location.path( '/home' );
		 console.log( $rootScope );

	  }else{
		 // use whatever the user specified
	  }

   }).error( function(){
	  $location.path( '/users' );
   });
   
}
AppCntl.$inject = [ '$scope', '$location', '$http', '$rootScope' ];





// ----------------------------------------------------------------------------
// RecipeController -- displays a given recipe
// ----------------------------------------------------------------------------
function RecipeController( $scope, $http, $routeParams ){
   
   
   $scope.rated = false;
    
   $http.get( '/recipe/' + $routeParams.recipeId ).success( function( data ){
	  console.log( data );	  
	  $scope.recipe = data;
   
   });


   $scope.rateRecipe = function( rId, rating ){
	  // assume it's going to work
	  $http.get( '/recipes/training/' + rId + '/' + rating );
	  $scope.rated = true;
   }

}
RecipeController.$inject = [ '$scope', '$http', '$routeParams' ];




// ----------------------------------------------------------------------------
// RecommendationController -- Displays a list of 
// ----------------------------------------------------------------------------
function RecommendationController( $scope, $http, $routeParams ){ 
   $http.get( '/recommendations' ).success( function( recs ){
	  $scope.recommendations = recs;
   }); 
}
RecommendationController.$inject = [ '$scope', '$http', '$routeParams' ];


// ----------------------------------------------------------------------------
// UserCntl
// ----------------------------------------------------------------------------
function UsersCntl( $scope, $http, $location, $rootScope){
   $scope.doLogin = function(){
	  var  loginName = $scope.login_name;
	  var loginPword = $scope.login_pass;
	  
	  $http( {
		 url: '/login',
		 data:{
			username: loginName,
		 	password: loginPword
		 },
		 method: 'POST'
	  }).success( function( response ){
			$location.path( '/home' );
			$rootScope.current_user = loginName;
	  } ).error( function( response ){
			$scope.login_error = response.error;
	  });
   }


   $scope.doSignUp = function(){
	  var name = $scope.signup_name
	  var pass = $scope.signup_pass
	  var pass2 = $scope.signup_pass2

	  if( pass != pass2 ){
		 $scope.sign_up_error = 'passwords do not match';	 
	  }
	  else{
		 $http.post( '/user_create', {
			username: name,
			password: pass	
		 } ).success( function( data ){
			$location.path( '/training' );
		 })
	  }
	  
	   
   }
}
UsersCntl.$inject = [ '$scope', '$http', '$location', '$rootScope' ];



// ----------------------------------------------------------------------------
// TrainingCntl
// ----------------------------------------------------------------------------
function TrainingCntl( $scope, $http, $location ) {

   $http.get( '/recipes/training' ).success( function( recipes ){
	  
	  for( var r in recipes ){
		 recipes[r].trained = false;
	  }
	  
	  $scope.recipes = recipes;
   });
   

   $scope.rateRecipe = function( rId, rating ){
	  // assume it's going to work
	  $http.get( '/recipes/training/' + rId + '/' + rating );

	  // now remove from the list
	  $scope.recipes = $scope.recipes.filter( function( r ){
		 return r.id != rId;
	  } );
   }
}
TrainingCntl.$inject = [ '$scope', '$http', '$location' ];





// ----------------------------------------------------------------------------
// Home Controller
// ----------------------------------------------------------------------------
function HomeCntl( $scope, $http, $location ){
   
   
    
   // populate inventory 
   $http.get( '/inventory' ).success( function( data ) {
	  console.log( 'got inventory' );
	  $scope.inventory = data;
   });

   $scope.addToInventory = function( item ){
	  
	  $scope.inventory.push({item: item} );
	  $scope.new_inventory = '';
	  $http.put( '/inventory', item ).success( function( ){
		  
		  
	  });
   }

   $scope.removeItem = function( itemname ){
	  $http.get( '/inventory/delete/' +  itemname ).success( function(){
		 // it was actually deleted...
	  });
	  
	  $scope.inventory = $scope.inventory.filter( function(inv){
		 return inv.item != itemname;
	  });
   }	  

   $scope.showRecipes = function(){
	  var toShow = $scope.recommendations.filter( function( e ) {
		 return e.selected;
	  } ).map( function( e ) { return e.id } );

	  
	  var url = toShow.join( '+' );
	  $location.path( '/recipes/' + url );
   
   }
   
   // populate recomendations
   $http.get( '/recipes/recommendations' ).success( function( recs ){
	  
	  console.log( recs );
	  $scope.recommendations = recs;  


   });
   

} // ent ctlt
HomeCntl.$inject = [ '$scope', '$http', '$location' ];




function RecipesController( $scope, $http ){

}
RecipesController.$inject = ['$scope', '$http' ];
