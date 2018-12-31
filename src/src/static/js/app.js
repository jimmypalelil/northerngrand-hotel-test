var app = angular.module('myApp', ['ngRoute','ngMaterial', 'ngMessages']);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

app.config(function($routeProvider) {
    $routeProvider
        .when("/:monthListNum/list/:type/:year/:month", {
            templateUrl: '/HK_Views/hkList',
            controller: 'listController'
        });
});

app.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('purple')
    .accentPalette('orange');
});

$(document).ready(function () {
    $('.navbar .card').click(function() {
        var navbar_toggle = $('.navbar-toggle');
        if (navbar_toggle.is(':visible')) {
            navbar_toggle.trigger('click');
        }
    });
});
