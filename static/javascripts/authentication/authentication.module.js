(function(){
  'use strict';

  angular.module('planting.authentication', [
    'planting.authentication.services',
    'planting.authentication.controllers'
  ]);

  angular.module('planting.authentication.services', ['ngCookies']);

  angular.module('planting.authentication.controllers', []);
})();
