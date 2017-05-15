(function(){
  'use strict';

  angular
  .module('planting.authentication.controllers')
  .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$location', '$scope', 'Authentication'];

  function RegisterController($location, $scope, Authentication){
    var vm = this;
    vm.register = register;
    activate();

    function activate(){
      // If the user is authenticated, he should not be here
      if(Authentication.isAuthenticated){
        $location.url('/');
      }
    }

    function register(){
      Authentication.register(vm.username, vm.password);
    }

  }
})();
