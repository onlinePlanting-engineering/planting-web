(function(){
  'use strict';

  angular.module('planting', [
    'planting.config',
    'planting.routes',
    'planting.authentication',
    'planting.layout',
    'planting.utils'
  ]);

  angular.module('planting.config', []);
  angular.module('planting.routes', ['ngRoute']);

  angular
  .module('planting')
  .run(run);

  run.$inject = ['$http'];

  // Update xsrf $http header to align with Django's defaults
  function run($http){
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken'
  }

})();
