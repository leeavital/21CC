angular.module( 'deepLinking', [] ).
   config( ['$routeProvider', function( $routeProvider ) {
	  $routeProvider
		 .when( '/welcome', {templateUrl: 'welcome.html', controller: WelcomeCntl} )
		 .when( '/recipe/:recipeId', {templateUrl: 'recipe.html', controller: RecipeController} );
   } ] );


function WelcomeCntl( $scope  ) {
    
}

WelcomeCntl.$inject = [ '$scope', '$location' ];


function AppCntl(){

}

AppCntl.$inject = [ '$scope', '$location' ];


function RecipeController( $scope, $http, $routeParams ){
   
   $http.get( '/recipe/' + $routeParams.recipeId ).success( function( data ){
	  
	  $scope.recipe = data;
   
   });

}

RecipeController.$inject = [ '$scope', '$http', '$routeParams' ];
