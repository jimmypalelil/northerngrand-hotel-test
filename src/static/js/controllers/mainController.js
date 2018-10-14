
app.controller('mainController', ['$scope', '$rootScope', '$routeParams', function($scope, $rootScope) {
    $rootScope.months = [
        ['jan', 'feb', 'mar', 'apr','may','jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
        ['jan to jun', 'jul to dec'],
        ['jan to jun', 'jul to dec'],
        ['jan to mar', 'apr to jun', 'july to sep', 'oct to dec'],
        ['jan to mar', 'apr to jun', 'july to sep', 'oct to dec']
    ];

    $scope.changeMonth = function(month, year) {
        $rootScope.currentMonth = month;
        $rootScope.currentYear = year;
    };
}]);

app.controller('listController', ['$scope', '$http', '$routeParams', '$rootScope', function($scope, $http, $routeParams, $rootScope) {
    $rootScope.monthListNum = $routeParams.monthListNum;
    $rootScope.status = 'all';
    $rootScope.currentMonth = $routeParams.month;
    $rootScope.currentYear = $routeParams.year;
    $scope.type = $routeParams.type;

    $scope.$watch('currentMonth', function(newV, old) {
        $rootScope.status = 'all';
        $scope.searchItem = '';
        $scope.doneCount = 0;
        $scope.undoneCount = 0;
        $http.get('/pyList/'+ $routeParams.type + '/' + $routeParams.year + '/' + newV) .success(function(data) {
            $scope.trial =  data;
            $scope.trial.forEach(function (value) {
               if(value.status === 'clean') $scope.doneCount++;
            });
            $scope.undoneCount = 127 - $scope.doneCount;
        }).error(function(err) {
            return err;
        });
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
    $scope.statusChange = function(room, status) {
        !$scope.statusChangeList.includes(room._id) ? $scope.addList(room) : ''; //For changing the state of a single room
        $http.post('/statusChange/' +$routeParams.type + "/" + status, $scope.statusChangeList); //send data
        $scope.inHouseStatusChangeList.forEach(function (value) {
            var thisRoom = $scope.trial[$scope.trial.indexOf(value)];
            if(status !== thisRoom.status) status === 'clean' ? $scope.doneCount++ : $scope.doneCount--;
            thisRoom.status = status;
            thisRoom.checked = false;
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
    }; //sorting mechanism

    $scope.show_if = function(status) {
        if($rootScope.status === 'all') return true;
        return $rootScope.status === status;

    }
}]);
