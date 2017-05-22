(function () {
  'use strict';

  angular
    .module('planting.accounts', [
      'planting.accounts.controllers',
      'planting.accounts.services'
    ]);

  angular
    .module('planting.accounts.controllers', ['ngMaterial','lfNgMdFileInput']);

  angular
    .module('planting.accounts.services', []);
})();
