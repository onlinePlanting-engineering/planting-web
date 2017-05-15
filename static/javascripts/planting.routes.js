(function(){
  'use strict';

  angular
  .module('planting.routes')
  .config(config);

  config.$inject = ['$routeProvider'];

  function config($routeProvider){
    $routeProvider
    .when('/', {
      controller: 'IndexController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/layout/index.html'
    })
    .when('/register', {
      controller: 'RegisterController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/layout/register.html'
    }).otherwise('/');
  }
})();
