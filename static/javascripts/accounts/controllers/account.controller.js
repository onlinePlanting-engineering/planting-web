(function(){
  'use strict';

  angular
  .module('planting.accounts.controllers')
  .controller('AccountController', AccountController);

  AccountController.$inject = ['$locatioin', '$routeParams', 'Account', 'Snackbar'];

  function AccountController($location, $routeParams, Account, Snackbar){
    var vm = this;

    vm.account = undefined;

    activate();

    function activate() {
      var username = $routeParams.username.substr(1);

      Account.get(username).then(accountSuccessFn, accountErrorFn);

      function accountSuccessFn(data, status, headers, config){
        vm.account = data.data;
      }

      function accountErrorFn(data, status, headers, config){
        $location.url('/');
        Snackbar.error('该用户不存在!');
      }
    }

  }
})();
