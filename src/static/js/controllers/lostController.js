app.controller('lostController', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
    $http.get('./lostList') .success(function(data) {
        $scope.trial =  data;
        $scope.editingData = {};
        for (var i = 0, length = $scope.trial.length; i < length; i++) {
          $scope.editingData[$scope.trial[i]._id] = false;
        }
    }).error(function(err) {
        return err;
    });

    $scope.send_info = function(item) {
        $scope.itemID = item._id;
        $scope.itemDescription = item.item_description;
        $scope.itemRoomNo = item.room_number;
    };

    $scope.confirmDelete = function() {
        console.log($scope.itemID);
        $http.post('./deleteLostItem/' + $scope.itemID).then(function (data) {
            $scope.trial = data.data;
        })
    };


    $scope.confirmReturn = function() {
      $http.post('./returnItem/' + $scope.itemID)
    };

    $scope.modify = function(id){
        $scope.editingData[id] = true;
    };

    $scope.update = function(tableData){
        $scope.editingData[tableData._id] = false;
        $http.post('./edit/'+tableData._id, tableData);
    };

    $scope.sortOrderBy = '+room_number';
    $scope.showRoomUpSort = true;

    $scope.sortOrder = function(cat) {
        $scope.sortOrderBy =  ($scope.sortOrderBy === '+' + cat ? '-' + cat : '+' + cat);
        switch(cat) {
            case 'room_number':
                $scope.showRoomUpSort = $scope.showRoomUpSort !== true;
                $scope.showRoomDownSort = !$scope.showRoomUpSort;
                $scope.showDateUpSort = false;
                $scope.showDateDownSort = false;
                break;
            case 'date':
                $scope.showDateUpSort = $scope.showDateUpSort !== true;
                $scope.showDateDownSort = !$scope.showDateUpSort;
                $scope.showRoomUpSort = false;
                $scope.showRoomDownSort = false;
                break;
        }
    };

}]);