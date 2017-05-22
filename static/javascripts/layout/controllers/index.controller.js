(function(){
  'use strict';

  angular
  .module('planting.layout.controllers')
  .controller('IndexController', IndexController);

  IndexController.$inject = ['$scope', 'Authentication', 'Snackbar'];

  function IndexController($scope, Authentication, Snackbar){
    var vm = this;

    vm.isAuthenticated = Authentication.isAuthenticated();

    activate();

    function activate(){
      console.log("Is Authenticated: ", vm.isAuthenticated);
    }

  }
})();
