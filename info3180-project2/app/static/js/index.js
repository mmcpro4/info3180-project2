
/*global angular*/
(function(){
    "use strict";
    
    angular
        .module('wishingApp', ['ngRoute']) 
            .config(function($routeProvider){
        	    $routeProvider
        	        .when('/add', {
        	            templateUrl: 'static/partials/add_wish.html',
        	            controller: 'Master'
        	        })
					.when('/logout', {
        	            templateUrl: 'static/partials/logout.html',
        	            controller: 'Master',
        	        })
        	        .when('/share', {
        	            templateUrl: 'static/partials/sendemail.html',
        	            controller: 'Master'
        	        })
        	        
        	        .when('/login', {
        	            templateUrl: 'static/partials/login.html',
        	            controller: 'Master'
        	        })
        	        .when('/signup', {
        	            templateUrl: 'static/partials/signup.html',
        	            controller: 'Master'
        	        })
        	        .when('/wishList/:userid', {
        	            templateUrl: 'static/partials/swishlst.html',
        	            controller: 'Master'
        	        })
        	        .when('/wishList', {
        	            templateUrl: 'static/partials/wishlst.html',
        	            controller: 'Master'
        	         })
        	        .otherwise( { 
        	            redirectTo:'/home',
        	            templateUrl: 'static/partials/index.html',
        	            controller: 'Master'
        	        });
        	}
	);
});
	




