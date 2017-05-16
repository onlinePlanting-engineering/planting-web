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
      logout: logout
    };

    return Authentication;

    function login(username, password){
      return $http.post('/api/v1/auth/login/', {
        username: username,
        password: password
      }).then(loginSuccessFn, loginErrorFn);

      function loginSuccessFn(data, status, headers, config){
        Authentication.setAuthenticatedAccount(data.data);

        windows.location = '/';
      }

      function loginErrorFn(data, status, headers, config){
        console.log('Login failure!');
      }
    }

    function logout(){
      return $http.post('/api/v1/auth/logout/').then(
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
        console.log('Register failure!');
      }
    }

    function getAuthenticateAccount(){
      if(!$cookies.authenticatedAccount){
        return;
      }
      return JSON.parse($cookies.authenticatedAccount);
    }

    function isAuthenticated(){
      return !!$cookies.authenticatedAccount;
    }

    function setAuthenticatedAccount(account){
      $cookies.authenticatedAccount = JSON.stringify(account);
    }

    function unauthenticate(){
      delete $cookies.authenticatedAccount;
    }
  }
})();
