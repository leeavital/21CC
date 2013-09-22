angular.module('deepLinking', ['ngAnimate']);


angular.module( 'deepLinking', [] ).
   config( ['$routeProvider', function( $routeProvider ) {
	  $routeProvider
		 .when( '/welcome', {templateUrl: '/static/welcome.html', controller: WelcomeCntl} )
		 .when( '/recipe/:recipeId', {templateUrl: '/static/recipe.html', controller: RecipeController} )
		 .when( '/recommendations', {templateUrl: '/static/recommendations.html', controller: RecommendationController} )
		 .when( '/users', {templateUrl: '/static/users.html', controller: UsersCntl} )
		 .when( '/training', {templateUrl: '/static/training.html', controller: TrainingCntl} )
		 .when( '/home', {templateUrl: '/static/home.html', controller: HomeCntl} );
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
function AppCntl( $scope, $location, $http ){
   
   $http.get( '/current_user' ).success( function( data, status, headers ){

	  console.log( status );
	  console.log( data );
	  console.log( 'success' ); 
	  $location.path( '/home' );

   }).error( function(){
	  console.log( 'error' );
	  $location.path( '/users' );
   });
   
}
AppCntl.$inject = [ '$scope', '$location', '$http' ];





// ----------------------------------------------------------------------------
// RecipeController -- displays a given recipe
// ----------------------------------------------------------------------------
function RecipeController( $scope, $http, $routeParams ){
   
   $http.get( '/recipe/' + $routeParams.recipeId ).success( function( data ){
	  
	  $scope.recipe = data;
   
   });

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
function UsersCntl( $scope, $http, $location){
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
			$scope.current_user = loginName
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
UsersCntl.$inject = [ '$scope', '$http', '$location' ];



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
	  } );

	  console.log( toShow );

   }
   
   // populate recomendations
   $http.get( '/recipes/recommendations' ).success( function( recs ){
	  
	  console.log( recs );
	  $scope.recommendations = recs;  


   });
   

} // ent ctlt
HomeCntl.$inject = [ '$scope', '$http', '$location' ];
