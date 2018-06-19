var app = angular.module('GetdataApp', []);
 
app.controller('GetdataController', function($timeout, $interval) {
    var vm = this;
    function getdata(){
        var request = new XMLHttpRequest();
        request.open("GET", "api/query_group");
        request.send();
        request.onreadystatechange = function() {
            console.log('hihihi');
            // 伺服器請求完成
            if (request.readyState === 4) {
                // 伺服器回應成功
                if (request.status === 200) {
                    var type = request.getResponseHeader("Content-Type");   // 取得回應類型

                    // 判斷回應類型，這裡使用 JSON
                    if (type.indexOf("application/json") === 0) {               
                        datas = JSON.parse(request.responseText);
                        showdata = [];
                        for (i in datas.recieved){
                            if(datas.recieved[i].is_pending === true){
                                showdata.push(datas.recieved[i])
                            }
                        }
                        // console.log(datas.recieved);
                        console.log(showdata);
                        vm.recieved = showdata;
                    }
                } else {
                    alert("發生錯誤: " + request.status);
                }
            }
        }
    };
    var auto = $timeout(function() {
        getdata();
    },100);
    var auto = $timeout(function() {
        getdata();
    },200);
    var auto = $interval(function() {
        getdata();
    }, 5000);

    vm.accept_group = function(id){
        var request = new XMLHttpRequest();
        url = "api/accept_group/"+id;
        request.open("GET", url);
        request.send();
        $timeout(function() {getdata();},500);
        $timeout(function() {getdata();},500);
    }

    vm.reject_group = function(id){
        var request = new XMLHttpRequest();
        url = "api/reject_group/"+id;
        request.open("GET", url);
        request.send();
        $timeout(function() {getdata();},500);
        $timeout(function() {getdata();},500);
    }
})
.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
  });