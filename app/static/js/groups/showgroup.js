var app = angular.module('ShowgroupApp', []);
 
app.controller('ShowgroupController', function($timeout) {
    var vm = this;
    recieve_time = [];
    sent_time = [];
    function getdata(){
        var request = new XMLHttpRequest();
        request.open("GET", "api/query_group",true);
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
                        recieve_show = [];
                        for (i in datas.recieved){
                            if(datas.recieved[i].is_success === true){
                                datas.recieved[i].last_modify_date = moment.unix(datas.recieved[i].last_modify_date)
                                getgrouptime(datas.recieved[i].id,'recieve');
                                recieve_show.push(datas.recieved[i]);
                            }
                        }
                        console.log(recieve_show);
                        vm.success_recieved = recieve_show;
                        sent_show = [];
                        for (i in datas.sent){
                            if(datas.sent[i].is_success === true){
                                datas.sent[i].last_modify_date = moment.unix(datas.sent[i].last_modify_date)
                                getgrouptime(datas.sent[i].id,'sent');
                                sent_show.push(datas.sent[i])
                            }
                        }
                        vm.success_sent = sent_show;
                        vm.group_num = recieve_show.length + sent_show.length;
                    }
                } else {
                    alert("發生錯誤: " + request.status);
                }
            }
        }
    };

    
    function getgrouptime(gnum,gtype){
        console.log(gnum);
        var greq = new XMLHttpRequest();
        url = "api/group_result/" + gnum;
        greq.open("GET", url,true);
        greq.send();
        greq.onreadystatechange = function() {
            // 伺服器請求完成
            if (greq.readyState === 4) {
                // 伺服器回應成功
                if (greq.status === 200) {
                    var type = greq.getResponseHeader("Content-Type");   // 取得回應類型
                    // 判斷回應類型，這裡使用 JSON
                    if (type.indexOf("application/json") === 0) {     
                        datas = JSON.parse(greq.responseText);
                        for (i in datas.time){
                            datas.time[i][0] = moment.unix(datas.time[i][0]).format('YYYY-MM-DD HH:mm')
                            datas.time[i][1] = moment.unix(datas.time[i][1]).format('YYYY-MM-DD HH:mm')
                        }
                        if(gtype == 'recieve'){
                            console.log('fuck');
                            recieve_time.push(datas.time);
                        }
                        else if(gtype == 'sent'){
                            sent_time.push(datas.time);
                        }
                    }
                } else {
                    alert("發生錯誤: " + greq.status);
                }
            }
        }
    };
    var auto = $timeout(function() {
        getdata();
    },200);
    var auto = $timeout(function() {
        for(i in recieve_time){
            vm.success_recieved[i].grouptime = recieve_time[i];
        }
        for (i in sent_time){
            vm.success_sent[i].grouptime = sent_time[i];
        }
    },300);
})
.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
  });
