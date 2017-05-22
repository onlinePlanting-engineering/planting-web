(function(){
  'use strict';

  angular
  .module('planting.accounts.services')
  .factory('Account', Account);

  Account.$inject = ['$http'];

  function Account($http){
    Account = {
      destroy: destroy,
      get: get,
      update: update
    };

    return Account;

    function destroy(username){
      return $http.delete('/api/v1/accounts/' + username + '/');
    }

    function get(username) {
      return $http.get('/api/v1/accounts/' + username + '/');
    }

    function update(username, account){
      var url = '/api/v1/accounts/' + username + '/';
      var formData = objectToFormData(account);
      // var formData = new FormData();
      // formData.set('username', account.username);
      // formData.set('profile.img_heading', account.profile.img_heading);
      // formData.set('profile.nickname', account.profile.nickname);
      return $http.put('/api/v1/accounts/' + username + '/',
        formData,
        {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        }
      );

      // return $http({
      //   method: 'PUT',
      //   url: url,
      //   transformRequest: formDataTransform,
      //   data: objectToFormData(account)
      // });

    }

    // takes a {} object and returns a FormData object
    function objectToFormData(obj, form, namespace) {

      var fd = form || new FormData();
      var formKey;

      for(var property in obj) {
        if(obj.hasOwnProperty(property)) {

          if(namespace) {
            // formKey = namespace + '[' + property + ']';
            formKey = namespace + '.' + property;
          } else {
            formKey = property;
          }

          // if the property is an object, but not a File,
          // use recursivity.
          if(typeof obj[property] === 'object' && !(obj[property] instanceof File)) {

            objectToFormData(obj[property], fd, property);

          } else {

            // if it's a string or a File object
            fd.append(formKey, obj[property]);
          }

        }
      }

      return fd;

    };

    // usage for Angular.js

    // wrap object to formdata method,
    // to use it as a transform with angular's http.
    var formDataTransform = function(data, headersGetter) {

      // we need to set Content-Type to undefined,
      // to make the browser set it to multipart/form-data
      // and fill in the correct *boundary*.
      // setting Content-Type to multipart/form-data manually
      // will fail to fill in the boundary parameter of the request.
      headersGetter()['Content-Type'] = undefined;

      return objectToFormData(data);

    };
  }
})();
