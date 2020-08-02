

var html2doc = {};
var base_url = "http://59.108.48.35:8060"

function getCheckbox(name){
    var checked_list = [];
    $('input[name="'+name+'"]:checked').each(function(){
        checked_list.push($(this).val());
    });
    return checked_list;
}

// 点击查询按钮，调用es检索
$(document).ready(function(){
    $("#btn_query").click(function(){

        // 先清空
        $('#tb_result_coarse').css('visibility', 'hidden');
        $('#tb_description').css('visibility', 'hidden');
        $('#tb_result_coarse_body').empty();
        $("#des_title").empty();
        $("#des_id").empty();
        $("#des_cause").empty();
        $("#des_source").empty();
        $("#des_court").empty();
        $("#des_judge").empty();
        $("#des_clerk").empty();
        $("#des_party").empty();
        $("#des_process").empty();
        $("#des_opinion").empty();
        $("#des_result").empty();


        var keywords = $("#keywords").val();                    // 关键词
        var ay = getCheckbox("ay");                            // 案由
        var cygzjbsx  = getCheckbox("cygzjbsx");                // 船员雇主基本属性 
        var lwhtdxs = getCheckbox("lwhtdxs");                   // 劳务合同的形式
        var lwgxczdzm = getCheckbox("lwgxczdzm");               // 劳务关系存在的证明
        var gzbzdyd = getCheckbox("gzbzdyd");                   // 工资标准的约定
        var yflwbchfy = getCheckbox("yflwbchfy");               // 应付劳务报酬和费用
        var yjzfdgzdzm = getCheckbox("yjzfdgzdzm");             // 已经支付的工资的证明
        var cyzcgzjgzsjdzm = getCheckbox("cyzcgzjgzsjdzm");     // 船员在船工作及工作时间的证明
        var zyjjfsdyd = getCheckbox("zyjjfsdyd");               // 争议解决方式的约定
        var ssqq = getCheckbox("ssqq");                         // 诉讼请求
        var flyj = getCheckbox("flyj");                         // 法律依据


        var data = {
            keywords: keywords,
            ay: ay,
            cygzjbsx: cygzjbsx,
            lwhtdxs: lwhtdxs,
            lwgxczdzm: lwgxczdzm,
            gzbzdyd: gzbzdyd,
            yflwbchfy: yflwbchfy,
            yjzfdgzdzm: yjzfdgzdzm,
            cyzcgzjgzsjdzm: cyzcgzjgzsjdzm,
            zyjjfsdyd: zyjjfsdyd,
            ssqq: ssqq,
            flyj: flyj
        };
        console.log(data);
        $.ajax({
            url: base_url + "/query",
            type: "PUT",
            // contentType: "application/json",
            dataType: "json",
            data: data,
            success:function(msg){
                for(var i=0; i<msg.length; i++){
                    // 在表格上追加
                    html = '<tr id="result_' + i + '">' +   
                           '<td>' + msg[i]["案号"]  + '</td>' +
                           '<td>' + msg[i]["标题"]  + '</td>' +
                           '<td>' + msg[i]["score"].toFixed(3) + '</td>' +
                           '</tr>';
                    $('#tb_result_coarse').append(html);
                    html2doc[i] = msg[i];

                    $('#tb_result_coarse').on("click", "#result_"+i, function(){
                        var id = $(this).attr("id").split("_")[1];

                        // 标题
                        $("#des_title").empty();
                        $('#des_title').append('<td>标题</td>');
                        $('#des_title').append('<td>'+html2doc[id]["标题"]+'</td>');

                        // 案号
                        $("#des_id").empty();
                        $('#des_id').append('<td>案号</td>');
                        $('#des_id').append('<td>'+html2doc[id]["案号"]+'</td>');

                        // 案由
                        $("#des_cause").empty();
                        $('#des_cause').append('<td>案由</td>');
                        $('#des_cause').append('<td>'+html2doc[id]["案由"]+'</td>');

                        // 来源
                        $("#des_source").empty();
                        $('#des_source').append('<td>来源</td>');
                        $('#des_source').append('<td>'+html2doc[id]["来源"]+'</td>');

                        // 审理法院
                        $("#des_court").empty();
                        $('#des_court').append('<td>审理法院</td>');
                        $('#des_court').append('<td>'+html2doc[id]["审理法院"]+'</td>');

                        // 审判员
                        $("#des_judge").empty();
                        $('#des_judge').append('<td>审判员</td>');
                        $('#des_judge').append('<td>'+html2doc[id]["审判员"]+'</td>');

                        // 书记员
                        $("#des_clerk").empty();
                        $('#des_clerk').append('<td>书记员</td>');
                        $('#des_clerk').append('<td>'+html2doc[id]["书记员"]+'</td>');

                        // 当事人
                        $("#des_party").empty();
                        $('#des_party').append('<td>当事人</td>');
                        $('#des_party').append('<td>'+html2doc[id]["当事人"]+'</td>');

                        // 庭审过程
                        $("#des_process").empty();
                        $('#des_process').append('<td>庭审过程</td>');
                        $('#des_process').append('<td>'+html2doc[id]["庭审过程"]+'</td>');

                        // 法院意见
                        $("#des_opinion").empty();
                        $('#des_opinion').append('<td>法院意见</td>');
                        $('#des_opinion').append('<td>'+html2doc[id]["法院意见"]+'</td>');

                        // 判决结果
                        $("#des_result").empty();
                        $('#des_result').append('<td>判决结果</td>');
                        $('#des_result').append('<td>'+html2doc[id]["判决结果"]+'</td>');

                        // 争议焦点
                        $("#des_result").empty();
                        $('#des_result').append('<td>争议焦点</td>');
                        $('#des_result').append('<td>'+""+'</td>');


                        $('#tb_description').css('visibility', 'visible');
                    });

                    $('#tb_result_coarse').css('visibility', 'visible');
                }

            
                // console.log("ok");
                // $('tr[id="result_'+i+'"]').each(function(){
                //     console.log(i);
                //     // var current = $(this);
                //     // current.click(function(){
                //     //     console.log(current.text());
                //     //     i = current.attr("id");
                //     //     console.log(html2doc);
                //     //     console.log(i);
                //     //     console.log(html2doc[i]);
                //     //     $('#des_title').append('<td>'+html2doc[i]["标题"]+'</td>');
                //     // });
                // });
            },
            error:function(xhr,status,error){
                console.log(status);
                console.log(error);
            }
        });
    });
});


// 点击抽取按钮，抽取文本内容
$(document).ready(function(){
    $("#btn_extract").click(function(){
        var description = $("#description").val();                    // 案情描述
        var data = {description: description};
        console.log(data);
        $.ajax({
            url: base_url + "/extract",
            type: "PUT",
            // contentType: "application/json",
            dataType: "json",
            data: data,
            success:function(msg){
                // 先清空
                $('input[type="checkbox"]').prop('checked', false);
                // 重新打勾
                console.log(msg);
                for(key in msg){
                    for(var value of msg[key]){
                        $('input[name="'+key+'"][value="'+value+'"]').prop('checked', true);
                    }
                }
            },
            error:function(xhr,status,error){
                console.log(status);
                console.log(error);
            }
        });
    });
});




// 案件库读取案件
function get_all_docs(){
    $.ajax({
        url: base_url + "/all_docs",
        type: "PUT",
        // contentType: "application/json",
        dataType: "json",
        data: "",
        success:function(msg){
            for(var i=0; i<msg.length; i++){
                // 在表格上追加
                html = '<tr id="result_' + i + '">' +   
                       '<td>' + msg[i]["案号"]  + '</td>' +
                       '<td>' + msg[i]["标题"]  + '</td>' +
                       '</tr>';
                $('#tb_result_lib').append(html);
                html2doc[i] = msg[i];

                $('#tb_result_lib').on("click", "#result_"+i, function(){
                    var id = $(this).attr("id").split("_")[1];

                    // 标题
                    $("#des_title").empty();
                    $('#des_title').append('<td>标题</td>');
                    $('#des_title').append('<td>'+html2doc[id]["标题"]+'</td>');

                    // 案号
                    $("#des_id").empty();
                    $('#des_id').append('<td>案号</td>');
                    $('#des_id').append('<td>'+html2doc[id]["案号"]+'</td>');

                    // 案由
                    $("#des_cause").empty();
                    $('#des_cause').append('<td>案由</td>');
                    $('#des_cause').append('<td>'+html2doc[id]["案由"]+'</td>');

                    // 来源
                    $("#des_source").empty();
                    $('#des_source').append('<td>来源</td>');
                    $('#des_source').append('<td>'+html2doc[id]["来源"]+'</td>');

                    // 审理法院
                    $("#des_court").empty();
                    $('#des_court').append('<td>审理法院</td>');
                    $('#des_court').append('<td>'+html2doc[id]["审理法院"]+'</td>');

                    // 审判员
                    $("#des_judge").empty();
                    $('#des_judge').append('<td>审判员</td>');
                    $('#des_judge').append('<td>'+html2doc[id]["审判员"]+'</td>');

                    // 书记员
                    $("#des_clerk").empty();
                    $('#des_clerk').append('<td>书记员</td>');
                    $('#des_clerk').append('<td>'+html2doc[id]["书记员"]+'</td>');

                    // 当事人
                    $("#des_party").empty();
                    $('#des_party').append('<td>当事人</td>');
                    $('#des_party').append('<td>'+html2doc[id]["当事人"]+'</td>');

                    // 庭审过程
                    $("#des_process").empty();
                    $('#des_process').append('<td>庭审过程</td>');
                    $('#des_process').append('<td>'+html2doc[id]["庭审过程"]+'</td>');

                    // 法院意见
                    $("#des_opinion").empty();
                    $('#des_opinion').append('<td>法院意见</td>');
                    $('#des_opinion').append('<td>'+html2doc[id]["法院意见"]+'</td>');

                    // 判决结果
                    $("#des_result").empty();
                    $('#des_result').append('<td>判决结果</td>');
                    $('#des_result').append('<td>'+html2doc[id]["判决结果"]+'</td>');


                    $('#tb_description').css('visibility', 'visible');
                });

                $('#tb_result_lib').css('visibility', 'visible');
            }

        },
        error:function(xhr,status,error){
            console.log(status);
            console.log(error);
        }
    });
}