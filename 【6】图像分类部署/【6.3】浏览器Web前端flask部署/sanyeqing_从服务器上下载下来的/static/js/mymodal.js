// 更新用户设置
function update_usershezhi() {
    var thumbnailInput = $('#FileUpload1')[0];
    var avatar = null;
    if (thumbnailInput.files && thumbnailInput.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var base64ImageData = e.target.result;
            var base64Data = base64ImageData.replace(/^data:image\/\w+;base64,/, "");
            var avatar = encodeURIComponent(base64Data);

            // 调用提交文章的函数，传入缩略图编码
            user_update(avatar);
        };

        reader.readAsDataURL(thumbnailInput.files[0]); // 开始读取文件
    } else {
        // 如果没有上传新的图片，可以保持原有图片或传递一个空值给服务器
        user_update(avatar);
    }
}


//提交图片设置
function submit_photos() {
    var thumbnailInput = $('#file0')[0];
    if (!(thumbnailInput.files && thumbnailInput.files[0])) {
        thumbnailInput = $('#file1')[0];
    }
    if (thumbnailInput.files && thumbnailInput.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var base64ImageData = e.target.result;
            var base64Data = base64ImageData.replace(/^data:image\/\w+;base64,/, "");
            var encodedThumbnail = encodeURIComponent(base64Data);

            // 调用提交文章的函数，传入缩略图编码
            submitphotos_add(encodedThumbnail);
        };

        reader.readAsDataURL(thumbnailInput.files[0]); // 开始读取文件
    } else {
        // 处理没有选择文件的情况
        bootbox.alert({title: "错误提示", message: "请选择提交图片."});
        // alert('错误')
    }
}
function submit_photos_ye() {
    var thumbnailInput = $('#file0')[0];
    if (!(thumbnailInput.files && thumbnailInput.files[0])) {
        thumbnailInput = $('#file1')[0];
    }
    if (thumbnailInput.files && thumbnailInput.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var base64ImageData = e.target.result;
            var base64Data = base64ImageData.replace(/^data:image\/\w+;base64,/, "");
            var encodedThumbnail = encodeURIComponent(base64Data);

            // 调用提交文章的函数，传入缩略图编码
            submitphotos_add_ye(encodedThumbnail);
        };

        reader.readAsDataURL(thumbnailInput.files[0]); // 开始读取文件
    } else {
        // 处理没有选择文件的情况
        bootbox.alert({title: "错误提示", message: "请选择提交图片."});
        // alert('错误')
    }
}


//
// //编辑工具设置
// function editor_tools() {
//     var thumbnailInput = $('#upload_ico')[0];
//     if (thumbnailInput.files && thumbnailInput.files[0]) {
//         var reader = new FileReader();
//
//         reader.onload = function (e) {
//             var base64ImageData = e.target.result;
//             var base64Data = base64ImageData.replace(/^data:image\/\w+;base64,/, "");
//             var encodedThumbnail = encodeURIComponent(base64Data);
//
//             // 调用提交文章的函数，传入缩略图编码
//             editortools_add(encodedThumbnail);
//         };
//
//         reader.readAsDataURL(thumbnailInput.files[0]); // 开始读取文件
//     } else {
//         // 处理没有选择文件的情况
//         // bootbox.alert({title: "错误提示", message: "请选择工具设置图例."});
//         alert('请选择为工具设置图标')
//     }
// }

