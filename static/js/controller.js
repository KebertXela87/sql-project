var ArchivesApp = angular.module('ArchivesApp', []);

ArchivesApp.controller('ArchivesController', function($scope){
   
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/archives');
   
    $scope.showhide = [];
    for (var i = 1; i <= 6; i++) {
        $scope.showhide[i] = "Click to Hide";    
    }   
    
    $scope.toggle = function toggle(type){
        var i, rows = document.getElementsByClassName(type);
        var types = ["Movie", "Novel", "YA Book", "Short Story", "Comic", "TV Show"];
        
        if (rows[0].style.display == 'none') {
            for (i = 0; i < rows.length; i++) {
                rows[i].style.display="table-row";
            }
            for (var i = 0; i < types.length; i++) {
                if(type == types[i]) { 
                    $scope.showhide[i + 1] = "Click to Hide";
                }
            }
        }
        else {
            for (i = 0; i < rows.length; i++) {
                rows[i].style.display="none";
            }
            for (var i = 0; i < types.length; i++) {
                if(type == types[i]) { 
                    $scope.showhide[i + 1] = "Click to Show";
                }
            }
        }
    };
   
    socket.on('connect', function(){
        console.log('Connected'); 
    });
});