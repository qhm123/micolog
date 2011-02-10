$(document).ready(function(){  
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
                	alert('请输入你的名字!');
                    form.author.focus();
                    return false;
                }
                if (!form.email.value) {
                    alert('请输入邮件地址');
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
            	alert('请输入留言内容');
                form.comment.focus();
                return false;
            }
            
            $("#submit").attr('disabled', true);
            $("#submit").val('正在提交留言……');
            
            return true;
        },
        success: function(data){
            $("#submit").attr('disabled', false);
            $("#submit").val('提交');
            $('#checkret').val('');
            $('#check').load('/checkcode/');
            if (data[0]) {
                add_comment(data[1]);
                alert('留言提交成功！');
                $('#comment').val('');
                location = "#comments";
            }else{
				if(data[1] == -102){
					alert('验证码错误。');
				}
				$('#checkret').focus();
			}
        }
    });
})

function get_check_area(type){
    $('#check').load('/checkcode/');
    $('#checkarea').show();
}

function add_comment(msg){
    comment = $(msg)
    $("#commentlist").prepend(comment);
    $("#cancel-comment-reply-link").click();
}

function backcomment(author, id){
    backdb = document.getElementById('comment');
    backdb.focus();
    backdb.value = backdb.value + '<a href=\"#comment-' + id + '\">@' + author + '<\/a>' + '\n';
    return false;
}