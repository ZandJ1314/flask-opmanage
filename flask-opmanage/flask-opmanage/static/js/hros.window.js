/*
**  应用窗口
*/
HROS.window = (function(){
	return {
		/*
		**  创建窗口
		**  自定义窗口：HROS.window.createTemp({title,url,width,height,resize,isflash});
		**      后面参数依次为：标题、地址、宽、高、是否可拉伸、是否打开默认最大化、是否为flash
		**      示例：HROS.window.createTemp({title:"百度",url:"http://www.baidu.com",width:800,height:400,isresize:false,isopenmax:false,isflash:false});
		*/
		createTemp : function(obj){
			$('.popup-menu').hide();
			$('.quick_view_container').remove();
			var type = 'app', appid = obj.appid == null ? Date.parse(new Date()) : obj.appid;
			//判断窗口是否已打开
			var iswindowopen = false;
			$('#task-content-inner a.task-item').each(function(){
				if($(this).attr('appid') == appid){
					iswindowopen = true;
					HROS.window.show2top(appid);
				}
			});
			//如果没有打开，则进行创建
			if(iswindowopen == false){
				function nextDo(options){
					var windowId = '#w_' + options.appid;
					//新增任务栏
					$('#task-content-inner').prepend(taskTemp({
						'type' : options.type,
						'id' : 't_' + options.appid,
						'appid' : options.appid,
						'title' : options.title,
						'imgsrc' : options.imgsrc
					}));
					$('#task-content-inner').css('width', $('#task-content-inner .task-item').length * 114);
					HROS.taskbar.resize();
					//新增窗口
					TEMP.windowTemp = {
						'width' : options.width,
						'height' : options.height,
						'top' : ($(window).height() - options.height) / 2 <= 0 ? 0 : ($(window).height() - options.height) / 2,
						'left' : ($(window).width() - options.width) / 2 <= 0 ? 0 : ($(window).width() - options.width) / 2,
						'emptyW' : $(window).width() - options.width,
						'emptyH' : $(window).height() - options.height,
						'zIndex' : HROS.CONFIG.createIndexid,
						'type' : options.type,
						'id' : 'w_' + options.appid,
						'appid' : options.appid,
						'realappid' : 0,
						'title' : options.title,
						'url' : options.url,
						'imgsrc' : options.imgsrc,
						'isresize' : options.isresize,
						'isopenmax' : options.isopenmax,
						'istitlebar' : options.isresize,
						'istitlebarFullscreen' : options.isresize ? window.fullScreenApi.supportsFullScreen == true ? true : false : false,
						'issetbar' : options.issetbar,
						'isflash' : options.isflash
					};
					$('#desk').append(windowTemp(TEMP.windowTemp));
					$(windowId).data('info', TEMP.windowTemp);
					HROS.CONFIG.createIndexid += 1;
					//iframe加载完毕后
					$(windowId).find('iframe').on('load', function(){
						if(options.isresize){
							//绑定窗口拉伸事件
							HROS.window.resize($(windowId));
						}
						//隐藏loading
						$(windowId + ' .window-frame').children('div').eq(1).fadeOut();
					});
					$(windowId).on('contextmenu',function(){
						return false;
					});
					//绑定窗口上各个按钮事件
					HROS.window.handle($(windowId));
					//绑定窗口移动
					HROS.window.move($(windowId));
					//绑定窗口遮罩层点击事件
					$('.window-mask').off('click').on('click', function(){
						HROS.window.show2top($(this).parents('.window-container').attr('appid'));
					});
					HROS.window.show2top(options.appid);
				}
				nextDo({
					type : type,
					appid : appid,
					imgsrc : 'static/image/ui/default_icon.png',
					title : obj.title,
					url : obj.url,
					width : obj.width,
					height : obj.height,
					isresize : typeof obj.isresize == 'undefined' ? false : obj.isresize,
					isopenmax : typeof obj.isopenmax == 'undefined' ? false : obj.isopenmax,
					issetbar : false,
					isflash : typeof obj.isflash == 'undefined' ? true : obj.isflash
				});
			}else{
				//如果设置强制刷新
				if(obj.refresh){
					var windowId = '#w_' + appid;
					$(windowId).find('iframe').attr('src', obj.url);
				}
			}
		},
		/*
		**  创建窗口
		**  系统窗口：HROS.window.create(appid);
		**      示例：HROS.window.create(12);
		*/
		mycreate : function(obj){
			$('.popup-menu').hide();
			$('.quick_view_container').remove();
			//判断窗口是否已打开
			var iswindowopen = false;
			$('#task-content-inner a.task-item').each(function(){
				if($(this).attr('appid') == obj.attr('appid')){
					iswindowopen = true;
					HROS.window.show2top(obj.attr('appid'));
				}
			});
			//如果没有打开，则进行创建
			if(iswindowopen == false && $('#d_' + obj.attr('appid')).attr('opening') != 1){
				$('#d_' + obj.attr('appid')).attr('opening', 1);
				function nextDo(options){
					var windowId = '#w_' + options.appid;
					var top = ($(window).height() - options.height) / 2 <= 0 ? 0 : ($(window).height() - options.height) / 2;
					var left = ($(window).width() - options.width) / 2 <= 0 ? 0 : ($(window).width() - options.width) / 2;
					switch(options.type){
						case 'app':
						case 'papp':
							//新增任务栏
							$('#task-content-inner').prepend(taskTemp({
								'type' : options.type,
								'id' : 't_' + options.appid,
								'appid' : options.appid,
								'title' : options.title,
								'imgsrc' : options.imgsrc
							}));
							$('#task-content-inner').css('width', $('#task-content-inner .task-item').length * 114);
							HROS.taskbar.resize();
							//新增窗口
							TEMP.windowTemp = {
								'width' : options.width,
								'height' : options.height,
								'top' : top,
								'left' : left,
								'emptyW' : $(window).width() - options.width,
								'emptyH' : $(window).height() - options.height,
								'zIndex' : HROS.CONFIG.createIndexid,
								'type' : options.type,
								'id' : 'w_' + options.appid,
								'appid' : options.appid,
								'realappid' : options.realappid,
								'title' : options.title,
								'url' : options.url,
								'imgsrc' : options.imgsrc,
								'isresize' : options.isresize == 1 ? true : false,
								'isopenmax' :  options.isopenmax == 1 ? true : false,
								'istitlebar' : options.isresize == 1 ? true : false,
								'istitlebarFullscreen' : options.isresize == 1 ? window.fullScreenApi.supportsFullScreen == true ? true : false : false,
								'issetbar' : options.issetbar == 1 ? true : false,
								'isflash' : options.isflash == 1 ? true : false
							};
							$('#desk').append(windowTemp(TEMP.windowTemp));
							$(windowId).data('info', TEMP.windowTemp);
							HROS.CONFIG.createIndexid += 1;
							//iframe加载完毕后
							$(windowId + ' iframe').on('load', function(){
								if(options.isresize){
									//绑定窗口拉伸事件
									HROS.window.resize($(windowId));
								}
								//隐藏loading
								$(windowId + ' .window-frame').children('div').eq(1).fadeOut();
							});
							$(windowId).on('contextmenu',function(){
								return false;
							});
							//绑定窗口上各个按钮事件
							HROS.window.handle($(windowId));
							//绑定窗口移动
							HROS.window.move($(windowId));
							//绑定窗口遮罩层点击事件
							$('.window-mask').off('click').on('click', function(){
								HROS.window.show2top($(this).parents('.window-container').attr('appid'));
							});
							HROS.window.show2top(options.appid);
							break;

					}
				}
				ZENG.msgbox.show('应用正在加载中，请耐心等待...', 6, 100000);
				ZENG.msgbox._hide();
					nextDo({
						type : 'app',
						id : obj.attr('id'),
						appid : obj.attr('appid'),
						realappid : obj.attr('appid'),
						title : obj.attr('title'),
						imgsrc : obj.children("div").children("img").attr("src"),
						url : obj.attr('url'),
						width : obj.attr('width'),
						height : obj.attr('height'),
						isresize : obj.attr('isresize') == undefined ? 0 : obj.attr('isresize'),
						isopenmax : obj.attr('isopenmax') == undefined ? 0 : obj.attr('isopenmax'),
						issetbar : true,
						isflash : obj.attr('isflash') == 'true' ? true:false
					});
				
					$('#d_' + obj.attr('appid')).attr('opening', 0);
				
			}
		},
		/*
		**  创建窗口
		**  系统窗口：HROS.window.create(appid);
		**      示例：HROS.window.create(12);
		*/
		create : function(appid){
			$('.popup-menu').hide();
			$('.quick_view_container').remove();
			//判断窗口是否已打开
			var iswindowopen = false;
			$('#task-content-inner a.task-item').each(function(){
				if($(this).attr('appid') == appid){
					iswindowopen = true;
					HROS.window.show2top(appid);
				}
			});
			//如果没有打开，则进行创建
			if(iswindowopen == false && $('#d_' + appid).attr('opening') != 1){
				$('#d_' + appid).attr('opening', 1);
				function nextDo(options){
					var windowId = '#w_' + options.appid;
					var top = ($(window).height() - options.height) / 2 <= 0 ? 0 : ($(window).height() - options.height) / 2;
					var left = ($(window).width() - options.width) / 2 <= 0 ? 0 : ($(window).width() - options.width) / 2;
					switch(options.type){
						case 'app':
						case 'papp':
							//新增任务栏
							$('#task-content-inner').prepend(taskTemp({
								'type' : options.type,
								'id' : 't_' + options.appid,
								'appid' : options.appid,
								'title' : options.title,
								'imgsrc' : options.imgsrc
							}));
							$('#task-content-inner').css('width', $('#task-content-inner .task-item').length * 114);
							HROS.taskbar.resize();
							//新增窗口
							TEMP.windowTemp = {
								'width' : options.width,
								'height' : options.height,
								'top' : top,
								'left' : left,
								'emptyW' : $(window).width() - options.width,
								'emptyH' : $(window).height() - options.height,
								'zIndex' : HROS.CONFIG.createIndexid,
								'type' : options.type,
								'id' : 'w_' + options.appid,
								'appid' : options.appid,
								'realappid' : options.realappid,
								'title' : options.title,
								'url' : options.url,
								'imgsrc' : options.imgsrc,
								'isresize' : options.isresize == 1 ? true : false,
								'isopenmax' : options.isresize == 1 ? options.isopenmax == 1 ? true : false : false,
								'istitlebar' : options.isresize == 1 ? true : false,
								'istitlebarFullscreen' : options.isresize == 1 ? window.fullScreenApi.supportsFullScreen == true ? true : false : false,
								'issetbar' : options.issetbar == 1 ? true : false,
								'isflash' : options.isflash == 1 ? true : false
							};
							$('#desk').append(windowTemp(TEMP.windowTemp));
							$(windowId).data('info', TEMP.windowTemp);
							HROS.CONFIG.createIndexid += 1;
							//iframe加载完毕后
							$(windowId + ' iframe').on('load', function(){
								if(options.isresize){
									//绑定窗口拉伸事件
									HROS.window.resize($(windowId));
								}
								//隐藏loading
								$(windowId + ' .window-frame').children('div').eq(1).fadeOut();
							});
							$(windowId).on('contextmenu',function(){
								return false;
							});
							//绑定窗口上各个按钮事件
							HROS.window.handle($(windowId));
							//绑定窗口移动
							HROS.window.move($(windowId));
							//绑定窗口遮罩层点击事件
							$('.window-mask').off('click').on('click', function(){
								HROS.window.show2top($(this).parents('.window-container').attr('appid'));
							});
							HROS.window.show2top(options.appid);
							break;

					}
				}
				ZENG.msgbox.show('应用正在加载中，请耐心等待...', 6, 100000);
				ZENG.msgbox._hide();
					nextDo({
						type : 'app',
						id : '1',
						appid : '2',
						realappid : '1',
						title : '秦美人后台',
						
						url : 'http://qmrht.moloong.com',
						width : 1024,
						height : 768,
						isresize : true,
						isopenmax : false,
						issetbar : true,
						isflash : false
					});
				
					$('#d_' + appid).attr('opening', 0);
				
			}
		},
		close : function(appid){
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			$(windowId).removeData('info').html('').remove();
			$('#task-content-inner ' + taskId).html('').remove();
			$('#task-content-inner').css('width', $('#task-content-inner .task-item').length * 114);
			$('#task-bar, #nav-bar').removeClass('min-zIndex');
			HROS.taskbar.resize();
		},
		closeAll : function(){
			$('#desk .window-container').each(function(){
				HROS.window.close($(this).attr('appid'));
			});
		},
		hide : function(appid){
			HROS.window.show2top(appid);
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			$(windowId).css('left', '-10000px').attr('state', 'hide');
			$('#task-content-inner ' + taskId).removeClass('task-item-current');
			if($(windowId).attr('ismax') == 1){
				$('#task-bar, #nav-bar').removeClass('min-zIndex');
			}
		},
		hideAll : function(){
			$('#task-content-inner a.task-item').removeClass('task-item-current');
			$('#desk-' + HROS.CONFIG.desk).nextAll('div.window-container').css('left', -10000).attr('state', 'hide');
		},
		max : function(appid){
			HROS.window.show2top(appid);
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			$(windowId + ' .title-handle .ha-max').hide().next(".ha-revert").show();
			$(windowId).addClass('window-maximize').attr('ismax',1).animate({
				width : '100%',
				height : '100%',
				top : 0,
				left : 0
			}, 200);
			$('#task-bar, #nav-bar').addClass('min-zIndex');
		},
		revert : function(appid){
			HROS.window.show2top(appid);
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			$(windowId + ' .title-handle .ha-revert').hide().prev('.ha-max').show();
			var obj = $(windowId), windowdata = obj.data('info');
			obj.removeClass('window-maximize').attr('ismax',0).animate({
				width : windowdata['width'],
				height : windowdata['height'],
				left : windowdata['left'],
				top : windowdata['top']
			}, 500);
			$('#task-bar, #nav-bar').removeClass('min-zIndex');
		},
		refresh : function(appid){
			HROS.window.show2top(appid);
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			//判断是应用窗口，还是文件夹窗口
			if($(windowId + '_iframe').length != 0){
				$(windowId + '_iframe').attr('src', $(windowId + '_iframe').attr('src'));
			}else{
				HROS.window.updateFolder(appid);
			}
		},
		show2top : function(appid){
			HROS.window.show2under();
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			var windowdata = $(windowId).data('info');
			//改变当前任务栏样式
			$('#task-content-inner ' + taskId).addClass('task-item-current');
			if($(windowId).attr('ismax') == 1){
				$('#task-bar, #nav-bar').addClass('min-zIndex');
			}
			//改变当前窗口样式
			$(windowId).addClass('window-current').css({
				'z-index' : HROS.CONFIG.createIndexid,
				'left' : windowdata['left'],
				'top' : windowdata['top']
			}).attr('state', 'show');
			//如果窗口最小化前是最大化状态的，则坐标位置设为0
			if($(windowId).attr('ismax') == 1){
				$(windowId).css({
					'left' : 0,
					'top' : 0
				});
			}
			//改变当前窗口遮罩层样式
			$(windowId + ' .window-mask').hide();
			//改变当前iframe显示
			$(windowId + ' iframe').show();
			HROS.CONFIG.createIndexid += 1;
		},
		show2under : function(){
			//改变任务栏样式
			$('#task-content-inner a.task-item').removeClass('task-item-current');
			//改变窗口样式
			$('#desk .window-container').removeClass('window-current');
			//改变窗口遮罩层样式
			$('#desk .window-container .window-mask').show();
			//改变iframe显示
			$('#desk .window-container-flash iframe').hide();
		},
		updateFolder : function(appid){
			HROS.window.show2top(appid);
			var windowId = '#w_' + appid, taskId = '#t_' + appid;
			$.getJSON(ajaxUrl + '?ac=getMyFolderApp&folderid=' + appid, function(sc){
				if(sc != null){
					var folder_append = '';
					for(var i = 0; i < sc.length; i++){
						folder_append += appbtnTemp({
							'top' : 0,
							'left' : 0,
							'title' : sc[i]['name'],
							'type' : sc[i]['type'],
							'id' : 'd_' + sc[i]['appid'],
							'appid' : sc[i]['appid'],
							'imgsrc' : sc[i]['icon']
						});
					}
					$(windowId).find('.folder_body').html('').append(folder_append).on('contextmenu', '.appbtn', function(e){
						$('.popup-menu').hide();
						$('.quick_view_container').remove();
						TEMP.AppRight = HROS.popupMenu.app($(this));
						var l = ($(document).width() - e.clientX) < TEMP.AppRight.width() ? (e.clientX - TEMP.AppRight.width()) : e.clientX;
						var t = ($(document).height() - e.clientY) < TEMP.AppRight.height() ? (e.clientY - TEMP.AppRight.height()) : e.clientY;
						TEMP.AppRight.css({
							left : l,
							top : t
						}).show();
						return false;
					});
					HROS.app.move();
				}
			});
		},
		handle : function(obj){
			obj.on('dblclick', '.title-bar', function(e){
				//判断当前窗口是否已经是最大化
				if(obj.find('.ha-max').is(':hidden')){
					obj.find('.ha-revert').click();
				}else{
					obj.find('.ha-max').click();
				}
			}).on('click', '.ha-hide', function(){
				HROS.window.hide(obj.attr('appid'));
			}).on('click', '.ha-max', function(){
				HROS.window.max(obj.attr('appid'));
			}).on('click', '.ha-revert', function(){
				HROS.window.revert(obj.attr('appid'));
			}).on('click', '.ha-fullscreen', function(){
				window.fullScreenApi.requestFullScreen(document.getElementById(obj.find('iframe').attr('id')));
			}).on('click', '.ha-close', function(){
				HROS.window.close(obj.attr('appid'));
			}).on('click', '.refresh', function(){
				HROS.window.refresh(obj.attr('appid'));
			}).on('click', '.help', function(){
				if(obj.attr('realappid') !== 0){
					HROS.window.createTemp({
						appid : 'hoorayos-yysc',
						title : '应用市场',
						url : 'sysapp/appmarket/index.php?id=' + obj.attr('realappid'),
						width : 800,
						height : 484,
						isflash : false,
						refresh : true
					});
				}else{
					ZENG.msgbox.show('对不起，该应用没有任何详细介绍', 1, 2000);
				}
			}).on('click', '.star', function(){
				$.ajax({
					type : 'POST',
					url : ajaxUrl,
					data : 'ac=getAppStar&id=' + obj.data('info').appid,
					success : function(point){
						$.dialog({
							title : '给“' + obj.data('info').title + '”打分',
							width : 250,
							id : 'star',
							content : starDialogTemp({
								'point' : Math.floor(point),
								'realpoint' : point * 20
							})
						});
						$('#star ul').data('appid', obj.data('info').appid);
					}
				});
				$('body').off('click').on('click', '#star ul li', function(){
					var num = $(this).attr('num');
					var appid = $(this).parent('ul').data('appid');
					if(!isNaN(num) && /^[1-5]$/.test(num)){
						$.ajax({
							type : 'POST',
							url : ajaxUrl,
							data : 'ac=updateAppStar&id=' + appid + '&starnum=' + num,
							success : function(msg){
								art.dialog.list['star'].close();
								if(msg){
									ZENG.msgbox.show("打分成功！", 4, 2000);
								}else{
									ZENG.msgbox.show("你已经打过分了！", 1, 2000);
								}
							}
						});
					}
				});
			}).on('contextmenu', '.window-container', function(){
				$('.popup-menu').hide();
				$('.quick_view_container').remove();
				return false;
			});
		},
		move : function(obj){
			obj.on('mousedown', '.title-bar', function(e){
				if(obj.attr('ismax') == 1){
					return false;
				}
				HROS.window.show2top(obj.attr('appid'));
				var windowdata = obj.data('info'), lay, x, y;
				x = e.clientX - obj.offset().left;
				y = e.clientY - obj.offset().top;
				//绑定鼠标移动事件
				$(document).on('mousemove', function(e){
					lay = HROS.maskBox.desk();
					lay.show();
					//强制把右上角还原按钮隐藏，最大化按钮显示
					obj.find('.ha-revert').hide().prev('.ha-max').show();
					_l = e.clientX - x;
					_t = e.clientY - y;
					_w = windowdata['width'];
					_h = windowdata['height'];
					//窗口贴屏幕顶部10px内 || 底部60px内
					_t = _t <= 10 ? 0 : _t >= lay.height()-30 ? lay.height()-30 : _t;
					obj.css({
						width : _w,
						height : _h,
						left : _l,
						top : _t
					});
					obj.data('info').left = obj.offset().left;
					obj.data('info').top = obj.offset().top;
				}).on('mouseup', function(){
					$(this).off('mousemove').off('mouseup');
					if(typeof(lay) !== 'undefined'){
						lay.hide();
					}
				});
			});
		},
		resize : function(obj){
			obj.find('div.window-resize').on('mousedown', function(e){
				//增加背景遮罩层
				var resizeobj = $(this), lay, x = e.clientX, y = e.clientY, w = obj.width(), h = obj.height();
				$(document).on('mousemove', function(e){
					lay = HROS.maskBox.desk();
					lay.show();
					_x = e.clientX;
					_y = e.clientY;
					//当拖动到屏幕边缘时，自动贴屏
					_x = _x <= 10 ? 0 : _x >= (lay.width()-12) ? (lay.width()-2) : _x;
					_y = _y <= 10 ? 0 : _y >= (lay.height()-12) ? lay.height() : _y;
					switch(resizeobj.attr('resize')){
						case 't':
							h + y - _y > HROS.CONFIG.windowMinHeight ? obj.css({
								height : h + y - _y,
								top : _y
							}) : obj.css({
								height : HROS.CONFIG.windowMinHeight
							});
							break;
						case 'r':
							w - x + _x > HROS.CONFIG.windowMinWidth ? obj.css({
								width : w - x + _x
							}) : obj.css({
								width : HROS.CONFIG.windowMinWidth
							});
							break;
						case 'b':
							h - y + _y > HROS.CONFIG.windowMinHeight ? obj.css({
								height : h - y + _y
							}) : obj.css({
								height : HROS.CONFIG.windowMinHeight
							});
							break;
						case 'l':
							w + x - _x > HROS.CONFIG.windowMinWidth ? obj.css({
								width : w + x - _x,
								left : _x
							}) : obj.css({
								width : HROS.CONFIG.windowMinWidth
							});
							break;
						case 'rt':
							h + y - _y > HROS.CONFIG.windowMinHeight ? obj.css({
								height : h + y - _y,
								top : _y
							}) : obj.css({
								height : HROS.CONFIG.windowMinHeight
							});
							w - x + _x > HROS.CONFIG.windowMinWidth ? obj.css({
								width : w - x + _x
							}) : obj.css({
								width : HROS.CONFIG.windowMinWidth
							});
							break;
						case 'rb':
							w - x + _x > HROS.CONFIG.windowMinWidth ? obj.css({
								width : w - x + _x
							}) : obj.css({
								width : HROS.CONFIG.windowMinWidth
							});
							h - y + _y > HROS.CONFIG.windowMinHeight ? obj.css({
								height : h - y + _y
							}) : obj.css({
								height : HROS.CONFIG.windowMinHeight
							});
							break;
						case 'lt':
							w + x - _x > HROS.CONFIG.windowMinWidth ? obj.css({
								width : w + x - _x,
								left : _x
							}) : obj.css({
								width : HROS.CONFIG.windowMinWidth
							});
							h + y - _y > HROS.CONFIG.windowMinHeight ? obj.css({
								height : h + y - _y,
								top : _y
							}) : obj.css({
								height : HROS.CONFIG.windowMinHeight
							});
							break;
						case 'lb':
							w + x - _x > HROS.CONFIG.windowMinWidth ? obj.css({
								width : w + x - _x,
								left : _x
							}) : obj.css({
								width : HROS.CONFIG.windowMinWidth
							});
							h - y + _y > HROS.CONFIG.windowMinHeight ? obj.css({
								height : h - y + _y
							}) : obj.css({
								height : HROS.CONFIG.windowMinHeight
							});
							break;
					}
				}).on('mouseup',function(){
					if(typeof(lay) !== 'undefined'){
						lay.hide();
					}
					obj.data('info').width = obj.width();
					obj.data('info').height = obj.height();
					obj.data('info').left = obj.offset().left;
					obj.data('info').top = obj.offset().top;
					obj.data('info').emptyW = $(window).width() - obj.width();
					obj.data('info').emptyH = $(window).height() - obj.height();
					$(this).off('mousemove').off('mouseup');
				});
			});
		}
	}
})();