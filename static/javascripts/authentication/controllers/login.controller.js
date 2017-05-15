(function(){
  'use strict';

  angular
  .module('planting.authentication.controllers')
  .controller('LoginController', LoginController);

  function LoginController($location, $scope, Authentication){
    var vm = this;
    vm.login = login;

    activate();

    function activate(){
      // If the user is authenticated, he should not be here
      if(Authentication.isAuthenticated){
        $location.url('/');
      }
    }

    function login(){
      Authentication.login(vm.username, vm.password);
    }
  }
})();
