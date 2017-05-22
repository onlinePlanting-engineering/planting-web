(function(){
  'use strict';

  angular
  .module('planting.authentication.services')
  .factory('Authentication', Authentication);

  Authentication.$inject = ['$cookies', '$http'];

  function Authentication($cookies, $http){
    var Authentication = {
      register: register,
      login: login,
      logout: logout,
      unauthenticate: unauthenticate,
      getAuthenticateAccount: getAuthenticateAccount,
      isAuthenticated: isAuthenticated,
      setAuthenticatedAccount: setAuthenticatedAccount
    };

    return Authentication;

    function getAuthenticateAccount(){
      if(!$cookies.get('authenticatedAccount')){
        return;
      }
      return JSON.parse($cookies.get('authenticatedAccount'));
    }

    function isAuthenticated(){
      return !!$cookies.get('authenticatedAccount');
    }

    function setAuthenticatedAccount(account){
      $cookies.put('authenticatedAccount', JSON.stringify(account));
    }

    function unauthenticate(){
      delete $cookies.remove('authenticatedAccount');
    }

    function login(username, password){
      return $http.post('/api/v1/accounts/login/', {
        username: username,
        password: password
      }).then(loginSuccessFn, loginErrorFn);

      function loginSuccessFn(data, status, headers, config){
        Authentication.setAuthenticatedAccount(data.data.data);

        window.location = '/';
      }

      function loginErrorFn(data, status, headers, config){
        console.log('登入失败!', data.data);
      }
    }

    function logout(){
      return $http.get('/api/v1/accounts/logout/').then(
        logoutSuccessFn, logoutErrorFn
      );

      function logoutSuccessFn(data, status, headers, config){
        Authentication.unauthenticate();

        window.location = '/';
      }

      function logoutErrorFn(data, status, headers, config){
        console.error('logout failure!');
      }
    }

    function register(username, password){
      return $http.post('/api/v1/accounts/register/', {
        username: username,
        password: password
      }).then(registerSuccessFn, registerErrorFn);

      function registerSuccessFn(data, status, headers, config){
        Authentication.login(username, password);
      }

      function registerErrorFn(data, status, headers, config){
        console.log('注册失败!', data.data);
      }
    }


  }
})();
