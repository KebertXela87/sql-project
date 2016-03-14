var ArchivesApp = angular.module('ArchivesApp', []);

ArchivesApp.controller('ArchivesController', function($scope){
   
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/archives');
   
    $scope.toggle = function toggle(type){
        var i, rows = document.getElementsByClassName(type);
        if (rows[0].style.display == 'none') {
            for (i = 0; i < rows.length; i++) {
                rows[i].style.display="table-row";
            }
        }
        else {
            for (i = 0; i < rows.length; i++) {
                rows[i].style.display="none";
            }
        }
    };
   
    socket.on('connect', function(){
        console.log('Connected'); 
    });
});