var api_get_data = "next";
var api_submit_data = "chain";
var api_submit_dispute = "commit";


// 标注部分全局变量
var curr_id = "FaxinClass1_id4";
var curr_page = 0;
var yg_evidence = new Array();
var bg_evidence = new Array();
var yg_suqiu = new Array();
var bg_biancheng = new Array();
var trials = "";
var disputes = new Array();
var ret_disputes = new Array();

// 标注页标注结果
var tag_page_1 = new Array();
var tag_page_2 = new Array();
var tag_page_3 = new Array();
var tag_page_4 = new Array();
var tag_page_5 = new Array();
var tag_page_6 = new Array();
var tag_page_7 = new Array();
var tag_page_8 = new Array();

// 标注阶段，总共两个阶段，第一阶段前7标注内容，第二阶段争议焦点
var tagging_stage = 0;

// 获取目前页面已经标注的内容，填入相应全局变量
function collect_tagging(){
    if(curr_page == 1){
        tag_page_1 = new Array();
        for(i in yg_suqiu){
            tag_page_1[i] = $("#input_1_"+i).val();
        }
    }else if(curr_page == 2){
        tag_page_2 = new Array();
        for(i in bg_evidence){
            tag_page_2[i] = $("#input_2_"+i).val();
        }
    }else if(curr_page == 3){
        tag_page_3 = new Array();
        for(i in bg_biancheng){
            tag_page_3[i] = $("#input_3_"+i).val();
        }
    }else if(curr_page == 4){
        tag_page_4 = new Array();
        for(i in bg_evidence){
            tag_page_4[i] = $("#input_4_"+i).val();
        }
    }else if(curr_page == 5){
        tag_page_5 = new Array();
        for(i in bg_biancheng){
            tag_page_5[i] = $("#input_5_"+i).val();
        }
    }else if(curr_page == 6){
        tag_page_6 = new Array();
        for(i in bg_biancheng){
            tag_page_6[i] = $("#input_6_"+i).val();
        }
    }else if(curr_page == 7){
        tag_page_7 = new Array();
        for(i in yg_suqiu){
            num = parseInt($("input[name='input_7_"+i+"']:checked").val());
            if (num != null){
                tag_page_7[i] = num;
            }else{
                tag_page_7[i] = -1;
            }
        }
    }else if(curr_page == 8){
        tag_page_8 = new Array();
        for(i in bg_biancheng){
            tag_page_8[i] = parseInt($("input[name='input_8_"+i+"']:checked").val());
            if(tag_page_8[i] == 0){
                ret_disputes.push(disputes[i]);
            }
        }
    }
}


// 获取案件
function get_law_case(){

    var data = {id: curr_id};

    $.ajax({
        url: api_get_data,
        type: "PUT",
        // contentType: "application/json",
        // dataType: "json",
        data: data,
        success:function(msg){

            console.log(msg);
            tagging_stage = 0;
            // 文书详情
            doc = msg["文书详情"];
            curr_id = doc["ID"];

            // 标题
            $("#des_title").empty();
            $("#des_title").append("<td>标题</td>");
            $("#des_title").append("<td>"+doc["标题"]+"</td>");
            // 案号
            $("#des_id").empty();
            $("#des_id").append("<td>案号</td>");
            $("#des_id").append("<td>"+doc["案号"]+"</td>");
            // 标题
            $("#des_cause").empty();
            $("#des_cause").append("<td>案由</td>");
            $("#des_cause").append("<td>"+doc["案由"]+"</td>");
            // 标题
            $("#des_source").empty();
            $("#des_source").append("<td>来源</td>");
            $("#des_source").append("<td>"+doc["来源"]+"</td>");
            // 标题
            $("#des_court").empty();
            $("#des_court").append("<td>审理法院</td>");
            $("#des_court").append("<td>"+doc["审理法院"]+"</td>");
            // 标题
            $("#des_judge").empty();
            $("#des_judge").append("<td>审判员</td>");
            $("#des_judge").append("<td>"+doc["审判员"]+"</td>");
            // 标题
            $("#des_clerk").empty();
            $("#des_clerk").append("<td>书记员</td>");
            $("#des_clerk").append("<td>"+doc["书记员"]+"</td>");
            // 标题
            $("#des_party").empty();
            $("#des_party").append("<td>当事人</td>");
            $("#des_party").append("<td>"+doc["当事人"]+"</td>");
            // 标题
            $("#des_process").empty();
            $("#des_process").append("<td>庭审过程</td>");
            $("#des_process").append("<td>"+doc["庭审过程"].replace(/\n/g, "<br>")+"</td>");
            // 标题
            $("#des_opinion").empty();
            $("#des_opinion").append("<td>法院意见</td>");
            $("#des_opinion").append("<td>"+doc["法院意见"].replace(/\n/g, "<br>")+"</td>");
            // 标题
            $("#des_result").empty();
            $("#des_result").append("<td>判决结果</td>");
            $("#des_result").append("<td>"+doc["判决结果"].replace(/\n/g, "<br>")+"</td>");

            tag_page_1 = new Array();
            tag_page_2 = new Array();
            tag_page_3 = new Array();
            tag_page_4 = new Array();
            tag_page_5 = new Array();
            tag_page_6 = new Array();
            tag_page_7 = new Array();
            tag_page_8 = new Array();

            // 标注部分
            yg_evidence = msg["原告证据"];
            bg_evidence = msg["被告证据"];
            yg_suqiu = msg["诉求"];
            bg_biancheng = msg["辩称"];
            trials = doc["判决结果"];
            disputes = new Array();
            ret_disputes = new Array();
            // 导航目录
            $("#page_panel").show();
            // 自动点击第一页
            $("#tagging_title").empty();
            $("#tagging_title").append("原告证据-原告诉求");
            // ol left
            $("#tagging_page_left").empty();
            $("#tagging_page_left").append('<ol id="ol_left"></ol>');
            $("#tagging_page_left").append('<ol id="ol_left_2"></ol>');
            for(i in yg_evidence){
                html = "<li>" + yg_evidence[i] + "</li>";
                $("#ol_left").append(html);
            }
            // ol right
            $("#tagging_page_right").empty();
            $("#tagging_page_right").append('<ol id="ol_right"></ol>');
            $("#tagging_page_right").append('<ol id="ol_right_2"></ol>');
            for(i in yg_suqiu){
                html = "<li>" + yg_suqiu[i] + '<input type="text" class="form-control" id="input_1_'+i+'" placeholder="输入相关原告证据编号，空格隔开">' + "</li>";
                $("#ol_right").append(html);
                if(tag_page_1.length >= i)
                    $("#input_1_"+i).val(tag_page_1[i]);
            // ol center
            $("#tagging_page_center").empty();
            $("#tagging_page_center").append('<ol id="ol_center"></ol>');
            }
            curr_page = 1;
        },
        error:function(xhr,status,error){
            console.log(status);
            console.log(error);
        }
    });
}




function strArray_to_2dArray(arr){
    for(i in arr){
        arr[i] = arr[i].split(" ").map(function(data){
            return +data;
        });
    }
    return JSON.stringify(arr);
}

// 提交标注
function submit_tagging(){


    collect_tagging();

    var data = {
        "ID": curr_id,
        "rel_plainev_ap": strArray_to_2dArray(tag_page_1),
        "rel_plain_defen": strArray_to_2dArray(tag_page_2),
        "rel_plainev_ar": strArray_to_2dArray(tag_page_3),
        "rel_defenev_ap": strArray_to_2dArray(tag_page_4),
        "rel_ap_ar": strArray_to_2dArray(tag_page_5),
        "rel_defenev_ar": strArray_to_2dArray(tag_page_6),
        "appeal_class": JSON.stringify(tag_page_7),
    };
    console.log("submit data:");
    console.log(data);

    $.ajax({
        url: api_submit_data,
        type: "PUT",
        // contentType: "application/json",
        dataType: "json",
        data: data,
        success:function(msg){
            console.log(msg);
            tagging_stage = 1;
            $("#page_panel").hide();
            $("#tagging_title").empty();

            // ol_left
            $("#ol_left").empty();
            $("#ol_left").before("<h3 class='text-center'>原告证据</h3>")
            for(i in yg_evidence){
                html = "<li>" + yg_evidence[i] + "</li>";
                $("#ol_left").append(html);
            }
            $("#ol_left_2").before("<h3 class='text-center'>原告诉求</h3>")
            for(i in yg_suqiu){
                html = "<li>" + yg_suqiu[i] + "</li>";
                $("#ol_left_2").append(html);
            }

            // ol_right
            $("#ol_right").empty();
            $("#ol_right").before("<h3 class='text-center'>被告证据</h3>")
            for(i in bg_evidence){
                html = "<li>" + bg_evidence[i] + "</li>";
                $("#ol_right").append(html);
            }
            $("#ol_right_2").before("<h3 class='text-center'>被告辩称</h3>")
            for(i in bg_biancheng){
                html = "<li>" + bg_biancheng[i] + "</li>";
                $("#ol_right_2").append(html);
            }

            // ol_center
            $("#ol_center").before("<h3 class='text-center'>争议焦点</h3>")
            $("#ol_center").empty();
            for(i in msg){
                disputes[i] = msg[i];
                var yg_e = msg[i][0];
                var bg_e = msg[i][1];
                var yg_s = msg[i][2];
                var bg_b = msg[i][3];
                var chain = new Array();
                if(yg_e != -1){
                    chain.push("原告证据"+(yg_e));
                }
                if(yg_s != -1){
                    chain.push("原告诉求"+(yg_s));
                }
                if(bg_e != -1){
                    chain.push("被告证据"+(bg_e));
                }
                if(bg_b != -1){
                    chain.push("被告辩称"+(bg_b));
                }
                chain = chain.join("-");

                html = "<div class='col-sm-12'>" +
                       "<li><div class='col-sm-6'>" + chain + "</div>" +
                       '<div class="col-sm-6">' +
                       '<input type="radio" name="input_8_'+i+'" value="0"> 存在争议焦点' +
                       '<input type="radio" name="input_8_'+i+'" value="1"> 不存在争议焦点' +
                       "</div></li></div>"
                $("#ol_center").append(html);
            }
            curr_page = 8;
        },
        error:function(xhr,status,error){
            console.log(status);
            console.log(error);
        }
    });
}


// 提交争议焦点
function submit_dispute(){

    collect_tagging();
    var data = {
        "id": curr_id,
        "chains": JSON.stringify(ret_disputes)
    };
    console.log(data);

    $.ajax({
        url: api_submit_dispute,
        type: "PUT",
        // contentType: "application/json",
        dataType: "json",
        data: data,
        success:function(msg){
            get_law_case();
        },
        error:function(xhr,status,error){
            console.log(status);
            console.log(error);
        }
    });
}

$(document).ready(function(){

    // page_1 原告证据-原告诉求
    $("#page_1").click(function(){
        collect_tagging();
        $("#tagging_title").empty();
        $("#tagging_title").append("原告证据-原告诉求");
        // ol left
        $("#ol_left").empty();
        for(i in yg_evidence){
            html = "<li>" + yg_evidence[i] + "</li>";
            $("#ol_left").append(html);
        }
        // ol right
        $("#ol_right").empty();
        for(i in yg_suqiu){
            html = "<li>" + yg_suqiu[i] + '<input type="text" class="form-control" id="input_1_'+i+'" placeholder="输入相关原告证据编号，空格隔开">' + "</li>";
            $("#ol_right").append(html);
            if(tag_page_1.length >= i)
                $("#input_1_"+i).val(tag_page_1[i]);
        }
        curr_page = 1;
    });

    // page_2 原告证据-被告证据
    $("#page_2").click(function(){
        collect_tagging();
        $("#tagging_title").empty();
        $("#tagging_title").append("原告证据-被告证据");
        // ol left
        $("#ol_left").empty();
        for(i in yg_evidence){
            html = "<li>" + yg_evidence[i] + "</li>";
            $("#ol_left").append(html);
        }
        // ol right
        $("#ol_right").empty();
        for(i in bg_evidence){
            html = "<li>" + bg_evidence[i] + '<input type="text" class="form-control" id="input_2_'+i+'"  placeholder="输入相关原告证据编号，空格隔开">' + "</li>";
            $("#ol_right").append(html);
            if(tag_page_2.length >= i)
                $("#input_2_"+i).val(tag_page_2[i]);
        }
        curr_page = 2;
    });

    // page_3 原告证据-被告辩称
    $("#page_3").click(function(){
        collect_tagging();
        $("#tagging_title").empty();
        $("#tagging_title").append("原告证据-被告辩称");
        // ol left
        $("#ol_left").empty();
        for(i in yg_evidence){
            html = "<li>" + yg_evidence[i] + "</li>";
            $("#ol_left").append(html);
        }
        // ol right
        $("#ol_right").empty();
        for(i in bg_biancheng){
            html = "<li>" + bg_biancheng[i] + '<input type="text" class="form-control" id="input_3_'+i+'"  placeholder="输入相关原告证据编号，空格隔开">' + "</li>";
            $("#ol_right").append(html);
            if(tag_page_3.length >= i)
                $("#input_3_"+i).val(tag_page_3[i]);
        }
        curr_page = 3;
    });

    // page_4 原告诉求-被告证据
    $("#page_4").click(function(){
        collect_tagging();
        $("#tagging_title").empty();
        $("#tagging_title").append("原告诉求-被告证据");
        // ol left
        $("#ol_left").empty();
        for(i in yg_suqiu){
            html = "<li>" + yg_suqiu[i] + "</li>";
            $("#ol_left").append(html);
        }
        // ol right
        $("#ol_right").empty();
        for(i in bg_evidence){
            html = "<li>" + bg_evidence[i] + '<input type="text" class="form-control" id="input_4_'+i+'"  placeholder="输入相关原告诉求编号，空格隔开">' + "</li>";
            $("#ol_right").append(html);
            if(tag_page_4.length >= i)
                $("#input_4_"+i).val(tag_page_4[i]);
        }
        curr_page = 4;
    });

    // page_5 原告诉求-被告辩称
    $("#page_5").click(function(){
        collect_tagging();
        $("#tagging_title").empty();
        $("#tagging_title").append("原告诉求-被告辩称");
        // ol left
        $("#ol_left").empty();
        for(i in yg_suqiu){
            html = "<li>" + yg_suqiu[i] + "</li>";
            $("#ol_left").append(html);
        }
        // ol right
        $("#ol_right").empty();
        for(i in bg_biancheng){
            html = "<li>" + bg_biancheng[i] + '<input type="text" class="form-control" id="input_5_'+i+'"  placeholder="输入相关原告诉求编号，空格隔开">' + "</li>";
            $("#ol_right").append(html);
            if(tag_page_5.length >= i)
                $("#input_5_"+i).val(tag_page_5[i]);
        }
        curr_page = 5;
    });

    // page_6 被告证据-被告辩称
    $("#page_6").click(function(){
        collect_tagging();
        $("#tagging_title").empty();
        $("#tagging_title").append("被告证据-被告辩称");
        // ol left
        $("#ol_left").empty();
        for(i in bg_evidence){
            html = "<li>" + bg_evidence[i] + "</li>";
            $("#ol_left").append(html);
        }
        // ol right
        $("#ol_right").empty();
        for(i in bg_biancheng){
            html = "<li>" + bg_biancheng[i] + '<input type="text" class="form-control" id="input_6_'+i+'"  placeholder="输入相关被告证据编号，空格隔开">' + "</li>";
            $("#ol_right").append(html);
            if(tag_page_6.length >= i)
                $("#input_6_"+i).val(tag_page_6[i]);
        }
        curr_page = 6;
    });

    // page_7 诉求判别
    $("#page_7").click(function(){
        collect_tagging();
        $("#tagging_title").empty();
        $("#tagging_title").append("审判结果-原告诉求");
        // ol left
        $("#ol_left").empty();
        html = "<li>" + trials + "</li>";
        $("#ol_left").append(html);

        // ol right
        $("#ol_right").empty();
        for(i in yg_suqiu){
            html = "<li>" + yg_suqiu[i]
                   + '<div class="col-sm-12">'
                   + '<input type="radio" name="input_7_'+i+'" value="2"> 支持&nbsp;'
                   + '<input type="radio" name="input_7_'+i+'" value="1"> 部分支持&nbsp;'
                   + '<input type="radio" name="input_7_'+i+'" value="0"> 驳回 '
                   + "</div></li>";
            $("#ol_right").append(html);
            if(tag_page_7.length >= i)
                $("input:radio[name='input_7_"+i+"'][value="+tag_page_7[i]+"]").attr("checked", "true");
        }
        curr_page = 7;
    });


    $("#skip_btn").click(function(){
        get_law_case();
    });

    $("#submit_btn").click(function(){
        if(tagging_stage == 0){
            submit_tagging();
        }else if(tagging_stage == 1){
            submit_dispute();
        }
    });

    get_law_case();
});


