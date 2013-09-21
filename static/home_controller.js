angular.module( 'deepLinking', [] ).
   config( ['$routeProvider', function( $routeProvider ) {
	  $routeProvider
		 .when( '/welcome', {templateUrl: 'welcome.html', controller: WelcomeCntl} )
		 .when( '/recipe/:recipeId', {templateUrl: 'recipe.html', controller: RecipeController} )
		 .when( '/recommendations', {templateUrl: 'recommendations.html', controller: RecommendationController} )
		 .when( '/users', {templateUrl: 'users.html', controller: UsersCntl} );
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
function UsersCntl( $scope, $http){
   $scope.doLogin = function(){
	  var  loginName = $scope.login_name;
	  var loginPword = $scope.login_pass;
	  console.log( 'logging in... ' );
   }


   $scope.doSignUp = function(){
   }
}
UsersCntl.$inject = [ '$scope', '$http' ];

