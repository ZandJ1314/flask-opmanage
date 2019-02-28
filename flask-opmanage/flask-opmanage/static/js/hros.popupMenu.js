/*
**  右键菜单
*/
HROS.popupMenu = (function(){
	return {
		/*
		**  应用图标右键
		*/
		app : function(obj){
			HROS.window.show2under();
			if(!TEMP.popupMenuApp){
				TEMP.popupMenuApp = $('<div class="popup-menu app-menu" style="z-index:9990;display:none"><ul><li style="border-bottom:1px solid #F0F0F0"><a menu="open" href="javascript:;">打开应用</a></li><li><a menu="move" href="javascript:;">移动应用到<b class="arrow">»</b></a><div class="popup-menu" style="display:none"><ul><li><a menu="moveto" desk="1" href="javascript:;">桌面1</a></li><li><a menu="moveto" desk="2" href="javascript:;">桌面2</a></li><li><a menu="moveto" desk="3" href="javascript:;">桌面3</a></li><li><a menu="moveto" desk="4" href="javascript:;">桌面4</a></li><li><a menu="moveto" desk="5" href="javascript:;">桌面5</a></li></ul></div></li><li><b class="edit"></b><a menu="edit" href="javascript:;">编辑</a></li><li><b class="uninstall"></b><a menu="del" href="javascript:;">卸载应用</a></li></ul></div>');
				$('body').append(TEMP.popupMenuApp);
				$('.app-menu').on('contextmenu', function(){
					return false;
				});
			}
			$('.app-menu a[menu="moveto"]').removeClass('disabled');
			if(obj.parent().hasClass('desktop-container')){
				$('.app-menu a[menu="moveto"]').each(function(){
					if($(this).attr('desk') == HROS.CONFIG.desk){
						$(this).addClass('disabled');
					}
				});
			}
			//绑定事件
			$('.app-menu li').off('mouseover').off('mouseout').on('mouseover', function(){
				if($(this).children('a').attr('menu') == 'move'){
					$(this).children('a').addClass('focus');
					if($(document).width() - $('.app-menu').offset().left > 250){
						$(this).children('div').css({
							left : 122,
							top : -2
						});
					}else{
						$(this).children('div').css({
							left : -126,
							top : -2
						});
					}
					$(this).children('div').show();
				}
			}).on('mouseout', function(){
				$(this).children('a').removeClass('focus');
				$(this).children('div').hide();
			});
			$('.app-menu a[menu="moveto"]').off('click').on('click', function(){
				var desk = $(this).attr('desk');
				$.ajax({
					type : 'POST',
					url : ajaxUrl,
					data : 'ac=moveMyApp&id=' + obj.attr('appid') + '&todesk=' + desk,
					success : function(){
						$('#desk-' + desk + ' li.add').before(obj);
						HROS.deskTop.appresize();
						HROS.app.getScrollbar();
					}
				});
				$('.popup-menu').hide();
			});
			$('.app-menu a[menu="open"]').off('click').on('click', function(){
				HROS.window.create(obj.attr('appid'), obj.attr('type'));
				$('.task-menu').hide();
			});
			$('.app-menu a[menu="edit"]').off('click').on('click', function(){
				$.dialog.open('sysapp/dialog/app.php?id=' + obj.attr('appid'), {
					id : 'editdialog',
					title : '编辑应用“' + obj.children('span').text() + '”',
					width : 570,
					height : 350
				});
				$('.popup-menu').hide();
			});
			$('.app-menu a[menu="del"]').off('click').on('click', function(){
				HROS.app.remove(obj.attr('appid'), function(){
					obj.find('img, span').show().animate({
						opacity : 'toggle',
						width : 0,
						height : 0
					}, 500, function(){
						obj.remove();
						HROS.deskTop.resize(250);
					});
				});
				$('.popup-menu').hide();
			});
			return TEMP.popupMenuApp;
		},
		papp : function(obj){
			HROS.window.show2under();
			if(!TEMP.popupMenuPapp){
				TEMP.popupMenuPapp = $('<div class="popup-menu papp-menu" style="z-index:9990;display:none"><ul><li style="border-bottom:1px solid #F0F0F0"><a menu="open" href="javascript:;">打开应用</a></li><li><a menu="move" href="javascript:;">移动应用到<b class="arrow">»</b></a><div class="popup-menu" style="display:none"><ul><li><a menu="moveto" desk="1" href="javascript:;">桌面1</a></li><li><a menu="moveto" desk="2" href="javascript:;">桌面2</a></li><li><a menu="moveto" desk="3" href="javascript:;">桌面3</a></li><li><a menu="moveto" desk="4" href="javascript:;">桌面4</a></li><li><a menu="moveto" desk="5" href="javascript:;">桌面5</a></li></ul></div></li><li><b class="edit"></b><a menu="edit" href="javascript:;">编辑</a></li><li><b class="del"></b><a menu="del" href="javascript:;">删除应用</a></li></ul></div>');
				$('body').append(TEMP.popupMenuPapp);
				$('.papp-menu').on('contextmenu', function(){
					return false;
				});
			}
			$('.papp-menu a[menu="moveto"]').removeClass('disabled');
			if(obj.parent().hasClass('desktop-container')){
				$('.papp-menu a[menu="moveto"]').each(function(){
					if($(this).attr('desk') == HROS.CONFIG.desk){
						$(this).addClass('disabled');
					}
				});
			}
			//绑定事件
			$('.papp-menu li').off('mouseover').off('mouseout').on('mouseover', function(){
				if($(this).children('a').attr('menu') == 'move'){
					$(this).children('a').addClass('focus');
					if($(document).width() - $('.papp-menu').offset().left > 250){
						$(this).children('div').css({
							left : 122,
							top : -2
						});
					}else{
						$(this).children('div').css({
							left : -126,
							top : -2
						});
					}
					$(this).children('div').show();
				}
			}).on('mouseout', function(){
				$(this).children('a').removeClass('focus');
				$(this).children('div').hide();
			});
			$('.papp-menu a[menu="moveto"]').off('click').on('click', function(){
				var desk = $(this).attr('desk');
				$.ajax({
					type : 'POST',
					url : ajaxUrl,
					data : 'ac=moveMyApp&id=' + obj.attr('appid') + '&todesk=' + desk,
					success : function(){
						$('#desk-' + desk + ' li.add').before(obj);
						HROS.deskTop.appresize();
						HROS.app.getScrollbar();
					}
				});
				$('.popup-menu').hide();
			});
			$('.papp-menu a[menu="open"]').off('click').on('click', function(){
				switch(obj.attr('type')){
					case 'papp':
						HROS.window.create(obj.attr('appid'), obj.attr('type'));
						break;
					case 'pwidget':
						HROS.widget.create(obj.attr('appid'), obj.attr('type'));
						break;
				}
				$('.popup-menu').hide();
			});
			$('.papp-menu a[menu="edit"]').off('click').on('click', function(){
				$.dialog.open('sysapp/dialog/papp.php?id=' + obj.attr('appid'), {
					id : 'editdialog',
					title : '编辑私人应用“' + obj.children('span').text() + '”',
					width : 600,
					height : 450
				});
				$('.popup-menu').hide();
			});
			$('.papp-menu a[menu="del"]').off('click').on('click', function(){
				HROS.app.remove(obj.attr('appid'), function(){
					obj.find('img, span').show().animate({
						opacity : 'toggle',
						width : 0,
						height : 0
					}, 500, function(){
						obj.remove();
						HROS.deskTop.resize(250);
					});
				});
				$('.popup-menu').hide();
			});
			return TEMP.popupMenuPapp;
		},
		/*
		**  文件夹右键
		*/
		folder : function(obj){
			HROS.window.show2under();
			if(!TEMP.popupMenuFolder){
				TEMP.popupMenuFolder = $('<div class="popup-menu folder-menu" style="z-index:9990;display:none"><ul><li><a menu="view" href="javascript:;">预览</a></li><li style="border-bottom:1px solid #F0F0F0"><a menu="open" href="javascript:;">打开</a></li><li><b class="edit"></b><a menu="rename" href="javascript:;">重命名</a></li><li><b class="del"></b><a menu="del" href="javascript:;">删除</a></li></ul></div>');
				$('body').append(TEMP.popupMenuFolder);
				$('.folder-menu').on('contextmenu', function(){
					return false;
				});
			}
			//绑定事件
			$('.folder-menu a[menu="view"]').off('click').on('click', function(){
				HROS.folderView.init(obj);
				$('.popup-menu').hide();
			});
			$('.folder-menu a[menu="open"]').off('click').on('click', function(){
				HROS.window.create(obj.attr('appid'), obj.attr('type'));
				$('.popup-menu').hide();
			});
			$('.folder-menu a[menu="del"]').off('click').on('click', function(){
				$.dialog({
					id : 'delfolder',
					title : '删除“' + obj.find('span').text() + '”文件夹',
					content : '删除文件夹的同时会删除文件夹内所有应用',
					icon : 'warning',
					ok : function(){
						HROS.app.remove(obj.attr('appid'), function(){
							obj.find('img, span').show().animate({
								opacity : 'toggle',
								width : 0,
								height : 0
							}, 500, function(){
								obj.remove();
								HROS.deskTop.resize(250);
							});
						});
					},
					cancel : true
				});
				$('.popup-menu').hide();
			});
			$('.folder-menu a[menu="rename"]').off('click').on('click', function(){
				$.dialog({
					id : 'addfolder',
					title : '重命名“' + obj.find('span').text() + '”文件夹',
					padding : 0,
					content : editFolderDialogTemp({
						'name' : obj.find('span').text(),
						'src' : obj.find('img').attr('src')
					}),
					ok : function(){
						if($('#folderName').val() != ''){
							$.ajax({
								type : 'POST',
								url : ajaxUrl,
								data : 'ac=updateFolder&name=' + $('#folderName').val() + '&icon=' + $('.folderSelector img').attr('src') + '&id=' + obj.attr('appid'),
								success : function(){
									HROS.app.get();
								}
							});
						}else{
							$('.folderNameError').show();
							return false;
						}
					},
					cancel : true
				});
				$('.folderSelector').off('click').on('click', function(){
					$('.fcDropdown').show();
				});
				$('.fcDropdown_item').off('click').on('click', function(){
					$('.folderSelector img').attr('src', $(this).children('img').attr('src')).attr('idx', $(this).children('img').attr('idx'));
					$('.fcDropdown').hide();
				});
				$('.popup-menu').hide();
			});
			return TEMP.popupMenuFolder;
		},
		/*
		**  任务栏右键
		*/
		task : function(obj){
			HROS.window.show2under();
			if(!TEMP.popupMenuTask){
				TEMP.popupMenuTask = $('<div class="popup-menu task-menu" style="z-index:9990;display:none"><ul><li><a menu="max" href="javascript:;">最大化</a></li><li style="border-bottom:1px solid #F0F0F0"><a menu="hide" href="javascript:;">最小化</a></li><li><a menu="close" href="javascript:;">关闭</a></li></ul></div>');
				$('body').append(TEMP.popupMenuTask);
				$('.task-menu').on('contextmenu', function(){
					return false;
				});
			}
			//绑定事件
			$('.task-menu a[menu="max"]').off('click').on('click', function(){
				HROS.window.max(obj.attr('appid'), obj.attr('type'));
				$('.popup-menu').hide();
			});
			$('.task-menu a[menu="hide"]').off('click').on('click', function(){
				HROS.window.hide(obj.attr('appid'), obj.attr('type'));
				$('.popup-menu').hide();
			});
			$('.task-menu a[menu="close"]').off('click').on('click', function(){
				HROS.window.close(obj.attr('appid'), obj.attr('type'));
				$('.popup-menu').hide();
			});
			return TEMP.popupMenuTask;
		},
		/*
		**  桌面右键
		*/
		desk : function(){
			HROS.window.show2under();
			if(!TEMP.popupMenuDesk){
				TEMP.popupMenuDesk = $('<div class="popup-menu desk-menu" style="z-index:9990;display:none"><ul><li><a menu="hideall" href="javascript:;">显示桌面</a></li><li style="border-bottom:1px solid #F0F0F0"><a menu="closeall" href="javascript:;">关闭所有应用</a></li><li><a href="javascript:;">新建<b class="arrow">»</b></a><div class="popup-menu" style="display:none"><ul><li><b class="folder"></b><a menu="addfolder" href="javascript:;">新建文件夹</a></li><li><b class="customapp"></b><a menu="addpapp" href="javascript:;">新建私人应用</a></li></ul></div></li><!--li style="border-bottom:1px solid #F0F0F0"><b class="upload"></b><a menu="uploadfile" href="javascript:;">上传文件</a></li--><li><b class="themes"></b><a menu="themes" href="javascript:;">主题设置</a></li><li><b class="setting"></b><a menu="setting" href="javascript:;">桌面设置</a></li><li style="border-bottom:1px solid #F0F0F0"><a href="javascript:;">图标设置<b class="arrow">»</b></a><div class="popup-menu" style="display:none"><ul><li><b class="hook"></b><a menu="orderby" orderby="x" href="javascript:;">横向排列</a></li><li><b class="hook"></b><a menu="orderby" orderby="y" href="javascript:;">纵向排列</a></li></ul></div></li><li><a menu="logout" href="javascript:;">注销</a></li></ul></div>');
				$('body').append(TEMP.popupMenuDesk);
				$('.desk-menu').on('contextmenu', function(){
					return false;
				});
				//绑定事件
				$('.desk-menu li').on('mouseover', function(){
					if($(this).children('a').next() != ''){
						$(this).children('a').addClass('focus');
						if($(document).width() - $('.desk-menu').offset().left > 250){
							$(this).children('div').css({
								left : 122,
								top : -2
							});
						}else{
							$(this).children('div').css({
								left : -126,
								top : -2
							});
						}
						$(this).children('div').show();
					}
				}).on('mouseout', function(){
					$(this).children('a').removeClass('focus');
					$(this).children('div').hide();
				});
				$('.desk-menu a[menu="orderby"]').on('click', function(){
					var xy = $(this).attr('orderby');
					if(HROS.CONFIG.appXY != xy){
						HROS.app.updateXY(xy, function(){
							HROS.deskTop.appresize();
							HROS.app.getScrollbar();
						});
					}
					$('.popup-menu').hide();
				});
				$('.desk-menu a[menu="hideall"]').on('click', function(){
					HROS.window.hideAll();
					$('.popup-menu').hide();
				});
				$('.desk-menu a[menu="closeall"]').on('click', function(){
					HROS.window.closeAll();
					$('.popup-menu').hide();
				});
				$('.desk-menu a[menu="addfolder"]').on('click', function(){
					$.dialog({
						id : 'addfolder',
						title : '新建文件夹',
						padding : 0,
						content : editFolderDialogTemp({
							'name' : '新建文件夹',
							'src' : 'img/ui/folder_default.png'
						}),
						ok : function(){
							if($('#folderName').val() != ''){
								$.ajax({
									type : 'POST',
									url : ajaxUrl,
									data : 'ac=addFolder&name=' + $('#folderName').val() + '&icon=' + $('.folderSelector img').attr('src') + '&desk=' + HROS.CONFIG.desk,
									success : function(){
										HROS.app.get();
									}
								});
							}else{
								$('.folderNameError').show();
								return false;
							}
						},
						cancel : true
					});
					$('.folderSelector').on('click', function(){
						$('#addfolder .fcDropdown').show();
						return false;
					});
					$(document).click(function(){
						$('#addfolder .fcDropdown').hide();
					});
					$('.fcDropdown_item').on('click', function(){
						$('.folderSelector img').attr('src', $(this).children('img').attr('src')).attr('idx', $(this).children('img').attr('idx'));
						$('#addfolder .fcDropdown').hide();
					});
					$('.popup-menu').hide();
				});
				$('.desk-menu a[menu="addpapp"]').on('click', function(){
					$.dialog.open('sysapp/dialog/papp.php?desk=' + HROS.CONFIG.desk, {
						id : 'editdialog',
						title : '新建私人应用',
						width : 600,
						height : 450
					});
					$('.popup-menu').hide();
				});
				$('.desk-menu a[menu="uploadfile"]').on('click', function(){
					HROS.uploadFile.getDialog();
					$('.popup-menu').hide();
				});
				$('.desk-menu a[menu="themes"]').on('click', function(){
					HROS.window.createTemp({
						appid : 'hoorayos-ztsz',
						title : '主题设置',
						url : 'sysapp/wallpaper/index.php',
						width : 580,
						height : 520,
						isflash : false
					});
					$('.popup-menu').hide();
				});
				$('.desk-menu a[menu="setting"]').on('click', function(){
					HROS.window.createTemp({
						appid : 'hoorayos-zmsz',
						title : '桌面设置',
						url : 'sysapp/desksetting/index.php',
						width : 750,
						height : 450,
						isflash : false
					});
					$('.popup-menu').hide();
				});
				$('.desk-menu a[menu="logout"]').on('click', function(){
					HROS.base.logout();
					$('.popup-menu').hide();
				});
			}
			$('.desk-menu a[menu="orderby"]').each(function(){
				$(this).prev().hide();
				if($(this).attr('orderby') == HROS.CONFIG.appXY){
					$(this).prev().show();
				}
				$('.popup-menu').hide();
			});
			return TEMP.popupMenuDesk;
		}
	}
})();