angular.module( 'deepLinking', [] ).
   config( ['$routeProvider', function( $routeProvider ) {
	  $routeProvider
		 .when( '/welcome', {templateUrl: 'welcome.html', controller: WelcomeCntl} )
		 .when( '/recipe/:recipeId', {templateUrl: 'recipe.html', controller: RecipeController} )
		 .when( '/recommendations', {templateUrl: 'recommendations.html', controller: RecommendationController} )
		 .when( '/users', {templateUrl: 'users.html', controller: UsersCntl} )
		 .when( '/training', {templateUrl: 'training.html', controller: TrainingCntl} );
   }]);



// ----------------------------------------------------------------------------
// 
// ----------------------------------------------------------------------------
function WelcomeCntl( $scope  ) {
    
}
WelcomeCntl.$inject = [ '$scope', '$location' ];




// ----------------------------------------------------------------------------
// AppCntl -- main driver for the app. Does nothing so far
// ----------------------------------------------------------------------------
function AppCntl(){

}
AppCntl.$inject = [ '$scope', '$location' ];





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
		 
		 if( response.status == "ok" ){
			alert( "successful login" );
			$location.path( '/welcome' );
		 }else{
			$scope.login_error = response.error;
		 }
	  } );
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
	  console.log( 'got recipes for training' );
	  console.log( recipes );
	  $scope.recipes = recipes;
   });


   $scope.rateRecipe = function( rId, rating ){
	  
	  $http.get( '/recipes/training/' + rId + '/' + rating )
		 .success( function(){
			alert( 'ok!' ); 		 	
		 });

   }
}
TrainingCntl.$inject = [ '$scope', '$http', '$location' ];
