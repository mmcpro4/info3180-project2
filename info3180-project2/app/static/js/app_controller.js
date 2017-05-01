(function(){
    "use strict";
    
    angular
        .module('wishingApp') //Accesses the angular module wishListApp
            .controller('Master', Master); //Controller for wishListApp created
        
    Master.$inject = ['$http', '$scope', '$location', '$window', '$route'];
   
    function Master($http, $scope, $location, $window, $route){
        
        var login= false;
        var person_name = ""
        this.login = function(){
            $http({
                url: 'api/users/login',
                method: "POST",
                data: { 'email' :$scope.email,'pword':$scope.password }
            })
            .then(function(response) {
                if(response.info){
                    $window.alert(response.message); 
                    $window.localStorage.setItem('uid', response.info.uid);
                    login=true;
                    person_name =data.email
                    this.Route('wishList');
                    }
                else{
                    this.login.message = "Something went wrong on our end please give us a moment";
                    $window.alert(this.login.message);
                    this.Route('/login')
                }
            });
        };
            
        this.logout = function(){
           
            if (login){
                $window.alert("You have been logged out");
                login=false;
                this.Route('/logout');
            }
            else
            {
                // Alert user
                $window.alert("You're not logged in.");
            }
            
        };
        
        // Share funtion
        this.share = function(){
            
            
            var emails = {
                email1: this.share.email1,
                email2: this.share.email2,
                email3: this.share.email3
            };
            var uid=$window.localStorage.getItem('uid');
            $http({
                url: 'api/users/' + uid + '/swishlist',
                method: "POST",
                data: { 'emails' :emails }
            })
            .then(function(response) {
                if(response.info){
                    this.sent.emails = response.info["persons"];
                    $window.alert(this.sent.emails);
                    }
                else{
                    this.sent.message = "Something went wrong on our end please give us a moment";
                        $window.alert(this.sent.message);
                }
            });
            
            
        };
        
        
        this.register = function(){
            var info = {
                email: this.register.email,
                name: this.register.name,
                pword: this.register.pword,
                age: this.register.age,
                sex: this.register.sex,
            };
            
            $http({
                url: 'api/users/register',
                method: "POST",
                data: { 'info' :info }
            })
            .then(function(response) {
                if(response.info){
                    $window.alert('You have been successfully registered');
                    this.Route('home');
                    }
                else{
                    this.sent.message = "Something went wrong on our end please give us a moment";
                    $window.alert(this.sent.message);
                }
            });
            
        }; 
        this.isauthorized = function(){
                return login;
            }
            
        };
        
        this.getWishList = function(){
            // Check for local storage stuff
            var uid=$window.localStorage.getItem('uid');
            
            $http({
                url: 'api/users/' + uid + '/wishlist',
                method: "GET",
            })
            .then(function(response) {
                if(response.info){
                    this.wishes.stuff = response.info["wishes"];
                    if this.wishes.stuff.length !=0:
                    {
                    $window.alert("Everything went ok we found your wishes");
                    }
                
                else{
                    this.sent.message = "Something went wrong on our end please give us a moment";
                        $window.alert(this.sent.message);
                    }
                }
            });
        };
        
        
        this.postwish = function(){
           var uid=$window.localStorage.getItem('uid');
           var info = {
                name: this.add.name,
                description: this.add.description_,
                url: this.add.url,
                thumbnail: $scope.thumbnail;
            };
            
            $http({
                url: 'api/users/' + uid + '/wishlist',
                method: "POST",
                data: { 'info' :info }
            })
            .then(function(response) {
                if(response.info){
                    this.wishes.stuff = response.info["info"];
                    $window.alert("Everything went ok we found your wishes");
                    this.Route('wishList')
                    }
                else{
                    this.sent.message = "Something went wrong on our end please give us a moment";
                        $window.alert(this.sent.message);
                    }
                }
            );
        };
        
        this.delete = function(){
            var uid = $window.localStorage.getItem('uid');
            var pid = this.delwish.pid;
            
            $http({
                url: 'api/users/' + uid + '/wishlist/' + str(pid),
                method: "DELETE"
            })
            .then(function(response) {
                if(response.info){
                    this.wish.stuff = response.info["info"];
                    $window.alert("Everything went ok we deleted your wish");
                    $route.reload();
                    }
                else{
                    this.sent.message = "Something went wrong on our end please give us a moment";
                    $window.alert(this.sent.message);
                    }
                }
            );
        }; 
        
         this.Routing = function(route){
	        $location.path(route);
            };
            
        };
        
    }
}());