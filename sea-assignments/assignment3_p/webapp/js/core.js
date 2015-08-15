var searchApp = angular.module('searchApp', ['ui.bootstrap', 'ngSanitize']).config(
	function($locationProvider) {
		$locationProvider.html5Mode(true);
    });

searchApp.controller('mainController', function ($scope, $rootScope, $http, $location, $window, $timeout) {
	$scope.formData = {};

	$scope.search = function() {
		$window.location = "/?q=" + $scope.formData.query;
	};

	$scope.pageChanged = function() {
		console.log('Page changed to: ' + $scope.formData.page);
		$scope.fetchRecords();
		document.body.scrollTop = document.documentElement.scrollTop = 0;
	};

	$scope.fetchRecords = function() {
		$scope.statusText = 'Searching...';
		var start = new Date().getTime();
    var elapsed = '0.0';
    console.log("Fetching");
		$http.get('/search?q=' + escape($scope.formData.query)).success(function(data) {
			$scope.delay = (new Date().getTime() - start) / 1000.0;
			$scope.totalItems = data.numResults;
			$scope.itemsPerPage = 10; //data.itemsPerPage;
			$scope.errorText = data.error;
			$scope.statusText = '';
			var results = [];
			for (var i = 0; i < data.results.length; i++) {
				results.push("<h4><a href='" + data.results[i].url + "'>" + data.results[i].title + "</a></h4>" + data.results[i].snippet);
			}
			$scope.results = results;
			console.log("Fetched");
		})
		.error(function(data) {
			$scope.totalItems = 0;
			$scope.errorText = data;
			$scope.statusText = '';
		});
		$location.search('q', $scope.formData.query);
	};
	
	$rootScope.$on('$locationChangeSuccess', function(event){
		if ($location.search().q) {
			$scope.formData.query = $location.search().q;
			$scope.formData.page = 1;
			$scope.activeQuery = $scope.formData.query;
			$scope.fetchRecords();
		} else {
			$scope.activeQuery = false;
		}
	});
});
