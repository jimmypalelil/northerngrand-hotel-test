
app.controller('trialListController', ['$scope', '$http', '$routeParams', '$rootScope', function($scope, $http, $routeParams, $rootScope) {
    $rootScope.status = 'all';
    $rootScope.currentMonth = $routeParams.trial_month;
    $rootScope.currentYear = $routeParams.year;
    $scope.type = $routeParams.type;
    $http.get('/pyList/'+ $routeParams.type + '/' + $routeParams.year) .success(function(data) {
        $scope.trial =  data;
        $scope.trial.forEach(function (value) {
            value.checked = false;
            if(value.month === $rootScope.currentMonth && value.status === 'clean') $scope.doneCount++;
        });
        $scope.undoneCount = 127 - $scope.doneCount;
    }).error(function(err) {
        return err;
    });

    $scope.$watch('currentMonth', function(newV, old) {
        $rootScope.status = 'all';
        $scope.searchItem = '';
        $scope.doneCount = 0;
        $scope.undoneCount = 0;
        $scope.trial.forEach(function (value) {
            value.checked = false;
            if(value.month === newV && value.status === 'clean') $scope.doneCount++;
        });
        $scope.undoneCount = 127 - $scope.doneCount;
    });

    $scope.statusButton = function(status) {
        $rootScope.status = status;
    };

    //For status changing
    $scope.statusChangeList = [];
    $scope.inHouseStatusChangeList = [];
    $scope.addList = function(room) {
        if($scope.statusChangeList.includes(room._id)) {
            var index = $scope.statusChangeList.indexOf(room._id);
            $scope.statusChangeList.splice(index, 1);
            $scope.inHouseStatusChangeList.splice(index, 1);
            room.checked = false;
        } else {
            $scope.statusChangeList.push(room._id);
            $scope.inHouseStatusChangeList.push(room);
            room.checked = true;
        }
    };

    //Status change function
    $scope.statusChange = function(room) {
        !$scope.statusChangeList.includes(room._id) ? $scope.addList(room) : ''; //For changing the state of a single room
        $http.post('/statusChange/' +$routeParams.type, $scope.statusChangeList);
        $scope.inHouseStatusChangeList.forEach(function (value) {
            var thisRoom = $scope.trial[$scope.trial.indexOf(value)];
            thisRoom.status = (thisRoom.status === 'clean' ? 'not done' : 'clean');
            thisRoom.checked = false;
            thisRoom.status === 'clean' ? $scope.doneCount++ : $scope.doneCount--;
        });
        $scope.undoneCount = 127 - $scope.doneCount;
        $scope.statusChangeList = [];
        $scope.inHouseStatusChangeList = [];
    };

    $scope.$watch('statusChangeList.length', function (newV, old) {
       $scope.selected = newV;
    });

    //Sorting mechanism
    $scope.greaterThan = function(prop, val){
        return function(item){
          if(val === undefined) val = 200;
          if (item[prop] >= val) return true;
        }
    };
    $scope.sortOrderBy = '+room_number';
    $scope.showRoomUpSort = true;

    $scope.sortOrder = function(cat) {
        $scope.sortOrderBy =  ($scope.sortOrderBy === '+' + cat ? '-' + cat : '+' + cat);
        switch(cat) {
            case 'room_number':
                $scope.showRoomUpSort = $scope.showRoomUpSort !== true;
                $scope.showRoomDownSort = !$scope.showRoomUpSort;
                $scope.showTypeUpSort = false;
                $scope.showTypeDownSort = false;
                break;
            case 'type':
                $scope.showTypeUpSort = $scope.showTypeUpSort !== true;
                $scope.showTypeDownSort = !$scope.showTypeUpSort;
                $scope.showRoomUpSort = false;
                $scope.showRoomDownSort = false;
                break;
        }
    };

    $scope.show_if = function(status, month) {
        if(month === $rootScope.currentMonth) {
            if($rootScope.status === 'all') return true;
            return status === $rootScope.status;
        }
    };

}]);