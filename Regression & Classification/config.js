/**
 * Created by Lalit on 6/18/2016.
 */
(function(){
    angular
        .module("productCustomizer")
        .config(Config);

    function Config($routeProvider){
        $routeProvider
            .when("/", {
                templateUrl: "index.html",
                controller: "MainController"
            })
            .otherwise({
                redirectTo: "/"
            });
    }
})();