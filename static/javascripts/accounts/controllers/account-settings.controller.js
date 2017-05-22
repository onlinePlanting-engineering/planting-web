(function(){
  'use strict';

  angular
  .module('planting.accounts.controllers')
  .controller('AccountSettingsController', AccountSettingsController);

  AccountSettingsController.$inject = [
    '$location', '$routeParams', 'Authentication', 'Account', 'Snackbar'
  ];

  function AccountSettingsController($location, $routeParams, Authentication, Account, Snackbar){
    var vm = this;

    vm.destroy = destroy;
    vm.update = update;

    vm.genders = [
      {"name": "男", "code": "M"},
      {"name": "女", "code": "F"}
    ];

    activate();

    function activate(){
      var authenticatedAccount = Authentication.getAuthenticateAccount();
      var username = $routeParams.username.substr(1);

      if(!authenticatedAccount){
        $location.url('/');
        Snackbar.error('您未授权');
      } else {
        if (authenticatedAccount.username !== username){
          // debugger;
          $location.url('/');
          Snackbar.error(('您未授权'));
        }
      }

      Account.get(username).then(accountSuccessFn, accountErrorFn);

      function accountErrorFn(data, status, headers, config){
        $location.url('/');
        Snackbar.error('该用户不存在');
      }

      function accountSuccessFn(data, status, headers, config){
        vm.account = data.data.data;
      }

    }

    function destroy(){
      Account.destroy(vm.account.username).then(accountSuccessFn, accountErrorFn);

      function accountSuccessFn(data, status, headers, config){
        Authentication.unauthenticate();
        window.location('/');
        Snackbar.show('您的账号已被删除');
      }

      function accountErrorFn(data, status, headers, conifg){
        Snackbar.error(data.error)
      }
    }

    function update(){
      var username = $routeParams.username.substr(1);

      if (!!vm.account.profile.img_heading) {
        delete vm.account.profile.img_heading;
      }
      // Process for image heading
      if (vm.files.length > 0) {
        var img_heading = vm.files[0];
        if (!img_heading.isRemote) {
          vm.account.profile.img_heading = img_heading.lfFile;
        }
      }

      Account.update(username, vm.account).then(accountSuccessFn, accountErrorFn);

      /**
       * @name accountSuccessFn
       * @desc Show success snackbar
       */
      function accountSuccessFn(data, status, headers, config) {
        Snackbar.show('您的账户已更新！');
      }


      /**
       * @name accountErrorFn
       * @desc Show error snackbar
       */
      function accountErrorFn(data, status, headers, config) {
        console.log('更新失败!', data.data);
        Snackbar.error(data.data);
      }
    }

  }
})();
