(function(){
    angular
        .module("productCustomizer")
        .controller("MainController", MainController);

    function MainController($scope, $http){
        $scope.method = 'prediction';
        $scope.show = "teat";
        $scope.slider = {
            value: 10,
            options: {
                showSelectionBar: true
            }
        };
        var output = [];
        var classification_result = [];
        var rex_result = [];
        var clustering = [];
        $scope.predict = function() {
          if ($scope.method == 'prediction'){
            var d = {
                "Inputs": {
                    "input1": {
                        "ColumnNames": [
                          "loan_amnt",
                          "last_meanfico",
                          "dti",
                          "addr_state",
                          "emp_length",
                          "purpose"
                          ],
                        "Values": [
                            [   $scope.loan_amount,
                                $scope.fico,
                                $scope.dti,
                                $scope.state,
                                $scope.employmnt_length,
                                $scope.purpose
                            ]
                        ]
                    }
                },
                "GlobalParameters": {}
            };
            $http.post('/classification', d)
                .then(function (response) {
                    console.log(response);
                    var result = JSON.parse(response.data);
                    result = result.Results.output1.value.Values;
                    for (var i = 0; i < result.length; i++) {
                        classification_result.push({
                            'loan_amount': result[i][0],
                            'approved_status': result[i][0] == 1 ? "Approved" : "Rejected",
                            'probability': result[i][1]
                        });
                    }
                    $scope.classification_results = classification_result;
            });
          } else if($scope.method == 'classification'){
                var d = {
                    "Inputs": {
                        "input1": {
                            "ColumnNames": [
                                "loan_amnt",
                                "term",
                                "emp_length",
                                "home_ownership",
                                "annual_inc",
                                "verification_status",
                                "purpose",
                                "addr_state",
                                "dti",
                                "delinq_2yrs",
                                "fico_range_high",
                                "inq_last_6mths",
                                "mths_since_last_delinq",
                                "open_acc",
                                "pub_rec",
                                "revol_util",
                                "total_acc",
                                "mths_since_last_major_derog",
                                "application_type",
                                "open_acc_6m",
                                "pub_rec_bankruptcies"
                              ],
                            "Values": [
                                [   $scope.loan_amount,
                                    $scope.term,
                                    $scope.employmnt_length,
                                    $scope.home_ownership,
                                    $scope.annual_inc,
                                    $scope.verification_status,
                                    $scope.purpose,
                                    $scope.state,
                                    $scope.dti,
                                    $scope.delinq_2yrs,
                                    $scope.fico,
                                    $scope.inq_last_6mths,
                                    $scope.mths_since_last_delinq,
                                    $scope.open_acc,
                                    $scope.pub_rec,
                                    $scope.revol_util,
                                    $scope.total_acc,
                                    $scope.mths_since_last_major_derog,
                                    $scope.application_type,
                                    $scope.open_acc_6m,
                                    $scope.pub_rec_bankruptcies
                                ]
                            ]
                        }
                    },
                    "GlobalParameters": {}
                };
                var xy = {
                    "Inputs": {
                        "input1": {
                            "ColumnNames": [
                                  "loan_amnt",
                                  "term",
                                  "emp_length",
                                  "home_ownership",
                                  "annual_inc",
                                  "verification_status",
                                  "purpose",
                                  "addr_state",
                                  "dti",
                                  "delinq_2yrs",
                                  "fico_range_high",
                                  "inq_last_6mths",
                                  "mths_since_last_delinq",
                                  "open_acc",
                                  "pub_rec",
                                  "revol_util",
                                  "total_acc",
                                  "mths_since_last_major_derog",
                                  "application_type",
                                  "acc_now_delinq",
                                  "open_acc_6m",
                                  "pub_rec_bankruptcies"
                                ],
                            "Values": [
                                [   $scope.loan_amount,
                                    $scope.term,
                                    $scope.employmnt_length,
                                    $scope.home_ownership,
                                    $scope.annual_inc,
                                    $scope.verification_status,
                                    $scope.purpose,
                                    $scope.state,
                                    $scope.dti,
                                    $scope.delinq_2yrs,
                                    $scope.fico,
                                    $scope.inq_last_6mths,
                                    $scope.mths_since_last_delinq,
                                    $scope.open_acc,
                                    $scope.pub_rec,
                                    $scope.revol_util,
                                    $scope.total_acc,
                                    $scope.mths_since_last_major_derog,
                                    $scope.application_type,
                                    $scope.acc_now_delinq,
                                    $scope.open_acc_6m,
                                    $scope.pub_rec_bankruptcies
                                ]
                            ]
                        }
                    },
                    "GlobalParameters": {}
                };

                $http.post('/clustering', d)
                    .then(function (response) {
                        console.log(response);
                        var result = JSON.parse(response.data);
                        result = result.Results.output1.value.Values;
                        for (var i = 0; i < result.length; i++) {
                            /*output.push({
                                'type': 'KNN-clustering',
                                'persqm': parseFloat(result[i][0]),
                                'total': 'First'
                            });*/
                            var dx = {
                                "Inputs": {
                                    "input1": {
                                        "ColumnNames": [
                                            "loan_amnt",
                                            "term",
                                            "emp_length",
                                            "home_ownership",
                                            "annual_inc",
                                            "verification_status",
                                            "purpose",
                                            "addr_state",
                                            "dti",
                                            "delinq_2yrs",
                                            "fico_range_high",
                                            "inq_last_6mths",
                                            "mths_since_last_delinq",
                                            "open_acc",
                                            "pub_rec",
                                            "revol_util",
                                            "total_acc",
                                            "mths_since_last_major_derog",
                                            "application_type",
                                            "open_acc_6m",
                                            "pub_rec_bankruptcies",
                                            "Assignments"
                                          ],
                                        "Values": [
                                            [   $scope.loan_amount,
                                                $scope.term,
                                                $scope.employmnt_length,
                                                $scope.home_ownership,
                                                $scope.annual_inc,
                                                $scope.verification_status,
                                                $scope.purpose,
                                                $scope.state,
                                                $scope.dti,
                                                $scope.delinq_2yrs,
                                                $scope.fico,
                                                $scope.inq_last_6mths,
                                                $scope.mths_since_last_delinq,
                                                $scope.open_acc,
                                                $scope.pub_rec,
                                                $scope.revol_util,
                                                $scope.total_acc,
                                                $scope.mths_since_last_major_derog,
                                                $scope.application_type,
                                                $scope.open_acc_6m,
                                                $scope.pub_rec_bankruptcies,
                                                result[i][0]

                                            ]
                                        ]
                                    }
                                },
                                "GlobalParameters": {}
                            };



                            if (result[i][0] == 0){
                              console.log("ZERO-0")
                              $http.post('/clustering/zero', dx)
                                  .then(function (response) {
                                      console.log(response);
                                      var result = JSON.parse(response.data);
                                      result = result.Results.output1.value.Values;
                                      for (var i = 0; i < result.length; i++) {

                                        var out_default;
                                        console.log("DEFAULT PREDICTION")
                                        $http.post('/prediction/regression', xy)
                                            .then(function (response) {
                                                console.log(response);
                                                var rex = JSON.parse(response.data);
                                                rex = rex.Results.output1.value.Values;
                                                for (var i = 0; i < rex.length; i++) {
                                                    rex_result.push({
                                                        'int_rate': rex[i][22]
                                                    });
                                                }

                                        });

                                          output.push({
                                              'type': 'KMeans-clustering',
                                              'cluster': parseFloat(result[i][0]),
                                              'interest': parseFloat(result[i][1])
                                          });
                                      }
                              });

                            }
                            else if (result[i][0] == 1){
                              console.log("ONE-1")
                              $http.post('/clustering/one', dx)
                                  .then(function (response) {
                                      console.log(response);
                                      var result = JSON.parse(response.data);
                                      result = result.Results.output1.value.Values;
                                      for (var i = 0; i < result.length; i++) {

                                        var out_default;
                                        console.log("DEFAULT PREDICTION")
                                        $http.post('/prediction/regression', xy)
                                            .then(function (response) {
                                                console.log(response);
                                                var rex = JSON.parse(response.data);
                                                rex = rex.Results.output1.value.Values;
                                                for (var i = 0; i < rex.length; i++) {
                                                    rex_result.push({
                                                        'int_rate': rex[i][22]
                                                    });
                                                }

                                        });


                                          output.push({
                                              'type': 'KMeans-clustering',
                                              'cluster': parseFloat(result[i][0]),
                                              'interest': parseFloat(result[i][1])
                                          });
                                      }
                              });

                            }
                            else if (result[i][0] == 2){
                              console.log("TWO-2")
                              $http.post('/clustering/two', dx)
                                  .then(function (response) {
                                      console.log(response);
                                      var result = JSON.parse(response.data);
                                      result = result.Results.output1.value.Values;
                                      for (var i = 0; i < result.length; i++) {

                                        var out_default;
                                        console.log("DEFAULT PREDICTION")
                                        $http.post('/prediction/regression', xy)
                                            .then(function (response) {
                                                console.log(response);
                                                var rex = JSON.parse(response.data);
                                                rex = rex.Results.output1.value.Values;
                                                for (var i = 0; i < rex.length; i++) {
                                                    rex_result.push({
                                                        'int_rate': rex[i][22]
                                                    });
                                                }

                                        });


                                          output.push({
                                              'type': 'KMeans-clustering',
                                              'cluster': parseFloat(result[i][0]),
                                              'interest': parseFloat(result[i][1])
                                          });
                                      }
                              });

                            }
                            else if (result[i][0] == 3){
                              console.log("THREE-3")
                              $http.post('/clustering/three', dx)
                                  .then(function (response) {
                                      console.log(response);
                                      var result = JSON.parse(response.data);
                                      result = result.Results.output1.value.Values;
                                      for (var i = 0; i < result.length; i++) {

                                        var out_default;
                                        console.log("DEFAULT PREDICTION")
                                        $http.post('/prediction/regression', xy)
                                            .then(function (response) {
                                                console.log(response);
                                                var rex = JSON.parse(response.data);
                                                rex = rex.Results.output1.value.Values;
                                                for (var i = 0; i < rex.length; i++) {
                                                    rex_result.push({
                                                        'int_rate': rex[i][22]
                                                    });
                                                }

                                        });


                                          output.push({
                                              'type': 'KMeans-clustering',
                                              'cluster': parseFloat(result[i][0]),
                                              'interest': parseFloat(result[i][1])
                                          });
                                      }
                              });

                            }
                            else if (result[i][0] == 4){
                              console.log("FOUR-4")
                              $http.post('/clustering/four', dx)
                                  .then(function (response) {
                                      console.log(response);
                                      var result = JSON.parse(response.data);
                                      result = result.Results.output1.value.Values;
                                      for (var i = 0; i < result.length; i++) {

                                        var out_default;
                                        console.log("DEFAULT PREDICTION")
                                        $http.post('/prediction/regression', xy)
                                            .then(function (response) {
                                                console.log(response);
                                                var rex = JSON.parse(response.data);
                                                rex = rex.Results.output1.value.Values;
                                                for (var i = 0; i < rex.length; i++) {
                                                    rex_result.push({
                                                        'int_rate': rex[i][22]
                                                    });
                                                }

                                        });

                                          output.push({
                                              'type': 'KMeans-clustering',
                                              'cluster': parseFloat(result[i][0]),
                                              'interest': parseFloat(result[i][1])
                                          });
                                      }
                              });

                            }




                        }
                        $scope.results = output;
                        $scope.def = rex_result;


                });
            }
        }
    }
})();
