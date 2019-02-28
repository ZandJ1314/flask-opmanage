/*
**  小挂件
*/
HROS.widget = (function(){
	return {
		/*
		**  创建挂件
		**  自定义挂件：HROS.widget.createTemp({url,width,height,left,top});
		**      示例：HROS.widget.createTemp({url:"http://www.baidu.com",width:800,height:400,left:100,top:100});
		*/
		createTemp : function(obj){
			$('.popup-menu').hide();
			$('.quick_view_container').remove();
			var type = 'widget', appid = obj.appid == null ? Date.parse(new Date()) : obj.appid;
			//判断窗口是否已打开
			var iswidgetopen = false;
			$('#desk .widget').each(function(){
				if($(this).attr('appid') == appid){
					iswidgetopen = true;
				}
			});
			//如果没有打开，则进行创建
			if(iswidgetopen == false){
				function nextDo(options){
					$('#desk').append(widgetWindowTemp({
						'width' : options.width,
						'height' : options.height,
						'type' : 'widget',
						'id' : 'w_' + options.appid,
						'appid' : options.appid,
						'realappid' : 0,
						'top' : options.top,
						'left' : options.left,
						'url' : options.url
					}));
					var widgetId = '#w_' + options.appid;
					//绑定小挂件上各个按钮事件
					HROS.widget.handle($(widgetId));
					//绑定小挂件移动
					HROS.widget.move($(widgetId));
				}
				nextDo({
					appid : appid,
					url : obj.url,
					width : obj.width,
					height : obj.height,
					top : obj.top == null ? 0 : obj.top,
					left : obj.left == null ? 0 : obj.left
				});
			}
		},
		create : function(obj){
			var appid = obj.attr('appid');
			//判断窗口是否已打开
			var iswidgetopen = false;
			$('#desk .widget').each(function(){
				if($(this).attr('appid') == appid){
					iswidgetopen = true;
				}
			});
			//如果没有打开，则进行创建
			if(iswidgetopen == false && $('#d_' + appid).attr('opening') != 1){
				$('#d_' + appid).attr('opening', 1);
				function nextDo(options){
					//if(HROS.widget.checkCookie(appid)){
					//	if($.cookie('widgetState' + HROS.CONFIG.memberID)){
					//		widgetState = eval("(" + $.cookie('widgetState' + HROS.CONFIG.memberID) + ")");
					//		$(widgetState).each(function(){
					//			if(this.appid == options.appid){
					//				options.top = this.top;
					//				options.left = this.left;
					//			}
					//		});
					//	}
					//}else{
					//	HROS.widget.addCookie(options.appid, 0, 0);
					//}
					$('#desk').append(widgetWindowTemp({
						'width' : options.width,
						'height' : options.height,
						'type' : 'widget',
						'id' : 'w_' + options.appid,
						'appid' : options.appid,
						'realappid' : options.realappid,
						'top' : options.top,
						'left' : options.left,
						'url' : options.url
					}));
					var widgetId = '#w_' + options.appid;
					//绑定小挂件上各个按钮事件
					HROS.widget.handle($(widgetId));
					//绑定小挂件移动
					HROS.widget.move($(widgetId));
				}
				ZENG.msgbox.show('小挂件正在加载中，请耐心等待...', 6, 100000);
				ZENG.msgbox._hide();
					var options = {
						appid : obj.attr('appid'),
						realappid : obj.attr('appid'),
						url : obj.attr('url'),
						width : obj.attr('width'),
						height : obj.attr('height'),
						top : obj.attr('top'),
						left : $(window).width()-200
					};
					nextDo(options);
					$('#d_' + appid).attr('opening', 0);
				
			}
		},
		//还原上次退出系统时widget的状态
		reduction : function(){
			var widgetState = $.parseJSON($.cookie('widgetState' + HROS.CONFIG.memberID));
			$(widgetState).each(function(){
				HROS.widget.create(this.appid, {'left' : this.left, 'top' : this.top});
			});
		},
		//根据id验证是否存在cookie中
		checkCookie : function(appid){
			var flag = false, widgetState = $.parseJSON($.cookie('widgetState' + HROS.CONFIG.memberID));
			$(widgetState).each(function(){
				if(this.appid == appid){
					flag = true;
				}
			});
			return flag;
		},
		/*
		**  以下三个方法：addCookie、updateCookie、removeCookie
		**  用于记录widget打开状态以及摆放位置
		**  实现用户再次登入系统时，还原上次widget的状态
		*/
		addCookie : function(appid, top, left){
			if(!HROS.widget.checkCookie(appid)){
				var widgetState = $.parseJSON($.cookie('widgetState' + HROS.CONFIG.memberID));
				if(widgetState == null){
					widgetState = [];
				}
				widgetState.push({
					appid : appid,
					top : top,
					left : left
				});
				$.cookie('widgetState' + HROS.CONFIG.memberID, $.toJSON(widgetState), {expires : 95});
			}else{
				HROS.widget.updateCookie(appid, top, left);
			}
		},
		updateCookie : function(appid, top, left){
			if(HROS.widget.checkCookie(appid)){
				var widgetState = $.parseJSON($.cookie('widgetState' + HROS.CONFIG.memberID));
				$(widgetState).each(function(){
					if(this.appid == appid){
						this.top = top;
						this.left = left;
					}
				});
				$.cookie('widgetState' + HROS.CONFIG.memberID, $.toJSON(widgetState), {expires : 95});
			}
		},
		removeCookie : function(appid){
			if(HROS.widget.checkCookie(appid)){
				var widgetState = $.parseJSON($.cookie('widgetState' + HROS.CONFIG.memberID));
				$(widgetState).each(function(i){
					if(this.appid == appid){
						widgetState.splice(i, 1);
						return false;
					}
				});
				$.cookie('widgetState' + HROS.CONFIG.memberID, $.toJSON(widgetState), {expires : 95});
			}
		},
		move : function(obj){
			obj.on('mousedown', '.move', function(e){
				var lay, x, y;
				x = e.clientX - obj.offset().left;
				y = e.clientY - obj.offset().top;
				//绑定鼠标移动事件
				$(document).on('mousemove', function(e){
					lay = HROS.maskBox.desk();
					lay.show();
					_l = e.clientX - x;
					_t = e.clientY - y;
					_t = _t < 0 ? 0 : _t;
					obj.css({
						left : _l,
						top : _t
					});
				}).on('mouseup', function(){
					$(this).off('mousemove').off('mouseup');
					if(typeof(lay) !== 'undefined'){
						lay.hide();
					}
					HROS.widget.updateCookie(obj.attr('appid'), _t, _l);
				});
			});
		},
		close : function(appid){
			var widgetId = '#w_' + appid;
			$(widgetId).html('').remove();
			//HROS.widget.removeCookie(appid);
		},
		handle : function(obj){
			obj.on('click', '.ha-close', function(){
				HROS.widget.close(obj.attr('appid'));
			})
		}
	}
})();