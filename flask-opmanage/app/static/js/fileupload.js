//res文件上传
jQuery(function() {
    var $ = jQuery,
        $list = $('#resthelist'),
        $btn = $('#resctlBtn'),
        state = 'pending',
        uploader;

    uploader = WebUploader.create({
        swf: '../static/js/Uploader.swf',
        server: '/fileUpload',
        pick: '#respicker',
		accept: {
			title : 'zip',
			extensions : 'zip',
			mimeTypes: 'zip/*'
		}
    });

    // 当有文件添加进来的时候
    uploader.on( 'fileQueued', function( file ) {
		var curTotalFile = $('#totalFile').val();
		$('#totalFile').val(curTotalFile+"1");
		$('#isupload').val("no");
        $list.append('<div id="' + file.id + '" class="item">' +
				'<h4 class="info">' + file.name + '</h4>' +
				'<p class="state">文件MD5计算中...</p>' +
				'</div>');
		uploader.md5File( file )
		.then(function(val) {
				$list.find('p.state').text('MD5计算完毕'+val+'，等待上传...');
				$('#fileMd5').val(val);
			});
    });

    // 文件上传过程中创建进度条实时显示。
    uploader.on( 'uploadProgress', function( file, percentage ) {
        var $li = $( '#'+file.id ),
            $percent = $li.find('.progress .progress-bar');

        // 避免重复创建
        if ( !$percent.length ) {
            $percent = $('<div class="progress progress-striped active">' +
              '<div class="progress-bar" role="progressbar" style="width: 0%">' +
              '</div>' +
            '</div>').appendTo( $li ).find('.progress-bar');
        }

        $li.find('p.state').text('上传中');

        $percent.css( 'width', percentage * 100 + '%' );
    });

    uploader.on( 'uploadSuccess', function( file ) {
        $( '#'+file.id ).find('p.state').text('已上传');
		$('#isupload').val("yes");
    });

    uploader.on( 'uploadError', function( file ) {
        $( '#'+file.id ).find('p.state').text('上传出错');
    });

    uploader.on( 'uploadComplete', function( file ) {
        $( '#'+file.id ).find('.progress').fadeOut();
    });

    uploader.on( 'all', function( type ) {
        if ( type === 'startUpload' ) {
            state = 'uploading';
        } else if ( type === 'stopUpload' ) {
            state = 'paused';
        } else if ( type === 'uploadFinished' ) {
            state = 'done';
        }

        if ( state === 'uploading' ) {
            $btn.text('暂停上传');
        } else {
            $btn.text('开始上传');
        }
    });

    $btn.on( 'click', function() {
		var uploadTotalfile = $('#totalFile').val();
		if (uploadTotalfile.length > 1){
			bootstrapAlert("只能上传一个文件")
		}else{
			if ( state === 'uploading' ) {
				uploader.stop();
			} else {
				uploader.upload();
			}
		}
    });
});
