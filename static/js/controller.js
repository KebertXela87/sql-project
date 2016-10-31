/*global angular*/
var ArchivesApp = angular.module('ArchivesApp', []);

ArchivesApp.controller('ArchivesController', function($scope){
   
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/archives');
   
    $scope.searchTerm = '';
    $scope.searchResults = [];
   
    $scope.showhide = [];
    for (var i = 1; i <= 6; i++) {
        $scope.showhide[i] = "Click to Hide";    
    }   
    
    $scope.toggle = function toggle(type){
        console.log('pressing toggle');
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

    
    $scope.search = function search() {
        console.log('Searching for: ', $scope.searchTerm);
        $scope.searchResults = [];
        socket.emit('search', $scope.searchTerm);
        $scope.searchTerm = '';
    };
    
    socket.on('searchResult', function(ser) {
        console.log(ser);
        $scope.searchResults.push(ser);
        $scope.$apply();
    });
    
    socket.on('showResults', function() {
       console.log("Results found");
       showResults('show');
    });
    
    socket.on('showNoResults', function() {
       console.log("Results not found");
       showResults('hide');
    });
});

function showResults(showhide){
    if(showhide == 'show'){
        console.log("SHOW");
        document.getElementById('searchpane').style.visibility="visible";
        document.getElementById('noresults').style.visibility="hidden";
        document.getElementById('noresults').style.height="0px";
    }
    else if(showhide == 'hide'){
        console.log("HIDE");
        document.getElementById('searchpane').style.visibility="hidden";
        document.getElementById('noresults').style.visibility="visible";
        document.getElementById('noresults').style.height="10px";
    }
}