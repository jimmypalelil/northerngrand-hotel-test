app.config(function($interpolateProvider, $routeProvider) {
    $routeProvider
    .when('/inventorylist/:type', {
        templateUrl: '/inventory/inventorylist',
        controller: 'inventoryListController'
    });
});

app.controller('inventoryController', ['$scope', '$http', '$routeParams','$rootScope', function($scope, $http, $routeParams, $rootScope) {
    $scope.categories = ['Linen', 'Guest Room Supplies', 'Laundry Supplies', 'Cleaning Supplies', 'Miscellaneous'];
    $scope.catCard = function(cat) {
        $rootScope.currentCat = cat;
    };
}]);


app.controller('inventoryListController', ['$scope', '$http', '$routeParams', '$rootScope', function($scope, $http, $routeParams, $rootScope) {
    $rootScope.currentCat = $routeParams.type;
    $http.get('/inventory/inventoryList/').success(function(data) {
        $scope.linen =  data;
        $scope.editingData = {};
        for (var i = 0, length = $scope.linen.length; i < length; i++) {
            $scope.editingData[$scope.linen[i]._id] = false;
        }
    }).error(function(err) {
        return err;
    });

    $scope.$watch('linen', function(newV, old) {
        $scope.linenCount = 0;
        $scope.linenCost = 0;
        newV.forEach(function (value) {
           if(value.type === $rootScope.currentCat) {
               $scope.linenCount += value.total_count;
               $scope.linenCost += value.total_cost;
           }
        });
    });

    $scope.$watch('searchItem', function(newV, old) {
        $scope.linenCount = 0;
        $scope.linenCost = 0;
        if(newV === undefined || newV === '') {
            $scope.linen.forEach(function (value) {
                if(value.type === $rootScope.currentCat) {
                    $scope.linenCount += value.total_count;
                    $scope.linenCost += value.total_cost;
                }
            });
        } else {
            $scope.linen.forEach(function (value) {
                if(value.item_name.includes(newV.toLowerCase())) {
                    $scope.linenCount += value.total_count;
                    $scope.linenCost += value.total_cost;
                }
            });
        }
    });

    $scope.$watch('currentCat', function(newV, old) {
        $scope.searchItem = '';
        $scope.linenCount = 0;
        $scope.linenCost = 0;
        $scope.linen.forEach(function (value) {
            if(value.type === newV) {
                $scope.linenCount += value.total_count;
                $scope.linenCost += value.total_cost;
            }
        });
    });

    $scope.done_button = function(id, type) {
        $http.post('/inventory/delete/'+id).then(function(data) {
            $scope.linen = data.data;
        });
        $('#confirmModal').toggle();
    };

    $scope.send_info = function(id, type) {
        $scope.id = id;
        $scope.type = type;
        $scope.currentCat = type;
    };

    $scope.modify = function(id){
        $scope.editingData[id] = true;
    };

    $scope.update = function(tableData){
        $scope.editingData[tableData._id] = false;
        tableData['total_count'] = 0;
        for (var key in tableData) {
            if(!isNaN(tableData[key]) && key !== 'total_count' && key !== 'total_cost' && key !== 'cost_per_item') {
                tableData[key] = Number(tableData[key]);
                tableData['total_count'] = tableData['total_count'] + tableData[key];
            }
        }
        tableData['total_cost'] = tableData['cost_per_item'] * tableData['total_count'];
        $http.post('./edit', tableData);
    };

    $scope.show_if = function(item, query) {
        if(query !== undefined && query !== '' && item.item_name.includes(query.toLowerCase())) {
            return true;
        }
        return $rootScope.currentCat === item.type;
    }

}]);