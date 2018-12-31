app.controller('returnController', ['$scope', '$http', function($scope, $http) {

    //Get returned item list
    $http.get('./returnList').then(function (response) {
        $scope.returnList = response.data;
        $scope.editingData = {};
        for (var i = 0, length = $scope.returnList.length; i < length; i++) {
          $scope.editingData[$scope.returnList[i]._id] = false;
        }
    }).catch(function (err) {
            return err;
    });

    $scope.modify = function(item){
        $scope.ITEM = item;
        $scope.ITEM.room_number = item.room_number;
        $scope.ITEM._id = item._id;
        $scope.ITEM.item_description = item.item_description;
        $scope.ITEM.guest_name = item.guest_name;
        $scope.ITEM.return_date = item.return_date;
        $scope.ITEM.date_found = item.date_found;
        $scope.ITEM.returned_by = item.returned_by;
        $scope.ITEM.comments = item.comments;
    };

    $scope.update = function(){
        $http.post('./editReturn/'+$scope.ITEM._id, $scope.ITEM);
    };

    $scope.send_info = function(itemID) {
        $scope.id = itemID;
    };

    $scope.confirmButton = function() {
        $http.post('./undoReturn/'+ $scope.id).then(function (data) {
            $scope.returnList = data.data;
        })
    };

    $scope.confirmDeleteButton = function() {
        $http.post('./deleteReturnedItem/'+ $scope.id).then(function (data) {
            $scope.returnList = data.data;
        })
    };

}]);