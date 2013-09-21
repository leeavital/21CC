angular.module( 'deepLinking', [] ).
   config( ['$routeProvider', function( $routeProvider ) {
	  $routeProvider
		 .when( '/welcome', {templateUrl: 'welcome.html', controller: welcomeCtrl } );
   } ] );


function welcomeCtrl( $scope  ) {
    
}

WelcomeCntl.$inject = [ '$scope', '$location' ];


function AppCntl(){

}

AppCntl.$inject = [ '$scope', '$location' ];
