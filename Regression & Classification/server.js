var express = require('express');
var app = express();
var http = require("http");

var https = require("https");

var querystring = require("querystring");

var fs = require('fs');

var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// configure a public directory to host static content
app.use(express.static(__dirname + '/public'));


var ipaddress = process.env.OPENSHIFT_NODEJS_IP;
var port      = process.env.OPENSHIFT_NODEJS_IPORT || 3000;

app.listen(port, ipaddress);
// app.post("/prediction/neural-network", neuralNetwork);
// app.post("/prediction/linear-regression", linearRegression);
app.post("/clustering",clustering);
app.post("/prediction/regression",regression);
app.post("/classification",classification);
app.post("/clustering/zero",clusteringzero);
app.post("/clustering/one",clusteringone);
app.post("/clustering/two",clusteringtwo);
app.post("/clustering/three",clusteringthree);
app.post("/clustering/four",clusteringfour);
//maml-server.js
var result = '';

function classification(req, res){
    var data = req.body;
    //console.log(data);
    var path = '/workspaces/cb863d4f3f39452ba855f979fdc9c60c/services/58acc102ceff417bb446bc236559a2ce/execute?api-version=2.0&details=true';
    var key = 'r2AAk9wLsUH6MGbaxUdTTqN8ZDlNwr8is2kHNcMKH0Jk8UD+JQPCBFv8qomu/rrDPavO25LLr+BVlb9Y+fjHjg==';
    getPred(data, path, key);
    setTimeout(function() {
        //console.log(result);
        res.json(result);
    }, 1000);

}

function regression(req, res){
    var data = req.body;
    console.log(data);
    var path = '/workspaces/5f59fa9fa20e40bdbb68b87d4b1e7006/services/a6b2e4a5b11f4a7699929777cc4a4e81/execute?api-version=2.0&details=true';
    var key = 'hwWT5UbnU3QYJGKaWAFvpQqGKRHerg+SUYJ+8NxXUlPfE07xZ9lHyIov0SA2bxP7GM/G4hC+m+m1Tb2VWbTyTg==';
    getPred(data, path, key)

    //console.log(result);
    setTimeout(function() {
        res.json(result);
    }, 10000);
}

function clustering(req, res){
    var data = req.body;
    //console.log(data);
    var path = '/workspaces/895503c96ee3453e8e49e4a6b911d739/services/3a81368bbb374858974992c2a30dfaea/execute?api-version=2.0&details=true';
    var key = 'XbE69XAEME3HPkChQP4PEPdBGeF/o5yC16h9kGOT7L3PyEnvfmxw7Y/SqgA8oehC36nYzifgf4Cf1OJKP6zeWg==';
    getPred(data, path, key)

    //console.log(result);
    setTimeout(function() {
        res.json(result);
    }, 10000);
}


function clusteringzero(req, res){
    var data = req.body;
    var path = '/workspaces/5f59fa9fa20e40bdbb68b87d4b1e7006/services/fa52623ce23b40dead41fb8cbc6e1cda/execute?api-version=2.0&details=true';
    var key = 'zar+dREgzTcAQkVYy0PeFlg/P3LGRr+qBrf8XYpDnOJcGextzwBhRGgV/RWnJhIqeixYZX6o91BRBWP0PFB1Cg==';
    getPred(data, path, key)

    setTimeout(function() {
        res.json(result);
    }, 1000);
}

function clusteringone(req, res){
    var data = req.body;
    var path = '/workspaces/5f59fa9fa20e40bdbb68b87d4b1e7006/services/1811c128a52a4d20b9bfa814c68027fc/execute?api-version=2.0&details=true';
    var key = 'ODJ9aUnSSUX5ikCwa933iVubddf5iomHPxJKwDTyDneyT+t83NtgXqVM0c2YPZ7qDzqkjX5YJdUzLfz+q+IYkQ==';
    getPred(data, path, key)

    setTimeout(function() {
        res.json(result);
    }, 1000);
}

function clusteringtwo(req, res){
    var data = req.body;
    var path = '/workspaces/5f59fa9fa20e40bdbb68b87d4b1e7006/services/dbaac879671c4c62ae6b201d1aebddd6/execute?api-version=2.0&details=true';
    var key = 'UNF0i8ZI0zd5OdUNh95pT3QgMF9FOcV9reN1kzvn0tNh1yIRKBBgUi7FOjuyzhw8PqAd3K/oesSdSLHPuxzcdg==';
    getPred(data, path, key)

    setTimeout(function() {
        res.json(result);
    }, 1000);
}
function clusteringthree(req, res){
    var data = req.body;
    var path = '/workspaces/5f59fa9fa20e40bdbb68b87d4b1e7006/services/cf9dda01f3784d99bcb02c7eb1089ab7/execute?api-version=2.0&details=true';
    var key = '+5bFUtL8eVlT8hnv4I6Gzrutod5rc5N5yc2ti0JxPx2r6VdzUE3F4QsTYbcC4Q7SBpP1lebpGXssfoBeHjNHEA==';
    getPred(data, path, key)

    setTimeout(function() {
        res.json(result);
    }, 1000);
}
function clusteringfour(req, res){
    var data = req.body;
    var path = '/workspaces/5f59fa9fa20e40bdbb68b87d4b1e7006/services/e76e44f2a005470cb0b2faa09beeaa03/execute?api-version=2.0&details=true';
    var key = '1bp7sWTisI3s6WlHvLeGct7XO0eyCCABEt7TLOyitTWdksvZPBgDdNOLqzzxIHGYL4DX+v26Ein+BqUFEe+P1A==';
    getPred(data, path, key)

    setTimeout(function() {
        res.json(result);
    }, 1000);
}



function getPred(data, path, api_key) {

    var dataString = JSON.stringify(data);
    var host = 'ussouthcentral.services.azureml.net';
    var headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key};

    var options = {
        host: host,
        port: 443,
        path: path,
        method: 'POST',
        headers: headers
    };

    result = '';
    var reqPost = https.request(options, function (res) {
        res.on('data', function (d) {
            setTimeout(function() {
                process.stdout.write(d);
                result += d;
            }, 300);
            //return d;
        });
    });
    //console.log(result);
// Would need more parsing out of prediction from the result
    reqPost.write(dataString);
    reqPost.end();
    reqPost.on('error', function (e) {
        console.error(e);
    });
    //console.log(result);
    //return result;

    //callback(null, result);
}

function send404Reponse(response) {
    response.writeHead(404, {"Context-Type": "text/plain"});
    response.write("Error 404: Page not Found! Not sure");
    response.end();
}

function onRequest(request, response) {
    if(request.method == 'GET' && request.url == '/' ){
        response.writeHead(200, {"Context-Type": "text/plain"});
        fs.createReadStream("./index.html").pipe(response);
    }else {
        send404Reponse(response);
    }
}

http.createServer(onRequest).listen(8050);
//buildFeatureInput();
