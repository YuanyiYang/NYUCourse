/**
 * Created by yuanyiyang on 2/26/15.
 */
'use strict'

var searchEngine = angular.module('searchEngine', []);
var url = "http://linserv2.cims.nyu.edu:25800/search";

searchEngine.controller('ResultsCtrl', ['$scope', '$http', function($scope, $http){
  $scope.num = 0;
  $scope.submit = function(){
    var whole_url = url + "?q=" + $scope.query;
    $http.get(whole_url).success(function(data){
      $scope.num = data["numResults"]
      $scope.results = data['results'];
    })
  }
}]);