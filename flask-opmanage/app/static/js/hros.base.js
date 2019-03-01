/*
**  一个不属于其他模块的模块
*/
HROS.base = (function(){
	return {
		/*
		**	系统初始化
		*/
		init : function(){
			//更新当前用户ID
			HROS.CONFIG.memberID = $.cookie('memberID');
			//文件上传
			//HROS.uploadFile.init();
			//增加离开页面确认窗口，IE不支持，故屏蔽
			//if(!$.browser.msie){
			//	window.onbeforeunload = Util.confirmExit;
			//}
			//绑定body点击事件，主要目的就是为了强制隐藏右键菜单
			$('#desktop').on('click', function(){
				$('.popup-menu').hide();
				$('.quick_view_container').remove();
			});
			//隐藏浏览器默认右键菜单
			$('body').on('contextmenu', function(){
				$(".popup-menu").hide();
				return false;
			});
			//绑定浏览器resize事件
			HROS.base.resize();
			//用于判断网页是否缩放，该功能提取自QQ空间
			HROS.zoom.init();
			//初始化分页栏
			HROS.navbar.init();
			//绑定任务栏点击事件
			HROS.taskbar.init();
			//获得dock的位置
			
			HROS.dock.getPos(function(){
				//获取图标排列顺序
				HROS.app.getXY(function(){
					/*
					**      当dockPos为top时          当dockPos为left时         当dockPos为right时
					**  -----------------------   -----------------------   -----------------------
					**  | o o o         dock  |   | o | o               |   | o               | o |
					**  -----------------------   | o | o               |   | o               | o |
					**  | o o                 |   | o | o               |   | o               | o |
					**  | o +                 |   |   | o               |   | o               |   |
					**  | o             desk  |   |   | o         desk  |   | o         desk  |   |
					**  | o                   |   |   | +               |   | +               |   |
					**  -----------------------   -----------------------   -----------------------
					**  因为desk区域的尺寸和定位受dock位置的影响，所以加载图标前必须先定位好dock的位置
					*/
					HROS.app.get();
				});
			});	
			
			//加载壁纸
			HROS.wallpaper.get(function(){
				HROS.wallpaper.set();
			});
			//绑定应用码头2个按钮的点击事件
			$('.dock-tool-logout').on('mousedown', function(){
				return false;
			}).on('click',function(){
				HROS.base.logout();
			});
			$('.dock-tool-setting').on('mousedown', function(){
				return false;
			}).on('click', function(){
				
				HROS.window.createTemp({
					appid : 'hoorayos-ztsz',
					title : $(this).attr("title"),
					url : '/changePassword',
					width : 580,
					height : 520,
					isflash : false
				});
			});
			//桌面右键
			/*
			$('#desk').on('contextmenu', function(e){
				$(".popup-menu").hide();
				$('.quick_view_container').remove();
				var popupmenu = HROS.popupMenu.desk();
				l = ($(document).width() - e.clientX) < popupmenu.width() ? (e.clientX - popupmenu.width()) : e.clientX;
				t = ($(document).height() - e.clientY) < popupmenu.height() ? (e.clientY - popupmenu.height()) : e.clientY;
				popupmenu.css({
					left : l,
					top : t
				}).show();
				return false;
			});
			*/
			//还原widget
			//HROS.widget.reduction();
			//加载新手帮助
			HROS.base.help();
			//配置artDialog全局默认参数
			(function(config){
				config['lock'] = true;
				config['fixed'] = true;
				config['resize'] = false;
				config['background'] = '#000';
				config['opacity'] = 0.5;
			})($.dialog.defaults);
		},
		logout : function(){
			$.dialog({
				title: '退出',
				icon: 'question',
				width: 320,
				content: '确定退出？',
				cancel: true,
				ok:function(){
					location.href = '/logout';
				}
			});
		},
		resize : function(){
			$(window).on('resize', function(){
				HROS.deskTop.resize(200);
			});
		},
		getSkin : function(callback){
			$.ajax({
				type : 'POST',
				url : ajaxUrl,
				data : 'ac=getSkin',
				success : function(skin){
					function styleOnload(node, callback) {
						// for IE6-9 and Opera
						if(node.attachEvent){
							node.attachEvent('onload', callback);
							// NOTICE:
							// 1. "onload" will be fired in IE6-9 when the file is 404, but in
							// this situation, Opera does nothing, so fallback to timeout.
							// 2. "onerror" doesn't fire in any browsers!
						}
						// polling for Firefox, Chrome, Safari
						else{
							setTimeout(function(){
								poll(node, callback);
							}, 0); // for cache
						}
					}
					function poll(node, callback) {
						if(callback.isCalled){
							return;
						}
						var isLoaded = false;
						//webkit
						if(/webkit/i.test(navigator.userAgent)){
							if (node['sheet']) {
								isLoaded = true;
							}
						}
						// for Firefox
						else if(node['sheet']){
							try{
								if (node['sheet'].cssRules) {
									isLoaded = true;
								}
							}catch(ex){
								// NS_ERROR_DOM_SECURITY_ERR
								if(ex.code === 1000){
									isLoaded = true;
								}
							}
						}
						if(isLoaded){
							// give time to render.
							setTimeout(function() {
								callback();
							}, 1);
						}else{
							setTimeout(function() {
								poll(node, callback);
							}, 1);
						}
					}					
					//将原样式修改id，并载入新样式
					$('#window-skin').attr('id', 'window-skin-ready2remove');
					var css = document.createElement('link');
					css.rel = 'stylesheet';
					css.href = 'img/skins/' + skin + '.css?' + version;
					css.id = 'window-skin';
					document.getElementsByTagName('head')[0].appendChild(css);
					//新样式载入完毕后清空原样式
					//方法为参考seajs源码并改编，文章地址：http://www.blogjava.net/Hafeyang/archive/2011/10/08/360183.html
					styleOnload(css, function(){
						$('#window-skin-ready2remove').remove();
						callback && callback();
					});
				}
			});
		},
		help : function(){
			if($.cookie('isLoginFirst') == null){
				$.cookie('isLoginFirst', '1', {expires : 95});
				if(!$.browser.msie || ($.browser.msie && $.browser.version < 9)){
					$('body').append(helpTemp);
					//IE6,7,8基本就告别新手帮助了
					$('#step1').show();
					$('.close').on('click', function(){
						$('#help').remove();
					});
					$('.next').on('click', function(){
						var obj = $(this).parents('.step');
						var step = obj.attr('step');
						obj.hide();
						$('#step' + (parseInt(step) + 1)).show();
					});
					$('.over').on('click', function(){
						$('#help').remove();
					});
				}
			}
		}
	}
})();
