function HomeCtrl($scope, $location, $http, $modal) {
    $scope.projects = {};

    $scope.loadProjects = function(url) {
        $http.get(url).then(function(data) {
            $scope.projects = data.data;
        });
    };
    
    $scope.loadProjects('/api/1/projects?limit=10');


    $scope.newDataset = function(){
        var d = $modal.open({
            templateUrl: 'projects/new.html',
            controller: 'ProjectsNewCtrl'
        });
    };
}

HomeCtrl.$inject = ['$scope', '$location', '$http', '$modal'];
