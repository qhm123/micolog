$(document).ready(function(){
    $('.commentlist li .comments .commentcontent').each(function(){
        $(this).html(showsmiles($(this).html()));
    });
    
	loadjs=false;
    commentuser = $.cookie('comment_user');
    if (commentuser) {
        //[user,email,url]=commentuser.split('#@#');
        data = commentuser.split('#@#');
        $('#author').val(data[0]);
        $('#email').val(data[1]);
        $('#url').val(data[2]);
    };
    $('#check').load('/checkcode/');
    
    $('#commentform').ajaxForm({
        type: 'post',
        dataType: 'json',
        beforeSubmit: function(formData, jqForm, options){
            var form = jqForm[0];
            if (form.author) {
                if (!form.author.value) {
                    showinfo('请输入你的名字!');
                    form.author.focus();
                    return false;
                }
                if (!form.email.value) {
                    showinfo('请输入邮件地址');
                    form.email.focus();
                    return false;
                }
            }
            
			if($('#checkarea').css('display') == 'block'){
				if(!form.checkret.value){
					alert('请输入验证码！');
					form.checkret.focus();
					return false;
				}
			}

            if (!form.comment.value) {
                showinfo('请输入留言内容');
                form.comment.focus();
                return false;
            }
            
            $("#submit").attr('disabled', true);
            $("#submit").val('正在提交留言……');
            
            return true;
        },
        success: function(data){
            $("#submit").attr('disabled', false);
            if (data[0]) {
                /*document.cookie=data[2];*/
                alert('留言提交成功！');
                $("#submit").val('提交');
                add_comment(data[1]);
                
                //$('#s_msg').text('留言提交成功！');
                $('#comment').val('');
                if($('#checkarea').css('display') == 'block'){
                    if($("#check_type").val() > 0){
                    	get_check_area($("#check_type").val());
                    }
                }
                $('#checkret').val('');
                location = "#comments";
            }else{
				if(data[1] == -102){
					showinfo('验证码错误。');
				}
				$('#s_msg').text('留言提交失败！');
				$('#checkret').focus();
			}
        }
    });
})

function get_check_area(type){
    if (type == 1) {
        $('#check').load('/checkcode/');
        $('#checkarea').show();
    }
    else if (type == 2) {
        $('#check').html('<img id="checkimg" src="/checkimg/" style="border:0px;padding:0;float:left;margin-right:8px" title="点击图片切换" onclick="reloadCheckImage();"/>');
        $('#checkarea').show();
    }
}

function reloadCheckImage(){
    var img = document.getElementById('checkimg');
    img.src += "?";
}

function add_comment(msg){
    comment = $(msg)
    if (!loadjs) {
        $("#commentlist").prepend(comment).show();
        $.getScript("http://dev.jquery.com/view/trunk/plugins/color/jquery.color.js", function(){
            comment.animate({
                backgroundColor: '#fbc7c7'
            }, "slow").animate({
                backgroundColor: 'white'
            }, "slow")
            loadjs = true;
        });
    }
    else {
        $("#commentlist").prepend(comment);
        comment.animate({
            backgroundColor: '#fbc7c7'
        }, "slow").animate({
            backgroundColor: 'white'
        }, "slow")
    }
}

function backcomment(author, id){
    backdb = document.getElementById('comment');
    backdb.focus();
    backdb.value = backdb.value + '<a href=\"#comment-' + id + '\">@' + author + '<\/a>' + '\n';
    return false;
}

function showinfo(msg){
    alert(msg);
}

//以下表情
function grin(tag){
    if (typeof tinyMCE != 'undefined') {
        grin_tinymcecomments(tag);
    }
    else {
        grin_plain(tag);
    }
}

function grin_tinymcecomments(tag){
    tinyMCE.execCommand('mceInsertContent', false, ' ' + tag + ' ');
}

function grin_plain(tag){
    var myField;
    var myCommentTextarea = "comment";
    tag = ' ' + tag + ' ';
    if (document.getElementById(myCommentTextarea) && document.getElementById(myCommentTextarea).type == 'textarea') {
        myField = document.getElementById(myCommentTextarea);
    }
    else {
        return false;
    }
    if (document.selection) {
        myField.focus();
        sel = document.selection.createRange();
        sel.text = tag;
        myField.focus();
    }
    else 
        if (myField.selectionStart || myField.selectionStart == '0') {
            var startPos = myField.selectionStart;
            var endPos = myField.selectionEnd;
            var cursorPos = endPos;
            myField.value = myField.value.substring(0, startPos) +
            tag +
            myField.value.substring(endPos, myField.value.length);
            cursorPos += tag.length;
            myField.focus();
            myField.selectionStart = cursorPos;
            myField.selectionEnd = cursorPos;
        }
        else {
            myField.value += tag;
            myField.focus();
        }
}

function showsmiles(content){
    return content.replace(/\^~/ig, "<img src=http://hikeimg.appspot.com/static/images/icon/icon_").replace(/~\^/ig, '.gif />');
}