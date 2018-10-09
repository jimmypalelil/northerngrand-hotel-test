var app = angular.module('myApp', ['ngRoute'])

app.config(function($interpolateProvider, $routeProvider) {
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

app.config(function($interpolateProvider, $routeProvider) {
    $routeProvider
    .when('/list/:type/:year/:trial_month', {
        templateUrl: '/trial/triallist',
        controller: 'trialListController'
    });
});

$(document).ready(function () {
    $('.navbar .card').click(function() {
        var navbar_toggle = $('.navbar-toggle');
        if (navbar_toggle.is(':visible')) {
            navbar_toggle.trigger('click');
        }
    });
});
